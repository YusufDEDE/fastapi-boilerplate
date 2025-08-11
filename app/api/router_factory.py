from fastapi import APIRouter, Depends, Query, HTTPException
from typing import Type, TypeVar, Generic, List
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.database import get_db
from app.schemas.commons import PaginatedResponse

TRead = TypeVar("TRead")
TCreate = TypeVar("TCreate")
TUpdate = TypeVar("TUpdate")


def create_router(
    model_name: str,
    schema_read: Type[TRead],
    schema_create: Type[TCreate],
    schema_update: Type[TUpdate],
    crud,
) -> APIRouter:
    router = APIRouter(prefix=f"/{model_name.lower()}", tags=[model_name])

    ResponseModel = PaginatedResponse[schema_read]  # Type annotation workaround

    @router.get("/", response_model=ResponseModel)
    async def get_all(
        skip: int = Query(0, ge=0),
        limit: int = Query(10, le=100),
        db: AsyncSession = Depends(get_db),
    ):
        total, db_items = await crud.get_multi_paginated(db, skip, limit)
        return ResponseModel(
            total=total,
            items=[schema_read.model_validate(obj, from_attributes=True) for obj in db_items],
        )

    @router.get("/{id}", response_model=schema_read)
    async def get_one(id: str, db: AsyncSession = Depends(get_db)):
        obj = await crud.get(db, id)
        if not obj:
            raise HTTPException(status_code=404, detail=f"{model_name} not found")
        return schema_read.model_validate(obj, from_attributes=True)

    @router.post("/", response_model=schema_read, status_code=201)
    async def create(obj_in: schema_create, db: AsyncSession = Depends(get_db)):
        obj = await crud.create(db, obj_in)
        return schema_read.model_validate(obj, from_attributes=True)

    @router.put("/{id}", response_model=schema_read)
    async def update(id: str, obj_in: schema_update, db: AsyncSession = Depends(get_db)):
        obj = await crud.update(db, id, obj_in)
        if not obj:
            raise HTTPException(status_code=404, detail=f"{model_name} not found")
        return schema_read.model_validate(obj, from_attributes=True)

    @router.delete("/{id}", status_code=204)
    async def delete(id: str, db: AsyncSession = Depends(get_db)):
        result = await crud.delete(db, id)
        if not result:
            raise HTTPException(status_code=404, detail=f"{model_name} not found")
        return  # 204 No Content dönüşü (boş gövde)

    return router
