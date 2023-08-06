from fastapi_jsonrpc import BaseError


class CryptoServiceError(BaseError):
    CODE = -5000
    MESSAGE = "Error occured running CryptoService."


class FailedToCreateHashError(BaseError):
    CODE = -5100
    MESSAGE = "Failed to create hash for given instance."


class HashNotMatchError(BaseError):
    CODE = -5200
    MESSAGE = "Hashes do not match."
