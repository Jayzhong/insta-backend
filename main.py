from fastapi import FastAPI, Request, status
from fastapi.responses import JSONResponse
from src.interfaces.api.router import api_router
from src.domain.users.exceptions import InvalidCredentialsError

app = FastAPI(
    title="Insta-Backend",
    description="An Instagram-like backend service built with Clean Architecture.",
    version="0.1.0",
)

@app.exception_handler(InvalidCredentialsError)
async def invalid_credentials_exception_handler(request: Request, exc: InvalidCredentialsError):
    return JSONResponse(
        status_code=status.HTTP_401_UNAUTHORIZED,
        content={"detail": "Invalid authentication credentials"},
    )

app.include_router(api_router, prefix="/api/v1")

@app.get("/")
async def root() -> dict[str, str]:
    """
    Root endpoint for basic connectivity check.
    """
    return {"message": "Server is running"}
