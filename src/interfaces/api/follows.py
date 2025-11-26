from uuid import UUID

from fastapi import APIRouter, Depends, status
from pydantic import BaseModel, ConfigDict

from src.application.follows.use_cases.follow_user import FollowUserRequest, FollowUserUseCase
from src.application.follows.use_cases.get_followers import GetFollowersRequest, GetFollowersUseCase
from src.application.follows.use_cases.get_following import GetFollowingRequest, GetFollowingUseCase
from src.application.follows.use_cases.unfollow_user import UnfollowUserRequest, UnfollowUserUseCase
from src.domain.users.user import User as DomainUser
from src.interfaces.api.auth import get_current_user
from src.interfaces.api.dependencies import (
    get_follow_user_use_case,
    get_get_followers_use_case,
    get_get_following_use_case,
    get_unfollow_user_use_case,
)
from src.interfaces.api.users import UserOut


follows_router = APIRouter(prefix="/users", tags=["Follows"])


@follows_router.post("/{user_id}/follow", status_code=status.HTTP_204_NO_CONTENT)
async def follow_user(
    user_id: UUID,
    current_user: DomainUser = Depends(get_current_user),
    use_case: FollowUserUseCase = Depends(get_follow_user_use_case),
):
    """
    Follow a user.
    """
    request = FollowUserRequest(
        follower_id=current_user.id,
        followed_id=user_id,
    )
    await use_case.execute(request)


@follows_router.delete("/{user_id}/follow", status_code=status.HTTP_204_NO_CONTENT)
async def unfollow_user(
    user_id: UUID,
    current_user: DomainUser = Depends(get_current_user),
    use_case: UnfollowUserUseCase = Depends(get_unfollow_user_use_case),
):
    """
    Unfollow a user.
    """
    request = UnfollowUserRequest(
        follower_id=current_user.id,
        followed_id=user_id,
    )
    await use_case.execute(request)


@follows_router.get("/{user_id}/followers", response_model=list[UserOut])
async def get_followers(
    user_id: UUID,
    use_case: GetFollowersUseCase = Depends(get_get_followers_use_case),
):
    """
    Get a list of users who follow the specified user.
    """
    request = GetFollowersRequest(user_id=user_id)
    followers = await use_case.execute(request)
    return followers


@follows_router.get("/{user_id}/following", response_model=list[UserOut])
async def get_following(
    user_id: UUID,
    use_case: GetFollowingUseCase = Depends(get_get_following_use_case),
):
    """
    Get a list of users that the specified user follows.
    """
    request = GetFollowingRequest(user_id=user_id)
    following = await use_case.execute(request)
    return following
