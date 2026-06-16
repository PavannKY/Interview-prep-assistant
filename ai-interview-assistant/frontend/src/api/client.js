import axios from 'axios'

const api = axios.create({
  baseURL: import.meta.env.VITE_API_URL || 'http://localhost:8000',
  timeout: 60000,
})

// ─── Resume ───────────────────────────────────────────────────────────────────

export const uploadResume = (file, onProgress) => {
  const form = new FormData()
  form.append('file', file)
  return api.post('/resume/upload', form, {
    headers: { 'Content-Type': 'multipart/form-data' },
    onUploadProgress: e => onProgress?.(Math.round((e.loaded / e.total) * 100)),
  })
}

// ─── Interview ────────────────────────────────────────────────────────────────

export const getQuestions = (sessionId, numQuestions = 10) =>
  api.get(`/interview/${sessionId}/questions`, { params: { num_questions: numQuestions } })

export const submitAnswer = (sessionId, payload) =>
  api.post(`/interview/${sessionId}/answer`, payload)

export const getSessionState = (sessionId) =>
  api.get(`/interview/${sessionId}/state`)

// ─── Feedback ─────────────────────────────────────────────────────────────────

export const getFeedback = (sessionId) =>
  api.get(`/feedback/${sessionId}`)
