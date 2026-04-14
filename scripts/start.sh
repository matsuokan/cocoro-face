#!/usr/bin/env bash
# scripts/start.sh
# Starts backend and frontend (used by systemd or manual run)
# Usage: bash scripts/start.sh [--no-frontend]
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_DIR="$(dirname "$SCRIPT_DIR")"
CONDA_ENV="facefusion"
BACKEND_PORT=8010
FRONTEND_PORT=5173
NO_FRONTEND=false

for arg in "$@"; do
  case $arg in
    --no-frontend) NO_FRONTEND=true ;;
  esac
done

echo "=== cocoro-face start.sh ==="

# ---------------------------------------------------------------------------
# Backend
# ---------------------------------------------------------------------------
echo "Starting FastAPI backend on port $BACKEND_PORT..."
cd "$PROJECT_DIR/backend"
conda run -n "$CONDA_ENV" \
  uvicorn main:app \
  --host 0.0.0.0 \
  --port "$BACKEND_PORT" \
  --workers 1 \
  --log-level info &
BACKEND_PID=$!
echo "  Backend PID: $BACKEND_PID"

# ---------------------------------------------------------------------------
# Frontend (dev server) — skip with --no-frontend for production
# ---------------------------------------------------------------------------
if [ "$NO_FRONTEND" = false ]; then
  echo "Starting Vite dev server on port $FRONTEND_PORT..."
  cd "$PROJECT_DIR/frontend"
  npm run dev -- --host 0.0.0.0 --port "$FRONTEND_PORT" &
  FRONTEND_PID=$!
  echo "  Frontend PID: $FRONTEND_PID"
fi

echo ""
echo "✅ cocoro-face started"
echo "  Backend  : http://192.168.50.112:$BACKEND_PORT"
if [ "$NO_FRONTEND" = false ]; then
  echo "  Frontend : http://192.168.50.112:$FRONTEND_PORT"
fi
echo ""
echo "Press Ctrl+C to stop all services"

# Wait for any process to exit
wait
