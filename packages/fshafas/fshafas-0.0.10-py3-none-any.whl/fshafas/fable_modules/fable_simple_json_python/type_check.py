from typing import (Any, Optional, List)
from ..fable_library.option import some

def _007CNativeString_007C__007C(x: Any=None) -> Optional[str]:
    if isinstance(x, str):
        return x
    
    else: 
        return None
    


def _007CNativeBool_007C__007C(x: Any=None) -> Optional[bool]:
    if isinstance(x, bool):
        return x
    
    else: 
        return None
    


def _007CNativeNumber_007C__007C(x: Any=None) -> Optional[float]:
    if isinstance(x, int) or isinstance(x, float):
        return x
    
    else: 
        return None
    


def _007CNativeObject_007C__007C(x: Any=None) -> Optional[Any]:
    if isinstance(x, dict):
        return some(x)
    
    else: 
        return None
    


def _007CNull_007C__007C(x: Any=None) -> Optional[Any]:
    if x is None:
        return some(x)
    
    else: 
        return None
    


def _007CNativeArray_007C__007C(x: Any=None) -> Optional[List[Any]]:
    if isinstance(x, list):
        return x
    
    else: 
        return None
    


