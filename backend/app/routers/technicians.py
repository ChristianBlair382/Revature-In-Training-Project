from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.dependencies import get_db, get_current_user, require_role
from app.orm_models import Technician, User, ROLE
from app.schemas.technician import Technician_Read, Technician_Create

router = APIRouter(prefix="/technicians", tags=["technicians"])

# GET ENDPOINTS

@router.get("", response_model=list[Technician_Read])
async def list_technicians(
    db: AsyncSession = Depends(get_db),
    _: User = Depends(get_current_user)
):
    statement = select(Technician).order_by(Technician.id)

    results = await db.execute(statement)

    return list(results.scalars().all())

@router.get("/{technician_id}", response_model=Technician_Read)
async def find_technician_by_id(
    technician_id: int,
    db: AsyncSession = Depends(get_db),
    _: User = Depends(get_current_user)
):
    technician = await db.get(Technician, technician_id)

    if not technician:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Technician {technician_id} not found."
        )
    return technician

# POST ENDPOINTS

@router.post("", response_model=Technician_Read, status_code=status.HTTP_201_CREATED)
async def create_technician(
    payload: Technician_Create,
    db: AsyncSession = Depends(get_db),
    _: User = Depends(require_role(ROLE.OPERATIONS_ADMIN))
):
    new_technician = Technician(**payload.model_dump())
    db.add(new_technician)
    await db.commit()
    await db.refresh(new_technician)
    return new_technician