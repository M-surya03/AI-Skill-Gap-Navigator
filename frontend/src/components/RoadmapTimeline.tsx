import React, { useState } from 'react';
import { ChevronDown, ChevronUp, ExternalLink, Clock, Zap, BookOpen } from 'lucide-react';
import type { LearningRoadmap, RoadmapPhase, SkillInfo } from '../api/client';

interface Props {
  roadmap: LearningRoadmap;
}

const PHASE_COLORS = [
  { dot: '#6366f1', bg: 'rgba(99,102,241,0.15)', border: 'rgba(99,102,241,0.4)' },
  { dot: '#10b981', bg: 'rgba(16,185,129,0.15)', border: 'rgba(16,185,129,0.4)' },
  { dot: '#f59e0b', bg: 'rgba(245,158,11,0.15)', border: 'rgba(245,158,11,0.4)' },
  { dot: '#06b6d4', bg: 'rgba(6,182,212,0.15)', border: 'rgba(6,182,212,0.4)' },
];

const DIFFICULTY_LABELS: Record<number, { label: string; color: string }> = {
  1: { label: 'Beginner', color: '#10b981' },
  2: { label: 'Easy', color: '#34d399' },
  3: { label: 'Intermediate', color: '#f59e0b' },
  4: { label: 'Advanced', color: '#f97316' },
  5: { label: 'Expert', color: '#ef4444' },
};

const RESOURCE_ICONS: Record<string, string> = {
  course: '🎓',
  book: '📚',
  documentation: '📖',
  tutorial: '💡',
  platform: '🔧',
  video: '🎬',
};

// ── Skill Card within a phase ────────────────────────────────────────────────
const SkillCard: React.FC<{ skill: SkillInfo; isExpanded: boolean; onToggle: () => void }> = ({
  skill, isExpanded, onToggle
}) => {
  const diff = DIFFICULTY_LABELS[skill.difficulty] || DIFFICULTY_LABELS[3];

  return (
    <div
      style={{
        background: 'var(--bg-glass)',
        border: '1px solid var(--border)',
        borderRadius: 12,
        overflow: 'hidden',
        transition: 'all 0.2s ease',
      }}
    >
      <button
        onClick={onToggle}
        style={{
          width: '100%',
          background: 'none',
          border: 'none',
          padding: '0.875rem 1rem',
          cursor: 'pointer',
          display: 'flex',
          alignItems: 'center',
          gap: '0.75rem',
          textAlign: 'left',
          color: 'var(--text-primary)',
          fontFamily: 'inherit',
        }}
      >
        <div style={{
          width: 32, height: 32,
          background: 'rgba(99,102,241,0.15)',
          borderRadius: 8,
          display: 'flex', alignItems: 'center', justifyContent: 'center',
          flexShrink: 0, fontSize: '0.9rem',
        }}>
          {RESOURCE_ICONS[skill.resources[0]?.type] || '🔷'}
        </div>
        <div style={{ flex: 1, minWidth: 0 }}>
          <div style={{ fontWeight: 600, fontSize: '0.9rem', color: 'var(--text-primary)' }}>
            {skill.canonical}
          </div>
          <div style={{ fontSize: '0.75rem', color: 'var(--text-muted)', marginTop: '0.1rem' }}>
            {skill.category}
          </div>
        </div>
        <div style={{ display: 'flex', alignItems: 'center', gap: '0.75rem', flexShrink: 0 }}>
          <span style={{
            fontSize: '0.72rem',
            fontWeight: 600,
            color: diff.color,
            background: `${diff.color}20`,
            padding: '0.15rem 0.5rem',
            borderRadius: 999,
            border: `1px solid ${diff.color}40`,
          }}>
            {diff.label}
          </span>
          <span style={{ fontSize: '0.78rem', color: 'var(--text-muted)', display: 'flex', alignItems: 'center', gap: '0.3rem' }}>
            <Clock size={12} />
            {skill.avg_weeks_to_learn}w
          </span>
          {isExpanded ? <ChevronUp size={16} color="var(--text-muted)" /> : <ChevronDown size={16} color="var(--text-muted)" />}
        </div>
      </button>

      {isExpanded && skill.resources.length > 0 && (
        <div style={{ padding: '0 1rem 1rem', borderTop: '1px solid var(--border)' }}>
          <div style={{ paddingTop: '0.875rem', display: 'flex', flexDirection: 'column', gap: '0.5rem' }}>
            <div style={{ fontSize: '0.75rem', color: 'var(--text-muted)', textTransform: 'uppercase', letterSpacing: '0.05em', marginBottom: '0.25rem', display: 'flex', alignItems: 'center', gap: '0.4rem' }}>
              <BookOpen size={12} /> Learning Resources
            </div>
            {skill.resources.map((res, i) => (
              <a
                key={i}
                href={res.url}
                target="_blank"
                rel="noopener noreferrer"
                style={{
                  display: 'flex',
                  alignItems: 'center',
                  gap: '0.625rem',
                  padding: '0.5rem 0.75rem',
                  background: 'rgba(99,102,241,0.08)',
                  border: '1px solid rgba(99,102,241,0.2)',
                  borderRadius: 8,
                  color: 'var(--primary-light)',
                  fontSize: '0.82rem',
                  textDecoration: 'none',
                  transition: 'all 0.2s ease',
                }}
                onMouseOver={e => (e.currentTarget.style.background = 'rgba(99,102,241,0.15)')}
                onMouseOut={e => (e.currentTarget.style.background = 'rgba(99,102,241,0.08)')}
              >
                <span>{RESOURCE_ICONS[res.type] || '🔗'}</span>
                <span style={{ flex: 1, color: 'var(--text-primary)' }}>{res.title}</span>
                <ExternalLink size={12} style={{ flexShrink: 0 }} />
              </a>
            ))}
          </div>
          {skill.prerequisites.length > 0 && (
            <div style={{ marginTop: '0.75rem' }}>
              <div style={{ fontSize: '0.75rem', color: 'var(--text-muted)', marginBottom: '0.4rem' }}>
                Prerequisites:
              </div>
              <div style={{ display: 'flex', gap: '0.4rem', flexWrap: 'wrap' }}>
                {skill.prerequisites.map(p => (
                  <span key={p} className="badge badge-gray" style={{ fontSize: '0.72rem' }}>{p}</span>
                ))}
              </div>
            </div>
          )}
        </div>
      )}
    </div>
  );
};

// ── Phase Block ──────────────────────────────────────────────────────────────
const PhaseBlock: React.FC<{ phase: RoadmapPhase; colorSet: typeof PHASE_COLORS[0]; isLast: boolean }> = ({
  phase, colorSet, isLast
}) => {
  const [expandedSkills, setExpandedSkills] = useState<Set<string>>(new Set());
  const [phaseOpen, setPhaseOpen] = useState(true);

  const toggleSkill = (key: string) => {
    setExpandedSkills(prev => {
      const next = new Set(prev);
      next.has(key) ? next.delete(key) : next.add(key);
      return next;
    });
  };

  return (
    <div className="roadmap-phase">
      {/* Connector line */}
      {!isLast && (
        <div style={{
          position: 'absolute',
          left: '0.9rem',
          top: '2.5rem',
          bottom: 0,
          width: 2,
          background: `linear-gradient(to bottom, ${colorSet.dot}60, transparent)`,
        }} />
      )}

      {/* Phase dot */}
      <div
        className="roadmap-dot"
        style={{
          background: colorSet.bg,
          borderColor: colorSet.dot,
          color: colorSet.dot,
        }}
      >
        {phase.phase}
      </div>

      {/* Phase header */}
      <button
        onClick={() => setPhaseOpen(!phaseOpen)}
        style={{
          background: 'none', border: 'none', cursor: 'pointer',
          width: '100%', textAlign: 'left', padding: 0,
          marginBottom: phaseOpen ? '1rem' : 0,
          color: 'inherit', fontFamily: 'inherit',
        }}
      >
        <div style={{ display: 'flex', alignItems: 'center', justifyContent: 'space-between', gap: '0.75rem' }}>
          <div>
            <h4 style={{ fontSize: '1rem', color: 'var(--text-primary)', marginBottom: '0.2rem' }}>
              {phase.title}
            </h4>
            <div style={{ display: 'flex', alignItems: 'center', gap: '0.75rem' }}>
              <span style={{ fontSize: '0.78rem', color: 'var(--text-muted)' }}>
                📅 {phase.weeks_label}
              </span>
              <span style={{ fontSize: '0.78rem', color: 'var(--text-muted)' }}>
                ⚡ {phase.skills.length} skills
              </span>
              <span
                className={`badge ${phase.priority === 'critical' ? 'badge-danger' : 'badge-info'}`}
                style={{ fontSize: '0.7rem' }}
              >
                {phase.priority === 'critical' ? '🔴 Critical' : '⭐ Preferred'}
              </span>
            </div>
          </div>
          {phaseOpen ? <ChevronUp size={18} color="var(--text-muted)" /> : <ChevronDown size={18} color="var(--text-muted)" />}
        </div>
        <p style={{ fontSize: '0.82rem', color: 'var(--text-secondary)', marginTop: '0.4rem' }}>
          {phase.description}
        </p>
      </button>

      {/* Skills list */}
      {phaseOpen && (
        <div style={{ display: 'flex', flexDirection: 'column', gap: '0.5rem' }}>
          {phase.skills.map((skill) => (
            <SkillCard
              key={skill.key}
              skill={skill}
              isExpanded={expandedSkills.has(skill.key)}
              onToggle={() => toggleSkill(skill.key)}
            />
          ))}
        </div>
      )}
    </div>
  );
};

// ── Main Roadmap Component ───────────────────────────────────────────────────
const RoadmapTimeline: React.FC<Props> = ({ roadmap }) => {
  if (!roadmap.phases.length) {
    return (
      <div className="card" style={{ textAlign: 'center', padding: '3rem' }}>
        <div style={{ fontSize: '3rem', marginBottom: '1rem' }}>🎉</div>
        <h3>No Skill Gaps Found!</h3>
        <p className="text-secondary mt-2">
          {roadmap.message || "You're fully qualified for this role."}
        </p>
      </div>
    );
  }

  return (
    <div>
      {/* Header stats */}
      <div
        style={{
          display: 'flex', gap: '1rem', marginBottom: '1.5rem', flexWrap: 'wrap',
        }}
      >
        {[
          { icon: '📅', label: 'Total Duration', value: `${roadmap.total_weeks} weeks`, color: '#6366f1' },
          { icon: '🎯', label: 'Skills to Learn', value: `${roadmap.total_skills} skills`, color: '#10b981' },
          { icon: '📚', label: 'Learning Phases', value: `${roadmap.phases.length} phases`, color: '#f59e0b' },
        ].map(stat => (
          <div key={stat.label} style={{
            flex: 1, minWidth: 140,
            background: 'var(--bg-glass)',
            border: '1px solid var(--border)',
            borderRadius: 12,
            padding: '0.875rem 1rem',
            display: 'flex', alignItems: 'center', gap: '0.75rem',
          }}>
            <span style={{ fontSize: '1.5rem' }}>{stat.icon}</span>
            <div>
              <div style={{ fontSize: '1.25rem', fontWeight: 800, color: stat.color }}>{stat.value}</div>
              <div style={{ fontSize: '0.75rem', color: 'var(--text-muted)' }}>{stat.label}</div>
            </div>
          </div>
        ))}
      </div>

      {/* Phases */}
      <div>
        {roadmap.phases.map((phase, i) => (
          <PhaseBlock
            key={phase.phase}
            phase={phase}
            colorSet={PHASE_COLORS[i % PHASE_COLORS.length]}
            isLast={i === roadmap.phases.length - 1}
          />
        ))}
      </div>
    </div>
  );
};

export default RoadmapTimeline;
