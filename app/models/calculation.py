# app/models/calculation.py
"""
Calculation Model

This module defines the Calculation model, which represents an arithmetic
calculation stored in the database.
"""

from datetime import datetime
import uuid
from sqlalchemy import Column, String, DateTime, ForeignKey, Float
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
from app.database import Base


class Calculation(Base):
    """
    Calculation model representing an arithmetic calculation.

    Attributes:
        id: Unique identifier for the calculation (UUID)
        a: First operand
        b: Second operand
        type: Arithmetic operation
        result: Computed result
        user_id: Optional UUID of the user who owns this calculation
        created_at: Timestamp when the calculation was created
        updated_at: Timestamp when the calculation was last updated
    """
    __tablename__ = 'calculations'

    id = Column(
        UUID(as_uuid=True),
        primary_key=True,
        default=uuid.uuid4,
        nullable=False
    )

    a = Column(
        Float,
        nullable=False
    )

    b = Column(
        Float,
        nullable=False
    )

    type = Column(
        String(20),
        nullable=False
    )

    result = Column(
        Float,
        nullable=False
    )

    user_id = Column(
        UUID(as_uuid=True),
        ForeignKey('users.id', ondelete='CASCADE'),
        nullable=True,
        index=True
    )

    created_at = Column(
        DateTime,
        default=datetime.utcnow,
        nullable=False
    )

    updated_at = Column(
        DateTime,
        default=datetime.utcnow,
        onupdate=datetime.utcnow,
        nullable=False
    )

    user = relationship(
        "User",
        back_populates="calculations"
    )
