from fastapi_jsonrpc import BaseError


class AuthorizationError(BaseError):
    CODE = -4000
    MESSAGE = "Failed to authorize with given credentials."


class MfaVerificationError(BaseError):
    CODE = -4100
    MESSAGE = "Cannot verify given mfa credentials."


class AuthenticationError(BaseError):
    CODE = -4200
    MESSAGE = "Authentication failed for given secrets."
