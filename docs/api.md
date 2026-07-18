# API Foundation

Base path: `/api/v1`

All successful responses use `{ "data": ... }`. Errors use `{ "error": { "code": "...", "message": "..." } }`, never a stack trace. Every response includes `x-request-id`; provide it when reporting an issue.

## `GET /health`

Public connectivity check used by the extension. It returns `200` with `{ "data": { "status": "ok" } }`.

## `POST /frames`

Protected frame-receipt endpoint. Send a Supabase access token as `Authorization: Bearer <token>` and a JSON body containing `imageDataUrl` (JPEG or PNG data URL, maximum 8 MB), `sourceUrl`, and a positive integer `capturedAt` timestamp.

It returns `202` with a request ID and `received` status after validation. This phase does not persist or analyze the image; Phase 4 will connect this contract to the AI pipeline.

## Configuration

`SUPABASE_URL` enables JWT verification through Supabase's JWKS endpoint. `SUPABASE_JWT_AUDIENCE` defaults to `authenticated`. Set `CORS_ALLOWED_ORIGINS` only for non-extension web clients; Chrome extension requests use their host permission and do not need an open CORS policy.
