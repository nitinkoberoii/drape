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

Internal-only endpoint used by the backend. It accepts `{ image_data_url, source_url }` and returns `{ people, items, thresholds }`. It normalizes EXIF orientation and bounds each image to `MAX_IMAGE_DIMENSION` before inference. Models load lazily on the first analysis request, so `/health` stays fast and does not download model weights.

`people` is the primary result: each entry has a stable left-to-right `id`, person confidence and bounding box, and that person's detected outfit `items`. `items` is retained as a flattened compatibility list for the current backend contract. The AI service first detects people, runs garment detection only within a padded crop of each person, maps crop boxes back to full-image coordinates, and then asks SAM 2 to segment each retained garment.

For controlled evaluation only, callers may include `detection_threshold` and `text_threshold`, each from 0 to 1. The response echoes the effective values in `thresholds`, making results directly comparable. Omitting them uses `DETECTION_CONFIDENCE_THRESHOLD` and `TEXT_CONFIDENCE_THRESHOLD`, which default to `0.5`. Do not lower a production threshold based on one image; compare the same labelled evaluation set at several settings and record misses as well as false positives.

Detected labels use Drape's canonical fashion taxonomy (`top`, `shirt`, `outerwear`, `dress`, `skirt`, `pants`, `shoe`, `bag`, and accessory categories). The detector receives specific garment prompts such as `cargo pants` and `shoulder bag`; synonym or merged model phrases are mapped to one canonical label before the response is returned.

Same-category boxes that overlap by at least `DUPLICATE_IOU_THRESHOLD` (default `0.6`) are reduced to the highest-confidence item before segmentation. Non-overlapping items remain, including the same category on different people.

`PERSON_CROP_PADDING` defaults to `0.1`, retaining a 10% margin around a detected person so accessories and shoes at the edge are not unnecessarily excluded. Increase it only after checking that it does not pull another person's garments into the crop.

### Debug visuals

For local evaluation, include `"include_debug_visuals": true` in an AI-service request. Each person then includes `debug_visuals.overlay_png_data_url`, a PNG data URL with retained item masks overlaid on the original image. Each displayed item includes `debug_visuals.masked_crop_png_data_url`, a transparent PNG crop containing only that item's SAM 2 mask. Decode these data URLs to `.png` files to inspect them.

Debug visuals are disabled by default. They are intentionally not forwarded by the backend and should not be enabled for normal extension traffic because base64 PNGs substantially increase response size. `DEBUG_VISUAL_MAX_DIMENSION` defaults to `768`; at most `DEBUG_VISUAL_MAX_ITEMS_PER_PERSON` item crops (default `12`) are returned per person. `debug_visuals_truncated: true` indicates that lower-confidence item crops were omitted.

## Configuration

`SUPABASE_URL` enables JWT verification through Supabase's JWKS endpoint. `SUPABASE_JWT_AUDIENCE` defaults to `authenticated`. Set `CORS_ALLOWED_ORIGINS` only for non-extension web clients; Chrome extension requests use their host permission and do not need an open CORS policy.
