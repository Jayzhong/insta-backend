from datetime import datetime
from uuid import UUID

from fastapi import APIRouter, Depends, File, Form, UploadFile, status
from pydantic import BaseModel, ConfigDict

from src.application.posts.use_cases.create_post import CreatePostRequest, CreatePostUseCase
from src.application.posts.use_cases.get_post import GetPostRequest, GetPostUseCase
from src.application.posts.use_cases.list_posts import ListPostsRequest, ListPostsUseCase
from src.domain.users.user import User as DomainUser
from src.interfaces.api.auth import get_current_user
from src.interfaces.api.dependencies import (
    get_create_post_use_case,
    get_get_post_use_case,
    get_list_posts_use_case,
)


class PostOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id: UUID
    user_id: UUID
    image_url: str
    caption: str | None
    created_at: datetime


posts_router = APIRouter(prefix="/posts", tags=["Posts"])


@posts_router.post("/", response_model=PostOut, status_code=status.HTTP_201_CREATED)
async def create_post(
    current_user: DomainUser = Depends(get_current_user),
    use_case: CreatePostUseCase = Depends(get_create_post_use_case),
    caption: str | None = Form(None),
    image: UploadFile = File(...),
):
    """
    Create a new post with an image and optional caption.
    """
    image_data = await image.read()
    request = CreatePostRequest(
        user_id=current_user.id,
        image_file_name=image.filename,
        image_file_data=image_data,
        caption=caption,
    )
    post = await use_case.execute(request)
    return post


@posts_router.get("/{post_id}", response_model=PostOut)
async def get_post(
    post_id: UUID,
    use_case: GetPostUseCase = Depends(get_get_post_use_case),
):
    """
    Get a specific post by its ID.
    """
    request = GetPostRequest(post_id=post_id)
    post = await use_case.execute(request)
    return post


@posts_router.get("/user/{user_id}", response_model=list[PostOut])
async def list_user_posts(
    user_id: UUID,
    use_case: ListPostsUseCase = Depends(get_list_posts_use_case),
):
    """
    List all posts belonging to a specific user.
    """
    request = ListPostsRequest(user_id=user_id)
    posts = await use_case.execute(request)
    return posts
