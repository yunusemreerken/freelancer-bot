import os

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles

from app.database import init_db
from app.routers import clients, decide, estimate, proposals, propose, reply


# Create the FastAPI application before wiring middleware or routers because all
# later setup calls mutate this app instance.
app = FastAPI(title="Freelancer Bot API", version="0.1.0")

# Allow the local static UI and local tooling to call the API during development.
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)


# Initialize SQLite tables at startup so the CRUD endpoints have storage ready.
@app.on_event("startup")
async def startup():
    init_db()


# Register AI draft endpoints under a versioned API prefix for future expansion.
app.include_router(propose.router, prefix="/api/v1")
app.include_router(reply.router, prefix="/api/v1")
app.include_router(estimate.router, prefix="/api/v1")
app.include_router(decide.router, prefix="/api/v1")


# Register memory CRUD endpoints under the same versioned API prefix.
app.include_router(clients.router, prefix="/api/v1")
app.include_router(proposals.router, prefix="/api/v1")


# Expose a lightweight health check for Docker, tests, and manual smoke checks.
@app.get("/health")
async def health():
    return {"status": "ok"}


# Serve the bundled single-page UI from the API container for local use.
STATIC_DIR = os.path.join(os.path.dirname(__file__), "..", "static")
app.mount("/", StaticFiles(directory=STATIC_DIR, html=True), name="static")
