import React, { useState } from 'react';
import { analyzeResume, type AnalysisResult } from '../api/client';
import ResumeUpload from '../components/ResumeUpload';
import SkillGapCharts from '../components/SkillGapCharts';
import RoadmapTimeline from '../components/RoadmapTimeline';
import SkillGapPanel from '../components/SkillGapPanel';
import { Loader2, Sparkles, ChevronDown, User, Mail, Phone, Link2, GitBranch, Clock } from 'lucide-react';

const SAMPLE_JD = `We are looking for a Senior Data Scientist to join our AI team.

Required Skills:
- Python (advanced)
- Machine Learning (scikit-learn, XGBoost)
- Deep Learning (PyTorch or TensorFlow)
- SQL and PostgreSQL
- Statistics and probability
- Data visualization (matplotlib, seaborn, plotly)
- Git version control
- REST API development

Preferred Qualifications:
- NLP / Large Language Models experience
- MLOps (model deployment, monitoring)
- Apache Spark for big data
- Cloud platforms (AWS, GCP, or Azure)
- Docker and containerization`;

const TABS = ['📊 Analysis', '📋 Skill Details', '🗺️ Roadmap'] as const;
type Tab = typeof TABS[number];

const HomePage: React.FC = () => {
  const [file, setFile] = useState<File | null>(null);
  const [jobTitle, setJobTitle] = useState('Senior Data Scientist');
  const [jobDesc, setJobDesc] = useState(SAMPLE_JD);
  const [requiredSkills, setRequiredSkills] = useState('');
  const [preferredSkills, setPreferredSkills] = useState('');
  const [showAdvanced, setShowAdvanced] = useState(false);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const [result, setResult] = useState<AnalysisResult | null>(null);
  const [activeTab, setActiveTab] = useState<Tab>('📊 Analysis');

  const handleAnalyze = async () => {
    if (!file) { setError('Please upload your resume first.'); return; }
    if (!jobDesc.trim()) { setError('Please enter a job description.'); return; }

    setError(null);
    setLoading(true);
    setResult(null);

    try {
      const data = await analyzeResume(file, jobTitle, jobDesc, requiredSkills || undefined, preferredSkills || undefined);
      setResult(data);
      setActiveTab('📊 Analysis');
      setTimeout(() => {
        document.getElementById('results-section')?.scrollIntoView({ behavior: 'smooth' });
      }, 100);
    } catch (err: any) {
      const msg = err?.response?.data?.detail || err?.message || 'Analysis failed. Make sure the backend is running.';
      setError(typeof msg === 'string' ? msg : JSON.stringify(msg));
    } finally {
      setLoading(false);
    }
  };

  const handleReset = () => {
    setResult(null);
    setFile(null);
    setError(null);
    window.scrollTo({ top: 0, behavior: 'smooth' });
  };

  const meta = result?.resume_metadata;

  return (
    <div className="page-wrapper">
      {/* ── Hero ─────────────────────────────────────────────────────────── */}
      <section style={{ position: 'relative', overflow: 'hidden', paddingTop: '3rem', paddingBottom: '2rem' }}>
        <div className="hero-glow hero-glow-purple" />
        <div className="hero-glow hero-glow-teal" />
        <div className="container" style={{ position: 'relative', zIndex: 1, textAlign: 'center' }}>
          <div className="animate-fade-up">
            <span className="badge badge-purple" style={{ marginBottom: '1.25rem', padding: '0.4rem 1rem', fontSize: '0.82rem' }}>
              <Sparkles size={12} />  AI-Powered Skill Intelligence
            </span>
            <h1 style={{ marginBottom: '1rem' }}>
              Find Your{' '}
              <span className="text-gradient">Skill Gaps</span>
              <br />Get a{' '}
              <span className="text-gradient">Personalized Roadmap</span>
            </h1>
            <p className="text-secondary" style={{ fontSize: '1.1rem', maxWidth: 600, margin: '0 auto 2rem' }}>
              Upload your resume, paste a job description, and get an AI-powered gap analysis
              with a week-by-week learning roadmap to land your dream role.
            </p>
          </div>

          {/* Stat pills */}
          <div className="flex justify-center gap-4 flex-wrap animate-fade-up" style={{ animationDelay: '0.1s', marginBottom: '3rem' }}>
            {[
              { icon: '🎯', text: '150+ Skills Tracked' },
              { icon: '📈', text: 'Readiness Score' },
              { icon: '🗺️', text: 'Prerequisite-Ordered Roadmap' },
              { icon: '🔄', text: 'Transferable Skill Detection' },
            ].map(s => (
              <div key={s.text} className="card-glass" style={{ padding: '0.5rem 1rem', display: 'flex', alignItems: 'center', gap: '0.5rem', fontSize: '0.85rem' }}>
                <span>{s.icon}</span>
                <span style={{ color: 'var(--text-secondary)' }}>{s.text}</span>
              </div>
            ))}
          </div>
        </div>
      </section>

      {/* ── Input Form ───────────────────────────────────────────────────── */}
      <section style={{ paddingBottom: '3rem' }}>
        <div className="container">
          <div style={{ maxWidth: 900, margin: '0 auto', display: 'flex', flexDirection: 'column', gap: '1.5rem' }}>

            {/* Resume Upload */}
            <div className="card animate-fade-up" style={{ animationDelay: '0.15s' }}>
              <div className="section-header">
                <div className="section-icon section-icon-primary">📄</div>
                <div>
                  <h3 style={{ fontSize: '1rem', marginBottom: '0.1rem' }}>Step 1 — Upload Resume</h3>
                  <p className="text-sm text-secondary">PDF, DOCX, or TXT · Max 10MB</p>
                </div>
              </div>
              <ResumeUpload onFileSelect={setFile} selectedFile={file} isAnalyzing={loading} />
            </div>

            {/* Job Description */}
            <div className="card animate-fade-up" style={{ animationDelay: '0.2s' }}>
              <div className="section-header">
                <div className="section-icon section-icon-success">💼</div>
                <div>
                  <h3 style={{ fontSize: '1rem', marginBottom: '0.1rem' }}>Step 2 — Job Description</h3>
                  <p className="text-sm text-secondary">Paste the full job description or use our example</p>
                </div>
              </div>
              <div style={{ display: 'flex', flexDirection: 'column', gap: '1rem' }}>
                <div className="form-group">
                  <label className="label" htmlFor="job-title">Job Title</label>
                  <input
                    id="job-title"
                    className="input"
                    placeholder="e.g. Senior Data Scientist"
                    value={jobTitle}
                    onChange={e => setJobTitle(e.target.value)}
                    disabled={loading}
                  />
                </div>
                <div className="form-group">
                  <label className="label" htmlFor="job-desc">Job Description</label>
                  <textarea
                    id="job-desc"
                    className="textarea input"
                    placeholder="Paste the full job description here..."
                    value={jobDesc}
                    onChange={e => setJobDesc(e.target.value)}
                    rows={10}
                    disabled={loading}
                  />
                </div>
              </div>

              {/* Advanced options */}
              <button
                onClick={() => setShowAdvanced(!showAdvanced)}
                className="btn btn-outline btn-sm"
                style={{ marginTop: '0.75rem', width: 'auto' }}
                type="button"
              >
                Advanced Options
                <ChevronDown size={14} style={{ transform: showAdvanced ? 'rotate(180deg)' : 'none', transition: 'transform 0.2s' }} />
              </button>

              {showAdvanced && (
                <div style={{ display: 'grid', gridTemplateColumns: '1fr 1fr', gap: '1rem', marginTop: '1rem' }}>
                  <div className="form-group">
                    <label className="label">Required Skills Override</label>
                    <input
                      className="input"
                      placeholder="Python, SQL, Machine Learning..."
                      value={requiredSkills}
                      onChange={e => setRequiredSkills(e.target.value)}
                    />
                  </div>
                  <div className="form-group">
                    <label className="label">Preferred Skills Override</label>
                    <input
                      className="input"
                      placeholder="Docker, Kubernetes, Spark..."
                      value={preferredSkills}
                      onChange={e => setPreferredSkills(e.target.value)}
                    />
                  </div>
                </div>
              )}
            </div>

            {/* Analyze Button */}
            {error && (
              <div style={{
                padding: '0.875rem 1.25rem',
                background: 'rgba(239,68,68,0.1)',
                border: '1px solid rgba(239,68,68,0.3)',
                borderRadius: 12,
                color: '#fca5a5',
                fontSize: '0.875rem',
              }}>
                ⚠ {error}
              </div>
            )}

            <button
              className="btn btn-primary btn-lg"
              onClick={handleAnalyze}
              disabled={loading || !file}
              style={{ alignSelf: 'center', minWidth: 240, justifyContent: 'center' }}
              id="analyze-btn"
            >
              {loading ? (
                <>
                  <Loader2 size={18} style={{ animation: 'spin 1s linear infinite' }} />
                  Analyzing your profile…
                </>
              ) : (
                <>
                  <Sparkles size={18} />
                  Analyze My Skills
                </>
              )}
            </button>
          </div>
        </div>
      </section>

      {/* ── Results ──────────────────────────────────────────────────────── */}
      {result && (
        <section id="results-section" style={{ paddingBottom: '4rem', borderTop: '1px solid var(--border)', paddingTop: '3rem' }}>
          <div className="container">
            {/* Candidate header */}
            {meta && (
              <div className="card animate-fade-up" style={{ marginBottom: '2rem', background: 'linear-gradient(135deg, rgba(99,102,241,0.1) 0%, rgba(16,185,129,0.05) 100%)' }}>
                <div style={{ display: 'flex', alignItems: 'center', gap: '1.5rem', flexWrap: 'wrap' }}>
                  <div style={{
                    width: 64, height: 64, borderRadius: '50%',
                    background: 'var(--grad-primary)',
                    display: 'flex', alignItems: 'center', justifyContent: 'center',
                    fontSize: '1.5rem', flexShrink: 0,
                  }}>
                    👤
                  </div>
                  <div style={{ flex: 1, minWidth: 200 }}>
                    <h2 style={{ fontSize: '1.375rem', marginBottom: '0.375rem' }}>
                      {meta.name_candidate || 'Candidate Analysis'}
                    </h2>
                    <div style={{ display: 'flex', gap: '1rem', flexWrap: 'wrap' }}>
                      {meta.email && <span className="flex items-center gap-1 text-sm text-secondary"><Mail size={13} />{meta.email}</span>}
                      {meta.phone && <span className="flex items-center gap-1 text-sm text-secondary"><Phone size={13} />{meta.phone}</span>}
                      {meta.linkedin && <span className="flex items-center gap-1 text-sm" style={{ color: 'var(--primary-light)' }}><Link2 size={13} />{meta.linkedin}</span>}
                      {meta.github && <span className="flex items-center gap-1 text-sm" style={{ color: 'var(--primary-light)' }}><GitBranch size={13} />{meta.github}</span>}
                      {meta.years_experience && <span className="flex items-center gap-1 text-sm text-secondary"><Clock size={13} />{meta.years_experience} years exp.</span>}
                    </div>
                  </div>
                  <div style={{ display: 'flex', gap: '0.75rem', flexWrap: 'wrap' }}>
                    <div style={{ textAlign: 'center' }}>
                      <div style={{ fontSize: '2rem', fontWeight: 900, color: 'var(--primary-light)', lineHeight: 1 }}>
                        {result.candidate_skills.length}
                      </div>
                      <div className="text-xs text-muted">Skills Found</div>
                    </div>
                    <div style={{ textAlign: 'center', paddingLeft: '0.75rem', borderLeft: '1px solid var(--border)' }}>
                      <div style={{ fontSize: '2rem', fontWeight: 900, color: result.gap_analysis.readiness_score >= 70 ? '#10b981' : result.gap_analysis.readiness_score >= 50 ? '#f59e0b' : '#ef4444', lineHeight: 1 }}>
                        {Math.round(result.gap_analysis.readiness_score)}%
                      </div>
                      <div className="text-xs text-muted">Readiness</div>
                    </div>
                    <div style={{ textAlign: 'center', paddingLeft: '0.75rem', borderLeft: '1px solid var(--border)' }}>
                      <div style={{ fontSize: '2rem', fontWeight: 900, color: '#6366f1', lineHeight: 1 }}>
                        {result.roadmap.total_weeks}w
                      </div>
                      <div className="text-xs text-muted">To Ready</div>
                    </div>
                  </div>
                  <button className="btn btn-outline btn-sm" onClick={handleReset}>
                    Analyze Another
                  </button>
                </div>
              </div>
            )}

            {/* Tabs */}
            <div className="tabs" style={{ marginBottom: '2rem' }}>
              {TABS.map(tab => (
                <button
                  key={tab}
                  className={`tab-btn ${activeTab === tab ? 'active' : ''}`}
                  onClick={() => setActiveTab(tab)}
                >
                  {tab}
                </button>
              ))}
            </div>

            {/* Tab Content */}
            <div className="animate-fade-in">
              {activeTab === '📊 Analysis' && (
                <SkillGapCharts chartData={result.chart_data} gapAnalysis={result.gap_analysis} />
              )}
              {activeTab === '📋 Skill Details' && (
                <div className="card">
                  <SkillGapPanel gapAnalysis={result.gap_analysis} />
                </div>
              )}
              {activeTab === '🗺️ Roadmap' && (
                <RoadmapTimeline roadmap={result.roadmap} />
              )}
            </div>
          </div>
        </section>
      )}
    </div>
  );
};

export default HomePage;
