#!/usr/bin/env bash
# scripts/install.sh
# Sets up conda env "facefusion" + FaceFusion 3.6.0 + backend/frontend deps
# Run as mdl on 192.168.50.112:
#   bash scripts/install.sh
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_DIR="$(dirname "$SCRIPT_DIR")"
CONDA_ENV="facefusion"
FACEFUSION_VERSION="3.6.0"
FACEFUSION_DIR="$HOME/facefusion"
PYTHON_VERSION="3.12"

echo "=== cocoro-face install.sh ==="
echo "Project : $PROJECT_DIR"
echo "Env     : $CONDA_ENV"
echo "Python  : $PYTHON_VERSION"
echo ""

# ---------------------------------------------------------------------------
# 1. Create conda environment
# ---------------------------------------------------------------------------
if conda env list | grep -q "^${CONDA_ENV} "; then
  echo "[1/6] conda env '$CONDA_ENV' already exists — skipping create"
else
  echo "[1/6] Creating conda env '$CONDA_ENV' (Python $PYTHON_VERSION)..."
  conda create -n "$CONDA_ENV" python="$PYTHON_VERSION" -y
fi

# ---------------------------------------------------------------------------
# 2. Install FaceFusion
# ---------------------------------------------------------------------------
echo "[2/6] Setting up FaceFusion $FACEFUSION_VERSION..."
if [ ! -d "$FACEFUSION_DIR" ]; then
  git clone --branch "$FACEFUSION_VERSION" \
    https://github.com/facefusion/facefusion.git "$FACEFUSION_DIR"
else
  echo "       $FACEFUSION_DIR already exists — skipping clone"
fi

conda run -n "$CONDA_ENV" pip install -r "$FACEFUSION_DIR/requirements.txt" \
  --extra-index-url https://download.pytorch.org/whl/cu128 \
  --quiet

# ---------------------------------------------------------------------------
# 3. Install ONNX Runtime (CUDA)
# ---------------------------------------------------------------------------
echo "[3/6] Installing onnxruntime-gpu..."
conda run -n "$CONDA_ENV" pip install \
  onnxruntime-gpu \
  --extra-index-url https://aiinfra.pkgs.visualstudio.com/PublicPackages/Python/onnxruntime-cuda12-build \
  --quiet

# ---------------------------------------------------------------------------
# 4. Install backend dependencies
# ---------------------------------------------------------------------------
echo "[4/6] Installing backend Python packages..."
conda run -n "$CONDA_ENV" pip install \
  fastapi \
  uvicorn[standard] \
  python-multipart \
  pydantic-settings \
  pytest \
  pytest-cov \
  httpx \
  --quiet

# ---------------------------------------------------------------------------
# 5. Install frontend dependencies
# ---------------------------------------------------------------------------
echo "[5/6] Installing frontend Node packages..."
cd "$PROJECT_DIR/frontend"
npm install --silent

# ---------------------------------------------------------------------------
# 6. Copy facefusion.ini into FaceFusion directory
# ---------------------------------------------------------------------------
echo "[6/6] Linking facefusion.ini..."
cp "$PROJECT_DIR/facefusion.ini" "$FACEFUSION_DIR/facefusion.ini"

echo ""
echo "✅ Installation complete!"
echo ""
echo "Next steps:"
echo "  1. Copy .env.example to .env and edit as needed"
echo "  2. Start backend: conda run -n facefusion uvicorn main:app --reload --port 8010 (from backend/)"
echo "  3. Start frontend: npm run dev (from frontend/)"
echo "  4. Test swap: curl -X POST http://localhost:8010/api/swap/image \\"
echo "       -F 'source_image=@face.jpg' -F 'target_image=@photo.jpg' --output result.png"
