from __future__ import annotations
from typing import (Optional, Any, TypeVar, Generic, List)
from ..fable_library.reflection import (TypeInfo, class_type, string_type, option_type, record_type)
from ..fable_library.string import (to_console, printf)
from ..fable_library.types import (Exception, Record)
from ..fable_library.util import equals

_B = TypeVar("_B")

_S = TypeVar("_S")

def expr_74() -> TypeInfo:
    return class_type("FsHafas.Client.Log", None, Log)


class Log:
    pass

Log_reflection = expr_74

def Log__ctor() -> Log:
    return Log()


def expr_75() -> TypeInfo:
    return class_type("FsHafas.Client.HafasError", None, HafasError, class_type("System.Exception"))


class HafasError(Exception):
    def __init__(self, code: str, msg: str) -> None:
        super().__init__(msg)
        self.code_004027 = code
    

HafasError_reflection = expr_75

def HafasError__ctor_Z384F8060(code: str, msg: str) -> HafasError:
    return HafasError(code, msg)


def expr_76() -> TypeInfo:
    return record_type("FsHafas.Client.Icon", [], Icon, lambda: [("type", string_type), ("title", option_type(string_type))])


class Icon(Record):
    def __init__(self, type: str, title: Optional[str]) -> None:
        super().__init__()
        self.type = type
        self.title = title
    

Icon_reflection = expr_76

def Log__cctor(__unit: Any=None) -> None:
    Log.debug = False


Log__cctor()

def Log_get_Debug() -> bool:
    return Log.debug


def Log_set_Debug_Z1FBCCD16(v: bool) -> None:
    Log.debug = v


def Log_Print(msg: str, o: Any=None) -> None:
    if Log.debug:
        to_console(printf("%s %A"))(msg)(o)
    


def HafasError__get_code(e: HafasError) -> str:
    return e.code_004027


def HafasError__get_isHafasError(e: HafasError) -> bool:
    return True


def expr_77(gen0: TypeInfo, gen1: TypeInfo) -> TypeInfo:
    return class_type("FsHafas.Client.IndexMap`2", [gen0, gen1], IndexMap_2)


class IndexMap_2(Generic[_B, _S]):
    def __init__(self, default_value: Optional[_B]=None) -> None:
        self.default_value = default_value
        self.dict = dict()
    

IndexMap_2_reflection = expr_77

def IndexMap_2__ctor_2B594(default_value: Optional[_B]=None) -> IndexMap_2[_B]:
    return IndexMap_2(default_value)


def IndexMap_2__get_Item_2B595(__: IndexMap_2[_S, _B], s: _S) -> _B:
    v : _B = __.dict.get(s)
    if not equals(v, None):
        return v
    
    else: 
        return __.default_value
    


def IndexMap_2__set_Item_541DA560(__: IndexMap_2[_S, _B], s: Any=None, b: Any=None) -> None:
    __.dict[s]=b


def IndexMap_2__get_Keys(__: IndexMap_2[_S, _B]) -> List[_S]:
    return list(__.dict)


