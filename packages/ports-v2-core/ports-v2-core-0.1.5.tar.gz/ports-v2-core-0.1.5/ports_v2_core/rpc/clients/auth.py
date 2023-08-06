import os
from jsonrpcclient.responses import Response
from ports_v2_core.rpc.errors import (
    AuthenticationError,
    AuthorizationError,
    MfaVerificationError,
)

from ports_v2_core.rpc.clients import BaseRpcClient
from ports_v2_core.schemas import (
    MfaVerifySchema,
    SecretsSchema,
    SessionSecretsSchema,
    UserLoginSchema,
)


class AuthRpcService(BaseRpcClient):
    url: str = os.environ.get("AUTH_RPC_URL")
    LOGIN_USER = "login_user"
    VERIFY_LOGIN = "verify_login"
    VERIFY_AUTHENTICATION = "verify_authentication"

    @classmethod
    def login_user(cls, data: UserLoginSchema) -> SecretsSchema:
        params = data.dict()
        response: Response = cls.send_request(cls, cls.LOGIN_USER, params)
        if hasattr(response, "message"):
            raise AuthorizationError()
        secrets = SecretsSchema(**response.result)
        return secrets

    @classmethod
    def login_verify(cls, data: MfaVerifySchema) -> SecretsSchema:
        params = data.dict()
        response: Response = cls.send_request(cls, cls.VERIFY_LOGIN, params)
        if hasattr(response, "message"):
            raise MfaVerificationError()
        secrets = SecretsSchema(**response.result)
        return secrets

    @classmethod
    def verify_authentication(cls, data: SessionSecretsSchema) -> SecretsSchema:
        params = data.dict()
        response: Response = cls.send_request(cls, cls.VERIFY_AUTHENTICATION, params)
        if hasattr(response, "message"):
            raise AuthenticationError()
        secrets = SecretsSchema(**response.result)
        return secrets
