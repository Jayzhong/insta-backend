from uuid import UUID

from fastapi import APIRouter, Depends, File, Form, UploadFile
from pydantic import BaseModel, ConfigDict, EmailStr

from src.application.users.login_user import (
    LoginUserRequest,
    LoginUserResponse,
    LoginUserUseCase,
)
from src.application.users.register_user import (
    RegisterUserRequest,
    RegisterUserUseCase,
)
from src.application.users.update_user_profile import (
    UpdateUserProfileRequest,
    UpdateUserProfileUseCase,
)
from src.domain.users.user import User as DomainUser
from src.interfaces.api.auth import get_current_user
from src.interfaces.api.dependencies import (
    get_login_user_use_case,
    get_register_user_use_case,
    get_update_user_profile_use_case,
)

# --- Pydantic Schemas ---

class UserRegisterIn(BaseModel):
    username: str
    email: EmailStr
    password: str


class UserOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id: UUID
    username: str
    email: EmailStr
    nickname: str | None
    avatar_url: str | None
    bio: str | None
    is_public: bool


class UserLoginIn(BaseModel):
    email: EmailStr
    password: str


class TokenOut(BaseModel):
    access_token: str
    token_type: str = "bearer"


# --- API Router ---

users_router = APIRouter(prefix="/users", tags=["Users"])


@users_router.post("/register", response_model=UserOut, status_code=201)
async def register_user(
    schema: UserRegisterIn,
    use_case: RegisterUserUseCase = Depends(get_register_user_use_case),
):
    request_dto = RegisterUserRequest(
        username=schema.username, email=schema.email, password=schema.password
    )
    user = await use_case.execute(request_dto)
    return user


@users_router.post("/login", response_model=TokenOut)
async def login_for_access_token(
    schema: UserLoginIn,
    use_case: LoginUserUseCase = Depends(get_login_user_use_case),
):
    request_dto = LoginUserRequest(email=schema.email, password=schema.password)
    login_response: LoginUserResponse = await use_case.execute(request_dto)
    return login_response


@users_router.patch("/profile", response_model=UserOut)
async def update_user_profile(
    current_user: DomainUser = Depends(get_current_user),
    use_case: UpdateUserProfileUseCase = Depends(get_update_user_profile_use_case),
    nickname: str | None = Form(None),
    bio: str | None = Form(None),
    is_public: bool | None = Form(None),
    delete_avatar: bool = Form(False),
    avatar: UploadFile | None = File(None),
):
    avatar_data = await avatar.read() if avatar else None
    avatar_filename = avatar.filename if avatar else None

    request_dto = UpdateUserProfileRequest(
        user_id=current_user.id,
        nickname=nickname,
        bio=bio,
        is_public=is_public,
        should_delete_avatar=delete_avatar,
        avatar_file_data=avatar_data,
        avatar_file_name=avatar_filename,
    )
    user = await use_case.execute(request_dto)
    return user
