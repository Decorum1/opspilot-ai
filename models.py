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
    Boolean,
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
    work_orders = relationship(
        "WorkOrder",
        back_populates= "equipment",
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


class WorkOrder(Base):
    __tablename__ = "work_orders"

    id = Column(Integer, primary_key=True, index=True)

    equipment_id = Column(
        Integer,
        ForeignKey("equipment.id", ondelete="RESTRICT"),
        nullable=False,
        index=True,
    )
    
    assigned_user_id = Column(
        Integer,
        ForeignKey("users.id", ondelete="SET NULL"),
        nullable=True,
        index=True
    )




    title = Column(String(150), nullable=False)
    description = Column(Text, nullable=False)

    priority = Column(
        String(20),
        nullable=False,
        default="medium",
    )

    status = Column(
        String(30),
        nullable=False,
        default="open",
    )

    assigned_to = Column(String(100), nullable=True)

    due_date = Column(Date, nullable=True)

    created_at = Column(
        DateTime,
        default=datetime.utcnow,
        nullable=False,
    )

    completed_at = Column(DateTime, nullable=True)

    equipment = relationship(
        "Equipment",
        back_populates="work_orders",
    )

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)

    full_name = Column(String(150), nullable=False)

    email = Column(
        String(255),
        unique=True,
        index=True,
        nullable=False
    )

    hashed_password = Column(String(255), nullable=False)

    role = Column(
        String(20),
        nullable=False,
        default="viewer"
    )

    is_active = Column(
        Boolean,
        nullable=False,
        default=True
    )

    created_at = Column(
        DateTime,
        default=datetime.utcnow,
        nullable=False
    )




