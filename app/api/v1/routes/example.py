from app.crud.base import CRUDBase
from app.models.example import Example
from app.schemas.example import ExampleCreate, ExampleUpdate, ExampleRead
from app.api.router_factory import create_router

crud_example = CRUDBase[Example, ExampleCreate, ExampleUpdate](Example)

example_router = create_router(
    model_name="Examples",
    schema_read=ExampleRead,
    schema_create=ExampleCreate,
    schema_update=ExampleUpdate,
    crud=crud_example,
)
