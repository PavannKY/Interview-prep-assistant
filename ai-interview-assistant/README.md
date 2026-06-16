# InterviewAI — AI-Powered Interview Assistant

> Phase 1 MVP: Resume Upload → Parse → Questions → Interview → Feedback

## Architecture

```
User
 │
 ├── Frontend (React + Tailwind + Vite)
 │    ├── ResumeUpload    — drag-drop PDF/DOCX upload
 │    ├── InterviewRoom   — adaptive Q&A with live evaluation
 │    └── FeedbackReport  — score chart, skill gaps, roadmap
 │
 └── Backend (FastAPI)
      ├── POST /resume/upload          → parse resume, create session
      ├── GET  /interview/:id/questions → generate 10 personalized questions
      ├── POST /interview/:id/answer    → evaluate answer (LLM-as-judge)
      └── GET  /feedback/:id           → final report + learning roadmap
```

## Quick Start

### 1. Clone & Configure

```bash
git clone <repo>
cd ai-interview-assistant
cp backend/.env.example backend/.env
# Edit backend/.env — add your OPENAI_API_KEY
```

### 2. Run with Docker (Recommended)

```bash
docker-compose up --build
```

- Frontend: http://localhost:5173
- Backend API: http://localhost:8000
- API Docs: http://localhost:8000/docs

### 3. Run Manually

**Backend:**
```bash
cd backend
python -m venv venv
source venv/bin/activate         # Windows: venv\Scripts\activate
pip install -r requirements.txt
python -m spacy download en_core_web_sm
uvicorn main:app --reload
```

**Frontend:**
```bash
cd frontend
npm install
npm run dev
```

## LLM Configuration

The backend is **OpenAI API compatible**. Swap to any local model:

| Model | Provider | .env settings |
|-------|----------|---------------|
| GPT-4o-mini | OpenAI | Default |
| Llama 3 8B | Ollama | `OPENAI_BASE_URL=http://localhost:11434/v1`, `LLM_MODEL=llama3` |
| Qwen 2.5 7B | Ollama | `LLM_MODEL=qwen2.5:7b` |
| Mistral 7B | Ollama | `LLM_MODEL=mistral` |

**To use Ollama (free, local):**
```bash
ollama serve
ollama pull llama3
# Then set in .env:
# OPENAI_BASE_URL=http://localhost:11434/v1
# LLM_MODEL=llama3
# OPENAI_API_KEY=ollama   (any non-empty string)
```

## Project Structure

```
ai-interview-assistant/
├── backend/
│   ├── main.py                    # FastAPI app + CORS
│   ├── requirements.txt
│   ├── .env.example
│   ├── models/
│   │   └── schemas.py             # All Pydantic models
│   ├── routers/
│   │   ├── resume.py              # Upload endpoint
│   │   ├── interview.py           # Questions + Answer endpoints
│   │   └── feedback.py            # Final report endpoint
│   ├── services/
│   │   ├── resume_parser.py       # PDF/DOCX → structured data
│   │   ├── question_generator.py  # Resume-aware question gen
│   │   ├── evaluator.py           # LLM-as-judge scoring
│   │   └── feedback.py            # Skill gap + roadmap gen
│   └── utils/
│       └── session_store.py       # In-memory sessions (MVP)
│
├── frontend/
│   ├── src/
│   │   ├── App.jsx                # Step router (upload→interview→report)
│   │   ├── api/client.js          # All API calls
│   │   └── components/
│   │       ├── upload/ResumeUpload.jsx
│   │       ├── interview/InterviewRoom.jsx
│   │       └── feedback/FeedbackReport.jsx
│   ├── tailwind.config.js
│   └── vite.config.js
│
└── docker-compose.yml
```

## Phase 2 Roadmap (from Blueprint)

- [ ] ChromaDB RAG for question retrieval
- [ ] spaCy NER for better skill extraction  
- [ ] PostgreSQL persistent sessions
- [ ] LangGraph adaptive interview agent
- [ ] Fine-tuned resume critic (LoRA/PEFT)
- [ ] Knowledge graph (NetworkX → Neo4j)
- [ ] Recruiter dashboard
- [ ] Anti-cheating monitoring
