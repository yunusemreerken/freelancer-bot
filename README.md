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
## ⚙️ Environment and Database Configurations (SaaS vs. Local)

The project can be executed in two distinct modes. To prevent database initialization errors (`sqlite3.OperationalError`), verify that your `.env` file's `DATABASE_URL` accurately matches your `docker-compose.yml` volume mappings:

* **SaaS / Docker Mode:** `DATABASE_URL=sqlite:////data/freelancer.db`
  * This mode strictly requires the volume mapping `- ./data:/data` inside your `docker-compose.yml` file.
* **Developer (Local) Mode:** `DATABASE_URL=sqlite:///./freelancer.db`


## 🛠️ Troubleshooting Common Docker Errors

### 1. Port 11434 Already In Use
**Error:** `bind: address already in use`
* **Root Cause:** An existing Ollama container (such as `ollama-saas`) is active and occupying the network port.
* **Solution:** Do not spin up a brand new container. Execute the model generation command directly inside the active, running container:
  ```bash
  docker exec -it ollama-saas ollama pull phi3:mini
  ```

### 2. Container Name Conflict
**Error:** `The container name "/freelancer-api-saas" is already in use...`
* **Root Cause:** A legacy or manually executed container instance is stopped but still occupying the namespace system-wide.
* **Solution:** Force-delete the conflicting container from memory and re-run Compose:
  ```bash
  docker rm -f freelancer-api-saas
  docker compose --profile cpu up -d
  ```

### 3. SQLite Storage Operational Failure
**Error:** `sqlite3.OperationalError: unable to open database file`
* **Root Cause:** The application code inside the container is targeting the absolute directory path `/data/`, but Docker cannot access the folder or write permissions are restricted on the host machine.
* **Solution:** Create the baseline target data directory on your host root workspace and expand its filesystem read/write privileges:
  ```bash
  mkdir -p data && chmod 777 data
  ```

---

## 🚀 Clean Turnkey Setup Commands

If container naming structures or file paths become corrupted or mixed up across paths, execute this sequence to wipe conflicting configurations and rebuild a fresh, stable stack:

```bash
# 1. Gracefully terminate and clear all active profile services
docker compose --profile cpu down

# 2. Reset host storage architectures and expand privileges
mkdir -p data && chmod -R 777 data

# 3. Spin up the localized stack using the designated CPU infrastructure
docker compose --profile cpu up -d

# 4. Pull the primary core LLM directly into your active runtime container
docker exec -it ollama-saas ollama pull phi3:mini
```


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
