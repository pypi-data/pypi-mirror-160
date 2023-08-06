from typing import Any
from ...fable_library.string import (to_text, printf)

def format_date(dt: Any, pattern: str) -> str:
    if "yyyyMMdd" == pattern:
        arg30 : int = (dt.day) or 0
        arg20 : int = (dt.month) or 0
        arg10 : int = (dt.year) or 0
        return to_text(printf("%04d%02d%02d"))(arg10)(arg20)(arg30)
    
    else: 
        raise Exception("nyi")
    


def format_time(dt: Any, pattern: str) -> str:
    if "HHmm" == pattern:
        arg20 : int = (dt.minute) or 0
        arg10 : int = (dt.hour) or 0
        return to_text(printf("%02d%02d"))(arg10)(arg20)
    
    else: 
        raise Exception("nyi")
    


