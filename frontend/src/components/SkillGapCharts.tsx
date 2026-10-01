import React, { useState } from 'react';
import {
  RadarChart, PolarGrid, PolarAngleAxis, Radar, ResponsiveContainer,
  BarChart, Bar, XAxis, YAxis, Tooltip, Legend, Cell,
  PieChart, Pie, AreaChart, Area, CartesianGrid,
} from 'recharts';
import type { ChartData, GapAnalysis } from '../api/client';

interface Props {
  chartData: ChartData;
  gapAnalysis: GapAnalysis;
}

// Custom tooltip style
const tooltipStyle = {
  backgroundColor: '#0d1117',
  border: '1px solid rgba(255,255,255,0.08)',
  borderRadius: 12,
  color: '#f1f5f9',
  fontSize: '0.85rem',
};

// ── Readiness Gauge ─────────────────────────────────────────────────────────
const ReadinessGauge: React.FC<{ score: number }> = ({ score }) => {
  const getColor = (s: number) => {
    if (s >= 80) return '#10b981';
    if (s >= 60) return '#6366f1';
    if (s >= 40) return '#f59e0b';
    return '#ef4444';
  };

  const getLabel = (s: number) => {
    if (s >= 80) return { text: 'Highly Ready', cls: 'badge-success' };
    if (s >= 60) return { text: 'Good Match', cls: 'badge-purple' };
    if (s >= 40) return { text: 'Needs Training', cls: 'badge-warning' };
    return { text: 'Skill Gap', cls: 'badge-danger' };
  };

  const label = getLabel(score);
  const color = getColor(score);

  // SVG arc gauge
  const r = 80;
  const cx = 110;
  const cy = 110;
  const startAngle = 210;
  const endAngle = 210 + (score / 100) * 300;

  const toRad = (deg: number) => (deg * Math.PI) / 180;
  const x1 = cx + r * Math.cos(toRad(startAngle));
  const y1 = cy + r * Math.sin(toRad(startAngle));
  const x2 = cx + r * Math.cos(toRad(endAngle));
  const y2 = cy + r * Math.sin(toRad(endAngle));
  const largeArc = (score / 100) * 300 > 180 ? 1 : 0;

  return (
    <div style={{ display: 'flex', flexDirection: 'column', alignItems: 'center', gap: '0.5rem' }}>
      <svg width={220} height={160} viewBox="0 0 220 160">
        {/* Background arc */}
        <path
          d={`M ${cx + r * Math.cos(toRad(210))} ${cy + r * Math.sin(toRad(210))} A ${r} ${r} 0 1 1 ${cx + r * Math.cos(toRad(510))} ${cy + r * Math.sin(toRad(510))}`}
          fill="none" stroke="rgba(255,255,255,0.07)" strokeWidth={14} strokeLinecap="round"
        />
        {/* Score arc */}
        {score > 0 && (
          <path
            d={`M ${x1} ${y1} A ${r} ${r} 0 ${largeArc} 1 ${x2} ${y2}`}
            fill="none" stroke={color} strokeWidth={14} strokeLinecap="round"
            style={{ filter: `drop-shadow(0 0 8px ${color}80)` }}
          />
        )}
        {/* Score text */}
        <text x={cx} y={cy + 12} textAnchor="middle" fill={color} fontSize={36} fontWeight={900} fontFamily="Inter">
          {Math.round(score)}
        </text>
        <text x={cx} y={cy + 32} textAnchor="middle" fill="rgba(148,163,184,0.8)" fontSize={13} fontFamily="Inter">
          Readiness %
        </text>
      </svg>
      <span className={`badge ${label.cls}`} style={{ fontSize: '0.85rem', padding: '0.3rem 0.9rem' }}>
        {label.text}
      </span>
    </div>
  );
};

// ── Radar Chart Component ────────────────────────────────────────────────────
const SkillRadar: React.FC<{ data: ChartData['radar_chart'] }> = ({ data }) => {
  if (!data || data.length === 0 || data.every(d => d.required === 0)) return null;
  return (
    <ResponsiveContainer width="100%" height={280}>
      <RadarChart data={data}>
        <PolarGrid stroke="rgba(255,255,255,0.08)" />
        <PolarAngleAxis
          dataKey="domain"
          tick={{ fill: 'rgba(148,163,184,0.9)', fontSize: 12 }}
        />
        <Radar
          name="Your Score"
          dataKey="score"
          stroke="#6366f1"
          fill="#6366f1"
          fillOpacity={0.25}
          strokeWidth={2}
        />
      </RadarChart>
    </ResponsiveContainer>
  );
};

// ── Category Match Bar Chart ─────────────────────────────────────────────────
const CategoryBar: React.FC<{ data: ChartData['category_match_chart'] }> = ({ data }) => {
  if (!data || data.length === 0) return null;
  return (
    <ResponsiveContainer width="100%" height={220}>
      <BarChart data={data} margin={{ top: 0, right: 10, left: -20, bottom: 0 }}>
        <CartesianGrid strokeDasharray="3 3" stroke="rgba(255,255,255,0.05)" />
        <XAxis
          dataKey="category"
          tick={{ fill: 'rgba(148,163,184,0.8)', fontSize: 11 }}
          axisLine={false}
          tickLine={false}
          angle={-20}
          textAnchor="end"
          height={48}
        />
        <YAxis tick={{ fill: 'rgba(148,163,184,0.8)', fontSize: 11 }} axisLine={false} tickLine={false} />
        <Tooltip
          contentStyle={tooltipStyle}
          cursor={{ fill: 'rgba(99,102,241,0.05)' }}
        />
        <Legend
          formatter={(val) => <span style={{ color: 'rgba(148,163,184,0.9)', fontSize: '0.8rem' }}>{val}</span>}
        />
        <Bar dataKey="matched" name="Matched" fill="#10b981" radius={[4, 4, 0, 0]} />
        <Bar dataKey="missing" name="Missing" fill="#ef4444" radius={[4, 4, 0, 0]} />
      </BarChart>
    </ResponsiveContainer>
  );
};

// ── Gap Donut Chart ──────────────────────────────────────────────────────────
const GapDonut: React.FC<{ data: ChartData['gap_donut'] }> = ({ data }) => {
  const filtered = data.filter(d => d.value > 0);
  if (!filtered.length) return null;

  return (
    <ResponsiveContainer width="100%" height={200}>
      <PieChart>
        <Pie
          data={filtered}
          cx="50%"
          cy="50%"
          innerRadius={55}
          outerRadius={80}
          dataKey="value"
          stroke="none"
          paddingAngle={3}
          label={({ label, percent }) =>
            percent > 0.08 ? `${label} ${(percent * 100).toFixed(0)}%` : ''
          }
          labelLine={false}
        >
          {filtered.map((entry, i) => (
            <Cell key={i} fill={entry.color} />
          ))}
        </Pie>
        <Tooltip
          contentStyle={tooltipStyle}
          formatter={(val: number, name: string) => [`${val} skills`, name]}
        />
      </PieChart>
    </ResponsiveContainer>
  );
};

// ── Roadmap Timeline ─────────────────────────────────────────────────────────
const TimelineChart: React.FC<{ data: ChartData['roadmap_timeline'] }> = ({ data }) => {
  if (!data || data.length === 0) return null;
  const colors = ['#6366f1', '#10b981', '#f59e0b', '#06b6d4'];

  return (
    <div style={{ display: 'flex', flexDirection: 'column', gap: '0.75rem', paddingTop: '0.5rem' }}>
      {data.map((phase, i) => (
        <div key={phase.phase}>
          <div className="flex justify-between text-sm mb-1">
            <span style={{ color: 'var(--text-primary)', fontWeight: 600, fontSize: '0.875rem' }}>
              {phase.title}
            </span>
            <span style={{ color: 'var(--text-muted)', fontSize: '0.8rem' }}>
              Wk {phase.week_start}–{phase.week_end} · {phase.skill_count} skills
            </span>
          </div>
          <div className="progress-bar" style={{ height: 12, borderRadius: 6 }}>
            <div
              className="progress-fill"
              style={{
                width: `${Math.min((phase.duration / Math.max(...data.map(d => d.duration))) * 100, 100)}%`,
                background: colors[i % colors.length],
                borderRadius: 6,
                boxShadow: `0 0 10px ${colors[i % colors.length]}60`,
              }}
            />
          </div>
        </div>
      ))}
    </div>
  );
};

// ── Main Charts Component ────────────────────────────────────────────────────
const SkillGapCharts: React.FC<Props> = ({ chartData, gapAnalysis }) => {
  const [activeTab, setActiveTab] = useState<'overview' | 'radar' | 'timeline'>('overview');

  return (
    <div style={{ display: 'flex', flexDirection: 'column', gap: '1.5rem' }}>

      {/* Row 1: Readiness + Donut */}
      <div className="grid-2">
        <div className="card" style={{ textAlign: 'center' }}>
          <h4 className="mb-4" style={{ color: 'var(--text-secondary)', fontSize: '0.875rem', textTransform: 'uppercase', letterSpacing: '0.05em' }}>
            Job Readiness Score
          </h4>
          <ReadinessGauge score={chartData.readiness_score} />
          <p className="text-sm text-secondary mt-4" style={{ maxWidth: 280, margin: '1rem auto 0' }}>
            {gapAnalysis.summary}
          </p>
        </div>

        <div className="card">
          <h4 className="mb-3" style={{ color: 'var(--text-secondary)', fontSize: '0.875rem', textTransform: 'uppercase', letterSpacing: '0.05em' }}>
            Skill Breakdown
          </h4>
          <GapDonut data={chartData.gap_donut} />
          <div style={{ display: 'grid', gridTemplateColumns: '1fr 1fr', gap: '0.5rem', marginTop: '0.75rem' }}>
            {chartData.gap_donut.filter(d => d.value > 0).map((item) => (
              <div key={item.label} className="flex items-center gap-2">
                <span style={{ width: 10, height: 10, borderRadius: '50%', background: item.color, flexShrink: 0 }} />
                <span style={{ fontSize: '0.78rem', color: 'var(--text-secondary)' }}>
                  {item.label}: <strong style={{ color: 'var(--text-primary)' }}>{item.value}</strong>
                </span>
              </div>
            ))}
          </div>
        </div>
      </div>

      {/* Tabs: Category Match | Radar | Timeline */}
      <div className="card">
        <div className="flex justify-between items-center mb-4">
          <h4 style={{ fontSize: '0.875rem', textTransform: 'uppercase', letterSpacing: '0.05em', color: 'var(--text-secondary)' }}>
            Skill Analysis
          </h4>
          <div className="tabs" style={{ width: 'auto' }}>
            {(['overview', 'radar', 'timeline'] as const).map((tab) => (
              <button
                key={tab}
                className={`tab-btn ${activeTab === tab ? 'active' : ''}`}
                onClick={() => setActiveTab(tab)}
                style={{ padding: '0.4rem 0.875rem', fontSize: '0.8rem' }}
              >
                {tab === 'overview' ? 'By Category' : tab === 'radar' ? 'Radar' : 'Timeline'}
              </button>
            ))}
          </div>
        </div>

        {activeTab === 'overview' && (
          <CategoryBar data={chartData.category_match_chart} />
        )}
        {activeTab === 'radar' && (
          <SkillRadar data={chartData.radar_chart} />
        )}
        {activeTab === 'timeline' && (
          <TimelineChart data={chartData.roadmap_timeline} />
        )}
      </div>

      {/* Stats row */}
      <div className="grid-4">
        {[
          { label: 'Required Skills', value: gapAnalysis.stats.total_required, color: 'var(--primary-light)', icon: '🎯' },
          { label: 'Skills Matched', value: gapAnalysis.stats.total_matched, color: 'var(--secondary-light)', icon: '✅' },
          { label: 'Critical Gaps', value: gapAnalysis.stats.total_missing_critical, color: '#fca5a5', icon: '🔴' },
          { label: 'Transferable', value: gapAnalysis.stats.total_transferable, color: '#a5b4fc', icon: '🔄' },
        ].map((stat) => (
          <div key={stat.label} className="card" style={{ textAlign: 'center', padding: '1.25rem' }}>
            <div style={{ fontSize: '1.5rem', marginBottom: '0.5rem' }}>{stat.icon}</div>
            <div style={{ fontSize: '2rem', fontWeight: 900, color: stat.color, lineHeight: 1 }}>
              {stat.value}
            </div>
            <div className="text-xs text-secondary mt-2">{stat.label}</div>
          </div>
        ))}
      </div>
    </div>
  );
};

export default SkillGapCharts;
