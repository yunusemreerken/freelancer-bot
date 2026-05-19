"""
app/routers/proposals.py

Proposal CRUD endpoints.
"""

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from pydantic import BaseModel, ConfigDict
from typing import Optional
from datetime import datetime

from app.database import get_db
from app import crud, models

router = APIRouter(prefix="/proposals", tags=["proposals"])


# ── Schemas (DTOs) ────────────────────────────────────
# These models define the proposal payloads without changing database behavior.

class ProposalCreate(BaseModel):
    client_id: int
    job_description: str
    proposal_text: str
    my_skills: Optional[str] = None
    my_rate: Optional[str] = None
    model: Optional[str] = None


class ProposalStatusUpdate(BaseModel):
    status: models.ProposalStatus


class ProposalResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    client_id: int
    job_description: str
    proposal_text: str
    my_skills: Optional[str]
    my_rate: Optional[str]
    model: Optional[str]
    status: models.ProposalStatus
    created_at: datetime


# ── Endpoints ─────────────────────────────────────────

@router.post("", response_model=ProposalResponse, status_code=201)
async def create_proposal(
    request: ProposalCreate,
    db: Session = Depends(get_db),
):
    # Verify the client exists first so proposals cannot point to missing clients.
    client = crud.get_client(db, request.client_id)
    if not client:
        raise HTTPException(status_code=404, detail="Client not found.")

    return crud.create_proposal(
        db,
        client_id=request.client_id,
        job_description=request.job_description,
        proposal_text=request.proposal_text,
        my_skills=request.my_skills,
        my_rate=request.my_rate,
        model=request.model,
    )


@router.get("/client/{client_id}", response_model=list[ProposalResponse])
async def list_proposals_by_client(
    client_id: int,
    db: Session = Depends(get_db),
):
    client = crud.get_client(db, client_id)
    if not client:
        raise HTTPException(status_code=404, detail="Client not found.")
    return crud.get_proposals_by_client(db, client_id)


@router.get("/{proposal_id}", response_model=ProposalResponse)
async def get_proposal(
    proposal_id: int,
    db: Session = Depends(get_db),
):
    proposal = crud.get_proposal(db, proposal_id)
    if not proposal:
        raise HTTPException(status_code=404, detail="Proposal not found.")
    return proposal


@router.patch("/{proposal_id}/status", response_model=ProposalResponse)
async def update_proposal_status(
    proposal_id: int,
    request: ProposalStatusUpdate,
    db: Session = Depends(get_db),
):
    proposal = crud.update_proposal_status(db, proposal_id, request.status)
    if not proposal:
        raise HTTPException(status_code=404, detail="Proposal not found.")
    return proposal


@router.delete("/{proposal_id}", status_code=204)
async def delete_proposal(
    proposal_id: int,
    db: Session = Depends(get_db),
):
    deleted = crud.delete_proposal(db, proposal_id)
    if not deleted:
        raise HTTPException(status_code=404, detail="Proposal not found.")
