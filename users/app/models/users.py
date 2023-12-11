from sqlalchemy import (
    Boolean,
    Column,
    String,
    TIMESTAMP,
)
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.sql.expression import text
from sqlalchemy.orm import relationship
import uuid

from app.models.base import Base


class User(Base):
    __tablename__ = "user"

    user_id = Column(
        UUID(as_uuid=True),
        primary_key=True,
        default=uuid.uuid4,
        unique=True,
        nullable=False,
    )
    email = Column(String(254), unique=True, nullable=False)
    password = Column(String(254), nullable=False)
    is_superuser = Column(Boolean, default=False)
    created_at = Column(
        TIMESTAMP(timezone=True), nullable=False, server_default=text("now()")
    )
    customer = relationship("Customer", back_populates="user", uselist=False)
