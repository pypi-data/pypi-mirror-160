from __future__ import annotations
from typing import (Any, Optional)
from ...fable_library.list import (FSharpList, last)
from ...fable_library.reg_exp import replace
from ...fable_library.string import (substring, to_console, printf)
from ...fable_simple_json_python.json_converter import Convert_fromJson
from ...fable_simple_json_python.simple_json import (SimpleJson_mapKeysByPath, SimpleJson_parseNative)
from ...fable_simple_json_python.type_info_converter import create_type_info
from ...fs_hafas_python.types_raw_hafas_client import (RawResponse_reflection, RawResponse)

def dashify(separator: str, input: str) -> str:
    def arrow_297(m: Any, separator: str=separator, input: str=input) -> str:
        return m[0].lower() if (len(m[0]) == 1) else ((substring(m[0], 0, 1) + separator) + substring(m[0], 1, 1).lower())
    
    return replace(input, "[a-z]?[A-Z]", arrow_297)


def to_dashed(xs: FSharpList[str]) -> Optional[str]:
    return dashify("_", last(xs))


def decode(input: str) -> RawResponse:
    try: 
        def arrow_298(xs: FSharpList[str]) -> Optional[str]:
            return to_dashed(xs)
        
        return Convert_fromJson(SimpleJson_mapKeysByPath(arrow_298, SimpleJson_parseNative(input)), create_type_info(RawResponse_reflection()))
    
    except Exception as e:
        arg10 : str = str(e)
        to_console(printf("error decode: %s"))(arg10)
        raise Exception(str(e))
    


