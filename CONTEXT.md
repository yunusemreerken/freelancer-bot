# Freelancer Bot — Project Context

## What This Project Is
Local AI-powered assistant for freelancers on Upwork and Fiverr.
Runs 100% locally — no paid APIs, no subscriptions, no data leaks.

## Hardware
- CPU: Intel i5-7200U (2 cores, 2.5GHz)
- RAM: 16GB
- Storage: 512GB SATA SSD
- GPU: NVIDIA 930MX — 2GB VRAM (not used, too small)
- OS: macOS (dev) → Ubuntu 22.04 (production)

## Current Status
- Phase 1 MVP complete
- Phase 2 (FastAPI backend) in progress

---

## Architecture

```
[Job posting / client message]
        ↓ copy-paste
      [n8n]
        ↓
  [Phi-3 Mini via Ollama]
        ↓
  [Draft proposal / reply]
        ↓
   [Human reviews & sends]
```

Future (Phase 2+):
```
[n8n webhook]
      ↓
[FastAPI backend]
      ↓
[Ollama + Phi-3 Mini]
      ↓
[SQLite → response]
      ↓
[n8n → notification]
```

---

## Stack

| Layer | Technology | Status |
|---|---|---|
| LLM | Ollama + Phi-3 Mini | ✅ Running |
| Workflow | n8n | ✅ Running |
| Chat UI | Open WebUI | ✅ Running |
| Backend | FastAPI (Python) |✅ Running |
| Database | SQLite | ✅ Running |
| Reverse proxy | Caddy | ⏳ Phase 3 |
| Auth | JWT (FastAPI-Users) | ⏳ Phase 3 |
| Database (SaaS) | PostgreSQL | ⏳ Phase 3 |

---

## Services & Ports

| Service | Port | Notes |
|---|---|---|
| n8n | 5678 | Basic auth enabled |
| Open WebUI | 3000 | Maps to container 8080 |
| Ollama | 11434 | Localhost only |
| FastAPI | 8000 | Phase 2 |

---

## Repositories

| Repo | Visibility | Purpose |
|---|---|---|
| freelancer-bot | Public | MVP, open source |
| freelancer-bot-saas | Private | SaaS development, backup |

---

## Phase Roadmap

### Phase 1 — MVP ✅
- [x] Docker stack (Ollama, n8n, Open WebUI)
- [x] Phi-3 Mini model
- [x] n8n proposal workflow
- [x] System prompt (EN only)

### Phase 2 — Backend 🔧✅
- [x] FastAPI with 4 endpoints
- [x] prompts.py
- [x] models.py (Pydantic)
- [x] database.py (SQLite)
- [x] config.py (freelancer profile, rate card)
- [x] Dockerfile for FastAPI
- [x] Add FastAPI to docker-compose.yml
- [x] Prompt injection guard

### Phase 3 — SaaS 🔧
- [ ] JWT authentication
- [ ] Multi-tenant support
- [ ] PostgreSQL migration
- [ ] HTTPS via Caddy
- [ ] Payment integration
- [ ] CI/CD (GitHub Actions)

---

## FastAPI Endpoints (Phase 2)

| Method | Endpoint | Input | Output |
|---|---|---|---|
| POST | /proposal | job posting text | proposal draft |
| POST | /reply | client message | reply draft |
| POST | /price | project description | price estimate |
| POST | /decisions | project description | risk/decision list |

---

## Key Decisions Made

**Model:** Phi-3 Mini (3.8B) — best balance for CPU-only hardware
**Language:** English only — Phi-3 Mini Turkish quality too low
**Platform integration:** Copy-paste only — Upwork/Fiverr APIs too expensive
**Database:** SQLite for MVP, PostgreSQL for SaaS
**n8n DB:** SQLite (removed PostgreSQL dependency for simplicity)
**No auto-send:** Every output is a draft, human reviews before sending
**No fine-tuning:** System prompt is sufficient, RAG planned for Phase 3

---

## Security Decisions

- `.env` never commits to git
- n8n protected with basic auth
- Ollama bound to localhost only
- Prompt injection guard in all system prompts
- No external API calls — all inference local

---

## Based On
- coleam00/local-ai-packaged — base Docker stack (Apache 2.0)
