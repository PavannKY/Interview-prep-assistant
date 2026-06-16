import { useState, useRef } from 'react'
import { Upload, FileText, CheckCircle, AlertCircle, Loader2 } from 'lucide-react'
import { uploadResume } from '../../api/client'
import clsx from 'clsx'

export default function ResumeUpload({ onSuccess }) {
  const [dragging, setDragging] = useState(false)
  const [file, setFile]         = useState(null)
  const [progress, setProgress] = useState(0)
  const [status, setStatus]     = useState('idle') // idle | uploading | success | error
  const [error, setError]       = useState('')
  const inputRef = useRef()

  const handleFile = (f) => {
    if (!f) return
    const ext = f.name.split('.').pop().toLowerCase()
    if (!['pdf', 'docx', 'doc'].includes(ext)) {
      setError('Only PDF and DOCX files are supported.')
      setStatus('error')
      return
    }
    setFile(f)
    setError('')
    setStatus('idle')
  }

  const handleDrop = (e) => {
    e.preventDefault()
    setDragging(false)
    handleFile(e.dataTransfer.files[0])
  }

  const handleUpload = async () => {
    if (!file) return
    setStatus('uploading')
    setProgress(0)

    try {
      const { data } = await uploadResume(file, setProgress)
      setStatus('success')
      onSuccess(data)
    } catch (err) {
      setStatus('error')
      setError(err.response?.data?.detail || 'Upload failed. Please try again.')
    }
  }

  return (
    <div className="max-w-xl mx-auto animate-slide-up">
      {/* Drop Zone */}
      <div
        onClick={() => inputRef.current?.click()}
        onDragOver={e => { e.preventDefault(); setDragging(true) }}
        onDragLeave={() => setDragging(false)}
        onDrop={handleDrop}
        className={clsx(
          'relative border-2 border-dashed rounded-2xl p-12 text-center cursor-pointer transition-all duration-200',
          dragging
            ? 'border-accent bg-accent-glow scale-[1.01]'
            : file
            ? 'border-accent/40 bg-accent-glow/50'
            : 'border-border hover:border-accent/60 hover:bg-accent-glow/30'
        )}
      >
        <input
          ref={inputRef}
          type="file"
          accept=".pdf,.docx,.doc"
          className="hidden"
          onChange={e => handleFile(e.target.files[0])}
        />

        <div className="flex flex-col items-center gap-4">
          {file ? (
            <FileText className="w-12 h-12 text-accent" />
          ) : (
            <Upload className="w-12 h-12 text-muted" />
          )}

          {file ? (
            <div>
              <p className="font-medium text-white">{file.name}</p>
              <p className="text-sm text-muted mt-1">{(file.size / 1024).toFixed(1)} KB</p>
            </div>
          ) : (
            <div>
              <p className="font-medium text-white">Drop your resume here</p>
              <p className="text-sm text-muted mt-1">PDF or DOCX · Max 10MB</p>
            </div>
          )}
        </div>
      </div>

      {/* Progress Bar */}
      {status === 'uploading' && (
        <div className="mt-4">
          <div className="h-1.5 bg-border rounded-full overflow-hidden">
            <div
              className="h-full bg-accent rounded-full transition-all duration-300"
              style={{ width: `${progress}%` }}
            />
          </div>
          <p className="text-xs text-muted mt-2 text-center">Parsing resume… {progress}%</p>
        </div>
      )}

      {/* Error */}
      {status === 'error' && (
        <div className="mt-4 flex items-center gap-2 text-danger text-sm bg-danger/10 border border-danger/20 rounded-xl px-4 py-3">
          <AlertCircle className="w-4 h-4 shrink-0" />
          {error}
        </div>
      )}

      {/* Success */}
      {status === 'success' && (
        <div className="mt-4 flex items-center gap-2 text-success text-sm bg-success/10 border border-success/20 rounded-xl px-4 py-3">
          <CheckCircle className="w-4 h-4 shrink-0" />
          Resume parsed successfully!
        </div>
      )}

      {/* Upload Button */}
      {file && status !== 'success' && (
        <button
          onClick={handleUpload}
          disabled={status === 'uploading'}
          className="btn-primary w-full mt-5 flex items-center justify-center gap-2"
        >
          {status === 'uploading' ? (
            <><Loader2 className="w-4 h-4 animate-spin" /> Analyzing Resume…</>
          ) : (
            <><Upload className="w-4 h-4" /> Upload & Start Interview</>
          )}
        </button>
      )}
    </div>
  )
}
