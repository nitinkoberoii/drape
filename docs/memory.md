# Project Memory

Last updated: 2026-07-20

## Project Overview

Drape is an AI-powered browser extension for discovering clothing and accessories seen in paused online videos. The MVP captures a frame, sends it to the backend and AI service, then presents visually similar retailer products.

## Current Status

- Overall progress: In Development
- Phase 0 completion: complete (verified 2026-07-15)
- Phase 1 completion: complete (verified 2026-07-18)
- Phase 2 completion: complete (verified 2026-07-19)
- Phase 3 completion: complete (verified 2026-07-19)
- Phase 4 completion: implementation complete; AI-service live inference verified
- Current phase: Phase 4 — AI Processing
- Current task: Re-evaluate garment-detection recall with the fashion-oriented prompt taxonomy, then perform an authenticated backend end-to-end check when a Supabase test token is available.
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
- The extension checks and displays backend health when `PLASMO_PUBLIC_API_BASE_URL` is configured.

## In Progress

- Phase 4 AI-service inference is verified. Confidence-threshold evaluation is in progress; remaining verification also includes the protected backend route with a Supabase test token.

## Next Tasks

1. Evaluate the same labelled clothing frames at detection thresholds `0.3`, `0.4`, and `0.5`, with text threshold held at `0.25`; record misses and false positives.
2. Choose a default only after comparing recall and precision across that set, then inspect the RLE mask for each returned item.
3. When a Supabase test token is available, submit that frame to `POST /api/v1/frames` to verify the backend-to-AI-service path.
4. Add an authenticated extension submission flow after Supabase sign-in is introduced in Phase 7, or define a separately approved anonymous workflow.

## Pending Decisions

- Confirm production hosting and secret-management approach.
- Confirm the approved product-feed and affiliate data sources before Phase 5.
- Confirm each supported platform's permitted integration approach before enabling site-specific capture behavior.

## Known Issues

- Docker services require a local `.env` with a non-default database password.
- Authenticated frame submission is not yet verified with a real Supabase user token; user sign-in UI is planned for Phase 7.
- Phase 4 currently retains no captured frames, masks, or analysis results; persistence requires an approved storage and retention design.

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
- Phase 4 implemented: the backend forwards validated frames to the stateless AI service, which preprocesses frames, detects multiple clothing items, produces SAM 2 masks, and returns confidence scores.
- Phase 3 verified: the extension popup successfully displayed `Backend: connected` against the local backend.
- Fixed extension configuration loading: Plasmo requires a statically referenced `PLASMO_PUBLIC_API_BASE_URL`; dynamic `globalThis.process` access left the popup in `not configured` state.
- Decision: Supabase JWTs are verified through JWKS using `jose`, rather than a static extension API key or a custom JWT implementation. See `docs/decisions.md` for trade-offs.

## Documentation Status

- PRD: up to date
- Architecture: up to date
- Rules: up to date
- Phases: up to date
- Memory: updated for Phase 4 live inference verification status
- API documentation: complete (Phase 4)
- Database schema: deferred until persistence requirements are defined
- AI pipeline documentation: complete (Phase 4); live AI-service inference verified

## Notes for the Next AI Assistant

Use pnpm for all JavaScript workspace commands. Do not add live retailer, affiliate, or browser-site integrations until their requirements are confirmed. Phase 4's AI-service inference is verified; complete the remaining multi-item and authenticated backend checks before marking the phase fully verified.
