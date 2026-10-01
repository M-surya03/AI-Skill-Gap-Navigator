"""
Pydantic Schemas — All API request/response contracts.
"""

from typing import List, Optional, Dict, Any
from pydantic import BaseModel, Field


# ── Skill Schemas ────────────────────────────────────────────────────────────

class SkillInfo(BaseModel):
    key: str
    canonical: str
    category: str
    difficulty: int = Field(ge=1, le=5)
    avg_weeks_to_learn: int
    resources: List[Dict[str, str]] = []
    prerequisites: List[str] = []
    confidence: Optional[float] = None
    matched_alias: Optional[str] = None


class TransferableSkill(BaseModel):
    target_skill: str
    target_canonical: str
    transferable_from: List[str]
    transfer_score: float


# ── Gap Analysis Schemas ─────────────────────────────────────────────────────

class GapStats(BaseModel):
    total_required: int
    total_matched: int
    total_missing_critical: int
    total_missing_preferred: int
    total_transferable: int


class GapAnalysisResult(BaseModel):
    matched: List[SkillInfo]
    missing_critical: List[SkillInfo]
    missing_preferred: List[SkillInfo]
    transferable: List[TransferableSkill]
    readiness_score: float = Field(ge=0, le=100)
    summary: str
    stats: GapStats


# ── Roadmap Schemas ──────────────────────────────────────────────────────────

class RoadmapPhase(BaseModel):
    phase: int
    title: str
    description: str
    week_start: int
    week_end: int
    weeks_label: str
    duration_weeks: int
    skills: List[SkillInfo]
    priority: str  # "critical" | "preferred"


class LearningRoadmap(BaseModel):
    phases: List[RoadmapPhase]
    total_weeks: int
    total_skills: int
    skill_sequence: List[str]
    message: Optional[str] = None


# ── Resume Metadata ──────────────────────────────────────────────────────────

class ResumeMetadata(BaseModel):
    name_candidate: Optional[str] = None
    email: Optional[str] = None
    phone: Optional[str] = None
    linkedin: Optional[str] = None
    github: Optional[str] = None
    years_experience: Optional[int] = None


# ── Main Analysis Request/Response ──────────────────────────────────────────

class AnalysisResponse(BaseModel):
    """Full response from /api/analyze"""
    # Input echoes
    resume_metadata: ResumeMetadata
    resume_raw_text_preview: str  # first 500 chars
    resume_sections: Dict[str, str]

    # Extracted skills
    candidate_skills: List[SkillInfo]
    required_skills: List[SkillInfo]
    preferred_skills: List[SkillInfo]

    # Gap analysis
    gap_analysis: GapAnalysisResult

    # Roadmap
    roadmap: LearningRoadmap

    # Chart data (pre-computed for frontend)
    chart_data: Dict[str, Any]

    class Config:
        json_schema_extra = {
            "example": {
                "resume_metadata": {"name_candidate": "John Doe", "email": "john@example.com"},
                "readiness_score": 72.5,
            }
        }


# ── JD-only parse ────────────────────────────────────────────────────────────

class JobDescriptionRequest(BaseModel):
    title: str = Field(..., example="Senior Data Scientist")
    description: str = Field(..., min_length=50, example="We are looking for a Data Scientist...")
    required_skills_override: Optional[List[str]] = Field(
        None, description="Optional manual override of required skills"
    )
    preferred_skills_override: Optional[List[str]] = Field(
        None, description="Optional manual override of preferred skills"
    )
