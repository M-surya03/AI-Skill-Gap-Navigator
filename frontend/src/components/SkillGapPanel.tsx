import React from 'react';
import { CheckCircle2, XCircle, AlertCircle, ArrowRight } from 'lucide-react';
import type { GapAnalysis, SkillInfo } from '../api/client';

interface Props {
  gapAnalysis: GapAnalysis;
}

const DifficultyDots: React.FC<{ difficulty: number }> = ({ difficulty }) => (
  <div style={{ display: 'flex', gap: 3 }}>
    {[1, 2, 3, 4, 5].map(d => (
      <span
        key={d}
        style={{
          width: 6, height: 6, borderRadius: '50%',
          background: d <= difficulty
            ? `hsl(${240 - d * 30}, 80%, 65%)`
            : 'rgba(255,255,255,0.1)',
        }}
      />
    ))}
  </div>
);

const SkillRow: React.FC<{ skill: SkillInfo; type: 'matched' | 'missing' | 'preferred' }> = ({ skill, type }) => {
  const styles = {
    matched: { icon: <CheckCircle2 size={14} color="#10b981" />, bg: 'rgba(16,185,129,0.06)', border: 'rgba(16,185,129,0.2)', tag: '#10b981' },
    missing: { icon: <XCircle size={14} color="#ef4444" />, bg: 'rgba(239,68,68,0.06)', border: 'rgba(239,68,68,0.2)', tag: '#ef4444' },
    preferred: { icon: <AlertCircle size={14} color="#f59e0b" />, bg: 'rgba(245,158,11,0.06)', border: 'rgba(245,158,11,0.2)', tag: '#f59e0b' },
  }[type];

  return (
    <div style={{
      display: 'flex', alignItems: 'center', gap: '0.75rem',
      padding: '0.625rem 0.875rem',
      background: styles.bg,
      border: `1px solid ${styles.border}`,
      borderRadius: 10,
      transition: 'all 0.15s',
    }}>
      <span style={{ flexShrink: 0 }}>{styles.icon}</span>
      <span style={{ flex: 1, fontSize: '0.875rem', fontWeight: 500, color: 'var(--text-primary)' }}>
        {skill.canonical}
      </span>
      <span style={{ fontSize: '0.72rem', color: 'var(--text-muted)' }}>{skill.category}</span>
      <DifficultyDots difficulty={skill.difficulty} />
      <span style={{
        fontSize: '0.72rem', color: styles.tag,
        background: `${styles.tag}20`,
        padding: '0.1rem 0.5rem',
        borderRadius: 999,
      }}>
        {skill.avg_weeks_to_learn}w
      </span>
    </div>
  );
};

const SkillSection: React.FC<{
  title: string;
  icon: React.ReactNode;
  skills: SkillInfo[];
  type: 'matched' | 'missing' | 'preferred';
  accent: string;
}> = ({ title, icon, skills, type, accent }) => {
  if (!skills.length) return null;
  return (
    <div>
      <div style={{ display: 'flex', alignItems: 'center', gap: '0.625rem', marginBottom: '0.875rem' }}>
        <span style={{
          width: 28, height: 28,
          background: `${accent}20`,
          border: `1px solid ${accent}40`,
          borderRadius: 8,
          display: 'flex', alignItems: 'center', justifyContent: 'center',
        }}>
          {icon}
        </span>
        <span style={{ fontWeight: 700, fontSize: '0.875rem', color: 'var(--text-primary)' }}>{title}</span>
        <span style={{ fontSize: '0.75rem', color: 'var(--text-muted)', background: 'var(--bg-glass)', padding: '0.1rem 0.5rem', borderRadius: 999 }}>
          {skills.length}
        </span>
      </div>
      <div style={{ display: 'flex', flexDirection: 'column', gap: '0.4rem' }}>
        {skills.map(s => <SkillRow key={s.key} skill={s} type={type} />)}
      </div>
    </div>
  );
};

const SkillGapPanel: React.FC<Props> = ({ gapAnalysis }) => {
  return (
    <div style={{ display: 'flex', flexDirection: 'column', gap: '1.75rem' }}>
      <SkillSection
        title="Skills You Already Have ✓"
        icon={<CheckCircle2 size={14} color="#10b981" />}
        skills={gapAnalysis.matched}
        type="matched"
        accent="#10b981"
      />
      <SkillSection
        title="Critical Skills to Acquire"
        icon={<XCircle size={14} color="#ef4444" />}
        skills={gapAnalysis.missing_critical}
        type="missing"
        accent="#ef4444"
      />
      <SkillSection
        title="Preferred Skills to Add"
        icon={<AlertCircle size={14} color="#f59e0b" />}
        skills={gapAnalysis.missing_preferred}
        type="preferred"
        accent="#f59e0b"
      />

      {/* Transferable skills */}
      {gapAnalysis.transferable.length > 0 && (
        <div>
          <div style={{ display: 'flex', alignItems: 'center', gap: '0.625rem', marginBottom: '0.875rem' }}>
            <span style={{
              width: 28, height: 28, background: 'rgba(99,102,241,0.2)',
              border: '1px solid rgba(99,102,241,0.4)',
              borderRadius: 8, display: 'flex', alignItems: 'center', justifyContent: 'center',
            }}>
              <ArrowRight size={14} color="#818cf8" />
            </span>
            <span style={{ fontWeight: 700, fontSize: '0.875rem', color: 'var(--text-primary)' }}>
              Transferable Skills 🔄
            </span>
            <span style={{ fontSize: '0.75rem', color: 'var(--text-muted)', background: 'var(--bg-glass)', padding: '0.1rem 0.5rem', borderRadius: 999 }}>
              {gapAnalysis.transferable.length}
            </span>
          </div>
          <div style={{ display: 'flex', flexDirection: 'column', gap: '0.5rem' }}>
            {gapAnalysis.transferable.map(t => (
              <div key={t.target_skill} style={{
                padding: '0.75rem 1rem',
                background: 'rgba(99,102,241,0.06)',
                border: '1px solid rgba(99,102,241,0.2)',
                borderRadius: 10,
              }}>
                <div style={{ display: 'flex', alignItems: 'center', gap: '0.5rem', flexWrap: 'wrap' }}>
                  {t.transferable_from.map(f => (
                    <span key={f} style={{ fontSize: '0.8rem', fontWeight: 600, color: '#a5b4fc', background: 'rgba(99,102,241,0.15)', padding: '0.15rem 0.6rem', borderRadius: 999 }}>
                      {f}
                    </span>
                  ))}
                  <ArrowRight size={14} color="var(--text-muted)" />
                  <span style={{ fontSize: '0.8rem', fontWeight: 600, color: 'var(--text-primary)' }}>
                    {t.target_canonical}
                  </span>
                  <span style={{
                    marginLeft: 'auto', fontSize: '0.72rem',
                    color: '#10b981', background: 'rgba(16,185,129,0.1)',
                    padding: '0.1rem 0.5rem', borderRadius: 999,
                  }}>
                    {t.transfer_score}% transferable
                  </span>
                </div>
              </div>
            ))}
          </div>
        </div>
      )}
    </div>
  );
};

export default SkillGapPanel;
