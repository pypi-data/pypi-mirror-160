from typing import (MutableSequence, List, Callable)
from ...fable_library.reflection import (TypeInfo, string_type, float64_type, array_type, lambda_type, record_type)
from ...fable_library.types import Record

def expr_289() -> TypeInfo:
    return record_type("FsHafas.Extensions.PolylineEx.GooglePolyline", [], GooglePolyline, lambda: [("decode", lambda_type(string_type, array_type(array_type(float64_type))))])


class GooglePolyline(Record):
    def __init__(self, decode: Callable[[str], List[MutableSequence[float]]]=None) -> None:
        super().__init__()
        self.decode = decode
    

GooglePolyline_reflection = expr_289

