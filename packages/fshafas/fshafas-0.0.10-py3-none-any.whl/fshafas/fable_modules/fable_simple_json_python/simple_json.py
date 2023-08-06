from __future__ import annotations
import json as json_1
from typing import (Any, Tuple, Optional, List, TypeVar, Callable)
from ..fable_library.array import map as map_2
from ..fable_library.list import (map as map_1, of_array, FSharpList, concat, singleton, empty, is_empty, tail, head)
from ..fable_library.map import (to_list, of_list, try_find)
from ..fable_library.option import value as value_5
from ..fable_library.seq import (to_list as to_list_1, delay, map as map_3)
from ..fable_library.string import (to_text, printf, join)
from ..fable_library.types import to_string
from ..fable_library.util import (IEnumerable, compare_primitives, get_enumerator, partial_apply)
from .json_type import Json
from .type_check import (_007CNativeString_007C__007C, _007CNativeBool_007C__007C, _007CNativeNumber_007C__007C, _007CNull_007C__007C, _007CNativeArray_007C__007C, _007CNativeObject_007C__007C)

_A = TypeVar("_A")

def InteropUtil_isDateOffset(value: Any=None) -> bool:
    if isinstance(value, Date):
        return True
    
    else: 
        return False
    


def SimpleJson_toString(_arg1: Json) -> str:
    if _arg1.tag == 2:
        if _arg1.fields[0]:
            return "true"
        
        else: 
            return "false"
        
    
    elif _arg1.tag == 0:
        return to_string(_arg1.fields[0])
    
    elif _arg1.tag == 1:
        return to_text(printf("\"%s\""))(_arg1.fields[0])
    
    elif _arg1.tag == 4:
        def mapping(_arg1_1: Json, _arg1: Json=_arg1) -> str:
            return SimpleJson_toString(_arg1_1)
        
        arg10_1 : str = join(",", map_1(mapping, _arg1.fields[0]))
        return to_text(printf("[%s]"))(arg10_1)
    
    elif _arg1.tag == 5:
        def mapping_1(tupled_arg: Tuple[str, Json], _arg1: Json=_arg1) -> str:
            arg20 : str = SimpleJson_toString(tupled_arg[1])
            return to_text(printf("\"%s\":%s"))(tupled_arg[0])(arg20)
        
        arg10_3 : str = join(",", map_1(mapping_1, to_list(_arg1.fields[0])))
        return to_text(printf("{%s}"))(arg10_3)
    
    else: 
        return "null"
    


def SimpleJson_parseNative_0027(x: Any=None) -> Json:
    active_pattern_result618 : Optional[str] = _007CNativeString_007C__007C(x)
    if active_pattern_result618 is not None:
        str_1 : str = active_pattern_result618
        return Json(1, str_1)
    
    else: 
        active_pattern_result617 : Optional[bool] = _007CNativeBool_007C__007C(x)
        if active_pattern_result617 is not None:
            value : bool = active_pattern_result617
            return Json(2, value)
        
        else: 
            active_pattern_result616 : Optional[float] = _007CNativeNumber_007C__007C(x)
            if active_pattern_result616 is not None:
                number : float = active_pattern_result616
                return Json(0, number)
            
            elif _007CNull_007C__007C(x) is not None:
                return Json(3)
            
            else: 
                active_pattern_result614 : Optional[List[Any]] = _007CNativeArray_007C__007C(x)
                if active_pattern_result614 is not None:
                    arr : List[Any] = active_pattern_result614
                    def arrow_4(x_1: Any=None, x: Any=x) -> Json:
                        return SimpleJson_parseNative_0027(x_1)
                    
                    return Json(4, of_array(map_2(arrow_4, arr, None)))
                
                else: 
                    active_pattern_result613 : Optional[Any] = _007CNativeObject_007C__007C(x)
                    if active_pattern_result613 is not None:
                        object : Any = value_5(active_pattern_result613)
                        def arrow_6(x: Any=x) -> IEnumerable[Tuple[str, Json]]:
                            def arrow_5(key: str) -> Tuple[str, Json]:
                                return (key, SimpleJson_parseNative_0027(object[key]))
                            
                            return map_3(arrow_5, object.keys())
                        
                        class ObjectExpr10:
                            @property
                            def Compare(self) -> Any:
                                def arrow_9(x_2: str, y: str) -> int:
                                    return compare_primitives(x_2, y)
                                
                                return arrow_9
                            
                        return Json(5, of_list(to_list_1(delay(arrow_6)), ObjectExpr10()))
                    
                    else: 
                        return Json(3)
                    
                
            
        
    


def SimpleJson_parseNative(input: str) -> Json:
    return SimpleJson_parseNative_0027(json_1.loads(input))


def SimpleJson_tryParseNative(input: str) -> Optional[Json]:
    try: 
        return SimpleJson_parseNative(input)
    
    except Exception as ex:
        return None
    


def SimpleJson_fromObjectLiteral(x: Optional[_A]=None) -> Optional[Json]:
    try: 
        return SimpleJson_parseNative_0027(x)
    
    except Exception as match_value:
        return None
    


def SimpleJson_mapKeys(f: Callable[[str], str], _arg1: Json) -> Json:
    if _arg1.tag == 5:
        def mapping(tupled_arg: Tuple[str, Json], f: Callable[[str], str]=f, _arg1: Json=_arg1) -> Tuple[str, Json]:
            return (f(tupled_arg[0]), SimpleJson_mapKeys(f, tupled_arg[1]))
        
        class ObjectExpr49:
            @property
            def Compare(self) -> Any:
                def arrow_48(x: str, y: str) -> int:
                    return compare_primitives(x, y)
                
                return arrow_48
            
        return Json(5, of_list(map_1(mapping, to_list(_arg1.fields[0])), ObjectExpr49()))
    
    elif _arg1.tag == 4:
        def mapping_1(_arg1_1: Json, f: Callable[[str], str]=f, _arg1: Json=_arg1) -> Json:
            return SimpleJson_mapKeys(f, _arg1_1)
        
        return Json(4, map_1(mapping_1, _arg1.fields[0]))
    
    else: 
        return _arg1
    


def SimpleJson_toPlainObject(input: Json) -> Any:
    if input.tag == 2:
        return input.fields[0]
    
    elif input.tag == 0:
        return input.fields[0]
    
    elif input.tag == 1:
        return input.fields[0]
    
    elif input.tag == 4:
        array : List[Any] = []
        with get_enumerator(input.fields[0]) as enumerator:
            while enumerator.System_Collections_IEnumerator_MoveNext():
                value_3 : Json = enumerator.System_Collections_Generic_IEnumerator_00601_get_Current()
                (array.append(SimpleJson_toPlainObject(value_3)))
        return array
    
    elif input.tag == 5:
        js_object : Any = {}
        with get_enumerator(to_list(input.fields[0])) as enumerator_1:
            while enumerator_1.System_Collections_IEnumerator_MoveNext():
                for_loop_var : Tuple[str, Json] = enumerator_1.System_Collections_Generic_IEnumerator_00601_get_Current()
                js_object[for_loop_var[0]] = SimpleJson_toPlainObject(for_loop_var[1])
        return js_object
    
    else: 
        return None
    


def SimpleJson_mapbyKey(f: Callable[[str, Json], Json], _arg1: Json) -> Json:
    if _arg1.tag == 5:
        def mapping(tupled_arg: Tuple[str, Json], f: Callable[[str, Json], Json]=f, _arg1: Json=_arg1) -> Tuple[str, Json]:
            key : str = tupled_arg[0]
            return (key, f(key, tupled_arg[1]))
        
        class ObjectExpr71:
            @property
            def Compare(self) -> Any:
                def arrow_70(x: str, y: str) -> int:
                    return compare_primitives(x, y)
                
                return arrow_70
            
        return Json(5, of_list(map_1(mapping, to_list(_arg1.fields[0])), ObjectExpr71()))
    
    elif _arg1.tag == 4:
        def mapping_1(_arg1_1: Json, f: Callable[[str, Json], Json]=f, _arg1: Json=_arg1) -> Json:
            return SimpleJson_mapbyKey(f, _arg1_1)
        
        return Json(4, map_1(mapping_1, _arg1.fields[0]))
    
    else: 
        return _arg1
    


def SimpleJson_mapKeysByPath(f: Callable[[FSharpList[str]], Optional[str]], json: Json) -> Json:
    def map_key(xs: FSharpList[str], _arg1: Json, f: Callable[[FSharpList[str]], Optional[str]]=f, json: Json=json) -> Json:
        if _arg1.tag == 5:
            def mapping(tupled_arg: Tuple[str, Json], xs: FSharpList[str]=xs, _arg1: Json=_arg1) -> Tuple[str, Json]:
                key : str = tupled_arg[0]
                value : Json = tupled_arg[1]
                key_path : FSharpList[str] = concat([xs, singleton(key)])
                match_value : Optional[str] = f(key_path)
                if match_value is None:
                    return (key, map_key(key_path, value))
                
                else: 
                    return (match_value, map_key(key_path, value))
                
            
            class ObjectExpr73:
                @property
                def Compare(self) -> Any:
                    def arrow_72(x: str, y: str) -> int:
                        return compare_primitives(x, y)
                    
                    return arrow_72
                
            return Json(5, of_list(map_1(mapping, to_list(_arg1.fields[0])), ObjectExpr73()))
        
        elif _arg1.tag == 4:
            return Json(4, map_1(partial_apply(1, map_key, [xs]), _arg1.fields[0]))
        
        else: 
            return _arg1
        
    
    return map_key(empty(), json)


def SimpleJson_readPath(keys_mut: FSharpList[str], input_mut: Json) -> Optional[Json]:
    while True:
        (keys, input) = (keys_mut, input_mut)
        match_value : Tuple[FSharpList[str], Json] = (keys, input)
        (pattern_matching_result, dict_1, key, dict_2, first_key, rest) = (None, None, None, None, None, None)
        if not is_empty(match_value[0]):
            if is_empty(tail(match_value[0])):
                if match_value[1].tag == 5:
                    pattern_matching_result = 1
                    dict_1 = match_value[1].fields[0]
                    key = head(match_value[0])
                
                else: 
                    pattern_matching_result = 3
                
            
            elif match_value[1].tag == 5:
                pattern_matching_result = 2
                dict_2 = match_value[1].fields[0]
                first_key = head(match_value[0])
                rest = tail(match_value[0])
            
            else: 
                pattern_matching_result = 3
            
        
        else: 
            pattern_matching_result = 0
        
        if pattern_matching_result == 0:
            return None
        
        elif pattern_matching_result == 1:
            return try_find(key, dict_1)
        
        elif pattern_matching_result == 2:
            match_value_1 : Optional[Json] = try_find(first_key, dict_2)
            (pattern_matching_result_1, next_dict) = (None, None)
            if match_value_1 is not None:
                if match_value_1.tag == 5:
                    pattern_matching_result_1 = 0
                    next_dict = match_value_1.fields[0]
                
                else: 
                    pattern_matching_result_1 = 1
                
            
            else: 
                pattern_matching_result_1 = 1
            
            if pattern_matching_result_1 == 0:
                keys_mut = rest
                input_mut = Json(5, next_dict)
                continue
            
            elif pattern_matching_result_1 == 1:
                return None
            
        
        elif pattern_matching_result == 3:
            return None
        
        break


