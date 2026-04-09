"""Application custom exceptions."""

class AppException(Exception):
    """Base application exception."""
    pass

class TaskNotFoundError(AppException):
    """Raised when task not found."""
    pass

class UserNotFoundError(AppException):
    """Raised when user not found."""
    pass

class CommentNotFoundError(AppException):
    """Raised when comment not found."""
    pass
