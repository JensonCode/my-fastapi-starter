from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from sqlalchemy.exc import SQLAlchemyError, IntegrityError
from pydantic import ValidationError

from .config import app_config, logger
from .database.migration import check_migrations

from .routers import user

app = FastAPI(
    title=app_config["project_name"],
    description=app_config["project_description"],
    version=app_config["project_version"],
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

check_migrations()


@app.exception_handler(SQLAlchemyError)
async def sqlalchemy_exception_handler(request: Request, exc: SQLAlchemyError):
    logger.error(
        f"SQLAlchemyError at {request.url.path} | Method: {request.method} | Error: {exc}"
    )
    return JSONResponse(
        status_code=500,
        content={"detail": "A database error occurred."},
    )


@app.exception_handler(IntegrityError)
async def integrity_error_handler(request: Request, exc: IntegrityError):
    logger.error(
        f"SQLAlchemyError at {request.url.path} | Method: {request.method} | Error: {exc}"
    )
    return JSONResponse(
        status_code=400,
        content={
            "detail": "Database integrity error (e.g., duplicate entry or constraint failed)"
        },
    )


@app.exception_handler(ValidationError)
async def validation_exception_handler(request: Request, exc: ValidationError):
    logger.error(
        f"ValidationError at {request.url.path} | Method: {request.method} | Error: {exc}"
    )
    return JSONResponse(
        status_code=400,
        content={"detail": exc.errors()},
    )


@app.get("/")
async def root():
    return {"message": "Hello World"}


@app.get("/health")
async def health():
    return {"status": "ok"}


app.include_router(user.router)


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=8000)
