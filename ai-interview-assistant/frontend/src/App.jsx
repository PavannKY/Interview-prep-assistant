import { useState } from 'react'
import ResumeUpload from './components/upload/ResumeUpload'
import InterviewRoom from './components/interview/InterviewRoom'
import FeedbackReport from './components/feedback/FeedbackReport'
import { Cpu, CircleDot } from 'lucide-react'

const STEPS = ['Upload', 'Interview', 'Report']

export default function App() {
  const [step, setStep]         = useState(0)   // 0=upload 1=interview 2=feedback
  const [sessionId, setSession] = useState(null)
  const [resumeData, setResume] = useState(null)
  const [history, setHistory]   = useState([])

  const handleResumeSuccess = (data) => {
    setSession(data.session_id)
    setResume(data.parsed)
    setTimeout(() => setStep(1), 800)
  }

  const handleInterviewComplete = (interviewHistory) => {
    setHistory(interviewHistory)
    setStep(2)
  }

  const handleRestart = () => {
    setStep(0)
    setSession(null)
    setResume(null)
    setHistory([])
  }

  return (
    <div className="min-h-screen bg-ink">
      {/* Nav */}
      <header className="border-b border-border px-8 py-4 flex items-center justify-between sticky top-0 bg-ink/80 backdrop-blur z-10">
        <div className="flex items-center gap-2.5">
          <div className="w-8 h-8 rounded-lg bg-accent flex items-center justify-center animate-pulse-ring">
            <Cpu className="w-4 h-4 text-white" />
          </div>
          <span className="font-display text-lg text-white">InterviewAI</span>
        </div>

        {/* Step Indicators */}
        <div className="flex items-center gap-2">
          {STEPS.map((label, i) => (
            <div key={i} className="flex items-center gap-2">
              <div className={`flex items-center gap-1.5 text-xs font-medium transition-colors ${
                i === step ? 'text-accent' : i < step ? 'text-success' : 'text-muted'
              }`}>
                <CircleDot className="w-3 h-3" />
                {label}
              </div>
              {i < STEPS.length - 1 && (
                <div className={`w-8 h-px ${i < step ? 'bg-success' : 'bg-border'}`} />
              )}
            </div>
          ))}
        </div>
      </header>

      {/* Main */}
      <main className="px-6 py-12">
        {step === 0 && (
          <div className="animate-fade-in">
            <div className="text-center mb-12">
              <h1 className="font-display text-4xl text-white mb-3">
                Be Interview Ready
              </h1>
              <p className="text-muted max-w-md mx-auto">
                Upload your resume and get a personalized AI interview — questions tailored to your exact experience, with real-time feedback.
              </p>
            </div>
            <ResumeUpload onSuccess={handleResumeSuccess} />
          </div>
        )}

        {step === 1 && sessionId && (
          <div>
            {/* Resume context bar */}
            <div className="max-w-3xl mx-auto mb-8 card flex items-center gap-4 py-3 px-5">
              <div className="w-8 h-8 rounded-full bg-accent/20 flex items-center justify-center text-accent font-display text-sm">
                {resumeData?.name?.[0] || '?'}
              </div>
              <div>
                <p className="text-white text-sm font-medium">{resumeData?.name || 'Candidate'}</p>
                <p className="text-xs text-muted">{resumeData?.skills?.slice(0, 4).join(' · ')}</p>
              </div>
            </div>
            <InterviewRoom
              sessionId={sessionId}
              resumeData={resumeData}
              onComplete={handleInterviewComplete}
            />
          </div>
        )}

        {step === 2 && sessionId && (
          <FeedbackReport
            sessionId={sessionId}
            history={history}
            onRestart={handleRestart}
          />
        )}
      </main>
    </div>
  )
}
