# FastAPI Boilerplate

## Setup

### 1. Create virtual environment and activate:

```bash
python -m venv venv
source venv/bin/activate   # Linux / macOS
# venv\Scripts\activate    # Windows
```

### 2. Install dependencies:

```bash
pip install -r requirements.txt
```

### 3. Configure database URL in app/core/database.py or via .env:

```bash
POSTGRES_USER=postgres
POSTGRES_PASSWORD=postgres
POSTGRES_SERVER=db
POSTGRES_PORT=5432
POSTGRES_DB=fastapi_boilerplate
```

### 4. Run database migrations:

````bash
alembic revision --autogenerate
alembic upgrade head
````

### 4. Start FastAPI server:

````bash
uvicorn app.main:app --reload
````

### 5. Access Swagger docs at:

````bash
http://localhost:8000/docs
````

## Useful commands

### Create new migration:

````bash
alembic revision -m "your message"
````

### Show current migrations:

````bash
alembic current
````

### Rollback migration:

````bash
alembic downgrade -1
````

## Notes
- Use /api/v1/... routes for version 1 API
- Generic CRUD and pagination ready
- Async SQLAlchemy with PostgreSQL supported
- Pydantic v2 with <code>form_orm=True</code> used