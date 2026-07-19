# Drape

Drape is an AI-powered browser extension that helps users discover and shop for
clothing and accessories seen in online videos.

When a user pauses a video on supported platforms, the extension
captures the current frame, identifies the clothing items present, and
recommends the exact products or visually similar alternatives from
multiple retailers. The goal is to transform fashion inspiration into an
effortless shopping experience.

---

# Project Goals

- Make fashion discovery from videos simple and fast.
- Provide high-quality visual product matching.
- Aggregate recommendations from multiple retailers.
- Deliver a seamless browser extension experience.
- Build a scalable platform that can grow beyond the MVP.

---

# Repository Structure

```text
.
├── docs/
│   ├── PRD.md
│   ├── architecture.md
│   ├── design.md
│   ├── memory.md
│   ├── phases.md
│   └── rules.md
│
├── apps/
│   ├── extension/
│   ├── backend/
│   └── ai-service/
│
├── packages/
│
├── docker/
│
└── README.md
```

---

# Documentation

---

Document Description

---

`docs/PRD.md` Product requirements and scope.

`docs/architecture.md` System architecture, folder structure,
and technology choices.

`docs/design.md` Design system, colors, typography, and
UI guidelines.

`docs/rules.md` Coding standards, AI boundaries, and
engineering rules.

`docs/phases.md` Development roadmap and implementation
phases.

`docs/memory.md` Current project status for AI and
developer handoffs.

---

> Start with **PRD.md** to understand the product vision, then read
> **architecture.md** before implementing any feature.

---

# Development Workflow

1.  Read the relevant documentation.
2.  Check `docs/memory.md` for the latest project status.
3.  Select the current phase from `docs/phases.md`.
4.  Implement the feature following `docs/rules.md`.
5.  Keep the UI consistent with `docs/design.md`.
6.  Update `docs/memory.md` after significant progress.

---

# Development Principles

- Keep the code modular and maintainable.
- Prioritize readability over clever implementations.
- Reuse existing patterns before introducing new ones.
- Build incrementally, one phase at a time.
- Test features before moving to the next phase.
- Keep documentation synchronized with implementation.

---

# Current Status

Refer to `docs/memory.md` for:

- Current phase
- Current task
- Completed work
- In-progress work
- Known issues
- Next priorities

---

# Contributing

When contributing:

- Follow the conventions defined in `docs/rules.md`.
- Keep commits focused and descriptive.
- Update documentation when behavior or architecture changes.
- Avoid introducing new dependencies without justification.

---

# Long-Term Vision

Build the fastest and most reliable way for users to discover and
purchase fashion items they see while watching online content, creating
a seamless bridge between inspiration and shopping.

---

# Local Setup

## Prerequisites

- Node.js 22 (see `.nvmrc`)
- pnpm 11.7
- Python 3.12+
- Docker Desktop (optional, for local data services)

## Install and run

```sh
pnpm install
Copy-Item .env.example .env
docker compose up -d

python -m venv apps/ai-service/.venv
apps/ai-service/.venv/bin/pip install -r apps/ai-service/requirements.txt

pnpm dev
apps/ai-service/.venv/bin/python apps/ai-service/main.py
```

The first frame-analysis request downloads the configured public Grounding DINO and SAM 2 weights from Hugging Face into the local model cache. No account is required for the default public checkpoints. A CUDA-capable machine is optional; CPU inference works but is slower.

On a standard Windows Python installation, virtual-environment executables are
under `Scripts` rather than `bin`. The backend health check is available at
`http://localhost:3001/api/v1/health`; the AI-service health check is at
`http://localhost:8000/health`.

Run repository checks with `pnpm format:check`, `pnpm lint`, `pnpm typecheck`,
and `pnpm test`. From `apps/ai-service`, run its health test with
`python -m pytest tests`.

---

Happy building! 🚀
