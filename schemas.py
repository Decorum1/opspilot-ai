from datetime import date, datetime

from enum import Enum
from typing import Optional
from decimal import Decimal

from pydantic import BaseModel, Field, EmailStr, ConfigDict, model_validator


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

class MaintenanceRecordCreate(BaseModel):
    equipment_id: int = Field(gt=0)
    maintenance_date: date
    maintenance_type: str = Field(min_length=2, max_length=50)
    description: str = Field(min_length=2)
    technician: str = Field(min_length=2, max_length=100)
    cost: Optional[Decimal] = Field(default=None, ge=0)

from typing import Literal

class WorkOrderCreate(BaseModel):
    equipment_id: int = Field(gt=0)
    title: str = Field(min_length=3, max_length=150)
    description: str = Field(min_length=3)

    priority: Literal[
        "low", "medium", "high", "critical"
    ] = "medium"

    assigned_to: Optional[str] = None
    due_date: Optional[date] = None


class WorkOrderStatusUpdate(BaseModel):
    status: Literal[
        "open",
        "in_progress",
        "completed",
        "cancelled"
    ]


class UserRegister(BaseModel):
    full_name: str = Field(
        min_length=2,
        max_length=150
    )

    email: EmailStr

    password: str = Field(
        min_length=12,
        max_length=128
    )


class UserResponse(BaseModel):
    id: int
    full_name: str
    email: EmailStr
    role: str
    is_active: bool
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)

class WorkOrderAssign(BaseModel):
    assigned_user_id: int = Field(gt=0)


# ========================================
# PHASE 5 - SENSOR DATA SCHEMAS
# ========================================

class SensorReadingCreate(BaseModel):
    equipment_id: int = Field(gt=0)

    temperature: float | None = None

    vibration: float | None = Field(
        default=None,
        ge=0
    )

    pressure: float | None = None

    operating_hours: float | None = Field(
        default=None,
        ge=0
    )

    @model_validator(mode="after")
    def validate_measurements(self):
        if all(
            value is None
            for value in (
                self.temperature,
                self.vibration,
                self.pressure,
                self.operating_hours,
            )
        ):
            raise ValueError(
                "At least one sensor measurement is required"
            )

        return self


class SensorReadingResponse(SensorReadingCreate):
    id: int
    recorded_at: datetime

    model_config = {
        "from_attributes": True
    }


# ==========================================
# PHASE 6: MACHINE LEARNING PREDICTION SCHEMAS
# ==========================================

from pydantic import BaseModel, Field


class PredictionRequest(BaseModel):
    air_temperature: float = Field(gt=0)
    process_temperature: float = Field(gt=0)
    rotational_speed: float = Field(ge=0)
    torque: float = Field(ge=0)
    tool_wear: float = Field(ge=0)


class PredictionResponse(BaseModel):
    predicted_failure: bool
    failure_score: float
    threshold: float
    model_version: str
    model_status: str



