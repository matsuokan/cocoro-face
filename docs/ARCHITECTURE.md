# Architecture - cocoro-face

## System Overview

```
Browser (React+TS+Tailwind)
        │ HTTP/WS
        ▼
FastAPI Backend (port 8010)
        │ subprocess
        ▼
FaceFusion 3.6.0 CLI
        │ CUDA
        ▼
RTX PRO 6000 / VRAM 94.96GB
```

## Components

### Frontend (`frontend/`)
- **Framework**: React 18 + TypeScript + Vite
- **Styling**: Tailwind CSS v3
- **State**: React hooks (no external state lib in Phase 1)
- **API**: `src/api/client.ts` (fetch wrapper, all calls go here)

#### Key Components
| Component | Responsibility |
|---|---|
| `UploadPanel.tsx` | Source / target face image upload |
| `PreviewPanel.tsx` | Show source and target before swap |
| `ResultPanel.tsx` | Display swapped result + download |
| `SettingsPanel.tsx` | Quality, model, enhancer toggles |

### Backend (`backend/`)
- **Framework**: FastAPI + Uvicorn (port 8010)
- **Runtime**: Python 3.12, conda env `facefusion`
- **Config**: `config.py` reads `.env` via pydantic-settings

#### Key Modules
| Module | Responsibility |
|---|---|
| `main.py` | FastAPI app, CORS, router registration |
| `config.py` | All env vars in one place |
| `models/schemas.py` | Pydantic request/response models |
| `routers/swap.py` | `POST /api/swap/image`, `POST /api/swap/video` |
| `routers/job.py` | `GET/DELETE /api/job/{job_id}` |
| `services/facefusion_service.py` | **Sole entry point to FaceFusion CLI** |
| `services/job_service.py` | In-memory / SQLite job state management |

### FaceFusion Integration
- FaceFusion is called **only** via `services/facefusion_service.py`
- Interface: `subprocess.run(["python", "-m", "facefusion", "headless-run", ...], ...)`
- Config file: `facefusion.ini` at repo root (passed via `--config-path`)
- Temp files: `/tmp/cocoro-face/` (auto-cleaned after job completion)

## Data Flow - Image Swap
```
1. Browser → POST /api/swap/image (multipart: source_image, target_image)
2. FastAPI saves uploads to /tmp/cocoro-face/{job_id}/
3. facefusion_service.py builds CLI args from facefusion.ini + request params
4. subprocess.run() → FaceFusion writes output to /tmp/cocoro-face/{job_id}/output.*
5. FastAPI reads output file, returns as StreamingResponse
6. Browser receives result, displays in ResultPanel
```

## Data Flow - Video Swap (Phase 2)
```
1. Browser → POST /api/swap/video → returns {job_id}
2. FastAPI spawns BackgroundTask → facefusion_service.py (async)
3. Browser polls GET /api/job/{job_id} or connects WS /ws/job/{job_id}
4. On completion → Browser fetches GET /api/job/{job_id}/result
```

## Server Environment
- **Host**: 192.168.50.112 (Debian 13 Trixie)
- **CPU**: Intel i9 285K
- **RAM**: 256GB DDR5
- **GPU**: RTX PRO 6000 / VRAM 94.96GB GDDR7
- **CUDA**: 12.8 / Driver: 595.58.03
- **Storage**: 4TB NVMe
- **User**: mdl
- **Conda env**: `facefusion` (separate from `cocoro-llm` venv)

## Ports
| Service | Port |
|---|---|
| FastAPI backend | 8010 |
| Vite dev server | 5173 |
| Vite preview | 4173 |

## Security
- CORS: allow only `http://localhost:5173` and `http://192.168.50.112:5173` in dev
- No external API calls (all models local)
- Uploads validated: allowed MIME types only (image/jpeg, image/png, image/webp, video/mp4)
- File size limits enforced at FastAPI layer
- Temp files deleted after job completion or on DELETE endpoint

## Design Decisions
| Decision | Rationale |
|---|---|
| FaceFusion via subprocess | Keeps FaceFusion upgradable without touching app code |
| Single `facefusion_service.py` | Single point of change if CLI args change |
| `config.py` for all env vars | mypy-safe, prevents scattered os.environ calls |
| No database in Phase 1 | In-memory job dict sufficient for image swap |
| SQLite in Phase 2 | Lightweight, no extra infra, sufficient for local use |

## File Creation History
| Date | File | Reason |
|---|---|---|
| 2026-04-14 | All initial files | Phase 1 initialization |
