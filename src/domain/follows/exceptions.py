class FollowError(Exception):
    """Base exception for follow-related errors."""
    pass


class AlreadyFollowingError(FollowError):
    """Raised when a user tries to follow someone they already follow."""
    pass


class NotFollowingError(FollowError):
    """Raised when a user tries to unfollow someone they are not following."""
    pass


class SelfFollowError(FollowError):
    """Raised when a user tries to follow themselves."""
    pass
