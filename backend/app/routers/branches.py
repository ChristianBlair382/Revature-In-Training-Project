from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.dependencies import get_db
from app.orm_models.branch import Branch
from app.schemas.branch import Branch_Read, Branch_Create

router = APIRouter(prefix="/branches", tags=["branches"])

# GET ENDPOINTS

@router.get("", response_model=list[Branch_Read])
async def list_branches(db: AsyncSession = Depends(get_db)):
    statement = select(Branch).order_by(Branch.id)

    results = await db.execute(statement)

    return list(results.scalars().all())

@router.get("/{branch_id}", response_model=Branch_Read)
async def find_branch_by_id(branch_id: int, db: AsyncSession = Depends(get_db)):
    branch = await db.get(Branch, branch_id)

    if not branch:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Branch {branch_id} not found."
        )
    return branch

# POST ENDPOINTS

@router.post("", response_model=Branch_Read, status_code=status.HTTP_201_CREATED)
async def create_branch(payload: Branch_Create, db: AsyncSession = Depends(get_db)):
    new_branch = Branch(**payload.model_dump())
    db.add(new_branch)
    await db.commit()
    await db.refresh(new_branch)
    return new_branch