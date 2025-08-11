from sqlalchemy.ext.asyncio import AsyncSession
from app.models.example import Example

EXAMPLE_SEED = [
    {"name": "Example Name 1"},
    {"name": "Example Name 2"},
    {"name": "Example Name 3"},
]

async def egypt_seed_data(db: AsyncSession):
    for _example in EXAMPLE_SEED:
        equipment = Example(
            name=_example["name"],
        )
        db.add(equipment)

    await db.commit()
    print("Example Seed data inserted.")
