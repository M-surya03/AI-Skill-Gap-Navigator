"""
Skill Extractor Service
Extracts and normalizes skills from resume or JD text using keyword matching
and alias resolution against the skills taxonomy.
"""

import re
from typing import List, Dict, Set, Tuple
from data.skills_taxonomy import ALIAS_INDEX, SKILLS_TAXONOMY, get_skill


class SkillExtractor:
    """
    Extracts skills from free-form text using alias-based matching
    against the curated skills taxonomy.
    """

    # Skills that are too common and cause false positives
    STOP_WORDS = {"the", "and", "for", "with", "from", "that", "this", "have", "will", "are"}

    def extract(self, text: str) -> List[Dict]:
        """
        Extract skills from text.

        Returns:
            List of skill dicts: [{ key, canonical, category, confidence, matched_alias }]
        """
        if not text:
            return []

        text_lower = text.lower()
        found: Dict[str, Dict] = {}  # key → match info

        # Try matching each alias from longest to shortest (avoid partial matches)
        sorted_aliases = sorted(ALIAS_INDEX.keys(), key=len, reverse=True)

        for alias in sorted_aliases:
            if alias in self.STOP_WORDS:
                continue
            if len(alias) < 2:
                continue

            # Use word-boundary-aware search
            pattern = r"(?<![a-zA-Z0-9_\.\+\#])" + re.escape(alias) + r"(?![a-zA-Z0-9_\.\+\#])"
            if re.search(pattern, text_lower):
                canonical_key = ALIAS_INDEX[alias]
                if canonical_key not in found:
                    skill_meta = get_skill(canonical_key)
                    found[canonical_key] = {
                        "key": canonical_key,
                        "canonical": skill_meta.get("canonical", canonical_key),
                        "category": skill_meta.get("category", "Unknown"),
                        "difficulty": skill_meta.get("difficulty", 3),
                        "avg_weeks_to_learn": skill_meta.get("avg_weeks_to_learn", 8),
                        "prerequisites": skill_meta.get("prerequisites", []),
                        "resources": skill_meta.get("resources", []),
                        "confidence": 1.0,
                        "matched_alias": alias,
                    }

        return list(found.values())

    def extract_from_sections(self, sections: Dict[str, str]) -> Dict[str, List[Dict]]:
        """Extract skills separately from each resume section."""
        section_skills = {}
        for section_name, content in sections.items():
            skills = self.extract(content)
            if skills:
                section_skills[section_name] = skills
        return section_skills

    def get_unique_skill_keys(self, skills: List[Dict]) -> Set[str]:
        """Return just the canonical keys from a skill list."""
        return {s["key"] for s in skills}


class GapAnalyzer:
    """
    Compares candidate skills vs JD required skills to produce
    a comprehensive skill gap analysis.
    """

    def analyze(
        self,
        candidate_skills: List[Dict],
        required_skills: List[Dict],
        preferred_skills: List[Dict] = None,
    ) -> Dict:
        """
        Perform skill gap analysis.

        Returns:
            {
                matched: [...],
                missing_critical: [...],
                missing_preferred: [...],
                transferable: [...],
                readiness_score: float (0-100),
                summary: str
            }
        """
        preferred_skills = preferred_skills or []

        candidate_keys = {s["key"] for s in candidate_skills}
        required_keys = {s["key"] for s in required_skills}
        preferred_keys = {s["key"] for s in preferred_skills}

        # Direct matches
        matched_keys = candidate_keys & required_keys
        missing_required_keys = required_keys - candidate_keys
        missing_preferred_keys = preferred_keys - candidate_keys - missing_required_keys

        # Transferable skill detection (candidate has a prerequisite that leads to a required skill)
        transferable = []
        for missing_key in missing_required_keys:
            skill_meta = get_skill(missing_key)
            prereqs = skill_meta.get("prerequisites", [])
            overlap = candidate_keys & set(prereqs)
            if overlap:
                transferable.append({
                    "target_skill": missing_key,
                    "target_canonical": skill_meta.get("canonical", missing_key),
                    "transferable_from": list(overlap),
                    "transfer_score": round(len(overlap) / max(len(prereqs), 1) * 100, 1),
                })

        # Build enriched match lists
        def enrich(keys: Set[str], all_skills: List[Dict]) -> List[Dict]:
            skill_map = {s["key"]: s for s in all_skills}
            result = []
            for key in keys:
                base = get_skill(key)
                result.append({
                    "key": key,
                    "canonical": base.get("canonical", key),
                    "category": base.get("category", "Unknown"),
                    "difficulty": base.get("difficulty", 3),
                    "avg_weeks_to_learn": base.get("avg_weeks_to_learn", 8),
                    "resources": base.get("resources", []),
                    "prerequisites": base.get("prerequisites", []),
                })
            return result

        matched = enrich(matched_keys, required_skills)
        missing_critical = enrich(missing_required_keys, required_skills)
        missing_preferred = enrich(missing_preferred_keys, preferred_skills)

        # Compute readiness score
        if not required_keys:
            readiness_score = 100.0
        else:
            # Base: % of required skills matched
            base_score = len(matched_keys) / len(required_keys) * 100
            # Bonus: transferable skills partially count (up to 15 pts)
            transfer_bonus = min(len(transferable) * 5, 15)
            # Bonus: preferred skills (up to 10 pts)
            preferred_matched = len(preferred_keys & candidate_keys)
            preferred_bonus = (preferred_matched / max(len(preferred_keys), 1)) * 10 if preferred_keys else 0
            readiness_score = round(min(base_score + transfer_bonus + preferred_bonus, 100), 1)

        # Human-readable summary
        summary = self._generate_summary(
            readiness_score, len(matched_keys), len(missing_required_keys),
            len(missing_preferred_keys), len(transferable)
        )

        return {
            "matched": matched,
            "missing_critical": missing_critical,
            "missing_preferred": missing_preferred,
            "transferable": transferable,
            "readiness_score": readiness_score,
            "summary": summary,
            "stats": {
                "total_required": len(required_keys),
                "total_matched": len(matched_keys),
                "total_missing_critical": len(missing_required_keys),
                "total_missing_preferred": len(missing_preferred_keys),
                "total_transferable": len(transferable),
            }
        }

    def _generate_summary(
        self,
        score: float,
        matched: int,
        missing_critical: int,
        missing_preferred: int,
        transferable: int,
    ) -> str:
        if score >= 85:
            level = "an excellent"
            verdict = "You are highly prepared for this role."
        elif score >= 70:
            level = "a good"
            verdict = "With focused learning on a few key areas, you can be fully ready."
        elif score >= 50:
            level = "a moderate"
            verdict = "Targeted upskilling over 2-3 months is recommended."
        else:
            level = "a low"
            verdict = "A structured learning roadmap over 4-6 months is required."

        return (
            f"You have {level} readiness score of {score}%. "
            f"You matched {matched} required skills, "
            f"with {missing_critical} critical skills to acquire "
            f"and {transferable} skills where your existing knowledge gives you a head start. "
            f"{verdict}"
        )


# Singletons
skill_extractor = SkillExtractor()
gap_analyzer = GapAnalyzer()
