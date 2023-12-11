from sqlalchemy import (
    Column,
    Date,
    Enum,
    ForeignKey,
    String,
    TIMESTAMP,
)
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.sql.expression import text
from sqlalchemy.orm import relationship
import uuid

from app.models.base import Base


class Customer(Base):
    __tablename__ = "customer"

    customer_id = Column(
        UUID(as_uuid=True),
        primary_key=True,
        default=uuid.uuid4,
        unique=True,
        nullable=False,
    )
    user_id = Column(UUID(as_uuid=True), ForeignKey("user.user_id"))
    first_name = Column(String(254), nullable=True)
    last_name = Column(String(254), nullable=True)
    email = Column(String(254), nullable=True)
    gender = Column(Enum("Pria", "Wanita", name="gender_choices"), nullable=True)
    phone = Column(String(15), nullable=True)
    date_of_birth = Column(Date, nullable=True)
    photo = Column(String(254), nullable=True, default="user-default.jpg")
    created_at = Column(
        TIMESTAMP(timezone=True), nullable=False, server_default=text("now()")
    )
    user = relationship("User", back_populates="customer")
    addresses = relationship("Address", back_populates="customer")
