// Axios API client for Skill Gap Navigator backend

import axios from 'axios';

const BASE_URL = 'http://localhost:8000';

export const api = axios.create({
  baseURL: BASE_URL,
  timeout: 60000, // 60s for ML inference
});

export interface AnalysisResult {
  resume_metadata: {
    name_candidate: string | null;
    email: string | null;
    phone: string | null;
    linkedin: string | null;
    github: string | null;
    years_experience: number | null;
  };
  resume_raw_text_preview: string;
  resume_sections: Record<string, string>;
  candidate_skills: SkillInfo[];
  required_skills: SkillInfo[];
  preferred_skills: SkillInfo[];
  gap_analysis: GapAnalysis;
  roadmap: LearningRoadmap;
  chart_data: ChartData;
}

export interface SkillInfo {
  key: string;
  canonical: string;
  category: string;
  difficulty: number;
  avg_weeks_to_learn: number;
  resources: { title: string; url: string; type: string }[];
  prerequisites: string[];
  confidence?: number;
  matched_alias?: string;
}

export interface TransferableSkill {
  target_skill: string;
  target_canonical: string;
  transferable_from: string[];
  transfer_score: number;
}

export interface GapAnalysis {
  matched: SkillInfo[];
  missing_critical: SkillInfo[];
  missing_preferred: SkillInfo[];
  transferable: TransferableSkill[];
  readiness_score: number;
  summary: string;
  stats: {
    total_required: number;
    total_matched: number;
    total_missing_critical: number;
    total_missing_preferred: number;
    total_transferable: number;
  };
}

export interface RoadmapPhase {
  phase: number;
  title: string;
  description: string;
  week_start: number;
  week_end: number;
  weeks_label: string;
  duration_weeks: number;
  skills: SkillInfo[];
  priority: 'critical' | 'preferred';
}

export interface LearningRoadmap {
  phases: RoadmapPhase[];
  total_weeks: number;
  total_skills: number;
  skill_sequence: string[];
  message?: string;
}

export interface ChartData {
  category_match_chart: { category: string; required: number; matched: number; missing: number }[];
  radar_chart: { domain: string; score: number; matched: number; required: number }[];
  readiness_score: number;
  roadmap_timeline: {
    phase: number; title: string; week_start: number;
    week_end: number; duration: number; skill_count: number; priority: string;
  }[];
  gap_donut: { label: string; value: number; color: string }[];
  candidate_skill_distribution: { category: string; count: number }[];
  total_weeks_to_ready: number;
}

export async function analyzeResume(
  resumeFile: File,
  jobTitle: string,
  jobDescription: string,
  requiredSkills?: string,
  preferredSkills?: string,
): Promise<AnalysisResult> {
  const formData = new FormData();
  formData.append('resume', resumeFile);
  formData.append('job_title', jobTitle);
  formData.append('job_description', jobDescription);
  if (requiredSkills) formData.append('required_skills_text', requiredSkills);
  if (preferredSkills) formData.append('preferred_skills_text', preferredSkills);

  const res = await api.post<AnalysisResult>('/api/analyze', formData, {
    headers: { 'Content-Type': 'multipart/form-data' },
  });
  return res.data;
}
