"""
Roadmap Generator Service
Generates a week-by-week personalized learning roadmap based on skill gaps,
prerequisites, and skill difficulty ordering.
"""

from typing import List, Dict, Any
from data.skills_taxonomy import get_skill, SKILLS_TAXONOMY


class RoadmapGenerator:
    """
    Generates a prerequisite-ordered, week-by-week learning roadmap
    for a candidate to close identified skill gaps.
    """

    def generate(
        self,
        missing_critical: List[Dict],
        missing_preferred: List[Dict],
        transferable: List[Dict],
        candidate_skill_keys: List[str],
    ) -> Dict[str, Any]:
        """
        Generate a personalized learning roadmap.

        Returns:
            {
                "phases": [
                    {
                        "phase": int,
                        "title": str,
                        "weeks": str,
                        "skills": [...],
                        "description": str,
                    }
                ],
                "total_weeks": int,
                "total_skills": int,
                "skill_sequence": [...]
            }
        """
        # Combine and deduplicate skills to learn
        all_missing = {s["key"]: s for s in missing_critical}
        all_missing.update({s["key"]: s for s in missing_preferred})

        if not all_missing:
            return {
                "phases": [],
                "total_weeks": 0,
                "total_skills": 0,
                "skill_sequence": [],
                "message": "No skill gaps found! You are fully qualified for this role."
            }

        candidate_keys = set(candidate_skill_keys)

        # Topological sort by prerequisites (dependency ordering)
        ordered_skills = self._topological_sort(
            list(all_missing.keys()),
            candidate_keys,
            all_missing
        )

        # Group into phases by category + difficulty
        phases = self._build_phases(ordered_skills, missing_critical)

        # Calculate total weeks
        total_weeks = sum(
            sum(s.get("avg_weeks_to_learn", 4) for s in phase["skills"])
            for phase in phases
        )
        # Apply parallelism factor (learn 1.5x faster with structure)
        total_weeks = max(round(total_weeks * 0.65), len(phases) * 2)

        return {
            "phases": phases,
            "total_weeks": total_weeks,
            "total_skills": len(ordered_skills),
            "skill_sequence": [s["canonical"] for s in ordered_skills],
        }

    def _topological_sort(
        self,
        skill_keys: List[str],
        candidate_keys: set,
        skill_map: Dict[str, Dict],
    ) -> List[Dict]:
        """
        Sort skills so prerequisites come before the skills that need them.
        Skills already known by the candidate are treated as satisfied prerequisites.
        """
        visited = set()
        result = []
        in_stack = set()

        # Expand: add prerequisites that are also missing
        def get_all_needed(key: str, depth: int = 0):
            if depth > 10 or key in visited or key in candidate_keys:
                return
            if key in in_stack:
                return  # Cycle guard
            in_stack.add(key)

            skill = get_skill(key)
            prereqs = skill.get("prerequisites", [])

            # Recurse into prerequisites first
            for prereq in prereqs:
                if prereq not in candidate_keys and prereq not in visited:
                    get_all_needed(prereq, depth + 1)

            if key not in visited:
                visited.add(key)
                in_stack.discard(key)
                meta = skill_map.get(key) or {}
                full_meta = get_skill(key)
                result.append({
                    "key": key,
                    "canonical": full_meta.get("canonical", key),
                    "category": full_meta.get("category", "General"),
                    "difficulty": full_meta.get("difficulty", 3),
                    "avg_weeks_to_learn": full_meta.get("avg_weeks_to_learn", 4),
                    "resources": full_meta.get("resources", []),
                    "prerequisites": full_meta.get("prerequisites", []),
                    "is_critical": key in skill_map,
                })

        for key in skill_keys:
            get_all_needed(key)

        return result

    def _build_phases(self, ordered_skills: List[Dict], missing_critical: List[Dict]) -> List[Dict]:
        """
        Group ordered skills into learning phases (Foundation → Core → Advanced → Preferred).
        """
        critical_keys = {s["key"] for s in missing_critical}

        # Group by difficulty tier
        foundation = [s for s in ordered_skills if s["difficulty"] <= 2]
        core = [s for s in ordered_skills if s["difficulty"] == 3 and s.get("is_critical", False)]
        advanced = [s for s in ordered_skills if s["difficulty"] >= 4 and s.get("is_critical", False)]
        preferred = [s for s in ordered_skills if not s.get("is_critical", False) and s["difficulty"] <= 3]
        preferred_adv = [s for s in ordered_skills if not s.get("is_critical", False) and s["difficulty"] >= 4]

        phases = []
        week_cursor = 1

        def make_phase(phase_num, title, description, skills):
            nonlocal week_cursor
            if not skills:
                return None
            weeks_needed = max(round(sum(s["avg_weeks_to_learn"] for s in skills) * 0.65), len(skills))
            phase = {
                "phase": phase_num,
                "title": title,
                "description": description,
                "week_start": week_cursor,
                "week_end": week_cursor + weeks_needed - 1,
                "weeks_label": f"Week {week_cursor}–{week_cursor + weeks_needed - 1}",
                "duration_weeks": weeks_needed,
                "skills": skills,
                "priority": "critical" if any(s.get("is_critical") for s in skills) else "preferred",
            }
            week_cursor += weeks_needed
            return phase

        p1 = make_phase(1, "🏗️ Foundation", "Build the prerequisite base that unlocks all advanced topics.", foundation)
        p2 = make_phase(2, "⚙️ Core Skills", "Acquire the critical skills directly required for the role.", core)
        p3 = make_phase(3, "🚀 Advanced Mastery", "Master advanced skills that differentiate top candidates.", advanced)
        p4 = make_phase(4, "⭐ Preferred Skills", "Add preferred skills to maximize your competitiveness.", preferred + preferred_adv)

        for p in [p1, p2, p3, p4]:
            if p:
                phases.append(p)

        return phases


# Singleton
roadmap_generator = RoadmapGenerator()
