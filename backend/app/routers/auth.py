from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.dependencies import get_db, require_role
from app.orm_models import User, ROLE
from app.schemas.user import User_Create, User_Read, Token
from app.security import create_access_token, encrypt_password, verify_password

router = APIRouter(prefix="/auth", tags=["auth"])

@router.post("/token", response_model=Token)
async def login(
    form_data: OAuth2PasswordRequestForm = Depends(),
    db: AsyncSession = Depends(get_db)
) -> Token:
    result = await db.execute(select(User).where(User.username == form_data.username))
    user = result.scalar_one_or_none()

    if user is None or not verify_password(form_data.password, user.hashed_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Username or Password is incorrect.",
            headers={"WWW-Authenticate": "Bearer"}
        )

    access_token = create_access_token(data={"sub": user.username, "role": user.role.value})
    return Token(access_token=access_token, token_type="bearer")

@router.post("/register", response_model=User_Read, status_code=status.HTTP_201_CREATED)
async def register_user(
    payload: User_Create,
    db: AsyncSession = Depends(get_db),
    _: User = Depends(require_role(ROLE.OPERATIONS_ADMIN)),
) -> User:
    existing = await db.execute(select(User).where(User.username == payload.username))
    if existing.scalar_one_or_none() is not None:
        raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"'{payload.username}' already exists.",
                headers={"WWW-Authenticate": "Bearer"}
            )

    user = User(
        username = payload.username, 
        hashed_password = encrypt_password(payload.password), 
        role = payload.role
    )

    db.add(user)
    await db.commit()
    await db.refresh(user)
    return user