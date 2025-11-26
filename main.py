from fastapi import FastAPI, Request, status
from fastapi.responses import JSONResponse
from src.interfaces.api.router import api_router
from src.domain.users.exceptions import InvalidCredentialsError, UserNotFoundError
from src.domain.posts.exceptions import PostNotFound
from src.domain.follows.exceptions import (
    AlreadyFollowingError,
    NotFollowingError,
    SelfFollowError,
)

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

@app.exception_handler(UserNotFoundError)
async def user_not_found_exception_handler(request: Request, exc: UserNotFoundError):
    return JSONResponse(
        status_code=status.HTTP_404_NOT_FOUND,
        content={"detail": "User not found"},
    )

@app.exception_handler(PostNotFound)
async def post_not_found_exception_handler(request: Request, exc: PostNotFound):
    return JSONResponse(
        status_code=status.HTTP_404_NOT_FOUND,
        content={"detail": "Post not found"},
    )

@app.exception_handler(AlreadyFollowingError)
async def already_following_exception_handler(request: Request, exc: AlreadyFollowingError):
    return JSONResponse(
        status_code=status.HTTP_400_BAD_REQUEST,
        content={"detail": "You are already following this user"},
    )

@app.exception_handler(NotFollowingError)
async def not_following_exception_handler(request: Request, exc: NotFollowingError):
    return JSONResponse(
        status_code=status.HTTP_400_BAD_REQUEST,
        content={"detail": "You are not following this user"},
    )

@app.exception_handler(SelfFollowError)
async def self_follow_exception_handler(request: Request, exc: SelfFollowError):
    return JSONResponse(
        status_code=status.HTTP_400_BAD_REQUEST,
        content={"detail": "You cannot follow yourself"},
    )

app.include_router(api_router, prefix="/api/v1")

@app.get("/")
async def root() -> dict[str, str]:
    """
    Root endpoint for basic connectivity check.
    """
    return {"message": "Server is running"}
