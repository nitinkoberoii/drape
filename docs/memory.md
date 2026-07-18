# Project Memory

Last updated: 2026-07-19

## Project Overview

Drape is an AI-powered browser extension for discovering clothing and
accessories seen in paused online videos. The MVP captures a frame, sends it to
the backend and AI service, then presents visually similar retailer products.

## Current Status

- Overall progress: In Development
- Phase 0 completion: complete (verified 2026-07-15)
- Phase 1 completion: complete (verified 2026-07-18)
- Phase 2 completion: complete (verified 2026-07-19)
- Current phase: Phase 3 — Backend Foundation
- Current task: Phase 2 verified; ready to begin Phase 3.
- Current branch: main

## Completed Work

- Project requirements, architecture, design system, engineering rules, and
  phase plan documented.
- pnpm workspace configured for the extension, backend, and shared packages.
- TypeScript package scaffolds created with strict compiler settings.
- Fastify backend scaffold created with an `/api/v1/health` endpoint and
  environment validation.
- Plasmo/React extension foundation completed: a styled popup, typed content-to-
  background messaging, supported-site detection, and persisted settings.
- The extension is restricted to an explicit allowlist: YouTube, Netflix,
  Prime Video, Instagram, and TikTok.
- The content script detects video elements and pause/play state; the popup
  reports the active supported site's readiness without capturing frames.
- Phase 2 now captures the largest visible paused frame through a local canvas,
  previews it in the popup, and reports unavailable or protected media clearly.
- Vitest unit coverage validates paused-video selection.
- FastAPI AI-service scaffold created with a health endpoint and pytest check.
- Docker Compose configured for PostgreSQL, Redis, and Qdrant.
- Prettier configuration, environment examples, `.gitignore`, CI workflow, and
  local setup documentation added.

## In Progress

- None.

## Next Tasks

1. Begin Phase 2: video capture.
2. Decide how DRM-protected sites should be handled when frame capture is not
   technically available.
3. Add unit tests for the supported-site and page-state logic alongside Phase 2.

## Pending Decisions

- Confirm production hosting and secret-management approach.
- Confirm the approved product-feed and affiliate data sources before Phase 5.
- Confirm each supported platform's permitted integration approach before
  enabling site-specific capture behavior.

## Known Issues

- No frame capture or product functionality is implemented yet.
- Docker services require a local `.env` with a non-default database password.

## Important Files

- `package.json`, `pnpm-workspace.yaml`, and `.github/workflows/ci.yml`
- `docker-compose.yml` and `.env.example`
- `apps/backend/src/app.ts`
- `apps/extension/src/popup.tsx`
- `apps/ai-service/app/main.py`

## Recent Changes

- Phase 1 implemented and verified: extension typecheck and Chrome MV3
  production build pass.
- Corrected popup-to-background state retrieval: the popup now sends its active
  tab ID, and the background worker queries the content script when no cached
  state is available.
- Decision: native canvas capture was selected over a capture library because
  it is standard browser functionality, adds no runtime dependency, and needs
  no new permissions. Tab or screen capture is a future alternative only for a
  user-initiated, permissioned workflow; it is not a silent DRM fallback.

## Documentation Status

- PRD: up to date
- Architecture: up to date
- Rules: up to date
- Phases: up to date
- Memory: updated for Phase 1
- API documentation: pending (Phase 3)
- Database schema: pending (Phase 3)
- AI pipeline documentation: pending (Phase 4)

## Notes for the Next AI Assistant

Use pnpm for all JavaScript workspace commands. Do not add live retailer,
affiliate, browser-site, or model integrations until their requirements are
confirmed. Phase 0 is complete; begin Phase 1 by replacing the extension
scaffold with supported-site detection and internal messaging.
