
from datetime import datetime

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

import models
from database import get_db
from schemas import WorkOrderCreate, WorkOrderStatusUpdate


router = APIRouter(
    prefix="/work-orders",
    tags=["Work Orders"]
)


# CREATE A WORK ORDER
@router.post("", status_code=201)
def create_work_order(
    work_order: WorkOrderCreate,
    db: Session = Depends(get_db)
):
    equipment = (
        db.query(models.Equipment)
        .filter(
            models.Equipment.id == work_order.equipment_id
        )
        .first()
    )

    if equipment is None:
        raise HTTPException(
            status_code=404,
            detail="Equipment not found"
        )

    new_work_order = models.WorkOrder(
        **work_order.model_dump()
    )

    db.add(new_work_order)
    db.commit()
    db.refresh(new_work_order)

    return new_work_order


# GET ALL WORK ORDERS
@router.get("")
def get_work_orders(
    skip: int = 0,
    limit: int = 20,
    db: Session = Depends(get_db)
):
    work_orders = (
        db.query(models.WorkOrder)
        .order_by(models.WorkOrder.id.desc())
        .offset(skip)
        .limit(limit)
        .all()
    )

    return work_orders


# GET ONE WORK ORDER
@router.get("/{work_order_id}")
def get_work_order(
    work_order_id: int,
    db: Session = Depends(get_db)
):
    work_order = (
        db.query(models.WorkOrder)
        .filter(models.WorkOrder.id == work_order_id)
        .first()
    )

    if work_order is None:
        raise HTTPException(
            status_code=404,
            detail="Work order not found"
        )

    return work_order


# UPDATE WORK ORDER STATUS
@router.patch("/{work_order_id}/status")
def update_work_order_status(
    work_order_id: int,
    update: WorkOrderStatusUpdate,
    db: Session = Depends(get_db)
):
    work_order = (
        db.query(models.WorkOrder)
        .filter(models.WorkOrder.id == work_order_id)
        .first()
    )

    if work_order is None:
        raise HTTPException(
            status_code=404,
            detail="Work order not found"
        )

    # Repeating the same status should not change anything
    if work_order.status == update.status:
        return work_order

    # Completed and cancelled work orders are final
    if work_order.status in ("completed", "cancelled"):
        raise HTTPException(
            status_code=409,
            detail="Cannot change a completed or cancelled work order"
        )

    # Define allowed status transitions
    allowed_transitions = {
        "open": {"in_progress", "cancelled"},
        "in_progress": {"completed", "cancelled"},
    }

    if update.status not in allowed_transitions.get(
        work_order.status, set()
    ):
        raise HTTPException(
            status_code=409,
            detail="Invalid work order status transition"
        )

    # Update the status
    work_order.status = update.status

    # Record completion time only when first completed
    if update.status == "completed":
        work_order.completed_at = datetime.utcnow()

    db.commit()
    db.refresh(work_order)

    return work_order
