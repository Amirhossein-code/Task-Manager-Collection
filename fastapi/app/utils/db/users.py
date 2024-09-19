from pydantic import EmailStr
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select

from fastapi import HTTPException, status

from ...models import User as UserDBModel
from ...schemas import users as user_schemas
from ..auth import hashing


async def get_user_by_email(email: EmailStr, db: AsyncSession) -> UserDBModel:
    stmt = select(UserDBModel).filter(UserDBModel.email == email)
    result = await db.execute(stmt)
    user = result.scalars().first()

    return user


async def get_user_by_email_or_404(email: EmailStr, db: AsyncSession) -> UserDBModel:
    user = await get_user_by_email(email, db)

    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="User not found"
        )

    return user


async def get_user_by_id_or_404(user_id: int, db: AsyncSession) -> UserDBModel:
    stmt = select(UserDBModel).filter(UserDBModel.id == user_id)
    result = await db.execute(stmt)
    user = result.scalars().first()

    # Check if suer exists
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="User not found"
        )

    return user


async def create_new_user(
    user_data: user_schemas.UserCreate, db: AsyncSession
) -> UserDBModel:
    existing_user = await get_user_by_email(user_data.email, db)

    if existing_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="Email already in use"
        )

    # Hash the Password
    hashed_password = hashing.hash_password(password=user_data.password)

    new_user = UserDBModel(
        email=user_data.email,
        hashed_password=hashed_password,
        full_name=user_data.full_name,
    )

    db.add(new_user)
    await db.commit()
    await db.refresh(new_user)

    return new_user


async def reset_user_password(
    user: UserDBModel, new_password: str, db: AsyncSession
) -> UserDBModel:
    # Hash the password
    hashed_password = hashing.hash_password(password=new_password)

    user.hashed_password = hashed_password

    await db.commit()
    await db.refresh(user)
    return user


async def update_user(
    user: UserDBModel,
    update_data: user_schemas.UserUpdate,
    db: AsyncSession,
    exclude_unset: bool = False,
) -> UserDBModel:
    # Creates a dictionary representation of a user data (Pydantic model instance)
    data_to_update = update_data.model_dump(exclude_unset=exclude_unset)

    for key, value in data_to_update.items():
        setattr(user, key, value)

    await db.commit()
    await db.refresh(user)

    return user


async def delete_user(user: UserDBModel, db: AsyncSession) -> None:
    await db.delete(user)
    await db.commit()
