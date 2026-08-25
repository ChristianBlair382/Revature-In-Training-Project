from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.dependencies import get_db, get_current_user, require_role
from app.orm_models import Diagnostic_Report, User, ROLE
from app.schemas.diagnostic_report import Diagnostic_Report_Create, Diagnostic_Report_Read

router = APIRouter(prefix="/diagnostic_reports", tags=["diagnostic_reports"])

# GET ENDPOINTS

@router.get("", response_model=list[Diagnostic_Report_Read])
async def list_diagnostic_reports(
    db: AsyncSession = Depends(get_db),
    _: User = Depends(get_current_user)
):
    statement = select(Diagnostic_Report).order_by(Diagnostic_Report.id)

    results = await db.execute(statement)

    return list(results.scalars().all())

@router.get("/{diagnostic_report_id}", response_model=Diagnostic_Report_Read)
async def find_diagnostic_report_by_id(
    diagnostic_report_id: int,
    db: AsyncSession = Depends(get_db),
    _: User = Depends(get_current_user)
):
    diagnostic_report = await db.get(Diagnostic_Report, diagnostic_report_id)

    if not diagnostic_report:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Diagnostic Log {diagnostic_report_id} not found."
        )
    return diagnostic_report

# POST ENDPOINTS

@router.post("", response_model=Diagnostic_Report_Read, status_code=status.HTTP_201_CREATED)
async def create_diagnostic_report(
    payload: Diagnostic_Report_Create,
    db: AsyncSession = Depends(get_db),
    _: User = Depends(require_role(ROLE.OPERATIONS_ADMIN))
):
    new_diagnostic_report = Diagnostic_Report(**payload.model_dump())
    db.add(new_diagnostic_report)
    await db.commit()
    await db.refresh(new_diagnostic_report)
    return new_diagnostic_report