# My FastAPI Starter

A RESTful API starter built with FastAPI, SQLAlchemy ORM, and Alembic for database migrations. This starter uses SQLite for development and Supabase PostgreSQL for production.

## Features

- FastAPI for high-performance API development
- SQLAlchemy ORM for database operations
- Alembic for database migrations
- SQLite for development environment
- Supabase PostgreSQL for production
- Automatic OpenAPI/Swagger documentation
- Environment-based configuration
- Authentication and security features
- Automatic database migrations on startup

## Project Structure

```
.
├── alembic/          # Database migration files
├── src/             # Source code
│   ├── models/      # Database models
│   │   └── __init__.py  # Imports all models for migrations
│   └── schemas/     # Pydantic schemas
├── .env             # Environment variables (not in version control)
├── .env.example     # Example environment variables
├── alembic.ini      # Alembic configuration
├── requirements.txt # Project dependencies
└── README.md        # This file
```

## Prerequisites

- Python 3.8+
- pip (Python package manager)
- Virtual environment (recommended)

## Setup

1. Create and activate a virtual environment:

```bash
# Create virtual environment
python -m venv ./venv

# Activate virtual environment
# On Windows:
./venv/Scripts/activate
# On Unix or MacOS:
source venv/bin/activate
```

2. Install dependencies:

```bash
pip install -r requirements.txt
```

3. Set up environment variables:

```bash
# Copy the example environment file
cp .env.example .env
# Edit .env with your configuration
```

## Database Setup

1. Initialize Alembic migrations:
   There is a example `user` model, take out before inti and applying migrations if you don't want it
   Don't forget to delete the array in `src/models/__init__.py`

```bash
alembic revision --autogenerate -m "init alembic migration"
```

2. Apply migrations:

```bash
alembic upgrade head
```

## Running the Application

Start the development server:

```bash
fastapi dev ./src/main.py
```

The API will be available at `http://localhost:8000`

- API documentation: `http://localhost:8000/docs`
- Alternative API documentation: `http://localhost:8000/redoc`

## Development

### Database Models

- Models are defined using SQLAlchemy ORM's Base
- Located in `src/models/`
- `__init__.py` should imported every models in order to do migrations

### API Schemas

- Request/response schemas are defined in `src/schemas/`
- OpenAPI and Swagger documentation is automatically generated by FastAPI

### Database Migrations

To create a new migration:

```bash
alembic revision --autogenerate -m "description of changes"
```

To apply migrations:

```bash
alembic upgrade head
```

## Production Deployment

For production deployment:

1. Configure PostgreSQL connection in `.env`
2. Migrations upgrade will run autoatically in main
