# Ecosystem - Data Schemas & Type Definitions

## Backend (Python / Pydantic)

### SwapImageRequest
`backend/models/schemas.py`
```python
class SwapImageRequest(BaseModel):
    enhance: bool = True
    pixel_boost: Literal["512x512", "1024x1024"] = "1024x1024"
    face_selector_order: Literal[
        "left-right", "right-left", "top-bottom", "bottom-top",
        "large-small", "small-large", "best-worst", "worst-best"
    ] = "best-worst"
```

### SwapVideoRequest
```python
class SwapVideoRequest(BaseModel):
    enhance: bool = True
    pixel_boost: Literal["512x512", "1024x1024"] = "1024x1024"
```

### JobStatus
```python
class JobStatusEnum(str, Enum):
    QUEUED = "queued"
    PROCESSING = "processing"
    COMPLETED = "completed"
    FAILED = "failed"

class JobResponse(BaseModel):
    job_id: str
    status: JobStatusEnum
    progress: int = 0          # 0-100
    created_at: datetime
    updated_at: datetime
    error: Optional[str] = None
```

### FaceFusionResult
Internal type returned by `facefusion_service.py`:
```python
@dataclass
class FusionResult:
    success: bool
    output_path: Path
    stderr: str
    returncode: int
```

### ErrorResponse
```python
class ErrorResponse(BaseModel):
    code: str
    message: str
    detail: Optional[str] = None
```

---

## Frontend (TypeScript)

### API Client Types
`frontend/src/api/client.ts`

```typescript
export type PixelBoost = '512x512' | '1024x1024';

export type FaceSelectorOrder =
  | 'left-right' | 'right-left'
  | 'top-bottom' | 'bottom-top'
  | 'large-small' | 'small-large'
  | 'best-worst'  | 'worst-best';

export type JobStatus = 'queued' | 'processing' | 'completed' | 'failed';

export interface SwapImageOptions {
  enhance?: boolean;
  pixelBoost?: PixelBoost;
  faceSelectorOrder?: FaceSelectorOrder;
}

export interface JobResponse {
  job_id: string;
  status: JobStatus;
  progress: number;
  created_at: string;
  updated_at: string;
  error: string | null;
}

export interface HealthResponse {
  status: 'ok';
  version: string;
  gpu: string;
  cuda: string;
}

export interface ApiError {
  code: string;
  message: string;
  detail?: string;
}
```

### Component Props
```typescript
// UploadPanel
export interface UploadPanelProps {
  onSourceFileChange: (file: File | null) => void;
  onTargetFileChange: (file: File | null) => void;
  sourceFile: File | null;
  targetFile: File | null;
}

// PreviewPanel
export interface PreviewPanelProps {
  sourceFile: File | null;
  targetFile: File | null;
}

// ResultPanel
export interface ResultPanelProps {
  resultUrl: string | null;
  isLoading: boolean;
  error: string | null;
}

// SettingsPanel
export interface SettingsPanelProps {
  options: SwapImageOptions;
  onChange: (options: SwapImageOptions) => void;
  disabled?: boolean;
}
```

---

## File System

### Temp Directory Structure
```
/tmp/cocoro-face/
└── {job_id}/
    ├── source.{ext}    # uploaded source face
    ├── target.{ext}    # uploaded target media
    └── output.png      # FaceFusion output (image) or output.mp4 (video)
```

### Model Directory (on server)
```
~/.facefusion/
├── models/
│   ├── inswapper_128_fp16.onnx
│   └── GFPGANv1.4.pth
└── cache/
```

---

## Environment Variables

Defined in `.env.example`:
```
TEMP_DIR=/tmp/cocoro-face
FACEFUSION_DIR=/home/mdl/facefusion
FACEFUSION_CONFIG=./facefusion.ini
MAX_IMAGE_SIZE_MB=10
MAX_VIDEO_SIZE_MB=500
CORS_ORIGINS=http://localhost:5173,http://192.168.50.112:5173
LOG_LEVEL=INFO
```
