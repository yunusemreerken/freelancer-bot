"""
app/models.py

Database tables represented as SQLAlchemy entity classes.
Each class maps to one table, and each attribute maps to one column.
"""

from sqlalchemy import (
    Column, Integer, String, Text, DateTime,
    ForeignKey, Enum as SAEnum
)
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
import enum

from app.database import Base


# ── Enums ─────────────────────────────────────────────

class Platform(str, enum.Enum):
    upwork = "upwork"
    fiverr = "fiverr"


class ProposalStatus(str, enum.Enum):
    pending  = "pending"
    sent     = "sent"
    accepted = "accepted"
    rejected = "rejected"


class MessageRole(str, enum.Enum):
    user      = "user"
    assistant = "assistant"


# ── Client ────────────────────────────────────────────

class Client(Base):
    __tablename__ = "clients"

    id         = Column(Integer, primary_key=True, index=True)
    name       = Column(String(200), nullable=False)
    platform   = Column(SAEnum(Platform), nullable=False)
    country    = Column(String(100), nullable=True)
    rating     = Column(String(10), nullable=True)   # Examples: "4.8", "Top Rated".
    notes      = Column(Text, nullable=True)
    created_at = Column(DateTime, server_default=func.now())

    # Relationships used as navigation properties between ORM models.
    proposals = relationship("Proposal", back_populates="client", cascade="all, delete-orphan")
    messages  = relationship("Message",  back_populates="client", cascade="all, delete-orphan")

    def __repr__(self):
        return f"<Client id={self.id} name={self.name} platform={self.platform}>"


# ── Proposal ──────────────────────────────────────────

class Proposal(Base):
    __tablename__ = "proposals"

    id               = Column(Integer, primary_key=True, index=True)
    client_id        = Column(Integer, ForeignKey("clients.id"), nullable=False)
    job_description  = Column(Text, nullable=False)
    proposal_text    = Column(Text, nullable=False)
    my_skills        = Column(String(500), nullable=True)
    my_rate          = Column(String(50),  nullable=True)
    model            = Column(String(100), nullable=True)   # "phi3:mini"
    status           = Column(SAEnum(ProposalStatus), default=ProposalStatus.pending)
    created_at       = Column(DateTime, server_default=func.now())

    # Relationships
    client   = relationship("Client",  back_populates="proposals")
    messages = relationship("Message", back_populates="proposal", cascade="all, delete-orphan")

    def __repr__(self):
        return f"<Proposal id={self.id} client_id={self.client_id} status={self.status}>"


# ── Message ───────────────────────────────────────────

class Message(Base):
    __tablename__ = "messages"

    id          = Column(Integer, primary_key=True, index=True)
    client_id   = Column(Integer, ForeignKey("clients.id"),   nullable=False)
    proposal_id = Column(Integer, ForeignKey("proposals.id"), nullable=True)   # Optional.
    role        = Column(SAEnum(MessageRole), nullable=False)
    content     = Column(Text, nullable=False)
    created_at  = Column(DateTime, server_default=func.now())

    # Relationships
    client   = relationship("Client",   back_populates="messages")
    proposal = relationship("Proposal", back_populates="messages")

    def __repr__(self):
        return f"<Message id={self.id} role={self.role} client_id={self.client_id}>"
