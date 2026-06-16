import { useState, useEffect, useRef } from 'react'
import { getQuestions, submitAnswer } from '../../api/client'
import { Loader2, ChevronRight, Send, Clock, Brain, Star } from 'lucide-react'
import clsx from 'clsx'

const DIFFICULTY_COLOR = {
  easy:   'bg-success/15 text-success border-success/30',
  medium: 'bg-warning/15 text-warning border-warning/30',
  hard:   'bg-danger/15 text-danger border-danger/30',
}

export default function InterviewRoom({ sessionId, resumeData, onComplete }) {
  const [questions, setQuestions] = useState([])
  const [current, setCurrent]     = useState(0)
  const [answer, setAnswer]       = useState('')
  const [evaluation, setEval]     = useState(null)
  const [loading, setLoading]     = useState(true)
  const [submitting, setSubmitting] = useState(false)
  const [history, setHistory]     = useState([])  // [{question, answer, evaluation}]
  const textRef = useRef()

  useEffect(() => {
    loadQuestions()
  }, [])

  const loadQuestions = async () => {
    try {
      const { data } = await getQuestions(sessionId, 10)
      setQuestions(data.questions)
    } catch (e) {
      console.error(e)
    } finally {
      setLoading(false)
    }
  }

  const handleSubmit = async () => {
    if (!answer.trim() || submitting) return
    setSubmitting(true)

    const q = questions[current]
    try {
      const { data } = await submitAnswer(sessionId, {
        session_id: sessionId,
        question_id: q.id,
        question_text: q.question,
        answer: answer.trim(),
      })
      setEval(data)
      setHistory(h => [...h, { question: q, answer: answer.trim(), evaluation: data }])
    } catch (e) {
      console.error(e)
    } finally {
      setSubmitting(false)
    }
  }

  const handleNext = () => {
    if (current + 1 >= questions.length) {
      onComplete(history)
    } else {
      setCurrent(i => i + 1)
      setAnswer('')
      setEval(null)
      textRef.current?.focus()
    }
  }

  if (loading) {
    return (
      <div className="flex flex-col items-center justify-center min-h-[400px] gap-4 animate-fade-in">
        <Loader2 className="w-10 h-10 text-accent animate-spin" />
        <p className="text-muted">Generating your personalized questions…</p>
      </div>
    )
  }

  const q = questions[current]
  const isLast = current + 1 >= questions.length
  const progress = ((current) / questions.length) * 100

  return (
    <div className="max-w-3xl mx-auto animate-slide-up">
      {/* Progress */}
      <div className="flex items-center justify-between mb-3 text-sm text-muted">
        <span>Question {current + 1} of {questions.length}</span>
        <span>{Math.round(progress)}% complete</span>
      </div>
      <div className="h-1 bg-border rounded-full mb-8">
        <div
          className="h-full bg-accent rounded-full transition-all duration-500"
          style={{ width: `${((current + (evaluation ? 1 : 0)) / questions.length) * 100}%` }}
        />
      </div>

      {/* Question Card */}
      <div className="card mb-6">
        <div className="flex items-center gap-3 mb-5">
          <span className={clsx('badge border', DIFFICULTY_COLOR[q.difficulty])}>
            {q.difficulty}
          </span>
          <span className="badge bg-surface border border-border text-muted">
            {q.topic}
          </span>
          {q.expected_concepts.length > 0 && (
            <span className="text-xs text-muted ml-auto flex items-center gap-1">
              <Brain className="w-3 h-3" /> {q.expected_concepts.length} concepts
            </span>
          )}
        </div>

        <h2 className="font-display text-xl text-white leading-relaxed">
          {q.question}
        </h2>
      </div>

      {/* Answer Area */}
      {!evaluation ? (
        <div className="card">
          <textarea
            ref={textRef}
            value={answer}
            onChange={e => setAnswer(e.target.value)}
            placeholder="Type your answer here… Be specific, use examples from your experience."
            rows={6}
            autoFocus
            className="w-full bg-transparent text-white placeholder:text-muted resize-none outline-none font-body text-[15px] leading-relaxed"
            onKeyDown={e => {
              if (e.key === 'Enter' && e.ctrlKey) handleSubmit()
            }}
          />
          <div className="flex items-center justify-between mt-4 pt-4 border-t border-border">
            <span className="text-xs text-muted">Ctrl + Enter to submit</span>
            <button
              onClick={handleSubmit}
              disabled={!answer.trim() || submitting}
              className="btn-primary flex items-center gap-2"
            >
              {submitting ? (
                <><Loader2 className="w-4 h-4 animate-spin" /> Evaluating…</>
              ) : (
                <><Send className="w-4 h-4" /> Submit Answer</>
              )}
            </button>
          </div>
        </div>
      ) : (
        /* Evaluation Result */
        <EvaluationCard evaluation={evaluation} answer={answer} onNext={handleNext} isLast={isLast} />
      )}
    </div>
  )
}

function EvaluationCard({ evaluation, answer, onNext, isLast }) {
  const scoreColor =
    evaluation.score >= 8 ? 'text-success' :
    evaluation.score >= 5 ? 'text-warning' :
    'text-danger'

  return (
    <div className="space-y-4 animate-slide-up">
      {/* Score */}
      <div className="card flex items-center gap-6">
        <div className="text-center">
          <span className={clsx('font-display text-5xl font-bold', scoreColor)}>
            {evaluation.score}
          </span>
          <span className="text-muted text-lg">/10</span>
        </div>
        <div className="flex-1">
          <p className="text-white text-[15px] leading-relaxed">{evaluation.feedback}</p>
        </div>
      </div>

      {/* Strengths & Improvements */}
      <div className="grid grid-cols-2 gap-4">
        {evaluation.strengths.length > 0 && (
          <div className="card">
            <h4 className="text-success text-sm font-medium mb-3 flex items-center gap-2">
              <Star className="w-3.5 h-3.5" /> Strengths
            </h4>
            <ul className="space-y-1.5">
              {evaluation.strengths.map((s, i) => (
                <li key={i} className="text-sm text-muted leading-snug">• {s}</li>
              ))}
            </ul>
          </div>
        )}
        {evaluation.improvements.length > 0 && (
          <div className="card">
            <h4 className="text-warning text-sm font-medium mb-3">↑ To Improve</h4>
            <ul className="space-y-1.5">
              {evaluation.improvements.map((s, i) => (
                <li key={i} className="text-sm text-muted leading-snug">• {s}</li>
              ))}
            </ul>
          </div>
        )}
      </div>

      {/* Concepts */}
      {evaluation.concepts_missing.length > 0 && (
        <div className="card">
          <h4 className="text-sm font-medium text-muted mb-2">Concepts to study</h4>
          <div className="flex flex-wrap gap-2">
            {evaluation.concepts_missing.map((c, i) => (
              <span key={i} className="badge bg-danger/10 text-danger border border-danger/20">
                {c}
              </span>
            ))}
          </div>
        </div>
      )}

      <button
        onClick={onNext}
        className="btn-primary w-full flex items-center justify-center gap-2"
      >
        {isLast ? 'View Full Report' : 'Next Question'}
        <ChevronRight className="w-4 h-4" />
      </button>
    </div>
  )
}
