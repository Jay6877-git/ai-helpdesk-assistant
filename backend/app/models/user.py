from sqlalchemy import Integer, String, Column

from app.db.database import Base

class User(Base):
    """Database model for registered helpdesk users."""

    __tablename__ = 'users'

    id = Column(
        Integer,
        primary_key=True,
        index=True
    )

    # Email is used as the unique account identifier.
    email = Column(
        String,
        unique=True,
        index=True,
        nullable=False
    )

    # Store the password value separately from the public response schema.
    password_hash = Column(
        String,
        nullable=False
    )

    full_name = Column(
        String,
        nullable=False
    )
