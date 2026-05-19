"""
app/routers/clients.py

Client CRUD endpoints.
"""

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from pydantic import BaseModel
from typing import Optional
from datetime import datetime

from app.database import get_db
from app import crud, models

router = APIRouter(prefix="/clients", tags=["clients"])


# ── Schemas (Pydantic) ────────────────────────────────
# These DTOs keep request and response shapes explicit at the API boundary.

class ClientCreate(BaseModel):
    name: str
    platform: models.Platform
    country: Optional[str] = None
    rating: Optional[str] = None
    notes: Optional[str] = None


class ClientUpdate(BaseModel):
    name: Optional[str] = None
    country: Optional[str] = None
    rating: Optional[str] = None
    notes: Optional[str] = None


class ClientResponse(BaseModel):
    id: int
    name: str
    platform: models.Platform
    country: Optional[str]
    rating: Optional[str]
    notes: Optional[str]
    created_at: datetime

    class Config:
        from_attributes = True  # Converts ORM model instances into Pydantic responses.


# ── Endpoints ─────────────────────────────────────────

@router.post("", response_model=ClientResponse, status_code=201)
async def create_client(
    request: ClientCreate,
    db: Session = Depends(get_db),
):
    return crud.create_client(
        db,
        name=request.name,
        platform=request.platform,
        country=request.country,
        rating=request.rating,
        notes=request.notes,
    )


@router.get("", response_model=list[ClientResponse])
async def list_clients(
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db),
):
    return crud.get_clients(db, skip=skip, limit=limit)


@router.get("/{client_id}", response_model=ClientResponse)
async def get_client(
    client_id: int,
    db: Session = Depends(get_db),
):
    client = crud.get_client(db, client_id)
    if not client:
        raise HTTPException(status_code=404, detail="Client not found.")
    return client


@router.patch("/{client_id}", response_model=ClientResponse)
async def update_client(
    client_id: int,
    request: ClientUpdate,
    db: Session = Depends(get_db),
):
    client = crud.update_client(db, client_id, **request.model_dump(exclude_none=True))
    if not client:
        raise HTTPException(status_code=404, detail="Client not found.")
    return client


@router.delete("/{client_id}", status_code=204)
async def delete_client(
    client_id: int,
    db: Session = Depends(get_db),
):
    deleted = crud.delete_client(db, client_id)
    if not deleted:
        raise HTTPException(status_code=404, detail="Client not found.")
