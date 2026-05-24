#!/bin/bash
# AI-COS Startup Script for Windows WSL2
# Run this every morning to start all services

echo ""
echo "  Starting AI-COS..."
echo "  ===================="
echo ""

# Go to project root
cd /mnt/d/AI-AGENTS/AI-COS

# Step 1 — Start Docker containers
echo "  [1/4] Starting PostgreSQL and Redis..."
docker compose up -d
sleep 5

# Step 2 — Check containers
POSTGRES_OK=$(docker exec aicos_postgres pg_isready -U aicos_user -d aicos_db 2>/dev/null && echo "yes" || echo "no")
REDIS_OK=$(docker exec aicos_redis redis-cli ping 2>/dev/null | grep -c PONG || echo "0")

if [ "$POSTGRES_OK" = "yes" ]; then
    echo "  PostgreSQL  OK"
else
    echo "  PostgreSQL  FAILED — check Docker Desktop is running"
    exit 1
fi

if [ "$REDIS_OK" -gt "0" ]; then
    echo "  Redis       OK"
else
    echo "  Redis       FAILED"
fi

# Step 3 — Start Ollama
echo ""
echo "  [2/4] Starting Ollama LLM server..."
ollama serve > /tmp/ollama.log 2>&1 &
sleep 3

OLLAMA_OK=$(curl -s --max-time 2 http://127.0.0.1:11434/api/tags > /dev/null 2>&1 && echo "yes" || echo "no")
if [ "$OLLAMA_OK" = "yes" ]; then
    echo "  Ollama      OK"
else
    echo "  Ollama      Already running or starting..."
fi

# Step 4 — Start FastAPI
echo ""
echo "  [3/4] Starting FastAPI backend..."
cd /mnt/d/AI-AGENTS/AI-COS/backend
source /mnt/d/AI-AGENTS/AI-COS/venv/bin/activate
uvicorn app.main:app --host 0.0.0.0 --port 8000 &
sleep 4

BACKEND_OK=$(curl -s --max-time 3 http://127.0.0.1:8000/health/ > /dev/null 2>&1 && echo "yes" || echo "no")
if [ "$BACKEND_OK" = "yes" ]; then
    echo "  FastAPI     OK — http://127.0.0.1:8000"
else
    echo "  FastAPI     Starting... (may take a few more seconds)"
fi

echo ""
echo "  [4/4] Services status:"
echo ""
echo "    Backend API    →  http://172.30.116.123:8000"
echo "    API Docs       →  http://172.30.116.123:8000/docs"
echo "    Health Check   →  http://172.30.116.123:8000/health/full"
echo "    Voice Test     →  http://172.30.116.123:8000/static/test_voice.html"
echo "    Interview Room →  http://172.30.116.123:8000/static/interview.html"
echo ""
echo "  Start Next.js frontend separately:"
echo "    cd /mnt/d/AI-AGENTS/AI-COS/frontend && npm run dev"
echo ""
echo "  Frontend       →  http://localhost:3000"
echo ""
echo "  AI-COS is ready!"
echo ""
