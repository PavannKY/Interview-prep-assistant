import { useState, useEffect } from 'react'
import { getFeedback } from '../../api/client'
import {
  RadarChart, Radar, PolarGrid, PolarAngleAxis, ResponsiveContainer,
  BarChart, Bar, XAxis, YAxis, Tooltip, Cell
} from 'recharts'
import { Loader2, TrendingUp, TrendingDown, BookOpen, AlertTriangle, CheckCircle2, RotateCcw } from 'lucide-react'
import clsx from 'clsx'

const SCORE_COLOR = (s) =>
  s >= 7 ? '#10B981' : s >= 4 ? '#F59E0B' : '#EF4444'

export default function FeedbackReport({ sessionId, history, onRestart }) {
  const [report, setReport] = useState(null)
  const [loading, setLoading] = useState(true)
  const [error, setError]   = useState('')

  useEffect(() => {
    loadReport()
  }, [])

  const loadReport = async () => {
    try {
      const { data } = await getFeedback(sessionId)
      setReport(data)
    } catch (e) {
      setError(e.response?.data?.detail || 'Failed to generate report.')
    } finally {
      setLoading(false)
    }
  }

  if (loading) return (
    <div className="flex flex-col items-center justify-center min-h-[400px] gap-4">
      <Loader2 className="w-10 h-10 text-accent animate-spin" />
      <p className="text-muted">Generating your report…</p>
    </div>
  )

  if (error) return (
    <div className="text-center text-danger py-16">{error}</div>
  )

  // Chart data from history
  const barData = history.map(({ question, evaluation }) => ({
    name: question.topic,
    score: evaluation.score,
  }))

  const overall = report.overall_score

  return (
    <div className="max-w-4xl mx-auto space-y-6 animate-slide-up">
      {/* Header */}
      <div className="card text-center py-10">
        <div className="flex items-center justify-center mb-4">
          <div className={clsx(
            'w-28 h-28 rounded-full flex items-center justify-center border-4',
            overall >= 7 ? 'border-success bg-success/10' :
            overall >= 4 ? 'border-warning bg-warning/10' :
            'border-danger bg-danger/10'
          )}>
            <span className="font-display text-5xl text-white">{overall}</span>
          </div>
        </div>
        <h1 className="font-display text-3xl text-white mb-2">Interview Complete</h1>
        <p className="text-muted max-w-lg mx-auto">{report.performance_summary}</p>
        <div className="mt-4">
          {report.interview_ready ? (
            <span className="badge bg-success/15 text-success border border-success/30 text-sm px-4 py-1.5">
              <CheckCircle2 className="w-4 h-4" /> Interview Ready
            </span>
          ) : (
            <span className="badge bg-warning/15 text-warning border border-warning/30 text-sm px-4 py-1.5">
              <AlertTriangle className="w-4 h-4" /> Needs More Preparation
            </span>
          )}
        </div>
      </div>

      {/* Score Chart */}
      <div className="card">
        <h3 className="font-medium text-white mb-5">Score per Question</h3>
        <ResponsiveContainer width="100%" height={200}>
          <BarChart data={barData} barSize={28}>
            <XAxis dataKey="name" tick={{ fill: '#6B7280', fontSize: 12 }} axisLine={false} tickLine={false} />
            <YAxis domain={[0, 10]} tick={{ fill: '#6B7280', fontSize: 12 }} axisLine={false} tickLine={false} />
            <Tooltip
              contentStyle={{ background: '#1A1A26', border: '1px solid #2A2A3E', borderRadius: 12 }}
              labelStyle={{ color: '#E8E8F0' }}
              itemStyle={{ color: '#6C63FF' }}
            />
            <Bar dataKey="score" radius={[6, 6, 0, 0]}>
              {barData.map((entry, i) => (
                <Cell key={i} fill={SCORE_COLOR(entry.score)} />
              ))}
            </Bar>
          </BarChart>
        </ResponsiveContainer>
      </div>

      {/* Strengths & Weaknesses */}
      <div className="grid grid-cols-2 gap-4">
        <div className="card">
          <h3 className="text-success font-medium mb-4 flex items-center gap-2">
            <TrendingUp className="w-4 h-4" /> Strongest Areas
          </h3>
          <ul className="space-y-2">
            {report.strongest_areas.map((a, i) => (
              <li key={i} className="flex items-center gap-2 text-sm text-muted">
                <span className="w-1.5 h-1.5 rounded-full bg-success" />{a}
              </li>
            ))}
          </ul>
        </div>
        <div className="card">
          <h3 className="text-warning font-medium mb-4 flex items-center gap-2">
            <TrendingDown className="w-4 h-4" /> Areas to Improve
          </h3>
          <ul className="space-y-2">
            {report.weakest_areas.map((a, i) => (
              <li key={i} className="flex items-center gap-2 text-sm text-muted">
                <span className="w-1.5 h-1.5 rounded-full bg-warning" />{a}
              </li>
            ))}
          </ul>
        </div>
      </div>

      {/* Skill Gaps */}
      {report.skill_gaps.length > 0 && (
        <div className="card">
          <h3 className="font-medium text-white mb-5">Skill Gaps</h3>
          <div className="space-y-3">
            {report.skill_gaps.map((gap, i) => (
              <div key={i} className="flex items-center gap-4 p-3 bg-surface rounded-xl">
                <div className="flex-1">
                  <span className="text-white text-sm font-medium">{gap.skill}</span>
                  <div className="flex items-center gap-2 mt-1">
                    <span className="badge bg-danger/10 text-danger text-xs border border-danger/20">{gap.current_level}</span>
                    <span className="text-muted text-xs">→</span>
                    <span className="badge bg-success/10 text-success text-xs border border-success/20">{gap.required_level}</span>
                  </div>
                </div>
                {gap.resources.length > 0 && (
                  <div className="text-xs text-accent">{gap.resources[0]}</div>
                )}
              </div>
            ))}
          </div>
        </div>
      )}

      {/* Resume Feedback */}
      {report.resume_feedback.length > 0 && (
        <div className="card">
          <h3 className="font-medium text-white mb-4">Resume Improvements</h3>
          <ul className="space-y-2">
            {report.resume_feedback.map((tip, i) => (
              <li key={i} className="flex items-start gap-2 text-sm text-muted">
                <span className="text-accent mt-0.5">✦</span>{tip}
              </li>
            ))}
          </ul>
        </div>
      )}

      {/* Learning Roadmap */}
      {report.learning_roadmap.length > 0 && (
        <div className="card">
          <h3 className="font-medium text-white mb-5 flex items-center gap-2">
            <BookOpen className="w-4 h-4 text-accent" /> Learning Roadmap
          </h3>
          <div className="space-y-3">
            {report.learning_roadmap.map((week, i) => (
              <div key={i} className="flex gap-4 p-4 bg-surface rounded-xl">
                <span className="text-xs font-mono text-accent whitespace-nowrap pt-0.5">{week.week}</span>
                <div>
                  <p className="text-white text-sm font-medium">{week.focus}</p>
                  {week.resources.map((r, j) => (
                    <p key={j} className="text-xs text-muted mt-1">• {r}</p>
                  ))}
                </div>
              </div>
            ))}
          </div>
        </div>
      )}

      {/* Restart */}
      <button
        onClick={onRestart}
        className="btn-ghost w-full flex items-center justify-center gap-2"
      >
        <RotateCcw className="w-4 h-4" /> Start a New Interview
      </button>
    </div>
  )
}
