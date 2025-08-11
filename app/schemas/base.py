from datetime import datetime
from uuid import UUID
from pydantic import BaseModel


class BaseSchema(BaseModel):
    id: UUID
    created_at: datetime
    updated_at: datetime

    class Config:
        from_orm = True
        from_attributes = True
