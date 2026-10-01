from datetime import datetime

from sqlalchemy import (
    CheckConstraint,
    Column,
    Date,
    DateTime,
    ForeignKey,
    Integer,
    Numeric,
    String,
    Text,
)
from sqlalchemy.orm import relationship

from database import Base


class Equipment(Base):
    __tablename__ = "equipment"

    id = Column(Integer, primary_key=True, index=True)

    name = Column(String(100), nullable=False)
    equipment_type = Column(String(50), nullable=False)
    manufacturer = Column(String(100), nullable=False)
    model = Column(String(100), nullable=False)

    serial_number = Column(
        String(100),
        unique=True,
        nullable=False,
        index=True,
    )

    location = Column(String(150), nullable=False)
    installation_date = Column(Date, nullable=False)

    status = Column(
        String(30),
        nullable=False,
        default="active",
    )

    criticality = Column(String(20), nullable=False)

    last_maintenance_date = Column(
        Date,
        nullable=True,
    )

    created_at = Column(
        DateTime,
        default=datetime.utcnow,
        nullable=False,
    )

    maintenance_records = relationship(
        "MaintenanceRecord",
        back_populates="equipment",
    )


class MaintenanceRecord(Base):
    __tablename__ = "maintenance_records"
    __table_args__ = (
        CheckConstraint(
            "cost >= 0",
            name="check_maintenance_cost_non_negative",
        ),
    )

    id = Column(Integer, primary_key=True, index=True)

    equipment_id = Column(
        Integer,
        ForeignKey("equipment.id", ondelete="RESTRICT"),
        nullable=False,
        index=True,
    )

    maintenance_date = Column(Date, nullable=False)
    maintenance_type = Column(String(50), nullable=False)
    description = Column(Text, nullable=False)
    technician = Column(String(100), nullable=False)

    cost = Column(
        Numeric(12, 2),
        nullable=True,
    )

    created_at = Column(
        DateTime,
        default=datetime.utcnow,
        nullable=False,
    )

    equipment = relationship(
        "Equipment",
        back_populates="maintenance_records",
    )


