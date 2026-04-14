# API Reference - cocoro-face

Base URL: `http://192.168.50.112:8010`

## Authentication
None (local network only). Future: Bearer token if exposed externally.

---

## Face Swap

### POST /api/swap/image
同期フェイススワップ（画像→画像）

**Request** `multipart/form-data`

| Field | Type | Required | Description |
|---|---|---|---|
| `source_image` | File | ✓ | 顔の提供元画像 (JPEG/PNG/WebP, max 10MB) |
| `target_image` | File | ✓ | スワップ先画像 (JPEG/PNG/WebP, max 10MB) |
| `enhance` | bool | - | GFPGAN補正を有効化 (default: true) |
| `pixel_boost` | string | - | `"512x512"` / `"1024x1024"` (default: `"1024x1024"`) |
| `face_selector_order` | string | - | `"left-right"` / `"right-left"` / `"top-bottom"` / `"bottom-top"` / `"large-small"` / `"small-large"` / `"best-worst"` / `"worst-best"` (default: `"best-worst"`) |

**Response** `200 OK` `image/png`

ResultのPNG画像をStreamingResponseで返す。

**Error Responses**

| Status | Code | Description |
|---|---|---|
| 400 | `INVALID_FILE_TYPE` | 許可されていないMIMEタイプ |
| 400 | `FILE_TOO_LARGE` | ファイルサイズ上限超過 |
| 422 | - | バリデーションエラー (FastAPI標準) |
| 500 | `FACEFUSION_ERROR` | FaceFusion処理失敗 |

**Example**
```bash
curl -X POST http://192.168.50.112:8010/api/swap/image \
  -F "source_image=@face.jpg" \
  -F "target_image=@photo.jpg" \
  -F "enhance=true" \
  --output result.png
```

---

### POST /api/swap/video
非同期フェイススワップ（動画→動画）**[Phase 2]**

**Request** `multipart/form-data`

| Field | Type | Required | Description |
|---|---|---|---|
| `source_image` | File | ✓ | 顔の提供元画像 (JPEG/PNG/WebP, max 10MB) |
| `target_video` | File | ✓ | スワップ先動画 (MP4/MOV, max 500MB) |
| `enhance` | bool | - | GFPGAN補正を有効化 (default: true) |

**Response** `202 Accepted`
```json
{
  "job_id": "550e8400-e29b-41d4-a716-446655440000",
  "status": "queued",
  "created_at": "2026-04-14T23:52:11+09:00"
}
```

---

## Job Management

### GET /api/job/{job_id}
ジョブステータス確認 **[Phase 2]**

**Response** `200 OK`
```json
{
  "job_id": "550e8400-e29b-41d4-a716-446655440000",
  "status": "processing",
  "progress": 42,
  "created_at": "2026-04-14T23:52:11+09:00",
  "updated_at": "2026-04-14T23:53:00+09:00",
  "error": null
}
```

**Status Values**
| Value | Description |
|---|---|
| `queued` | 処理待ち |
| `processing` | 処理中 |
| `completed` | 完了 |
| `failed` | 失敗 |

---

### GET /api/job/{job_id}/result
完了ジョブの結果ダウンロード **[Phase 2]**

**Response** `200 OK` `video/mp4` (StreamingResponse)

**Error**
- `404` job not found or not yet completed

---

### DELETE /api/job/{job_id}
ジョブと一時ファイルを削除 **[Phase 2]**

**Response** `204 No Content`

---

## WebSocket

### WS /ws/job/{job_id}
進捗リアルタイム通知 **[Phase 2]**

**Message Format** (server → client)
```json
{
  "type": "progress",
  "job_id": "550e8400-e29b-41d4-a716-446655440000",
  "progress": 42,
  "status": "processing"
}
```

```json
{
  "type": "completed",
  "job_id": "550e8400-e29b-41d4-a716-446655440000",
  "status": "completed"
}
```

```json
{
  "type": "error",
  "job_id": "550e8400-e29b-41d4-a716-446655440000",
  "status": "failed",
  "error": "FaceFusion exited with code 1"
}
```

---

## Health Check

### GET /health
サービス生存確認

**Response** `200 OK`
```json
{
  "status": "ok",
  "version": "0.1.0",
  "gpu": "RTX PRO 6000",
  "cuda": "12.8"
}
```
