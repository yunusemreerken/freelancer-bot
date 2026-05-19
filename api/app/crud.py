"""
app/crud.py

Database operations for the API.
Each function performs one repository-style task.
"""

from sqlalchemy.orm import Session
from app import models


# ══════════════════════════════════════════════
# Client
# ══════════════════════════════════════════════

def create_client(
    db: Session,
    name: str,
    platform: models.Platform,
    country: str = None,
    rating: str = None,
    notes: str = None,
) -> models.Client:
    client = models.Client(
        name=name,
        platform=platform,
        country=country,
        rating=rating,
        notes=notes,
    )
    db.add(client)
    db.commit()
    db.refresh(client)
    return client


def get_client(db: Session, client_id: int) -> models.Client | None:
    return db.query(models.Client).filter(models.Client.id == client_id).first()


def get_clients(db: Session, skip: int = 0, limit: int = 100) -> list[models.Client]:
    return db.query(models.Client).offset(skip).limit(limit).all()


def update_client(
    db: Session,
    client_id: int,
    **kwargs,
) -> models.Client | None:
    client = get_client(db, client_id)
    if not client:
        return None
    for key, value in kwargs.items():
        if value is not None:
            setattr(client, key, value)
    db.commit()
    db.refresh(client)
    return client


def delete_client(db: Session, client_id: int) -> bool:
    client = get_client(db, client_id)
    if not client:
        return False
    db.delete(client)
    db.commit()
    return True


# ══════════════════════════════════════════════
# Proposal
# ══════════════════════════════════════════════

def create_proposal(
    db: Session,
    client_id: int,
    job_description: str,
    proposal_text: str,
    my_skills: str = None,
    my_rate: str = None,
    model: str = None,
) -> models.Proposal:
    proposal = models.Proposal(
        client_id=client_id,
        job_description=job_description,
        proposal_text=proposal_text,
        my_skills=my_skills,
        my_rate=my_rate,
        model=model,
        status=models.ProposalStatus.pending,
    )
    db.add(proposal)
    db.commit()
    db.refresh(proposal)
    return proposal


def get_proposal(db: Session, proposal_id: int) -> models.Proposal | None:
    return db.query(models.Proposal).filter(models.Proposal.id == proposal_id).first()


def get_proposals_by_client(db: Session, client_id: int) -> list[models.Proposal]:
    return (
        db.query(models.Proposal)
        .filter(models.Proposal.client_id == client_id)
        .order_by(models.Proposal.created_at.desc())
        .all()
    )


def update_proposal_status(
    db: Session,
    proposal_id: int,
    status: models.ProposalStatus,
) -> models.Proposal | None:
    proposal = get_proposal(db, proposal_id)
    if not proposal:
        return None
    proposal.status = status
    db.commit()
    db.refresh(proposal)
    return proposal


def delete_proposal(db: Session, proposal_id: int) -> bool:
    proposal = get_proposal(db, proposal_id)
    if not proposal:
        return False
    db.delete(proposal)
    db.commit()
    return True


# ══════════════════════════════════════════════
# Message
# ══════════════════════════════════════════════

def create_message(
    db: Session,
    client_id: int,
    role: models.MessageRole,
    content: str,
    proposal_id: int = None,
) -> models.Message:
    message = models.Message(
        client_id=client_id,
        proposal_id=proposal_id,
        role=role,
        content=content,
    )
    db.add(message)
    db.commit()
    db.refresh(message)
    return message


def get_messages_by_client(
    db: Session,
    client_id: int,
    limit: int = 20,
) -> list[models.Message]:
    """Return the latest messages for conversation history."""
    return (
        db.query(models.Message)
        .filter(models.Message.client_id == client_id)
        .order_by(models.Message.created_at.asc())
        .limit(limit)
        .all()
    )


def get_messages_by_proposal(
    db: Session,
    proposal_id: int,
) -> list[models.Message]:
    """Return messages that belong to a specific proposal."""
    return (
        db.query(models.Message)
        .filter(models.Message.proposal_id == proposal_id)
        .order_by(models.Message.created_at.asc())
        .all()
    )


def delete_messages_by_client(db: Session, client_id: int) -> int:
    """Delete all messages for a client and return the deleted row count."""
    count = (
        db.query(models.Message)
        .filter(models.Message.client_id == client_id)
        .delete()
    )
    db.commit()
    return count
