# rules.md

# AI Development Rules

This document defines the engineering rules and boundaries that every AI
agent contributing to this project must follow. The goal is to keep the
codebase consistent, maintainable, secure, and production-ready.

------------------------------------------------------------------------

# 1. What to Use

## General Principles

-   Prefer readability over clever implementations.
-   Write modular, reusable code.
-   Keep functions focused on a single responsibility.
-   Follow SOLID principles where applicable.
-   Prefer composition over inheritance.
-   Write descriptive variable, function, and component names.
-   Keep files small and organized.

------------------------------------------------------------------------

## Browser Extension

Use:

-   TypeScript
-   React
-   Plasmo
-   Tailwind CSS
-   shadcn/ui
-   Zustand
-   Chrome Extension Manifest V3 APIs

Always:

-   Keep popup components independent.
-   Separate UI from business logic.
-   Place API calls inside service modules.
-   Use async/await instead of nested promises.
-   Use strict TypeScript typing.

------------------------------------------------------------------------

## Backend

Use:

-   Node.js
-   Fastify
-   TypeScript
-   REST APIs
-   Repository pattern
-   Service layer architecture
-   Environment variables for configuration

Always:

-   Validate every request.
-   Return consistent API responses.
-   Centralize error handling.
-   Log meaningful errors only.
-   Keep controllers thin.
-   Move business logic into services.

------------------------------------------------------------------------

## AI Service

Use:

-   Python
-   FastAPI
-   Pretrained computer vision models.
-   Deterministic inference.
-   Configurable confidence thresholds.

Always:

-   Return confidence scores.
-   Handle partial detections gracefully.
-   Support multiple detected items.
-   Make inference stateless.

------------------------------------------------------------------------

## Database

Use:

-   PostgreSQL for relational data.
-   Vector database for embeddings.
-   Redis only for caching.

Always:

-   Normalize relational data.
-   Use indexes where appropriate.
-   Avoid duplicate product records.

------------------------------------------------------------------------

## Git

-   Small focused commits.
-   Feature branches.
-   Clear commit messages.
-   Pull Request before merging.

Commit example:

feat: add frame capture service

------------------------------------------------------------------------

# 2. What to Avoid

## Architecture

Do NOT:

-   Put business logic inside UI components.
-   Duplicate logic across services.
-   Create massive utility files.
-   Hardcode configuration values.
-   Mix AI inference with API controllers.

------------------------------------------------------------------------

## Code Quality

Avoid:

-   any
-   Magic numbers
-   Deep nesting
-   Long methods
-   Global mutable state
-   Dead code
-   Console logs in production

------------------------------------------------------------------------

## Error Handling

Never:

-   Ignore exceptions.
-   Swallow errors silently.
-   Return raw stack traces.
-   Leak internal server details.
-   Crash on recoverable errors.

Always:

-   Catch expected failures.
-   Return meaningful messages.
-   Log unexpected errors.
-   Retry transient failures where appropriate.

------------------------------------------------------------------------

## Security

Never:

-   Commit secrets.
-   Commit API keys.
-   Commit tokens.
-   Trust client input.
-   Skip authentication for protected endpoints.

Always:

-   Validate all input.
-   Sanitize user-provided data.
-   Use HTTPS.
-   Store secrets in environment variables.

------------------------------------------------------------------------

# 3. AI Boundaries

The AI assistant MUST NOT:

-   Invent APIs.
-   Invent database fields.
-   Invent retailer integrations.
-   Assume third-party endpoints exist.
-   Assume browser permissions.
-   Generate placeholder production credentials.
-   Create fake affiliate links.
-   Fabricate model accuracy numbers.
-   Assume legal permission to scrape websites.

The AI assistant SHOULD:

-   Ask for clarification when requirements are ambiguous.
-   Mark assumptions explicitly.
-   Recommend official APIs before scraping.
-   Prefer maintainable solutions over quick hacks.
-   Explain architectural trade-offs.
-   Keep responses concise unless more detail is requested.
-   Reuse existing project patterns before introducing new ones.

------------------------------------------------------------------------

# 4. Coding Standards

-   Use strict TypeScript.
-   Prefer named exports.
-   Keep functions under \~50 lines when practical.
-   Avoid files exceeding \~300 lines unless justified.
-   Use consistent naming conventions.
-   Remove unused imports.
-   Document public functions and complex logic.

------------------------------------------------------------------------

# 5. Testing Expectations

Every new feature should include:

-   Unit tests for business logic.
-   Integration tests for APIs where applicable.
-   Manual verification steps for extension behavior.
-   Regression testing for existing functionality.

------------------------------------------------------------------------

# 6. Documentation Rules

Whenever introducing a new feature, update relevant documentation:

-   README (if setup changes)
-   PRD (if scope changes)
-   architecture.md (if architecture changes)
-   API documentation (if endpoints change)

Do not leave documentation out of sync with implementation.

------------------------------------------------------------------------

# 7. Decision Making

When multiple implementation options exist, prefer the solution that is:

1.  Simpler
2.  Easier to maintain
3.  Easier to test
4.  More secure
5.  More scalable
6.  Better documented

If a trade-off exists, explicitly explain it before implementing.
