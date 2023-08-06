import os
import logging
from jsonrpcclient.responses import Response
from ports_v2_core.rpc.errors import FailedCreateUserError, UserNotFoundError

from ports_v2_core.rpc.clients import BaseRpcClient
from schemas.users import CreateUserSchema, UserSchema

logger = logging.getLogger(__name__)


class UserRpcClient(BaseRpcClient):
    url: str = os.environ.get("USER_RPC_URL")
    GET_BY_EMAIL = "get_user_by_email"
    GET_BY_ID = "get_user_by_id"
    CREATE_USER = "create_user"

    @classmethod
    def get_user_by_email(cls, email: str) -> UserSchema:
        params = {"email": email}
        response: Response = cls.send_request(cls, cls.GET_BY_EMAIL, params)
        if hasattr(response, "message"):
            raise UserNotFoundError()
        user = UserSchema(**response.result)
        return user

    @classmethod
    def get_user_by_id(cls, user_id: str) -> UserSchema:
        params = {"user_id": user_id}
        response: Response = cls.send_request(cls, cls.GET_BY_ID, params)

        if hasattr(response, "message"):
            raise UserNotFoundError()
        user = UserSchema(**response.result)
        return user

    @classmethod
    def create_new_user(cls, data: CreateUserSchema) -> UserSchema:
        params = data.dict()
        response: Response = cls.send_request(cls, cls.CREATE_USER, params)
        if hasattr(response, "message"):
            raise FailedCreateUserError()
        return UserSchema(**response.result)
