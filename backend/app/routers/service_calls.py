from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.dependencies import get_db, get_current_user, require_role
from app.orm_models import ATM, Service_Call, Technician, User, SERVICE_CALL_PRIORITY, SERVICE_CALL_STATUS, ROLE
from app.schemas.service_call import Service_Call_Create, Service_Call_Read, Discrepency_Read

router = APIRouter(prefix="/service_calls", tags=["service_calls"])

@router.get("", response_model=list[Service_Call_Read])
async def list_service_calls(
    db: AsyncSession = Depends(get_db),
    _: User = Depends(get_current_user)
):
    statement = select(Service_Call).order_by(Service_Call.id)

    results = await db.execute(statement)

    return list(results.scalars().all())

@router.get("/{service_call_id}", response_model=Service_Call_Read)
async def find_service_call_by_id(
    service_call_id: int,
    db: AsyncSession = Depends(get_db),
    _: User = Depends(get_current_user)
):
    service_call = await db.get(Service_Call, service_call_id)

    if not service_call:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Service_Call {service_call_id} not found."
        )
    return service_call

@router.get("/service_calls/discrepencies", response_model=list[Discrepency_Read])
async def colocation_discrepencies(
    priority: SERVICE_CALL_PRIORITY | None = None,
    db: AsyncSession = Depends(get_db),
    _: User = Depends(get_current_user)
):
    statement = (
        select(
            Service_Call.id.label("service_call_id"),
            Service_Call.title,
            Service_Call.atm_id,
            Service_Call.technician_id,
            ATM.branch_id.label("atm_branch_id"),
            Technician.branch_id.label("technician_branch_id")
        )
        .join(ATM, ATM.id == Service_Call.atm_id)
        .join(Technician, Technician.id == Service_Call.technician_id)
        .where(ATM.branch_id != Technician.branch_id)
        .order_by(Service_Call.id)
    )

    if priority is not None:
        statement = statement.where(Service_Call.priority == priority)

    result = await db.execute(statement)
    return list(result.mappings().all())

@router.post("", response_model=Service_Call_Read, status_code=status.HTTP_201_CREATED)
async def create_service_call(
    payload: Service_Call_Create,
    db: AsyncSession = Depends(get_db),
    _: User = Depends(require_role(ROLE.OPERATIONS_ADMIN))
):
    new_service_call = Service_Call(**payload.model_dump())
    db.add(new_service_call)
    await db.commit()
    await db.refresh(new_service_call)
    return new_service_call

@router.patch("/service_call/{service_call_id}/status", response_model=Service_Call_Read)
async def update_service_call_status(
    service_call_id: int,
    new_status: SERVICE_CALL_STATUS,
    db: AsyncSession = Depends(get_db),
    _: User = Depends(require_role(ROLE.OPERATIONS_ADMIN, ROLE.FIELD_TECHNICIAN)) 
):
    service_call = await db.get(Service_Call, service_call_id)
    if not service_call:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Service_Call {service_call_id} not found."
        )

    service_call.update_status(new_status)

    await db.commit()
    await db.refresh(service_call)
    return service_call