# 🚀 AI Communication Operating System (AI-COS)

A production-grade, multi-agent voice AI platform that coaches you to become
a confident, fluent, and professional communicator.

## What it does

- **Real-time voice coaching** — Speak and get instant AI feedback
- **10 specialized AI agents** — Each focused on one aspect of communication
- **Mock interview simulator** — HR, Technical, AI Engineering interviews
- **Persistent AI memory** — Remembers your history using ChromaDB RAG
- **Analytics dashboard** — Track improvement over time
- **100% local** — Runs on your machine, no cloud costs

## Tech Stack

| Layer | Technology |
|-------|-----------|
| Backend | Python, FastAPI, WebSockets |
| AI Agents | LangGraph, LangChain, Ollama (LLaMA 3) |
| Voice STT | OpenAI Whisper (local) |
| Voice TTS | gTTS |
| Memory | ChromaDB, RAG pipeline |
| Database | PostgreSQL, Redis |
| Frontend | Next.js 16, TailwindCSS |
| Infrastructure | Docker, Docker Compose |

## Quick Start

```bash
# Clone the repo
git clone https://github.com/yourusername/ai-cos.git
cd ai-cos

# Start all services
bash start.sh

# Start frontend (separate terminal)
cd frontend && npm run dev
```

## Architecture
Browser (Next.js)
↓ WebSocket
FastAPI Backend
↓
LangGraph Orchestrator
↓
10 AI Agents (parallel)
↓
Ollama LLaMA 3 (local LLM)
↓
ChromaDB (persistent memory)
PostgreSQL (structured data)

## The 10 AI Agents

1. **Fluency Coach** — Flow, rhythm, speaking speed
2. **Grammar Agent** — Mistakes, corrections, explanations
3. **Pronunciation Analyzer** — Unclear words, phoneme drills
4. **Confidence Agent** — Filler words, hesitation, pauses
5. **Interview Coach** — Mock interviews, answer scoring
6. **Conversation Partner** — 5 personas for practice
7. **Vocabulary Agent** — Professional word building
8. **Analytics Agent** — Progress tracking
9. **Memory Agent** — ChromaDB RAG persistence
10. **Learning Planner** — Daily personalized tasks

## Portfolio Value

This project demonstrates:
- Multi-agent AI system design
- Real-time voice AI pipeline
- RAG with vector databases
- Production FastAPI architecture
- WebSocket streaming
- Next.js dashboard development
- Local LLM integration
- Docker deployment

Built by Nikhat Shaikh — AI Engineer
