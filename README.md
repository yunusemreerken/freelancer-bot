# 🤖 Freelancer Bot

Local AI-powered assistant for freelancers on Upwork and Fiverr.
Runs 100% locally — no paid APIs, no data leaks, no monthly bills.

---

## What It Does

- **Proposal writer** — pastes a job posting, generates a professional proposal (TR/EN)
- **Client reply** — drafts replies to incoming client messages
- **Price estimator** — estimates project cost based on your rate card
- **Decision list** — flags risks and key questions before you accept a project

---

## Stack

| Layer | Technology | Cost |
|---|---|---|
| LLM | Ollama + Phi-3 Mini | Free |
| Workflow automation | n8n | Free |
| Backend | FastAPI (Python) | Free |
| Frontend | Open WebUI | Free |
| Database | SQLite → PostgreSQL (SaaS) | Free |
| Reverse proxy | Caddy | Free |
| Container | Docker + Docker Compose | Free |

---

## Requirements

- Ubuntu 22.04+
- Docker + Docker Compose
- 8GB RAM minimum (16GB recommended)
- 20GB free disk space (for models)

> Tested on: i5-7200U, 16GB RAM, 512GB SATA SSD, no GPU

---

## Quick Start

```bash
# 1. Clone
git clone https://github.com/YOUR_USERNAME/freelancer-bot
cd freelancer-bot

# 2. Copy and fill env file
cp .env.example .env
nano .env

# 3. Start all services
docker compose up -d

# 4. Pull the LLM model
docker exec -it ollama ollama pull phi3:mini

# 5. Open the UI
# n8n       → http://localhost:5678
# Open WebUI → http://localhost:3000
```

---

## Services

| Service | URL | Purpose |
|---|---|---|
| n8n | http://localhost:5678 | Workflow automation |
| Open WebUI | http://localhost:3000 | Chat interface |
| Ollama | http://localhost:11434 | LLM engine |
| FastAPI | http://localhost:8000 | Backend API |
| SearXNG | http://localhost:8080 | Local web search |

---

## Project Structure

```
freelancer-bot/
├── docker-compose.yml       # All services
├── .env.example             # Config template (copy to .env)
├── .gitignore               # .env and db files excluded
├── Caddyfile                # Reverse proxy (SaaS phase)
├── caddy-addon/             # Caddy config
├── flowise/                 # Flowise (unused for now)
├── searxng/                 # SearXNG config
├── n8n/
│   └── backup/workflows/    # n8n workflow exports
├── n8n-tool-workflows/      # Tool-specific workflows
├── assets/                  # Images and docs
└── README.md
```

> ⚠️ Some folders (flowise, searxng) are kept from the base repo for future use.
> They are not active in the current setup.

---

## Environment Variables

Copy `.env.example` to `.env` and fill in:

```env
# n8n
N8N_BASIC_AUTH_ACTIVE=true
N8N_BASIC_AUTH_USER=admin
N8N_BASIC_AUTH_PASSWORD=your_strong_password
WEBHOOK_SECRET=your_random_secret

# Postgres (SaaS phase)
POSTGRES_USER=
POSTGRES_PASSWORD=
POSTGRES_DB=

# Timezone
GENERIC_TIMEZONE=Europe/Istanbul
```

---

## Roadmap

### Phase 1 — MVP ✅ (current)
- [x] Docker stack (Ollama, n8n, Open WebUI)
- [ ] FastAPI backend with 4 endpoints
- [ ] Bilingual prompt system (TR/EN)
- [ ] Basic HTML UI

### Phase 2 — Memory
- [ ] Conversation history (SQLite)
- [ ] Client profiles
- [ ] Past proposal storage

### Phase 3 — SaaS
- [ ] User authentication (JWT)
- [ ] Multi-tenant support
- [ ] PostgreSQL migration
- [ ] HTTPS via Caddy
- [ ] Payment integration

---

## Security Notes

- `.env` is excluded from git via `.gitignore` — never commit it
- n8n is protected with basic auth
- Ollama is bound to `localhost` only (not exposed publicly)
- All LLM inference is local — no data sent to external APIs
- Prompt injection guard is included in all system prompts

---

## Based On

- [coleam00/local-ai-packaged](https://github.com/coleam00/local-ai-packaged) — base Docker stack

---

## License

MIT — free to use, modify, and sell.
