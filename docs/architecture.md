# Architecture Document

# DRAPE

---

# 1. Extension Flow & Architecture

## High-Level Flow

```text
User pauses a video
        │
        ▼
Opens Browser Extension
        │
        ▼
Extension captures current video frame
        │
        ▼
Frame sent to Backend API
        │
        ▼
AI Service
 ├── Detect clothing & accessories
 ├── Segment clothing items
 ├── Generate image embeddings
 └── Search visually similar products
        │
        ▼
Product Search Service
        │
        ▼
Rank products
        │
        ▼
Return recommendations
        │
        ▼
Extension displays products
        │
        ▼
User opens retailer via affiliate link
```

## Component Architecture

```text
┌────────────────────────────────────┐
│        Browser Extension           │
├────────────────────────────────────┤
│ Popup UI                           │
│ Background Script                  │
│ Content Script                     │
│ Local Storage                      │
└────────────────────────────────────┘
                 │
                 ▼
          Backend REST API
                 │
      ┌──────────┼──────────┐
      ▼          ▼          ▼
 Auth Service  Product API  Search API
                 │
                 ▼
          AI Processing Service
      ├── Clothing Detection
      ├── Segmentation
      ├── Embedding Generation
      └── Similarity Search
                 │
      ┌──────────┴──────────┐
      ▼                     ▼
 PostgreSQL             Vector DB
                 │
                 ▼
 Affiliate Redirect Service
```

## Request Lifecycle

1.  User pauses a video.
2.  User activates the extension.
3.  The content script captures the current frame.
4.  The frame is sent securely to the backend.
5.  The AI service detects clothing items.
6.  Each item is converted into an embedding.
7.  Similar products are retrieved from the vector database.
8.  Results are ranked and enriched with product metadata.
9.  The backend returns the recommendations.
10. The extension displays products with retailer links.

---

# 2. Folder & File Structure

```text
drape/
│
├── apps/
│   ├── extension/
│   │   ├── public/
│   │   ├── src/
│   │   │   ├── popup/
│   │   │   ├── content/
│   │   │   ├── background/
│   │   │   ├── components/
│   │   │   ├── hooks/
│   │   │   ├── services/
│   │   │   ├── store/
│   │   │   ├── types/
│   │   │   ├── utils/
│   │   │   └── assets/
│   │   ├── manifest.json
│   │   └── package.json
│   │
│   ├── backend/
│   │   ├── src/
│   │   │   ├── controllers/
│   │   │   ├── routes/
│   │   │   ├── middleware/
│   │   │   ├── services/
│   │   │   ├── models/
│   │   │   ├── repositories/
│   │   │   ├── jobs/
│   │   │   ├── config/
│   │   │   └── utils/
│   │   └── package.json
│   │
│   └── ai-service/
│       ├── app/
│       ├── models/
│       ├── inference/
│       ├── embeddings/
│       ├── search/
│       ├── utils/
│       ├── requirements.txt
│       └── main.py
│
├── packages/
│   ├── shared-types/
│   ├── shared-utils/
│   └── ui/
│
├── docker/
├── docs/
├── .github/
├── docker-compose.yml
└── README.md
```

---

# 3. Tech Stack

## Browser Extension

- Plasmo
- React
- TypeScript
- Tailwind CSS
- shadcn/ui
- Zustand

## Backend

- Node.js
- Fastify
- TypeScript
- REST API

## AI Service

- Python
- FastAPI
- GroundingDINO
- SAM 2
- FashionCLIP / OpenCLIP

## Data Layer

- PostgreSQL
- Qdrant (Vector Database)
- Redis
- Cloudflare R2 / Amazon S3

## Authentication

- Supabase Auth (Google, Email)

## DevOps

- Docker
- GitHub Actions

## Monitoring & Analytics

- PostHog
- Sentry

## Future Integrations

- Affiliate Networks
- Retailer Product Feeds
- Stripe (Premium Features)
