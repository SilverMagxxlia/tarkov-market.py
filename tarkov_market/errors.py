from __future__ import annotations
from typing import Dict, List, Optional, TYPE_CHECKING, Any, Tuple, Union

if TYPE_CHECKING:
    from aiohttp import ClientResponse

    try:
        from requests import Response

        _ResponseType = Union[ClientResponse, Response]
    except ModuleNotFoundError:
        _ResponseType = ClientResponse


class TarkovMarketException(Exception):
    pass


class ClientException(TarkovMarketException):
    pass


class HTTPException(TarkovMarketException):

    def __init__(self, response: _ResponseType, message: Optional[Union[str, Dict[str, Any]]]):
        self.response: _ResponseType = response
        self.status: int = response.status
        self.text: str

        if isinstance(message, dict):
            error = message.get('error')

            if error:
                self.text = '{}: {}'.format(self.status, error)

            else:
                self.text = f'{self.status}'

        else:
            self.text = message or ''

        super().__init__(self.text)


class LoginFailure(TarkovMarketException):
    pass


class InvalidArgument(ClientException):
    pass


class NotFound(ClientException):
    pass
