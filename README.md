# Freelancer Bot

Local AI assistant for freelancers on Upwork and Fiverr.
Runs 100% locally — no paid APIs, no subscriptions, no data leaks.

Built as a portfolio project demonstrating local LLM integration, FastAPI backend design, prompt injection defense, and Docker-based service orchestration.

---

## What It Does

Four tools, one UI:

| Tool | Input | Output |
|---|---|---|
| **Proposal writer** | Job posting text | Ready-to-edit proposal draft |
| **Client reply** | Incoming client message | Reply draft |
| **Price estimator** | Project description | Cost estimate with reasoning |
| **Decision helper** | Project description | Risk flags and key questions |

All outputs are drafts — nothing is sent automatically. Human reviews before sending.

---

## Stack

| Layer | Technology |
|---|---|
| LLM | Ollama + Phi-3 Mini (3.8B) |
| Backend | FastAPI (Python) |
| Workflow | n8n |
| Frontend | HTML/CSS/JS (single page, 4 tabs) |
| Database | SQLite |
| Container | Docker + Docker Compose |
| Reverse proxy | Caddy (Phase 3) |

Everything is free and self-hosted.

---

## Architecture

```
[User pastes job posting or message]
        ↓
  [Single-page UI — 4 tabs]
        ↓
  [FastAPI backend]
        ↓ injection check + validation
  [n8n workflow]
        ↓
  [Phi-3 Mini via Ollama]
        ↓
  [Draft response → modal popup]
        ↓
  [Human reviews and sends]
```

---

## Security

Two-layer prompt injection defense:

- **Layer 1 — Input guard:** Pattern matching, unicode normalization, RTL override detection, Cyrillic homoglyph detection. Runs before LLM is called. Returns 400 on detection.
- **Layer 2 — System prompt:** Injection guard embedded in every system prompt. LLM-level second line of defense.

No external API calls — all inference is local.

---

## Requirements

- Ubuntu 22.04+ (or macOS for dev)
- Docker + Docker Compose
- 8 GB RAM minimum (16 GB recommended)
- 20 GB free disk space

> Tested on: i5-7200U, 16 GB RAM, 512 GB SATA SSD, no GPU

---

## Quick Start

```bash
# 1. Clone
git clone https://github.com/yunusemreerken/freelancer-bot
cd freelancer-bot

# 2. Set up environment
cp .env.example .env
nano .env  # fill in passwords and your profile

# 3. Start services
docker compose --profile cpu up -d

# 4. Pull the model
docker exec -it ollama ollama pull phi3:mini

# 5. Open the UI
open http://localhost:8000
```

---

## Services

| Service | URL | Purpose |
|---|---|---|
| FastAPI + UI | http://localhost:8000 | Main interface |
| n8n | http://localhost:5678 | Workflow automation |
| Open WebUI | http://localhost:3000 | Direct chat with LLM |
| Ollama | http://localhost:11434 | LLM engine (localhost only) |

---

## Project Structure

```
freelancer-bot/
├── api/
│   ├── app/
│   │   ├── main.py           # FastAPI app, routers
│   │   ├── prompts.py        # All system prompts
│   │   ├── config.py         # Freelancer profile + rate card
│   │   ├── models.py         # SQLAlchemy ORM models
│   │   ├── database.py       # SQLite setup
│   │   ├── crud.py           # DB helper functions
│   │   ├── ollama_client.py  # Ollama HTTP client + injection guard
│   │   └── routers/
│   │       ├── base.py       # Router factory (DRY)
│   │       ├── propose.py
│   │       ├── reply.py
│   │       ├── estimate.py
│   │       └── decide.py
│   ├── static/
│   │   └── index.html        # Single-page UI
│   ├── tests/
│   │   └── test_endpoints.py # 96 tests, real app + mocked Ollama
│   └── Dockerfile
├── n8n/
│   └── my-workflows/
├── docker-compose.yml
├── Caddyfile
├── .env.example
└── docs/
    └── notes.md              # Architecture decisions and learning notes
```

---

## Roadmap

### Phase 1 — MVP ✅
- Docker stack (Ollama, n8n, Open WebUI)
- Phi-3 Mini model
- n8n proposal workflow
- System prompt (EN only)

### Phase 2 — Backend ✅
- FastAPI with 4 endpoints
- Single-page UI (4 tabs)
- SQLite schema (clients, proposals, messages)
- Prompt injection guard (input + system prompt layers)
- 96 passing tests

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
