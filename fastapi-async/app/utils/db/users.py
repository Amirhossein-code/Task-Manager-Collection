from fastapi import HTTPException, status
from pydantic import EmailStr
from sqlalchemy.ext.asyncio import AsyncSession

from ...models import User
from ...schemas import users as user_schemas
from ..auth.hashing import Hash


async def get_user_by_email(email: EmailStr, db: AsyncSession) -> User:
    user = await db.query(User).filter(User.email == email).first()
    return user


async def get_user_by_email_or_404(email: EmailStr, db: AsyncSession) -> User:
    user = await get_user_by_email(email, db)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="User not found"
        )
    return user


async def get_user_by_id_or_404(user_id: int, db: AsyncSession) -> User:
    user = await db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="User not found"
        )
    return user


async def create_new_user(user_data: user_schemas.UserCreate, db: AsyncSession) -> User:
    existing_user = await get_user_by_email(user_data.email, db)
    if existing_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="Email already in use"
        )

    hashed_password = Hash.hash_password(password=user_data.password)

    new_user = User(
        email=user_data.email,
        hashed_password=hashed_password,
        full_name=user_data.full_name,
    )

    db.add(new_user)
    await db.commit()
    await db.refresh(new_user)
    return new_user


async def reset_user_password(user: User, new_password: str, db: AsyncSession) -> User:
    hashed_password = Hash.hash_password(password=new_password)

    user.hashed_password = hashed_password

    await db.commit()
    await db.refresh(user)
    return user


async def update_user(
    user: User,
    update_data: user_schemas.UserUpdate,
    db: AsyncSession,
    full_update: bool,  # True -> PUT | False -> Patch
) -> User:
    data_to_update = update_data.model_dump(exclude_unset=not full_update)

    for key, value in data_to_update.items():
        setattr(user, key, value)

    await db.commit()
    await db.refresh(user)
    return user


async def delete_user(user: User, db: AsyncSession) -> None:
    await db.delete(user)
    await db.commit()
