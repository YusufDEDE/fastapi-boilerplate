from pydantic import BaseModel, ConfigDict
from app.schemas.base import BaseSchema


class ExampleCreate(BaseModel):
    name: str

    model_config = ConfigDict(from_attributes=True)


class ExampleUpdate(BaseModel):
    name: str | None = None


class ExampleRead(BaseSchema):
    name: str
