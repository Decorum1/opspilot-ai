from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

import models
from database import get_db
from schemas import EquipmentCreate, EquipmentUpdate


router = APIRouter(
    prefix="/equipment",
    tags=["Equipment"]
)


@router.post("")
def create_equipment(
    equipment: EquipmentCreate,
    db: Session = Depends(get_db)
):
    existing_equipment = (
        db.query(models.Equipment)
        .filter(
            models.Equipment.serial_number == equipment.serial_number
        )
        .first()
    )

    if existing_equipment:
        raise HTTPException(
            status_code=409,
            detail=(
                f"Equipment with serial number "
                f"{equipment.serial_number} already exists."
            )
        )

    db_equipment = models.Equipment(
        name=equipment.name,
        equipment_type=equipment.equipment_type,
        manufacturer=equipment.manufacturer,
        model=equipment.model,
        serial_number=equipment.serial_number,
        location=equipment.location,
        installation_date=equipment.installation_date,
        status=equipment.status.value,
        criticality=equipment.criticality.value,
        last_maintenance_date=equipment.last_maintenance_date
    )

    db.add(db_equipment)
    db.commit()
    db.refresh(db_equipment)

    return {
        "message": "Equipment created successfully",
        "equipment_id": db_equipment.id,
        "name": db_equipment.name,
        "serial_number": db_equipment.serial_number
    }


@router.get("")
def get_all_equipment(
    db: Session = Depends(get_db)
):
    equipment = db.query(models.Equipment).all()

    return equipment


@router.get("/{equipment_id}")
def get_equipment(
    equipment_id: int,
    db: Session = Depends(get_db)
):
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

    return equipment_record

@router.put("/{equipment_id}")
def update_equipment(
    equipment_id: int,
    equipment_update: EquipmentUpdate,
    db: Session = Depends(get_db)
):
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

    duplicate_serial = (
        db.query(models.Equipment)
        .filter(
            models.Equipment.serial_number
            == equipment_update.serial_number,
            models.Equipment.id != equipment_id
        )
        .first()
    )

    if duplicate_serial:
        raise HTTPException(
            status_code=409,
            detail=(
                f"Equipment with serial number "
                f"{equipment_update.serial_number} already exists."
            )
        )

    equipment_record.name = equipment_update.name
    equipment_record.equipment_type = equipment_update.equipment_type
    equipment_record.manufacturer = equipment_update.manufacturer
    equipment_record.model = equipment_update.model
    equipment_record.serial_number = equipment_update.serial_number
    equipment_record.location = equipment_update.location
    equipment_record.installation_date = equipment_update.installation_date
    equipment_record.status = equipment_update.status.value
    equipment_record.criticality = equipment_update.criticality.value
    equipment_record.last_maintenance_date = (
        equipment_update.last_maintenance_date
    )

    db.commit()
    db.refresh(equipment_record)

    return {
        "message": "Equipment updated successfully",
        "equipment": equipment_record
    }


@router.delete("/{equipment_id}")
def delete_equipment(
    equipment_id: int,
    db: Session = Depends(get_db)
):
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

    maintenance_record = (
        db.query(models.MaintenanceRecord)
        .filter(
            models.MaintenanceRecord.equipment_id == equipment_id
        )
        .first()
    )

    if maintenance_record:
        raise HTTPException(
            status_code=409,
            detail=(
                "Cannot delete equipment with existing "
                "maintenance records."
            )
        )

    db.delete(equipment_record)
    db.commit()

    return {
        "message": "Equipment deleted successfully",
        "equipment_id": equipment_id
    }
