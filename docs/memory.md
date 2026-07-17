# Project Memory

Last updated: 2026-07-15

## Project Overview

Drape is an AI-powered browser extension for discovering clothing and
accessories seen in paused online videos. The MVP captures a frame, sends it to
the backend and AI service, then presents visually similar retailer products.

## Current Status

- Overall progress: In Development
- Phase 0 completion: complete (verified 2026-07-15)
- Current phase: Phase 0 — Project Setup
- Current task: Ready to begin Phase 1 — Browser Extension Foundation.
- Current branch: Not recorded

## Completed Work

- Project requirements, architecture, design system, engineering rules, and
  phase plan documented.
- pnpm workspace configured for the extension, backend, and shared packages.
- TypeScript package scaffolds created with strict compiler settings.
- Fastify backend scaffold created with an `/api/v1/health` endpoint and
  environment validation.
- Plasmo/React extension scaffold created with popup, content, background,
  service, and Zustand store entry points.
- FastAPI AI-service scaffold created with a health endpoint and pytest check.
- Docker Compose configured for PostgreSQL, Redis, and Qdrant.
- Prettier configuration, environment examples, `.gitignore`, CI workflow, and
  local setup documentation added.

## In Progress

- None.

## Next Tasks

1. Begin Phase 1: browser-extension foundation.
2. Implement supported-site detection and extension messaging.
3. Update documentation and tests as Phase 1 progresses.

## Pending Decisions

- Confirm production hosting and secret-management approach.
- Confirm the approved product-feed and affiliate data sources before Phase 5.
- Confirm supported video sites and their permitted integration approach before
  Phase 1 implementation.

## Known Issues

- No product functionality beyond health endpoints and extension scaffolding is
  implemented yet.
- Docker services require a local `.env` with a non-default database password.

## Important Files

- `package.json`, `pnpm-workspace.yaml`, and `.github/workflows/ci.yml`
- `docker-compose.yml` and `.env.example`
- `apps/backend/src/app.ts`
- `apps/extension/src/popup.tsx`
- `apps/ai-service/app/main.py`

## Recent Changes

- Established the Phase 0 repository structure and developer tooling based on
  `docs/architecture.md`.
- Phase 0 verification completed successfully: formatting, linting, type
  checking, JavaScript tests, Python health test, and production builds pass.

## Documentation Status

- PRD: up to date
- Architecture: up to date
- Rules: up to date
- Phases: up to date
- Memory: updated for Phase 0
- API documentation: pending (Phase 3)
- Database schema: pending (Phase 3)
- AI pipeline documentation: pending (Phase 4)

## Notes for the Next AI Assistant

Use pnpm for all JavaScript workspace commands. Do not add live retailer,
affiliate, browser-site, or model integrations until their requirements are
confirmed. Phase 0 is complete; begin Phase 1 by replacing the extension
scaffold with supported-site detection and internal messaging.
