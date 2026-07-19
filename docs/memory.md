# Project Memory

Last updated: 2026-07-19

## Project Overview

Drape is an AI-powered browser extension for discovering clothing and accessories seen in paused online videos. The MVP captures a frame, sends it to the backend and AI service, then presents visually similar retailer products.

## Current Status

- Overall progress: In Development
- Phase 0 completion: complete (verified 2026-07-15)
- Phase 1 completion: complete (verified 2026-07-18)
- Phase 2 completion: complete (verified 2026-07-19)
- Phase 3 completion: complete (verified 2026-07-19)
- Current phase: Phase 4 — AI Processing
- Current task: Awaiting authorization to begin Phase 4.
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
- Supabase JWT authentication is implemented through JWKS verification for protected routes. `POST /api/v1/frames` validates and acknowledges a frame receipt without persisting or analyzing it.
- The extension checks and displays backend health when `PLASMO_PUBLIC_API_BASE_URL` is configured.

## In Progress

- None. Phase 3 is verified complete.

## Next Tasks

1. Begin Phase 4 only when authorized: define the AI service frame-analysis contract.
2. Add an authenticated extension submission flow after Supabase sign-in is introduced in Phase 7, or define a separately approved anonymous workflow.

## Pending Decisions

- Confirm production hosting and secret-management approach.
- Confirm the approved product-feed and affiliate data sources before Phase 5.
- Confirm each supported platform's permitted integration approach before enabling site-specific capture behavior.

## Known Issues

- Docker services require a local `.env` with a non-default database password.
- Authenticated frame submission is not yet verified with a real Supabase user token; user sign-in UI is planned for Phase 7.

## Important Files

- `package.json`, `pnpm-workspace.yaml`, and `.github/workflows/ci.yml`
- `docker-compose.yml` and `.env.example`
- `apps/backend/src/app.ts`
- `apps/extension/src/popup.tsx`
- `docs/api.md` and `docs/decisions.md`
- `docs/user-todo.md`

## Recent Changes

- Phase 3 verified: the extension popup successfully displayed `Backend: connected` against the local backend.
- Fixed extension configuration loading: Plasmo requires a statically referenced `PLASMO_PUBLIC_API_BASE_URL`; dynamic `globalThis.process` access left the popup in `not configured` state.
- Decision: Supabase JWTs are verified through JWKS using `jose`, rather than a static extension API key or a custom JWT implementation. See `docs/decisions.md` for trade-offs.

## Documentation Status

- PRD: up to date
- Architecture: up to date
- Rules: up to date
- Phases: up to date
- Memory: updated for Phase 3 verification status
- API documentation: complete (Phase 3)
- Database schema: deferred until persistence requirements are defined
- AI pipeline documentation: pending (Phase 4)

## Notes for the Next AI Assistant

Use pnpm for all JavaScript workspace commands. Do not add live retailer, affiliate, browser-site, or model integrations until their requirements are confirmed. Phase 3 is complete; do not begin Phase 4 unless the user explicitly authorizes it.
