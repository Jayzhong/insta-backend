class PostError(Exception):
    """Base exception for post-related errors."""
    pass


class PostNotFound(PostError):
    """Raised when a post is not found."""
    pass


class PostBelongsToAnotherUser(PostError):
    """Raised when a user tries to modify a post they do not own."""
    pass
