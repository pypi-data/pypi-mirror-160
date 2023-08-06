import logging
import requests
from typing import Union
from requests.exceptions import MissingSchema, ConnectionError
from jsonrpcclient import request, parse
from fastapi_jsonrpc import BaseError, BaseModel
from dotenv import load_dotenv

load_dotenv()


logger = logging.getLogger(__name__)


class RpcClientError(BaseError):
    CODE = -1111
    MESSAGE = "Service error."

    class DataModel(BaseModel):
        details: Union[str, dict]


# It sends a request to the service and parses the response
class BaseRpcClient:
    url: str

    def send_request(self, method, params):
        """
        It sends a request to the server, and if it fails, it logs the error and raises a ServiceError

        :param method: The method to call on the service
        :param params: a dictionary of parameters to be sent to the service
        """
        try:
            response = requests.post(self.url, json=request(method, params))
        except (MissingSchema, ConnectionError) as e:
            logger.error(e)
            raise RpcClientError(data={"details": str(e)})
        try:
            return parse(response.json())
        except (TypeError, KeyError):
            logger.error(response.json())
            raise RpcClientError(data={"details": response.json()})
