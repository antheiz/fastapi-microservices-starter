from sqlalchemy import (
    Boolean,
    Column,
    Enum,
    ForeignKey,
    String,
    Text,
    TIMESTAMP,
)
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.sql.expression import text
from sqlalchemy.orm import relationship
import uuid

from app.models.base import Base


class Address(Base):
    __tablename__ = "address"

    address_id = Column(
        UUID(as_uuid=True),
        primary_key=True,
        default=uuid.uuid4,
        unique=True,
        nullable=False,
    )
    customer_id = Column(UUID(as_uuid=True), ForeignKey("customer.customer_id"))
    first_name = Column(String(254))
    last_name = Column(String(254))
    email = Column(String(254))
    phone = Column(String(15))
    province = Column(String(254))
    city = Column(String(254))
    address_line = Column(Text)
    postal_code = Column(String(15))
    is_active = Column(Boolean, default=False)
    address_type = Column(
        Enum(
            "rumah",
            "asrama",
            "apartemen",
            "kantor",
            "sekolah",
            name="address_type_choices",
        ),
        default="rumah",
    )
    created_at = Column(
        TIMESTAMP(timezone=True), nullable=False, server_default=text("now()")
    )
    customer = relationship("Customer", back_populates="addresses")
