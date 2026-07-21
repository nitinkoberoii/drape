# Project Memory

Last updated: 2026-07-22

## Project Overview

Drape is an AI-powered browser extension for discovering clothing and accessories seen in paused online videos. The MVP captures a frame, sends it to the backend and AI service, then presents visually similar retailer products.

## Current Status

- Overall progress: In Development
- Phase 0 completion: complete (verified 2026-07-15)
- Phase 1 completion: complete (verified 2026-07-18)
- Phase 2 completion: complete (verified 2026-07-19)
- Phase 3 completion: complete (verified 2026-07-19)
- Phase 4 completion: AI service verified; protected backend end-to-end verification pending
- Current phase: Phase 4 — AI Processing
- Current task: Perform an authenticated backend end-to-end frame-analysis check with a Supabase test token.
- Current branch: main

## Completed Work

- Project requirements, architecture, design system, engineering rules, and phase plan documented.
- pnpm workspace configured for the extension, backend, and shared packages.
- TypeScript package scaffolds created with strict compiler settings.
- Plasmo/React extension foundation completed: styled popup, typed content-to-background messaging, supported-site detection, and persisted settings.
- The extension is restricted to an explicit allowlist: YouTube, Netflix, Prime Video, Instagram, and TikTok.
- The content script captures the largest visible paused frame through a local canvas and reports protected media clearly.
- Vitest unit coverage validates paused-video selection.
- FastAPI AI-service scaffold created with a health endpoint and pytest check.
- Docker Compose configured for PostgreSQL, Redis, and Qdrant.
- Phase 3 backend foundation completed: standard API envelopes, central error handling, request IDs, structured/redacted Fastify logs, configuration-driven CORS, and a public health endpoint.
- Supabase JWT authentication is implemented through JWKS verification for protected routes. `POST /api/v1/frames` validates a frame, forwards it to the AI service, and returns detected clothing items without persisting the frame.
- Phase 4 AI processing is implemented: image normalization, configurable open-vocabulary clothing detection, per-item segmentation, confidence scores, and a backend-to-AI-service contract.
- The pinned AI runtime was installed locally. A live `POST /analyze` request successfully returned a segmented `glasses` detection with confidence `0.5229`, a bounding box, and an RLE mask.
- Grounding DINO weights are cached locally after their initial download. No submitted frame or result is persisted by the AI service or backend in Phase 4.
- The person-first Grounding DINO + SAM 2 pipeline was live-tested on local clothing images, including visual PNG overlays and transparent masked garment crops. The user confirmed the debug visual output is working as expected.
- The extension checks and displays backend health when `PLASMO_PUBLIC_API_BASE_URL` is configured.

## In Progress

- Phase 4 AI-service inference, person grouping, segmentation masks, and opt-in visual outputs are verified. The sole exit-criterion check remaining is the protected backend route with a Supabase test token.

## Next Tasks

1. Obtain a Supabase test-user access token and submit a validated frame to `POST /api/v1/frames` while both backend and AI service are running.
2. Verify the backend returns the analyzed clothing items, confidence scores, boxes, and masks, then mark Phase 4 complete.
3. Begin Phase 5 only after that verification; confirm approved product-feed and affiliate data sources before implementing any retailer integration.
4. Add an authenticated extension submission flow after Supabase sign-in is introduced in Phase 7, or define a separately approved anonymous workflow.

## Pending Decisions

- Confirm production hosting and secret-management approach.
- Confirm the approved product-feed and affiliate data sources before Phase 5.
- Confirm each supported platform's permitted integration approach before enabling site-specific capture behavior.

## Known Issues

- Docker services require a local `.env` with a non-default database password.
- Authenticated frame submission is not yet verified with a real Supabase user token; user sign-in UI is planned for Phase 7.
- Phase 4 currently retains no captured frames, masks, or analysis results; persistence requires an approved storage and retention design.
- WebP input remains unsupported; the AI-service frame contract accepts JPEG and PNG data URLs only.

## Important Files

- `package.json`, `pnpm-workspace.yaml`, and `.github/workflows/ci.yml`
- `docker-compose.yml` and `.env.example`
- `apps/backend/src/app.ts`
- `apps/extension/src/popup.tsx`
- `docs/api.md` and `docs/decisions.md`
- `docs/user-todo.md`

## Recent Changes

- Phase 4 live inference verified: Grounding DINO and SAM 2 were downloaded and initialized successfully; a request returned a `glasses` item with confidence `0.5229`, bounding box, and RLE mask.
- Fixed Phase 4 runtime compatibility: upgraded Transformers from `4.53.2` to `4.57.3` for SAM 2 support and added Torchvision `0.22.1`, matched to Torch `2.7.1`.
- Added controlled confidence-threshold evaluation: `/analyze` now accepts validated per-request detection and text overrides and returns the effective thresholds.
- Added a fashion-oriented prompt taxonomy: specific garment prompts now map to canonical Drape categories before results are returned.
- Added class-aware duplicate suppression: overlapping canonical-category boxes retain only the highest-confidence result before segmentation.
- Added person-first inference: the AI service detects people, performs fashion detection within each padded person crop, and returns a grouped outfit set per person while preserving the legacy flattened items list.
- Added opt-in segmentation visuals for local evaluation: per-person mask overlays and transparent masked garment crops are returned as PNG data URLs only when requested.
- Verified person-first AI processing visually on local clothing images: each person can return an independent outfit set, and SAM 2 debug overlays/crops are available for manual review.
- Phase 4 implemented: the backend forwards validated frames to the stateless AI service, which preprocesses frames, detects multiple clothing items, produces SAM 2 masks, and returns confidence scores.
- Phase 3 verified: the extension popup successfully displayed `Backend: connected` against the local backend.
- Fixed extension configuration loading: Plasmo requires a statically referenced `PLASMO_PUBLIC_API_BASE_URL`; dynamic `globalThis.process` access left the popup in `not configured` state.
- Decision: Supabase JWTs are verified through JWKS using `jose`, rather than a static extension API key or a custom JWT implementation. See `docs/decisions.md` for trade-offs.

## Documentation Status

- PRD: up to date
- Architecture: up to date
- Rules: up to date
- Phases: up to date
- Memory: updated for Phase 4 AI-service verification status
- API documentation: complete (Phase 4)
- Database schema: deferred until persistence requirements are defined
- AI pipeline documentation: complete (Phase 4); AI-service and visual-debug inference verified

## Notes for the Next AI Assistant

Use pnpm for all JavaScript workspace commands. Do not add live retailer, affiliate, or browser-site integrations until their requirements are confirmed. Phase 4's AI-service path is verified, but do not start Phase 5 or mark Phase 4 complete until `/api/v1/frames` has returned real analyzed items using a Supabase test token.
