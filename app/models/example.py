from sqlalchemy import Column, String
from app.models.base import BaseModel


class Example(BaseModel):
    __tablename__: str = "example"
    name = Column(String)
