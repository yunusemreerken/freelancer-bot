# freelancer-bot

Local AI assistant for freelancers. Writes proposals, estimates prices, drafts client replies, and flags project risks — all running on your own machine.

No paid APIs. No subscriptions. No data sent anywhere.

---

## What It Does

| Endpoint | Input | Output |
|---|---|---|
| `/propose` | Job posting text | Proposal draft |
| `/reply` | Client message | Reply draft |
| `/estimate` | Project description | Price estimate |
| `/decide` | Project description | Risk & decision list |

Every output is a **draft** — you review before sending.

---

## Stack

| Layer | Technology |
|---|---|
| LLM | Ollama + Phi-3 Mini (3.8B) |
| Backend | FastAPI |
| Workflow | n8n |
| Frontend | Single-page HTML (4 tabs) |
| Database | SQLite |
| Containers | Docker Compose |

---

## Requirements

- Docker + Docker Compose
- 8GB RAM minimum (16GB recommended)
- 20GB free disk space
- Ubuntu 22.04+ or macOS

> Tested on: i5-7200U · 16GB RAM · 512GB SATA SSD · no GPU

---

## Quick Start

```bash
# 1. Clone
git clone https://github.com/yunusemreerken/freelancer-bot
cd freelancer-bot

# 2. Configure
cp .env.example .env
nano .env

# 3. Start
docker compose --profile cpu up -d

# 4. Pull the model
docker exec -it ollama ollama pull phi3:mini

# 5. Open
# UI        → http://localhost:8000
# n8n       → http://localhost:5678
# Open WebUI → http://localhost:3000
```

---

## Project Structure

```
freelancer-bot/
├── api/
│   ├── app/
│   │   ├── main.py          # FastAPI app, routers, lifespan
│   │   ├── prompts.py       # All system prompts (centralized)
│   │   ├── models.py        # SQLAlchemy ORM models
│   │   ├── config.py        # Freelancer profile + rate card
│   │   ├── database.py      # SQLite setup + session
│   │   ├── crud.py          # DB helper functions
│   │   ├── ollama_client.py # Ollama HTTP client + injection guard
│   │   └── routers/
│   │       ├── base.py      # Generic router factory
│   │       ├── propose.py   # POST /api/v1/propose
│   │       ├── reply.py     # POST /api/v1/reply
│   │       ├── estimate.py  # POST /api/v1/estimate
│   │       ├── decide.py    # POST /api/v1/decide
│   │       ├── clients.py   # CRUD /api/v1/clients
│   │       └── proposals.py # CRUD /api/v1/proposals
│   ├── static/
│   │   └── index.html       # Single-page UI, 4 tabs
│   ├── tests/
│   │   ├── test_endpoints.py
│   │   ├── stub_app.py      # Ollama-free test stub (reference)
│   │   └── pytest.ini
│   ├── requirements.txt
│   └── Dockerfile
├── n8n/
│   └── my-workflows/
│       └── 2026-05-14_proposal-generator.json
├── docs/
│   └── notes.md             # Architecture decisions + learning notes
├── docker-compose.yml
├── .env.example
├── Caddyfile                # Reverse proxy (Phase 3)
└── CLAUDE.md                # AI assistant instructions
```

---

## Security

- Prompt injection guard on every endpoint — pattern matching + unicode/RTL/homoglyph detection
- Input validation — blank inputs and suspicious content rejected before reaching the LLM
- Ollama bound to `localhost` only
- n8n protected with basic auth
- `.env` excluded from git

---

## Roadmap

### Phase 1 — MVP ✅
- Docker stack (Ollama + n8n + Open WebUI)
- Phi-3 Mini model
- n8n proposal workflow

### Phase 2 — Backend ✅
- FastAPI with 4 endpoints
- Centralized prompts + injection guard
- Single-page HTML UI
- SQLite models + CRUD
- Client + proposal storage (CRUD endpoints)
- Full test suite (96 passed)

### Phase 3 — SaaS ⏳
- JWT authentication
- Multi-tenant support
- PostgreSQL migration
- HTTPS via Caddy
- CI/CD (GitHub Actions)

---

## Based On

[coleam00/local-ai-packaged](https://github.com/coleam00/local-ai-packaged) — base Docker stack (Apache 2.0)

---

## License

Apache 2.0
