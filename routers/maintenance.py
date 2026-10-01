from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

import models
from database import get_db
from schemas import MaintenanceRecordCreate


router = APIRouter(
    prefix="/maintenance",
    tags=["Maintenance"]
)


@router.post("")
def create_maintenance_record(
    maintenance: MaintenanceRecordCreate,
    db: Session = Depends(get_db)
):
    # Check that the equipment exists
    equipment_record = (
        db.query(models.Equipment)
        .filter(models.Equipment.id == maintenance.equipment_id)
        .first()
    )

    if equipment_record is None:
        raise HTTPException(
            status_code=404,
            detail=(
                f"Equipment with ID "
                f"{maintenance.equipment_id} not found."
            )
        )

    # Create the maintenance record
    maintenance_record = models.MaintenanceRecord(
        equipment_id=maintenance.equipment_id,
        maintenance_date=maintenance.maintenance_date,
        maintenance_type=maintenance.maintenance_type,
        description=maintenance.description,
        technician=maintenance.technician,
        cost=maintenance.cost,
    )

    db.add(maintenance_record)
    db.commit()
    db.refresh(maintenance_record)

    return {
        "message": "Maintenance record created successfully",
        "maintenance_record": maintenance_record,
    }
@router.get("/equipment/{equipment_id}")
def get_equipment_maintenance_records(
    equipment_id: int,
    db: Session = Depends(get_db)
):
    # Check that the equipment exists
    equipment_record = (
        db.query(models.Equipment)
        .filter(models.Equipment.id == equipment_id)
        .first()
    )

    if equipment_record is None:
        raise HTTPException(
            status_code=404,
            detail=f"Equipment with ID {equipment_id} not found."
        )

    # Get all maintenance records belonging to this equipment
    maintenance_records = (
    db.query(models.MaintenanceRecord)
    .filter(
        models.MaintenanceRecord.equipment_id == equipment_id
    )
    .order_by(
        models.MaintenanceRecord.maintenance_date.desc()
    )
    .all()
)
    return maintenance_records 


@router.get("")
def get_maintenance_records_by_type(
    maintenance_type: str,
    skip: int = 0,
    limit: int = 20,
    db: Session = Depends(get_db)
):
    maintenance_records = (
        db.query(models.MaintenanceRecord)
        .filter(
            models.MaintenanceRecord.maintenance_type
            == maintenance_type
        )
        .order_by(
            models.MaintenanceRecord.maintenance_date.desc()
        )
        .offset(skip)
        .limit(limit)
        .all()
    )

    return maintenance_records

    
