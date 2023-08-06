import typing

from requests import Response

from .exceptions import RequestError
from ..base import TgMethod, TgObject, BaseModel
from ..loader import BOT_TOKEN, session
from ..objects import InlineKeyboard, Keyboard, Translations
from ..utils import cast, clean_dict

METHOD_URL = f'https://api.telegram.org/bot{BOT_TOKEN}/{{method}}'
FILE_URL = f'https://api.telegram.org/file/bot{BOT_TOKEN}/{{file_path}}'

OK = 'ok'
RESULT = 'result'
ERROR_CODE = 'error_code'
DESCRIPTION = 'description'


def get_method_url(method: str):
    return METHOD_URL.format(method=method)


def get_file_url(file_path: str):
    return FILE_URL.format(file_path=file_path)


def parse_response(resp: Response, method: type[TgMethod]):
    result: dict = resp.json()

    if result[OK]:
        result = result[RESULT]
    else:
        raise RequestError(result[ERROR_CODE], result[DESCRIPTION])

    return cast(result, method.__response_type__)


def request(method: type[TgMethod], params: dict, **alternatives) -> TgObject | typing.Any:
    endpoint = get_method_url(method.__name__)
    params = params.copy()

    for key in alternatives:
        if params[key] is None:
            params[key] = alternatives[key]

    for key, value in params.items():
        if isinstance(value, Keyboard):
            params[key] = value.to_tg_object()
        if isinstance(value, InlineKeyboard):
            params[key] = value.to_tg_object()
        if isinstance(value, Translations):
            params[key] = value.get()

    for key, value in params.items():
        if isinstance(value, BaseModel):
            params[key] = cast(value, dict)

    params = clean_dict(params)
    resp = session.post(endpoint, json=params)
    return parse_response(resp, method)
