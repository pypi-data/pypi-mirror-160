import os
import logging
from jsonrpcclient.responses import Response

from ports_v2_core.rpc.clients import BaseRpcClient
from ports_v2_core.rpc.errors import (
    CryptoServiceError,
    FailedToCreateHashError,
    HashNotMatchError,
)


logger = logging.getLogger(__name__)


class CryptoRpcClien(BaseRpcClient):
    url: str = os.environ.get("CRYPTO_RPC_URL")
    COMPARE_HASH = "compare_hash"
    CREATE_HASH = "create_hash"

    @classmethod
    def compare_hash(cls, plain_text: str, hashed: str) -> dict:
        """
        It compares the hash of the plain text with the hash provided.
        :param cls: The class that is calling the method
        :param plain_text: The plain text to be hashed
        :type plain_text: str
        :param hashed: The hash value to be compared
        :type hashed: str
        """
        params = {
            "plain_text": plain_text,
            "hashed": hashed,
        }
        response: Response = cls.send_request(cls, cls.COMPARE_HASH, params)
        if hasattr(response, "message"):
            logger.error(response.message)
            raise CryptoServiceError()
        if not response.result:
            raise HashNotMatchError()

    @classmethod
    def create_hash(cls, data: str):
        """
        It takes a string as input, and returns a hash of that string
        :param cls: The class that is calling the method
        :param data: The data to be hashed
        :type data: str
        :return: The hash of the data
        """
        params = {"data": data}
        response: Response = cls.send_request(cls, cls.CREATE_HASH, params)
        if hasattr(response, "message"):
            logger.error(response.message)
            raise FailedToCreateHashError()
        return response.result
