"""
Analyze Router — /api/analyze
Core endpoint: receives resume + JD, returns full skill gap analysis and roadmap.
"""

import json
import re
from typing import Optional
from fastapi import APIRouter, File, Form, UploadFile, HTTPException

from services.resume_parser import resume_parser
from services.skill_extractor import skill_extractor, gap_analyzer
from services.roadmap_generator import roadmap_generator
from models.schemas import AnalysisResponse, ResumeMetadata

router = APIRouter(prefix="/api", tags=["Analysis"])


@router.post("/analyze", response_model=AnalysisResponse, summary="Analyze resume vs job description")
async def analyze(
    resume: UploadFile = File(..., description="Resume file (PDF, DOCX, or TXT)"),
    job_title: str = Form(..., description="Job title, e.g. 'Senior Data Scientist'"),
    job_description: str = Form(..., description="Full job description text"),
    required_skills_text: Optional[str] = Form(
        None, description="Optional comma-separated list to override required skills"
    ),
    preferred_skills_text: Optional[str] = Form(
        None, description="Optional comma-separated list of preferred skills"
    ),
):
    """
    Main analysis endpoint:
    1. Parse resume → extract text
    2. Extract candidate skills from resume
    3. Extract required + preferred skills from JD
    4. Run gap analysis
    5. Generate learning roadmap
    6. Return full analysis + chart data
    """
    # ── 1. Parse Resume ──────────────────────────────────────────────────────
    allowed_types = {
        "application/pdf", "application/msword",
        "application/vnd.openxmlformats-officedocument.wordprocessingml.document",
        "text/plain"
    }
    if resume.content_type not in allowed_types and not resume.filename.endswith((".pdf", ".docx", ".doc", ".txt")):
        raise HTTPException(status_code=400, detail="Unsupported file type. Use PDF, DOCX, or TXT.")

    file_bytes = await resume.read()
    if len(file_bytes) > 10 * 1024 * 1024:  # 10MB limit
        raise HTTPException(status_code=400, detail="File too large. Maximum size is 10MB.")

    try:
        parsed = resume_parser.parse(file_bytes, resume.filename)
    except Exception as e:
        raise HTTPException(status_code=422, detail=f"Could not parse resume: {str(e)}")

    raw_text = parsed["raw_text"]
    sections = parsed["sections"]
    metadata = parsed["metadata"]

    # ── 2. Extract Candidate Skills ──────────────────────────────────────────
    candidate_skills = skill_extractor.extract(raw_text)

    # ── 3. Extract JD Skills ─────────────────────────────────────────────────
    # Priority: manual overrides > extracted from JD text
    if required_skills_text and required_skills_text.strip():
        required_skills = skill_extractor.extract(required_skills_text)
    else:
        # Split JD into required vs preferred by looking for section keywords
        required_text, preferred_text = _split_jd_sections(job_description)
        required_skills = skill_extractor.extract(required_text or job_description)
        preferred_skills_extracted = skill_extractor.extract(preferred_text) if preferred_text else []

    if preferred_skills_text and preferred_skills_text.strip():
        preferred_skills = skill_extractor.extract(preferred_skills_text)
    elif not required_skills_text:
        preferred_skills = preferred_skills_extracted
    else:
        preferred_skills = skill_extractor.extract(job_description)
        # Remove skills already in required
        req_keys = {s["key"] for s in required_skills}
        preferred_skills = [s for s in preferred_skills if s["key"] not in req_keys]

    # Remove required from preferred to avoid duplication
    req_keys = {s["key"] for s in required_skills}
    preferred_skills = [s for s in preferred_skills if s["key"] not in req_keys]

    # ── 4. Gap Analysis ──────────────────────────────────────────────────────
    gap = gap_analyzer.analyze(candidate_skills, required_skills, preferred_skills)

    # ── 5. Generate Roadmap ──────────────────────────────────────────────────
    candidate_keys = [s["key"] for s in candidate_skills]
    roadmap = roadmap_generator.generate(
        missing_critical=gap["missing_critical"],
        missing_preferred=gap["missing_preferred"],
        transferable=gap["transferable"],
        candidate_skill_keys=candidate_keys,
    )

    # ── 6. Build Chart Data ──────────────────────────────────────────────────
    chart_data = _build_chart_data(
        candidate_skills, required_skills, preferred_skills, gap, roadmap
    )

    # ── 7. Return Response ───────────────────────────────────────────────────
    return AnalysisResponse(
        resume_metadata=ResumeMetadata(**metadata),
        resume_raw_text_preview=raw_text[:600].strip(),
        resume_sections=sections,
        candidate_skills=candidate_skills,
        required_skills=required_skills,
        preferred_skills=preferred_skills,
        gap_analysis=gap,
        roadmap=roadmap,
        chart_data=chart_data,
    )


# ── Helper: Split JD into Required vs Preferred ──────────────────────────────

def _split_jd_sections(jd_text: str):
    """
    Try to split JD into required and preferred sections.
    Returns (required_text, preferred_text).
    """
    text_lower = jd_text.lower()

    # Markers for "preferred / nice to have"
    preferred_patterns = [
        r"preferred\s*(?:qualifications?|skills?|requirements?)?:",
        r"nice\s*to\s*have[:\s]",
        r"bonus\s*(?:points?)?[:\s]",
        r"plus(?:es)?[:\s]",
        r"desirable[:\s]",
    ]

    split_pos = None
    for pattern in preferred_patterns:
        match = re.search(pattern, text_lower)
        if match:
            split_pos = match.start()
            break

    if split_pos:
        return jd_text[:split_pos], jd_text[split_pos:]
    return jd_text, None


# ── Helper: Build Chart Data ─────────────────────────────────────────────────

def _build_chart_data(
    candidate_skills, required_skills, preferred_skills, gap, roadmap
) -> dict:
    """Pre-compute all chart datasets for the frontend."""

    # 1. Skill Match Bar Chart — by category
    categories = {}
    for skill in required_skills:
        cat = skill["category"]
        if cat not in categories:
            categories[cat] = {"required": 0, "matched": 0}
        categories[cat]["required"] += 1

    matched_keys = {s["key"] for s in gap["matched"]}
    for skill in required_skills:
        if skill["key"] in matched_keys:
            cat = skill["category"]
            categories[cat]["matched"] += 1

    category_chart = [
        {
            "category": cat,
            "required": data["required"],
            "matched": data["matched"],
            "missing": data["required"] - data["matched"],
        }
        for cat, data in categories.items()
    ]

    # 2. Radar Chart — 6 competency axes
    radar_data = _compute_radar(candidate_skills, required_skills)

    # 3. Readiness Gauge
    readiness_score = gap["readiness_score"]

    # 4. Roadmap Timeline (phase summary for Gantt-style chart)
    timeline = [
        {
            "phase": p["phase"],
            "title": p["title"],
            "week_start": p["week_start"],
            "week_end": p["week_end"],
            "duration": p["duration_weeks"],
            "skill_count": len(p["skills"]),
            "priority": p["priority"],
        }
        for p in roadmap.get("phases", [])
    ]

    # 5. Skill Gap Donut
    stats = gap["stats"]
    donut_data = [
        {"label": "Matched", "value": stats["total_matched"], "color": "#10b981"},
        {"label": "Missing Critical", "value": stats["total_missing_critical"], "color": "#ef4444"},
        {"label": "Missing Preferred", "value": stats["total_missing_preferred"], "color": "#f59e0b"},
        {"label": "Transferable", "value": stats["total_transferable"], "color": "#6366f1"},
    ]

    # 6. Skills by category (candidate)
    candidate_category_dist = {}
    for skill in candidate_skills:
        cat = skill["category"]
        candidate_category_dist[cat] = candidate_category_dist.get(cat, 0) + 1
    candidate_cat_chart = [
        {"category": k, "count": v} for k, v in sorted(
            candidate_category_dist.items(), key=lambda x: -x[1]
        )
    ]

    return {
        "category_match_chart": category_chart,
        "radar_chart": radar_data,
        "readiness_score": readiness_score,
        "roadmap_timeline": timeline,
        "gap_donut": donut_data,
        "candidate_skill_distribution": candidate_cat_chart,
        "total_weeks_to_ready": roadmap.get("total_weeks", 0),
    }


def _compute_radar(candidate_skills, required_skills) -> list:
    """Compute 6-axis radar chart: coverage per major domain."""
    domains = {
        "Programming": ["Programming Languages"],
        "Web/APIs": ["Web Frameworks", "Web Basics"],
        "Data & ML": ["AI/ML", "Data Science", "Data Engineering"],
        "Cloud & DevOps": ["Cloud", "DevOps"],
        "Databases": ["Databases"],
        "CS Fundamentals": ["Computer Science", "Mathematics"],
    }

    req_by_domain = {d: 0 for d in domains}
    matched_by_domain = {d: 0 for d in domains}

    candidate_keys = {s["key"] for s in candidate_skills}

    for skill in required_skills:
        cat = skill.get("category", "")
        for domain, cats in domains.items():
            if cat in cats:
                req_by_domain[domain] += 1
                if skill["key"] in candidate_keys:
                    matched_by_domain[domain] += 1
                break

    radar = []
    for domain in domains:
        req = req_by_domain[domain]
        matched = matched_by_domain[domain]
        score = round((matched / req * 100) if req > 0 else 0, 1)
        radar.append({
            "domain": domain,
            "score": score,
            "matched": matched,
            "required": req,
        })

    return radar
