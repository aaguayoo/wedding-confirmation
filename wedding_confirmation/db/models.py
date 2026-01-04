"""Defines the SQLAlchemy ORM schema for wedding guest invitations.

This module provides the database model for storing and managing guest invitation
details, including guest identification, invitation codes, confirmation status, and
related comments.
"""

from sqlalchemy import Integer, String
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column


class Base(DeclarativeBase):
    """Base class for all ORM models in the wedding confirmation database.

    This class serves as the common ancestor for SQLAlchemy models, providing
    shared configuration and metadata used when mapping Python classes to
    database tables.
    """

    pass


class Guest(Base):
    """Guest SQL Model Schema.

    Attributes:
        id: Unique identifier for the guest.
        code: Unique invitation code for the guest.
        name: Name of the guest.
        allowed_guests: Number of guests allowed for this invitation.
        confirmation: Confirmation status of the invitation.
        confirmed_guests: Number of guests confirmed.
        comments: Additional comments related to the invitation.

    """

    __tablename__ = "guests"

    id: Mapped[int] = mapped_column(primary_key=True)
    code: Mapped[str] = mapped_column(String, unique=True, nullable=False)
    name: Mapped[str] = mapped_column(String, nullable=False)

    allowed_guests: Mapped[int] = mapped_column(Integer, nullable=False)
    confirmation: Mapped[str] = mapped_column(String, default="pending")
    confirmed_guests: Mapped[int | None] = mapped_column(Integer)
    comments: Mapped[str | None] = mapped_column(String)
