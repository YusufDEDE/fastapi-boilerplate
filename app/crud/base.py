from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy import update, delete, func
from uuid import UUID
from typing import Any, TypeVar, Generic, Type, Tuple, List
from pydantic import BaseModel
from sqlalchemy.orm import DeclarativeMeta

ModelType = TypeVar("ModelType", bound=DeclarativeMeta)
CreateSchemaType = TypeVar("CreateSchemaType", bound=BaseModel)
UpdateSchemaType = TypeVar("UpdateSchemaType", bound=BaseModel)


class CRUDBase(Generic[ModelType, CreateSchemaType, UpdateSchemaType]):
    def __init__(self, model: Type[ModelType]):
        self.model = model

    async def get(self, db: AsyncSession, id: UUID) -> ModelType | None:
        result = await db.execute(
            select(self.model).where(self.model.id == id)
        )
        return result.scalars().first()

    async def get_multi_paginated(
            self, db: AsyncSession, skip: int = 0, limit: int = 10
    ) -> Tuple[int, List[ModelType]]:
        count_result = await db.execute(
            select(func.count()).select_from(self.model)
        )
        total_count = count_result.scalar_one()

        result = await db.execute(
            select(self.model).offset(skip).limit(limit)
        )
        items = result.scalars().all()
        return total_count, items

    async def create(self, db: AsyncSession, obj_in: CreateSchemaType) -> ModelType:
        obj = self.model(**obj_in.model_dump())  # Pydantic v2 -> model_dump()
        db.add(obj)
        await db.commit()
        await db.refresh(obj)
        return obj

    async def update(
            self, db: AsyncSession, id: UUID, obj_in: UpdateSchemaType
    ) -> ModelType | None:
        await db.execute(
            update(self.model)
            .where(self.model.id == id)
            .values(**obj_in.model_dump(exclude_unset=True))
        )
        await db.commit()
        return await self.get(db, id)

    async def delete(self, db: AsyncSession, id: UUID) -> bool:
        result = await db.execute(
            delete(self.model).where(self.model.id == id)
        )
        await db.commit()
        return result.rowcount > 0
