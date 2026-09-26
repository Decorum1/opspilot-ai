from datetime import date
from enum import Enum
from typing import Optional

from pydantic import BaseModel, Field


class EquipmentStatus(str, Enum):
    active = "active"
    inactive = "inactive"
    under_maintenance = "under_maintenance"
    retired = "retired"


class EquipmentCriticality(str, Enum):
    low = "low"
    medium = "medium"
    high = "high"
    critical = "critical"


class EquipmentCreate(BaseModel):
    name: str = Field(min_length=2, max_length=100)
    equipment_type: str = Field(min_length=2, max_length=50)
    manufacturer: str = Field(min_length=2, max_length=100)
    model: str = Field(min_length=1, max_length=100)
    serial_number: str = Field(min_length=3, max_length=100)
    location: str = Field(min_length=2, max_length=150)
    installation_date: date
    status: EquipmentStatus = EquipmentStatus.active
    criticality: EquipmentCriticality
    last_maintenance_date: Optional[date] = None


class EquipmentUpdate(BaseModel):
    name: str = Field(min_length=2, max_length=100)
    equipment_type: str = Field(min_length=2, max_length=50)
    manufacturer: str = Field(min_length=2, max_length=100)
    model: str = Field(min_length=1, max_length=100)
    serial_number: str = Field(min_length=3, max_length=100)
    location: str = Field(min_length=2, max_length=150)
    installation_date: date
    status: EquipmentStatus
    criticality: EquipmentCriticality
    last_maintenance_date: Optional[date] = None
