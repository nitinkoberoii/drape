# API Foundation

Base path: `/api/v1`

All successful responses use `{ "data": ... }`. Errors use `{ "error": { "code": "...", "message": "..." } }`, never a stack trace. Every response includes `x-request-id`; provide it when reporting an issue.

## `GET /health`

Public connectivity check used by the extension. It returns `200` with `{ "data": { "status": "ok" } }`.

## `POST /frames`

Protected frame-receipt endpoint. Send a Supabase access token as `Authorization: Bearer <token>` and a JSON body containing `imageDataUrl` (JPEG or PNG data URL, maximum 8 MB), `sourceUrl`, and a positive integer `capturedAt` timestamp.

It returns `200` with a request ID, `analyzed` status, and `items`. Each item has a clothing label, a 0--1 confidence score, a pixel bounding box, and a row-major RLE segmentation mask. The RLE mask has `size: [height, width]`; its alternating run lengths begin with background pixels. An empty `items` array is a valid result when no item meets the configured confidence threshold.

Frames are forwarded only to the configured Drape AI service and are not persisted in this phase. If it is unreachable, the API returns `503 AI_SERVICE_UNAVAILABLE`.

## AI service `POST /analyze`

Internal-only endpoint used by the backend. It accepts `{ image_data_url, source_url }` and returns `{ items }`. It normalizes EXIF orientation and bounds each image to `MAX_IMAGE_DIMENSION` before inference. Models load lazily on the first analysis request, so `/health` stays fast and does not download model weights.

## Configuration

`SUPABASE_URL` enables JWT verification through Supabase's JWKS endpoint. `SUPABASE_JWT_AUDIENCE` defaults to `authenticated`. Set `CORS_ALLOWED_ORIGINS` only for non-extension web clients; Chrome extension requests use their host permission and do not need an open CORS policy.
