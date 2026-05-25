<div align="center">

<img src="https://img.shields.io/badge/AI--COS-Communication%20Operating%20System-blue?style=for-the-badge&logo=openai&logoColor=white" alt="AI-COS"/>

# 🎙️ AI Communication Operating System

### *Your Personal AI Coach for Fluent, Confident, Professional Communication*

[![FastAPI](https://img.shields.io/badge/FastAPI-0.111-009688?style=flat-square&logo=fastapi)](https://fastapi.tiangolo.com)
[![Next.js](https://img.shields.io/badge/Next.js-16-black?style=flat-square&logo=next.js)](https://nextjs.org)
[![Python](https://img.shields.io/badge/Python-3.11-3776AB?style=flat-square&logo=python)](https://python.org)
[![LangGraph](https://img.shields.io/badge/LangGraph-Multi--Agent-FF6B6B?style=flat-square)](https://langchain-ai.github.io/langgraph)
[![Whisper](https://img.shields.io/badge/Whisper-STT-412991?style=flat-square&logo=openai)](https://openai.com/research/whisper)
[![ChromaDB](https://img.shields.io/badge/ChromaDB-Vector%20DB-orange?style=flat-square)](https://trychroma.com)
[![Docker](https://img.shields.io/badge/Docker-Containerized-2496ED?style=flat-square&logo=docker)](https://docker.com)
[![License](https://img.shields.io/badge/License-MIT-green?style=flat-square)](LICENSE)

<br/>

> **Not a chatbot. Not a grammar checker. Not a tutorial project.**
>
> AI-COS is a production-grade, multi-agent voice AI platform with persistent memory,
> real-time speech analysis, mock interview simulation, and a premium analytics dashboard —
> all running 100% locally on your machine.

<br/>

[🚀 Live Demo](#demo) · [📖 Documentation](#architecture) · [⚡ Quick Start](#quick-start) · [🎯 Features](#features)

---

</div>

## 📸 Screenshots

| Landing Page | Voice Workspace | Interview Room |
|:---:|:---:|:---:|
| ![Landing](docs/landing.png) | ![Voice](docs/voice.png) | ![Interview](docs/interview.png) |

| Analytics Dashboard | AI Memory | Daily Planner |
|:---:|:---:|:---:|
| ![Analytics](docs/analytics.png) | ![Memory](docs/memory.png) | ![Planner](docs/planner.png) |

---

## 🧠 What is AI-COS?

Most people struggle with communication — not because they lack knowledge,
but because they lack a safe space to practice, get feedback, and improve consistently.

**AI-COS solves this** by being your always-available personal communication coach that:

- 🎤 **Listens** to you speak in real-time using Whisper STT
- 🤖 **Analyzes** your speech with 10 specialized AI agents running in parallel
- 💬 **Coaches** you with natural, personalized feedback using a local LLM
- 🧠 **Remembers** your history using ChromaDB RAG — every session builds on the last
- 📊 **Tracks** your improvement across fluency, grammar, confidence, and pronunciation
- 🎯 **Prepares** you for real interviews with dynamic mock simulation

---

## ✨ Features

### 🎙️ Real-time Voice AI Pipeline
```
Your mic → Browser (WebSocket) → FastAPI → Whisper STT → LangGraph Agents → Ollama LLM → gTTS → You hear AI coach
```
- Sub-3-second round trip from speaking to hearing AI response
- Word-level timestamp analysis from Whisper for pronunciation scoring
- Filler word detection (um, uh, basically, like)
- Speaking speed calculation (words per minute)

### 🤖 10 Specialized AI Agents (LangGraph)

| Agent | Role | Output |
|-------|------|--------|
| 🎯 Fluency Coach | Sentence flow, rhythm, speaking speed | Fluency score 0-100 + daily drill |
| ✍️ Grammar Agent | Mistakes, corrections, explanations | Corrected sentence + professional alternative |
| 🔊 Pronunciation Analyzer | Unclear words using Whisper confidence scores | Problem word list + phoneme drill |
| 💪 Confidence Agent | Filler words, pauses, hesitation patterns | Confidence score + psychology tips |
| 💼 Interview Coach | Mock interviews, answer evaluation | Score + feedback + follow-up question |
| 👥 Conversation Partner | 5 personas (recruiter, client, founder, friend, tech lead) | Natural contextual reply |
| 📚 Vocabulary Agent | Weak words, professional alternatives, spaced repetition | Daily word challenge |
| 📊 Analytics Agent | Overall score, weakest area, strongest area | Progress summary + weekly report |
| 🧠 Memory Agent | ChromaDB RAG storage and retrieval | Personalized coaching context |
| 📅 Planner Agent | Daily tasks adapted to your weak areas | Personalized daily plan |

### 💼 Interview Simulation System
- **11 interview types** — HR, Technical, AI Engineering, DevOps, Freelance, Project Explanation (FastAPI, RAG, AI Agents, SaaS), Storytelling, Confidence Building
- Dynamic follow-up questions based on your answers
- STAR method framework for behavioral questions
- Answer scoring with specific feedback and improvement tips
- Overall interview score at completion

### 🧠 Persistent Memory (RAG)
- Every session stored as vector embeddings in ChromaDB
- Semantic retrieval — AI finds relevant past conversations
- Progress tracking across all sessions
- Personalized coaching that gets smarter over time
- "Last time you used 12 filler words. This session: 3. Great improvement!"

### 📊 Premium Dashboard (Next.js)
- Real-time voice coaching workspace with live scores
- Analytics with fluency, confidence, grammar trends
- Vocabulary builder with 50+ professional words
- AI memory history — every session stored
- Daily planner with task checklist
- Dark theme, responsive, professional design

---

## 🏗️ Architecture

```
┌─────────────────────────────────────────────────────────────────┐
│                    Next.js Frontend (Port 3000)                  │
│  Landing │ Dashboard │ Voice │ Interview │ Analytics │ Memory    │
└──────────────────────────┬──────────────────────────────────────┘
                           │ WebSocket + REST API
┌──────────────────────────▼──────────────────────────────────────┐
│                   FastAPI Backend (Port 8000)                    │
│  /voice/ws │ /interview/ws │ /memory/* │ /health/* │ /static/*  │
└──────────────────────────┬──────────────────────────────────────┘
                           │
┌──────────────────────────▼──────────────────────────────────────┐
│              LangGraph Agent Orchestrator                        │
│                                                                  │
│  ┌──────────┐ ┌─────────┐ ┌──────────┐ ┌──────────────────┐   │
│  │ Fluency  │ │ Grammar │ │Confidence│ │  Pronunciation   │   │
│  └──────────┘ └─────────┘ └──────────┘ └──────────────────┘   │
│  ┌──────────┐ ┌─────────┐ ┌──────────┐ ┌──────────────────┐   │
│  │Interview │ │Convo    │ │ Vocab    │ │   Analytics      │   │
│  └──────────┘ └─────────┘ └──────────┘ └──────────────────┘   │
│  ┌──────────┐ ┌─────────┐                                      │
│  │ Memory   │ │ Planner │                                      │
│  └──────────┘ └─────────┘                                      │
└──────────────────────────┬──────────────────────────────────────┘
                           │
        ┌──────────────────┼──────────────────┐
        │                  │                  │
┌───────▼──────┐  ┌────────▼────┐  ┌─────────▼────────┐
│  Ollama LLM  │  │  Whisper    │  │    ChromaDB      │
│  LLaMA 3 8B  │  │  STT Local  │  │  Vector Memory   │
│  Port 11434  │  │  + gTTS     │  │  + PostgreSQL    │
└──────────────┘  └─────────────┘  └──────────────────┘
```

---

## 🛠️ Tech Stack

### Backend
| Technology | Version | Purpose |
|-----------|---------|---------|
| Python | 3.11 | Core language — best AI ecosystem |
| FastAPI | 0.111 | Async REST API + WebSocket server |
| Uvicorn | 0.30 | ASGI server for async operations |
| SQLAlchemy | 2.0 | Async ORM for PostgreSQL |
| Alembic | 1.13 | Database migration tracking |
| Pydantic | 2.7 | Request/response validation |

### AI / Machine Learning
| Technology | Purpose |
|-----------|---------|
| Ollama + LLaMA 3 (8B) | Local LLM — powers all 10 agents, zero API cost |
| LangChain 0.2 | Prompt management, chains, memory |
| LangGraph 0.1 | Multi-agent orchestration state machine |
| OpenAI Whisper (base) | Local speech-to-text with word timestamps |
| gTTS | Text-to-speech — AI coach voice output |
| Sentence Transformers | Text embeddings for RAG memory |

### Data
| Technology | Purpose |
|-----------|---------|
| PostgreSQL 16 | Users, sessions, scores, vocabulary |
| ChromaDB 0.5 | Vector database for RAG memory |
| Redis 7 | Cache, Celery task queue, pub/sub |

### Frontend
| Technology | Purpose |
|-----------|---------|
| Next.js 16 | React framework with App Router |
| TailwindCSS 3 | Utility-first styling |
| TypeScript | Type-safe frontend code |
| Recharts | Analytics charts |
| Lucide React | Icon system |

### Infrastructure
| Technology | Purpose |
|-----------|---------|
| Docker | Containerization |
| Docker Compose | Multi-service orchestration |
| Nginx | Reverse proxy (production) |
| Git | Version control |

---

## ⚡ Quick Start

### Prerequisites
- Python 3.11+
- Node.js 18+
- Docker Desktop
- Git Bash (Windows) or Terminal (Mac/Linux)

### 1. Clone the repository
```bash
git clone https://github.com/yourusername/ai-cos.git
cd ai-cos
```

### 2. Install backend dependencies
```bash
cd backend
python3.11 -m venv venv
source venv/bin/activate  # Windows Git Bash: source venv/Scripts/activate
pip install --upgrade pip setuptools wheel
pip install -r requirements.txt --no-build-isolation
```

### 3. Install frontend dependencies
```bash
cd ../frontend
npm install
```

### 4. Start databases
```bash
# From project root — make sure Docker Desktop is running
docker compose up -d
```

### 5. Install and start Ollama
```bash
# Install from https://ollama.com/download
ollama pull llama3
ollama serve &
```

### 6. Start the backend
```bash
cd backend
source venv/bin/activate
uvicorn app.main:app --host 0.0.0.0 --port 8000
```

### 7. Start the frontend
```bash
cd frontend
npm run dev
```

### 8. Open the application
```
Frontend Dashboard  →  http://localhost:3000
Backend API Docs    →  http://localhost:8000/docs
Voice Test Page     →  http://localhost:8000/static/test_voice.html
Interview Room      →  http://localhost:8000/static/interview.html
```

---

## 📁 Project Structure

```
ai-cos/
│
├── backend/                        # FastAPI Python backend
│   ├── app/
│   │   ├── main.py                 # App entry point, lifespan, CORS
│   │   ├── config.py               # All settings from .env
│   │   ├── database.py             # PostgreSQL async engine
│   │   │
│   │   ├── agents/                 # 10 specialized AI agents
│   │   │   ├── base.py             # BaseAgent abstract class
│   │   │   ├── fluency_agent.py    # Fluency scoring and drills
│   │   │   ├── grammar_agent.py    # Grammar detection and correction
│   │   │   ├── confidence_agent.py # Filler word and confidence scoring
│   │   │   ├── pronunciation_agent.py  # Whisper confidence analysis
│   │   │   ├── interview_agent.py  # Mock interview evaluation
│   │   │   ├── conversation_agent.py   # 5-persona conversation partner
│   │   │   ├── vocab_agent.py      # Vocabulary tracking
│   │   │   ├── analytics_agent.py  # Overall scoring
│   │   │   ├── memory_agent.py     # ChromaDB RAG storage
│   │   │   └── planner_agent.py    # Daily learning plan
│   │   │
│   │   ├── orchestrator/
│   │   │   └── graph.py            # LangGraph multi-agent orchestration
│   │   │
│   │   ├── routers/                # FastAPI route handlers
│   │   │   ├── voice.py            # WebSocket voice endpoint
│   │   │   ├── interview.py        # Interview WebSocket
│   │   │   ├── memory.py           # Memory/progress API
│   │   │   └── health.py           # Health check endpoints
│   │   │
│   │   ├── voice/                  # Speech processing
│   │   │   ├── stt.py              # Whisper STT + audio conversion
│   │   │   ├── tts.py              # gTTS text-to-speech
│   │   │   └── llm.py              # Ollama LLM client
│   │   │
│   │   ├── memory/                 # RAG memory system
│   │   │   ├── vector_store.py     # ChromaDB client and storage
│   │   │   └── retriever.py        # Semantic search and retrieval
│   │   │
│   │   └── models/                 # SQLAlchemy database models
│   │       ├── user.py
│   │       └── session.py
│   │
│   ├── alembic/                    # Database migrations
│   ├── static/                     # Served HTML test pages
│   └── requirements.txt
│
├── frontend/                       # Next.js TypeScript frontend
│   ├── app/
│   │   ├── page.tsx                # Landing page
│   │   ├── layout.tsx              # Root layout
│   │   └── dashboard/
│   │       ├── page.tsx            # Main dashboard
│   │       ├── voice/page.tsx      # Voice coaching workspace
│   │       ├── interview/page.tsx  # Interview room
│   │       ├── analytics/page.tsx  # Progress analytics
│   │       ├── vocab/page.tsx      # Vocabulary builder
│   │       ├── memory/page.tsx     # AI memory history
│   │       └── planner/page.tsx    # Daily planner
│   │
│   ├── components/
│   │   ├── Sidebar.tsx             # Navigation sidebar
│   │   └── ScoreCard.tsx           # Reusable score display
│   │
│   └── lib/
│       ├── api.ts                  # API client functions
│       └── utils.ts                # Utility functions
│
├── docker-compose.yml              # Development: PostgreSQL + Redis
├── docker-compose.prod.yml         # Production: Full stack
├── start.sh                        # One-command startup script
├── .env                            # Environment variables
└── README.md
```

---

## 🔌 API Reference

### Voice WebSocket
```
ws://localhost:8000/voice/ws

Messages you can send:
  { "type": "start_session" }
  { "type": "text_message", "text": "Hello" }
  { "type": "set_persona", "persona": "recruiter" }
  Binary: raw audio bytes (webm format)

Messages you receive:
  { "type": "transcript", "text": "..." }
  { "type": "analysis", "data": { scores... } }
  { "type": "coaching", "text": "..." }
  { "type": "agent_feedback", "data": { tips... } }
  Binary: MP3 audio bytes (AI voice response)
```

### REST Endpoints
```
GET  /health/          Basic health check
GET  /health/full      Full service health (DB, Redis, Ollama, ChromaDB)
GET  /voice/status     Voice pipeline status
GET  /voice/personas   Available conversation personas
GET  /memory/stats     ChromaDB statistics
GET  /memory/progress/{user_id}   User progress summary
GET  /memory/sessions/{user_id}   Session history
GET  /interview/types  Available interview types
```

---

## 🎯 Use Cases

| Who | How they use AI-COS | What improves |
|-----|-------------------|---------------|
| **AI/Tech job seekers** | Daily voice sessions + mock interviews | Confident technical communication |
| **DevOps transitioning to AI** | Project explanation coaching + AI interview prep | Can explain LLM, RAG, agents professionally |
| **Freelancers** | Client call simulation + proposal explanation | Win more projects, command higher rates |
| **Non-native English speakers** | Daily fluency drills + pronunciation coaching | Natural professional English |
| **Students** | Campus placement interview practice | Handle pressure interviews calmly |
| **Managers** | Presentation practice + storytelling mode | Clearer, more persuasive communication |

---

## 📈 Performance

| Metric | Value |
|--------|-------|
| Voice round-trip latency | < 3 seconds (local) |
| Whisper transcription speed | 200-600ms for 5-10 second audio |
| LLM response time | 500ms-2s (LLaMA 3 8B) |
| Agents running in parallel | 4 simultaneously |
| Memory retrieval speed | < 200ms (ChromaDB semantic search) |
| WebSocket connection | Persistent — no reconnection needed |

---

## 🚀 Deployment

### Development (current)
```bash
bash start.sh          # Start all services
cd frontend && npm run dev   # Start frontend
```

### Production (Docker)
```bash
docker compose -f docker-compose.prod.yml up -d
```

### Environment Variables
```env
DATABASE_URL=postgresql+asyncpg://user:pass@localhost:5432/aicos_db
REDIS_URL=redis://localhost:6379/0
OLLAMA_BASE_URL=http://127.0.0.1:11434
OLLAMA_MODEL=llama3
SECRET_KEY=your-secret-key-here
CHROMA_PERSIST_DIR=./chroma_data
AUDIO_UPLOAD_DIR=./audio_uploads
```

---

## 🧑‍💻 What I Learned Building This

This project taught me end-to-end AI engineering:

- **Multi-agent systems** — designing 10 agents with clear separation of concerns
- **RAG pipelines** — chunking, embedding, and semantic retrieval with ChromaDB
- **Real-time voice AI** — WebSocket streaming, audio format conversion, STT/TTS integration
- **Async FastAPI** — WebSocket handlers, background tasks, async database operations
- **Local LLM integration** — Ollama setup, model selection, prompt engineering
- **Production engineering** — Docker, health checks, error handling, logging
- **Full-stack development** — Next.js App Router, TypeScript, TailwindCSS

---

## 🤝 Contributing

Pull requests are welcome. For major changes, please open an issue first.

---

## 📄 License

MIT License — see [LICENSE](LICENSE) for details.

---

<div align="center">

**Built by Nikhat Shaikh** — Transitioning from DevOps to AI Engineering

[![LinkedIn](https://img.shields.io/badge/LinkedIn-Connect-0A66C2?style=flat-square&logo=linkedin)](https://linkedin.com/in/yourprofile)
[![GitHub](https://img.shields.io/badge/GitHub-Follow-181717?style=flat-square&logo=github)](https://github.com/yourusername)

*If this project helped you, please give it a ⭐ on GitHub*

</div>
