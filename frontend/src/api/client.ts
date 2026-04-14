/**
 * API client - ALL fetch calls to the backend go through here.
 * No other file should call fetch() directly.
 */

const BASE_URL = '/api'

// ---------------------------------------------------------------------------
// Types
// ---------------------------------------------------------------------------

export type PixelBoost = '512x512' | '1024x1024'

export type FaceSelectorOrder =
  | 'left-right'
  | 'right-left'
  | 'top-bottom'
  | 'bottom-top'
  | 'large-small'
  | 'small-large'
  | 'best-worst'
  | 'worst-best'

export type JobStatus = 'queued' | 'processing' | 'completed' | 'failed'

export interface SwapImageOptions {
  enhance?: boolean
  pixelBoost?: PixelBoost
  faceSelectorOrder?: FaceSelectorOrder
}

export interface JobResponse {
  job_id: string
  status: JobStatus
  progress: number
  created_at: string
  updated_at: string
  error: string | null
}

export interface HealthResponse {
  status: 'ok'
  version: string
  gpu: string
  cuda: string
}

export interface ApiError {
  code: string
  message: string
  detail?: string
}

// ---------------------------------------------------------------------------
// Error handling
// ---------------------------------------------------------------------------

export class CocoroApiError extends Error {
  constructor(
    public readonly code: string,
    message: string,
    public readonly detail?: string,
  ) {
    super(message)
    this.name = 'CocoroApiError'
  }
}

async function handleErrorResponse(res: Response): Promise<never> {
  let body: { detail?: ApiError | string } = {}
  try {
    body = await res.json()
  } catch {
    throw new CocoroApiError('HTTP_ERROR', `HTTP ${res.status}: ${res.statusText}`)
  }
  const d = body.detail
  if (d && typeof d === 'object') {
    throw new CocoroApiError(d.code, d.message, d.detail)
  }
  throw new CocoroApiError('HTTP_ERROR', typeof d === 'string' ? d : `HTTP ${res.status}`)
}

// ---------------------------------------------------------------------------
// API methods
// ---------------------------------------------------------------------------

/**
 * POST /api/swap/image
 * Returns a Blob of the result PNG.
 */
export async function swapImage(
  sourceImage: File,
  targetImage: File,
  options: SwapImageOptions = {},
): Promise<Blob> {
  const form = new FormData()
  form.append('source_image', sourceImage)
  form.append('target_image', targetImage)
  form.append('enhance', String(options.enhance ?? true))
  form.append('pixel_boost', options.pixelBoost ?? '1024x1024')
  form.append('face_selector_order', options.faceSelectorOrder ?? 'best-worst')

  const res = await fetch(`${BASE_URL}/swap/image`, {
    method: 'POST',
    body: form,
  })

  if (!res.ok) await handleErrorResponse(res)
  return res.blob()
}

/**
 * GET /api/job/{job_id}
 */
export async function getJob(jobId: string): Promise<JobResponse> {
  const res = await fetch(`${BASE_URL}/job/${jobId}`)
  if (!res.ok) await handleErrorResponse(res)
  return res.json() as Promise<JobResponse>
}

/**
 * DELETE /api/job/{job_id}
 */
export async function deleteJob(jobId: string): Promise<void> {
  const res = await fetch(`${BASE_URL}/job/${jobId}`, { method: 'DELETE' })
  if (!res.ok && res.status !== 404) await handleErrorResponse(res)
}

/**
 * GET /health
 */
export async function getHealth(): Promise<HealthResponse> {
  const res = await fetch('/health')
  if (!res.ok) await handleErrorResponse(res)
  return res.json() as Promise<HealthResponse>
}
