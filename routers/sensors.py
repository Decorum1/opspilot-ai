from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from datetime import datetime
from fastapi import Query 

import models
import schemas

from database import get_db
from auth_dependencies import require_roles


router = APIRouter(
    prefix="/sensors",
    tags=["Sensors"]
)


@router.post(
    "/readings",
    response_model=schemas.SensorReadingResponse,
    status_code=status.HTTP_201_CREATED
)
def create_sensor_reading(
    reading: schemas.SensorReadingCreate,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(
        require_roles("admin", "technician")
    )
):
    # Confirm that the equipment exists
    equipment = (
        db.query(models.Equipment)
        .filter(models.Equipment.id == reading.equipment_id)
        .first()
    )

    if equipment is None:
        raise HTTPException(
            status_code=404,
            detail="Equipment not found"
        )

    # Save the sensor reading
    new_reading = models.SensorReading(
        **reading.model_dump()
    )

    db.add(new_reading)
    db.commit()
    db.refresh(new_reading)

    return new_reading
@router.get(
    "/equipment/{equipment_id}/readings",
    response_model=list[schemas.SensorReadingResponse]
)
def get_equipment_sensor_readings(
    equipment_id: int,
    skip: int = Query(default=0, ge=0),
    limit: int = Query(default=100, ge=1, le=1000),
    start_date: datetime | None = None,
    end_date: datetime | None = None,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(
        require_roles("admin", "technician", "viewer")
    )
):


    # Check whether the equipment exists
    equipment = (
        db.query(models.Equipment)
        .filter(models.Equipment.id == equipment_id)
        .first()
    )

    if equipment is None:
        raise HTTPException(
            status_code=404,
            detail="Equipment not found"
        )

  
    # Validate the date range
    if start_date and end_date and start_date > end_date:
        raise HTTPException(
            status_code=422,
            detail="start_date cannot be after end_date"
        )

    # Build the sensor readings query
    query = db.query(models.SensorReading).filter(
        models.SensorReading.equipment_id == equipment_id
    )

    # Apply optional date filters
    if start_date is not None:
        query = query.filter(
            models.SensorReading.recorded_at >= start_date
        )

    if end_date is not None:
        query = query.filter(
            models.SensorReading.recorded_at <= end_date
        )

    # Return the newest readings first
    readings = (
        query.order_by(
            models.SensorReading.recorded_at.desc(),
            models.SensorReading.id.desc()
        )
        .offset(skip)
        .limit(limit)
        .all()
    )

    return readings


@router.get(
    "/equipment/{equipment_id}/latest",
    response_model=schemas.SensorReadingResponse
)
def get_latest_sensor_reading(
    equipment_id: int,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(
        require_roles("admin", "technician", "viewer")
    )
):
    equipment = (
        db.query(models.Equipment)
        .filter(models.Equipment.id == equipment_id)
        .first()
    )

    if equipment is None:
        raise HTTPException(
            status_code=404,
            detail="Equipment not found"
        )

    latest_reading = (
        db.query(models.SensorReading)
        .filter(
            models.SensorReading.equipment_id == equipment_id
        )
        .order_by(
            models.SensorReading.recorded_at.desc(),
            models.SensorReading.id.desc()
        )
        .first()
    )

    if latest_reading is None:
        raise HTTPException(
            status_code=404,
            detail="No sensor readings found for this equipment"
        )

    return latest_reading


def assess_temperature(temperature: float | None) -> str:
    if temperature is None:
        return "UNKNOWN"

    if temperature >= 95:
        return "CRITICAL"

    if temperature >= 80:
        return "WARNING"

    return "NORMAL"


def assess_vibration(vibration: float | None) -> str:
    if vibration is None:
        return "UNKNOWN"

    if vibration >= 5.0:
        return "CRITICAL"

    if vibration >= 3.0:
        return "WARNING"

    return "NORMAL"


def assess_pressure(pressure: float | None) -> str:
    if pressure is None:
        return "UNKNOWN"

    if pressure >= 10.0:
        return "CRITICAL"

    if pressure >= 8.0:
        return "WARNING"

    return "NORMAL"


def assess_overall_health(
    temperature_status: str,
    vibration_status: str,
    pressure_status: str
) -> str:

    statuses = [
        temperature_status,
        vibration_status,
        pressure_status
    ]

    if "CRITICAL" in statuses:
        return "CRITICAL"

    if "WARNING" in statuses:
        return "WARNING"

    if "NORMAL" in statuses:
        return "NORMAL"

    return "UNKNOWN"



@router.get("/equipment/{equipment_id}/health")
def get_equipment_health(
    equipment_id: int,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(
        require_roles("admin", "technician", "viewer")
    )
):
    # Check that the equipment exists
    equipment = (
        db.query(models.Equipment)
        .filter(models.Equipment.id == equipment_id)
        .first()
    )

    if equipment is None:
        raise HTTPException(
            status_code=404,
            detail="Equipment not found"
        )

    # Retrieve the latest sensor reading
    latest_reading = (
        db.query(models.SensorReading)
        .filter(
            models.SensorReading.equipment_id == equipment_id
        )
        .order_by(
            models.SensorReading.recorded_at.desc(),
            models.SensorReading.id.desc()
        )
        .first()
    )

    if latest_reading is None:
        raise HTTPException(
            status_code=404,
            detail="No sensor readings found"
        )

    # Assess equipment temperature
    temperature_status = assess_temperature(
        latest_reading.temperature
    )
    #Assess equipment vibration
    vibration_status= assess_vibration(
        latest_reading.vibration
    )
    #Assess equipment pressure
    pressure_status=assess_pressure(
        latest_reading.pressure
    )
   # Calculate overall equipment health
    overall_health = assess_overall_health(
        temperature_status,
        vibration_status,
        pressure_status
    ) 

    return {
        "equipment_id": equipment_id,
        "temperature": latest_reading.temperature,
        "temperature_status": temperature_status,
        "vibration": latest_reading.vibration,
        "vibration_status": vibration_status,
        "pressure": latest_reading.pressure,
        "pressure_status": pressure_status,
        "overall_health": overall_health,
        "recorded_at": latest_reading.recorded_at
    }




