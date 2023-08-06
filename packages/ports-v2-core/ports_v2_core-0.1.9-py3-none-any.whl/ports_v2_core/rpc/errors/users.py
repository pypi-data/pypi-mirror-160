from fastapi_jsonrpc import BaseError


class FailedCreateUserError(BaseError):
    CODE = -3000
    MESSAGE = "Failed to create user."


class UserNotFoundError(BaseError):
    """
    Error that show that user was not found inside the UserService
    with the given credentials.
    """

    CODE = -3100
    MESSAGE = "No user was found with given credentials."
