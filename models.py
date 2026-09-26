from datetime import datetime

from sqlalchemy import Column, Date, DateTime, Integer, String

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
        index=True
    )

    location = Column(String(150), nullable=False)
    installation_date = Column(Date, nullable=False)

    status = Column(
        String(30),
        nullable=False,
        default="active"
    )

    criticality = Column(String(20), nullable=False)

    last_maintenance_date = Column(
        Date,
        nullable=True
    )

    created_at = Column(
        DateTime,
        default=datetime.utcnow,
        nullable=False
    )
