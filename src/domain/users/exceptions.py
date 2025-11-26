class UserError(Exception):
    """Base exception for user-related errors."""
    pass


class UsernameAlreadyExistsError(UserError):
    """Raised when a username is already taken."""
    pass


class EmailAlreadyExistsError(UserError):
    """Raised when an email is already registered."""
    pass


class InvalidCredentialsError(UserError):
    """Raised on login when credentials do not match."""
    pass


class UserNotFoundError(UserError):
    """Raised when a user is not found in the repository."""
    pass
