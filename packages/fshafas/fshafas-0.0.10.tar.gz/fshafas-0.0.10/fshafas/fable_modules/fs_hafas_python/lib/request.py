from __future__ import annotations
from hashlib import md5
from json import dumps
from requests import post
from typing import (Any, TypeVar)
from ...fable_library.async_builder import (singleton, Async)
from ...fable_library.map_util import add_to_dict
from ...fable_library.reflection import (TypeInfo, class_type)
from ...fs_hafas_python.extra_types import Log_Print

_A_ = TypeVar("_A_")

def expr_310() -> TypeInfo:
    return class_type("FsHafas.Client.Request.HttpClient", None, HttpClient)


class HttpClient:
    pass

HttpClient_reflection = expr_310

def HttpClient__ctor() -> HttpClient:
    return HttpClient()


def HttpClient__Dispose(__: HttpClient) -> None:
    pass


def HttpClient__PostAsync(__: HttpClient, url: str, salt: str, json: str) -> Async[str]:
    url_escaped : str = ((url + "?checksum=") + HttpClient__getMd5(__, json, salt)) if (len(salt) > 0) else url
    HttpClient__log(__, "url: ", url_escaped)
    headers : Any = dict([])
    add_to_dict(headers, "Content-Type", "application/json; charset=utf-8")
    add_to_dict(headers, "Accept-Encoding", "gzip, br, deflate")
    add_to_dict(headers, "Accept", "application/json")
    add_to_dict(headers, "User-Agent", "agent")
    def arrow_311(__: HttpClient=__, url: str=url, salt: str=salt, json: str=json) -> Async[str]:
        r : Any = post(url_escaped, data=json.encode('utf-8'), headers=headers)
        if (r.status_code) == 200:
            return singleton.Return(dumps(r.json()))
        
        else: 
            HttpClient__log(__, "statusCode: ", r.status_code)
            HttpClient__log(__, "text: ", r.text)
            return singleton.Return("")
        
    
    return singleton.Delay(arrow_311)


def HttpClient__log(this: HttpClient, msg: str, o: _A_) -> None:
    Log_Print(msg, o)


def HttpClient__getMd5(this: HttpClient, json: str, salt: str) -> str:
    return md5((json + salt).encode()).hexdigest()


