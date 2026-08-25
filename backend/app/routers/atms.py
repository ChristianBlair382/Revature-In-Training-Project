from decimal import Decimal

from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.dependencies import get_db, get_current_user, require_role
from app.orm_models import ATM, User, ATM_STATUS, ROLE
from app.schemas.atm import ATM_Create, ATM_Read

router = APIRouter(prefix="/atms", tags=["atms"])

# GET ENDPOINTS

@router.get("", response_model=list[ATM_Read])
async def list_atms(
        max_cash: Decimal | None = Query(
            default=None,
            ge=0,
            le=7500,
            description="Only return ATMs strictly below this cash limit"
        ),
        db: AsyncSession = Depends(get_db),
        _: User = Depends(get_current_user)
    ):
    statement = select(ATM).where(ATM.status != ATM_STATUS.OFFLINE)

    if max_cash is not None:
        statement = statement.where(ATM.cash_lvl < max_cash)
    statement = statement.order_by(ATM.id)

    result = await db.execute(statement)

    return list(result.scalars().all())

@router.get("/{atm_id}", response_model=ATM_Read)
async def get_atm_by_id(
    atm_id: int,
    db: AsyncSession = Depends(get_db),
    _: User = Depends(get_current_user)
):
    atm = await db.get(ATM, atm_id)

    if not atm:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"ATM {atm_id} not found."
        )

    return atm

# POST ENDPOINTS

@router.post("", response_model=ATM_Read, status_code=status.HTTP_201_CREATED)
async def create_atm(
    payload: ATM_Create,
    db: AsyncSession = Depends(get_db),
    _: User = Depends(require_role(ROLE.OPERATIONS_ADMIN))
):
    new_atm = ATM(**payload.model_dump())
    db.add(new_atm)
    await db.commit()
    await db.refresh(new_atm)
    return new_atm