from __future__ import annotations
import math
import base64
import json as json_1
from typing import (Any, List, Tuple, Optional, Callable, TypeVar)
from ..fable_library.array import (try_find as try_find_1, map as map_2, zip, equals_with, map_indexed, concat, find as find_1)
from ..fable_library.big_int import (parse as parse_3, from_int32)
from ..fable_library.bit_converter import (to_int64, get_bytes_int32)
from ..fable_library.choice import FSharpResult_2
from ..fable_library.date import (parse as parse_4, to_string as to_string_2)
from ..fable_library.date_offset import (parse as parse_5, datetime)
from ..fable_library.decimal import (Decimal, to_string as to_string_1)
from ..fable_library.double import parse
from ..fable_library.guid import parse as parse_6
from ..fable_library.int32 import (parse as parse_1, try_parse)
from ..fable_library.list import (singleton, empty, FSharpList, is_empty, head, tail as tail_1, length, to_array, try_find as try_find_2, of_array, choose, map as map_3)
from ..fable_library.long import (from_number, parse as parse_2, from_int, try_parse as try_parse_1, to_number, from_integer)
from ..fable_library.map import (remove, try_find, to_list as to_list_1, contains_key, count, find, of_list as of_list_1, is_empty as is_empty_1, to_array as to_array_2)
from ..fable_library.map_util import (add_to_dict, add_to_set)
from ..fable_library.mutable_map import Dictionary
from ..fable_library.mutable_set import HashSet
from ..fable_library.option import (map as map_1, some, value as value_86)
from ..fable_library.reflection import (TypeInfo, string_type, union_type as union_type_4, name as name_2, make_union, full_name, make_record, get_record_field, get_union_fields)
from ..fable_library.seq import (to_list, delay, append, singleton as singleton_1, empty as empty_1, for_all, try_find as try_find_3, collect, map as map_4, to_array as to_array_1)
from ..fable_library.set import of_list
from ..fable_library.string import (ends_with, substring, to_fail, printf, join, to_text)
from ..fable_library.types import (Union, to_string, FSharpRef, Uint8Array)
from ..fable_library.uri import Uri
from ..fable_library.util import (IEnumerable, equals, IComparable, compare, compare_primitives, safe_hash, structural_hash, get_enumerator, ignore, int32_to_string, int64_to_string)
from .json_type import (Json_reflection, Json)
from .simple_json import (SimpleJson_toPlainObject, SimpleJson_toString, SimpleJson_parseNative)
from .type_info import (TypeInfo as TypeInfo_1, UnionCase, RecordField)
from .type_info_converter import (is_primitive, enum_union)

_T = TypeVar("_T")

Convert_insideBrowser : bool = False

Convert_isUsingFable3 : bool = True

Convert_insideWorker : bool = False

def expr_78() -> TypeInfo:
    return union_type_4("Fable.SimpleJson.Python.Convert.InternalMap", [], Convert_InternalMap, lambda: [[], [("Item1", string_type), ("Item2", Json_reflection())], [("Item1", string_type), ("Item2", Json_reflection()), ("Item3", Convert_InternalMap_reflection()), ("Item4", Convert_InternalMap_reflection())]])


class Convert_InternalMap(Union):
    def __init__(self, tag: int, *fields: Any) -> None:
        super().__init__()
        self.tag : int = tag or 0
        self.fields : List[Any] = list(fields)
    
    @staticmethod
    def cases() -> List[str]:
        return ["MapEmpty", "MapOne", "MapNode"]
    

Convert_InternalMap_reflection = expr_78

def Convert_flattenMap(_arg1: Convert_InternalMap) -> FSharpList[Tuple[str, Json]]:
    if _arg1.tag == 1:
        return singleton((_arg1.fields[0], _arg1.fields[1]))
    
    elif _arg1.tag == 2:
        def arrow_81(_arg1: Convert_InternalMap=_arg1) -> IEnumerable[Tuple[str, Json]]:
            def arrow_80(__unit: Any=None) -> IEnumerable[Tuple[str, Json]]:
                def arrow_79(__unit: Any=None) -> IEnumerable[Tuple[str, Json]]:
                    return singleton_1((_arg1.fields[0], _arg1.fields[1]))
                
                return append(Convert_flattenMap(_arg1.fields[3]), delay(arrow_79))
            
            return append(Convert_flattenMap(_arg1.fields[2]), delay(arrow_80))
        
        return to_list(delay(arrow_81))
    
    else: 
        return empty()
    


def Convert__007CKeyValue_007C__007C(key: str, map: Any) -> Optional[Tuple[str, Json, Any]]:
    def mapping(value: Json, key: str=key, map: Any=map) -> Tuple[str, Json, Any]:
        return (key, value, remove(key, map))
    
    return map_1(mapping, try_find(key, map))


def Convert__007CNonArray_007C__007C(_arg1: Json) -> Optional[Json]:
    if _arg1.tag == 4:
        return None
    
    else: 
        return _arg1
    


def Convert__007CMapEmpty_007C__007C(json: Json) -> Optional[Json]:
    (pattern_matching_result,) = (None,)
    if json.tag == 1:
        if json.fields[0] == "MapEmpty":
            pattern_matching_result = 0
        
        else: 
            pattern_matching_result = 1
        
    
    else: 
        pattern_matching_result = 1
    
    if pattern_matching_result == 0:
        return json
    
    elif pattern_matching_result == 1:
        return None
    


def Convert__007CMapKey_007C__007C(_arg1: Json) -> Optional[str]:
    if _arg1.tag == 0:
        return to_string(_arg1.fields[0])
    
    elif _arg1.tag == 1:
        return _arg1.fields[0]
    
    else: 
        return None
    


def Convert__007CMapOne_007C__007C(_arg1: Json) -> Optional[Tuple[str, Json]]:
    (pattern_matching_result, key, value) = (None, None, None)
    if _arg1.tag == 4:
        if not is_empty(_arg1.fields[0]):
            if head(_arg1.fields[0]).tag == 1:
                if head(_arg1.fields[0]).fields[0] == "MapOne":
                    if not is_empty(tail_1(_arg1.fields[0])):
                        active_pattern_result808 : Optional[str] = Convert__007CMapKey_007C__007C(head(tail_1(_arg1.fields[0])))
                        if active_pattern_result808 is not None:
                            if not is_empty(tail_1(tail_1(_arg1.fields[0]))):
                                if is_empty(tail_1(tail_1(tail_1(_arg1.fields[0])))):
                                    pattern_matching_result = 0
                                    key = active_pattern_result808
                                    value = head(tail_1(tail_1(_arg1.fields[0])))
                                
                                else: 
                                    pattern_matching_result = 1
                                
                            
                            else: 
                                pattern_matching_result = 1
                            
                        
                        else: 
                            pattern_matching_result = 1
                        
                    
                    else: 
                        pattern_matching_result = 1
                    
                
                else: 
                    pattern_matching_result = 1
                
            
            else: 
                pattern_matching_result = 1
            
        
        else: 
            pattern_matching_result = 1
        
    
    else: 
        pattern_matching_result = 1
    
    if pattern_matching_result == 0:
        return (key, value)
    
    elif pattern_matching_result == 1:
        return None
    


def Convert__007CMapNode_007C__007C(_arg1: Json) -> Optional[Tuple[str, Json, Json, Json]]:
    (pattern_matching_result, key, left, right, value) = (None, None, None, None, None)
    if _arg1.tag == 4:
        if not is_empty(_arg1.fields[0]):
            if head(_arg1.fields[0]).tag == 1:
                if head(_arg1.fields[0]).fields[0] == "MapNode":
                    if not is_empty(tail_1(_arg1.fields[0])):
                        active_pattern_result810 : Optional[str] = Convert__007CMapKey_007C__007C(head(tail_1(_arg1.fields[0])))
                        if active_pattern_result810 is not None:
                            if not is_empty(tail_1(tail_1(_arg1.fields[0]))):
                                if not is_empty(tail_1(tail_1(tail_1(_arg1.fields[0])))):
                                    if not is_empty(tail_1(tail_1(tail_1(tail_1(_arg1.fields[0]))))):
                                        if not is_empty(tail_1(tail_1(tail_1(tail_1(tail_1(_arg1.fields[0])))))):
                                            if head(tail_1(tail_1(tail_1(tail_1(tail_1(_arg1.fields[0])))))).tag == 0:
                                                if is_empty(tail_1(tail_1(tail_1(tail_1(tail_1(tail_1(_arg1.fields[0]))))))):
                                                    pattern_matching_result = 0
                                                    key = active_pattern_result810
                                                    left = head(tail_1(tail_1(tail_1(_arg1.fields[0]))))
                                                    right = head(tail_1(tail_1(tail_1(tail_1(_arg1.fields[0])))))
                                                    value = head(tail_1(tail_1(_arg1.fields[0])))
                                                
                                                else: 
                                                    pattern_matching_result = 1
                                                
                                            
                                            else: 
                                                pattern_matching_result = 1
                                            
                                        
                                        else: 
                                            pattern_matching_result = 1
                                        
                                    
                                    else: 
                                        pattern_matching_result = 1
                                    
                                
                                else: 
                                    pattern_matching_result = 1
                                
                            
                            else: 
                                pattern_matching_result = 1
                            
                        
                        else: 
                            pattern_matching_result = 1
                        
                    
                    else: 
                        pattern_matching_result = 1
                    
                
                else: 
                    pattern_matching_result = 1
                
            
            else: 
                pattern_matching_result = 1
            
        
        else: 
            pattern_matching_result = 1
        
    
    else: 
        pattern_matching_result = 1
    
    if pattern_matching_result == 0:
        return (key, value, left, right)
    
    elif pattern_matching_result == 1:
        return None
    


def Convert_generateMap(json: Json) -> Optional[Convert_InternalMap]:
    if Convert__007CMapEmpty_007C__007C(json) is not None:
        return Convert_InternalMap(0)
    
    else: 
        active_pattern_result813 : Optional[Tuple[str, Json]] = Convert__007CMapOne_007C__007C(json)
        if active_pattern_result813 is not None:
            key : str = active_pattern_result813[0]
            value : Json = active_pattern_result813[1]
            return Convert_InternalMap(1, key, value)
        
        else: 
            active_pattern_result812 : Optional[Tuple[str, Json, Json, Json]] = Convert__007CMapNode_007C__007C(json)
            if active_pattern_result812 is not None:
                key_1 : str = active_pattern_result812[0]
                left : Json = active_pattern_result812[2]
                right : Json = active_pattern_result812[3]
                value_1 : Json = active_pattern_result812[1]
                match_value : Tuple[Optional[Convert_InternalMap], Optional[Convert_InternalMap]] = (Convert_generateMap(left), Convert_generateMap(right))
                (pattern_matching_result, left_map, right_map) = (None, None, None)
                if match_value[0] is not None:
                    if match_value[1] is not None:
                        pattern_matching_result = 0
                        left_map = match_value[0]
                        right_map = match_value[1]
                    
                    else: 
                        pattern_matching_result = 1
                    
                
                else: 
                    pattern_matching_result = 1
                
                if pattern_matching_result == 0:
                    return Convert_InternalMap(2, key_1, value_1, left_map, right_map)
                
                elif pattern_matching_result == 1:
                    return None
                
            
            else: 
                return None
            
        
    


def Convert_flatteFable3Map(tree: Any) -> FSharpList[Tuple[str, Json]]:
    def arrow_86(tree: Any=tree) -> IEnumerable[Tuple[str, Json]]:
        def arrow_82(__unit: Any=None) -> IEnumerable[Tuple[str, Json]]:
            match_value : Tuple[Optional[Json], Optional[Json]] = (try_find("k", tree), try_find("v", tree))
            (pattern_matching_result, key, value) = (None, None, None)
            if match_value[0] is not None:
                if match_value[0].tag == 1:
                    if match_value[1] is not None:
                        pattern_matching_result = 0
                        key = match_value[0].fields[0]
                        value = match_value[1]
                    
                    else: 
                        pattern_matching_result = 1
                    
                
                else: 
                    pattern_matching_result = 1
                
            
            else: 
                pattern_matching_result = 1
            
            if pattern_matching_result == 0:
                return singleton_1((key, value))
            
            elif pattern_matching_result == 1:
                return empty_1()
            
        
        def arrow_85(__unit: Any=None) -> IEnumerable[Tuple[str, Json]]:
            def arrow_83(__unit: Any=None) -> IEnumerable[Tuple[str, Json]]:
                match_value_1 : Optional[Json] = try_find("left", tree)
                (pattern_matching_result_1, left) = (None, None)
                if match_value_1 is not None:
                    if match_value_1.tag == 5:
                        pattern_matching_result_1 = 0
                        left = match_value_1.fields[0]
                    
                    else: 
                        pattern_matching_result_1 = 1
                    
                
                else: 
                    pattern_matching_result_1 = 1
                
                if pattern_matching_result_1 == 0:
                    return Convert_flatteFable3Map(left)
                
                elif pattern_matching_result_1 == 1:
                    return empty_1()
                
            
            def arrow_84(__unit: Any=None) -> IEnumerable[Tuple[str, Json]]:
                match_value_2 : Optional[Json] = try_find("right", tree)
                (pattern_matching_result_2, right) = (None, None)
                if match_value_2 is not None:
                    if match_value_2.tag == 5:
                        pattern_matching_result_2 = 0
                        right = match_value_2.fields[0]
                    
                    else: 
                        pattern_matching_result_2 = 1
                    
                
                else: 
                    pattern_matching_result_2 = 1
                
                if pattern_matching_result_2 == 0:
                    return Convert_flatteFable3Map(right)
                
                elif pattern_matching_result_2 == 1:
                    return empty_1()
                
            
            return append(arrow_83(), delay(arrow_84))
        
        return append(arrow_82(), delay(arrow_85))
    
    return to_list(delay(arrow_86))


def Convert_flattenFable3Lists(linked_list: Any) -> FSharpList[Json]:
    def arrow_89(linked_list: Any=linked_list) -> IEnumerable[Json]:
        def arrow_87(__unit: Any=None) -> IEnumerable[Json]:
            match_value : Optional[Json] = try_find("head", linked_list)
            if match_value is None:
                return empty_1()
            
            else: 
                return singleton_1(match_value)
            
        
        def arrow_88(__unit: Any=None) -> IEnumerable[Json]:
            match_value_1 : Optional[Json] = try_find("tail", linked_list)
            (pattern_matching_result, tail) = (None, None)
            if match_value_1 is not None:
                if match_value_1.tag == 5:
                    pattern_matching_result = 0
                    tail = match_value_1.fields[0]
                
                else: 
                    pattern_matching_result = 1
                
            
            else: 
                pattern_matching_result = 1
            
            if pattern_matching_result == 0:
                return Convert_flattenFable3Lists(tail)
            
            elif pattern_matching_result == 1:
                return empty_1()
            
        
        return append(arrow_87(), delay(arrow_88))
    
    return to_list(delay(arrow_89))


def Convert_arrayLike(_arg1: TypeInfo_1) -> bool:
    if _arg1.tag == 28:
        return True
    
    elif _arg1.tag == 26:
        return True
    
    elif _arg1.tag == 29:
        return True
    
    elif _arg1.tag == 30:
        return True
    
    elif _arg1.tag == 27:
        return True
    
    elif _arg1.tag == 33:
        return True
    
    elif _arg1.tag == 34:
        return True
    
    else: 
        return False
    


def Convert_isRecord(_arg1: TypeInfo_1) -> bool:
    if _arg1.tag == 37:
        return True
    
    else: 
        return False
    


def Convert_unionOfRecords(_arg1: TypeInfo_1) -> bool:
    if _arg1.tag == 38:
        def predicate(case: UnionCase, _arg1: TypeInfo_1=_arg1) -> bool:
            if len(case.CaseTypes) == 1:
                return Convert_isRecord(case.CaseTypes[0])
            
            else: 
                return False
            
        
        return for_all(predicate, _arg1.fields[0]()[0])
    
    else: 
        return False
    


def Convert_optional(_arg1: TypeInfo_1) -> bool:
    if _arg1.tag == 25:
        return True
    
    else: 
        return False
    


def Convert_isQuoted(input: str) -> bool:
    if input.find("\"") == 0:
        return ends_with(input, "\"")
    
    else: 
        return False
    


def Convert_betweenQuotes(input: str) -> str:
    return ("\"" + input) + "\""


def Convert_removeQuotes(input: str) -> str:
    return substring(input, 1, len(input) - 2)


def Convert_fromJsonAs(input_mut: Json, type_info_mut: TypeInfo_1) -> Any:
    while True:
        (input, type_info) = (input_mut, type_info_mut)
        match_value : Tuple[Json, TypeInfo_1] = (input, type_info)
        (pattern_matching_result, value_1) = (None, None)
        if match_value[0].tag == 0:
            if match_value[1].tag == 9:
                pattern_matching_result = 0
                value_1 = match_value[0].fields[0]
            
            else: 
                pattern_matching_result = 2
            
        
        elif match_value[0].tag == 1:
            if match_value[1].tag == 9:
                if match_value[0].fields[0].lower() == "nan":
                    pattern_matching_result = 1
                
                else: 
                    pattern_matching_result = 2
                
            
            else: 
                pattern_matching_result = 2
            
        
        else: 
            pattern_matching_result = 2
        
        if pattern_matching_result == 0:
            return value_1
        
        elif pattern_matching_result == 1:
            return NaN
        
        elif pattern_matching_result == 2:
            (pattern_matching_result_1, value_4, value_5) = (None, None, None)
            if match_value[0].tag == 1:
                if match_value[1].tag == 9:
                    pattern_matching_result_1 = 0
                    value_4 = match_value[0].fields[0]
                
                elif match_value[1].tag == 8:
                    if match_value[0].fields[0].lower() == "nan":
                        pattern_matching_result_1 = 2
                    
                    else: 
                        pattern_matching_result_1 = 3
                    
                
                else: 
                    pattern_matching_result_1 = 3
                
            
            elif match_value[0].tag == 0:
                if match_value[1].tag == 8:
                    pattern_matching_result_1 = 1
                    value_5 = match_value[0].fields[0]
                
                else: 
                    pattern_matching_result_1 = 3
                
            
            else: 
                pattern_matching_result_1 = 3
            
            if pattern_matching_result_1 == 0:
                return parse(value_4)
            
            elif pattern_matching_result_1 == 1:
                return value_5
            
            elif pattern_matching_result_1 == 2:
                return NaN
            
            elif pattern_matching_result_1 == 3:
                (pattern_matching_result_2, value_7, value_8, value_9, value_10, value_11, value_12, value_13, value_14, value_15, value_16, value_17, value_18, value_19, value_20, value_21, value_22, value_23, value_24, value_25, getl_elem_type, value_26, get_elem_type, value_27, get_elem_type_1, value_28, generic_json, value_29, value_30, value_31, value_32, value_33, value_34, value_35, value_36, value_37, value_38, get_types, values, json_value_5, optional_type_delayed_5) = (None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None)
                if match_value[0].tag == 1:
                    if match_value[1].tag == 8:
                        pattern_matching_result_2 = 0
                        value_7 = match_value[0].fields[0]
                    
                    elif match_value[1].tag == 6:
                        pattern_matching_result_2 = 3
                        value_10 = match_value[0].fields[0]
                    
                    elif match_value[1].tag == 1:
                        pattern_matching_result_2 = 4
                        value_11 = match_value[0].fields[0]
                    
                    elif match_value[1].tag == 2:
                        pattern_matching_result_2 = 6
                        value_13 = match_value[0].fields[0]
                    
                    elif match_value[1].tag == 10:
                        pattern_matching_result_2 = 8
                        value_15 = match_value[0].fields[0]
                    
                    elif match_value[1].tag == 21:
                        pattern_matching_result_2 = 10
                        value_17 = match_value[0].fields[0]
                    
                    elif match_value[1].tag == 11:
                        pattern_matching_result_2 = 11
                        value_18 = match_value[0].fields[0]
                    
                    elif match_value[1].tag == 3:
                        pattern_matching_result_2 = 14
                        value_21 = match_value[0].fields[0]
                    
                    elif match_value[1].tag == 4:
                        pattern_matching_result_2 = 15
                        value_22 = match_value[0].fields[0]
                    
                    elif match_value[1].tag == 5:
                        pattern_matching_result_2 = 17
                        value_24 = match_value[0].fields[0]
                    
                    elif match_value[1].tag == 36:
                        pattern_matching_result_2 = 19
                        getl_elem_type = match_value[1].fields[0]
                        value_26 = match_value[0].fields[0]
                    
                    elif match_value[1].tag == 28:
                        pattern_matching_result_2 = 21
                        get_elem_type_1 = match_value[1].fields[0]
                        value_28 = match_value[0].fields[0]
                    
                    elif match_value[1].tag == 20:
                        pattern_matching_result_2 = 24
                        generic_json = match_value[0]
                    
                    elif match_value[1].tag == 12:
                        pattern_matching_result_2 = 25
                        value_29 = match_value[0].fields[0]
                    
                    elif match_value[1].tag == 13:
                        pattern_matching_result_2 = 26
                        value_30 = match_value[0].fields[0]
                    
                    elif match_value[1].tag == 14:
                        pattern_matching_result_2 = 29
                        value_33 = match_value[0].fields[0]
                    
                    elif match_value[1].tag == 17:
                        pattern_matching_result_2 = 30
                        value_34 = match_value[0].fields[0]
                    
                    elif match_value[1].tag == 15:
                        pattern_matching_result_2 = 32
                        value_36 = match_value[0].fields[0]
                    
                    elif match_value[1].tag == 16:
                        pattern_matching_result_2 = 33
                        value_37 = match_value[0].fields[0]
                    
                    elif match_value[1].tag == 25:
                        if not equals(match_value[0], Json(3)):
                            pattern_matching_result_2 = 37
                            json_value_5 = match_value[0]
                            optional_type_delayed_5 = match_value[1].fields[0]
                        
                        else: 
                            pattern_matching_result_2 = 38
                        
                    
                    else: 
                        pattern_matching_result_2 = 38
                    
                
                elif match_value[0].tag == 0:
                    if match_value[1].tag == 6:
                        pattern_matching_result_2 = 1
                        value_8 = match_value[0].fields[0]
                    
                    elif match_value[1].tag == 1:
                        pattern_matching_result_2 = 5
                        value_12 = match_value[0].fields[0]
                    
                    elif match_value[1].tag == 2:
                        pattern_matching_result_2 = 7
                        value_14 = match_value[0].fields[0]
                    
                    elif match_value[1].tag == 10:
                        pattern_matching_result_2 = 9
                        value_16 = match_value[0].fields[0]
                    
                    elif match_value[1].tag == 11:
                        pattern_matching_result_2 = 12
                        value_19 = match_value[0].fields[0]
                    
                    elif match_value[1].tag == 3:
                        pattern_matching_result_2 = 13
                        value_20 = match_value[0].fields[0]
                    
                    elif match_value[1].tag == 5:
                        pattern_matching_result_2 = 16
                        value_23 = match_value[0].fields[0]
                    
                    elif match_value[1].tag == 18:
                        pattern_matching_result_2 = 18
                        value_25 = match_value[0].fields[0]
                    
                    elif match_value[1].tag == 36:
                        pattern_matching_result_2 = 20
                        get_elem_type = match_value[1].fields[0]
                        value_27 = match_value[0].fields[0]
                    
                    elif match_value[1].tag == 20:
                        pattern_matching_result_2 = 24
                        generic_json = match_value[0]
                    
                    elif match_value[1].tag == 13:
                        pattern_matching_result_2 = 27
                        value_31 = match_value[0].fields[0]
                    
                    elif match_value[1].tag == 14:
                        pattern_matching_result_2 = 28
                        value_32 = match_value[0].fields[0]
                    
                    elif match_value[1].tag == 17:
                        pattern_matching_result_2 = 31
                        value_35 = match_value[0].fields[0]
                    
                    elif match_value[1].tag == 16:
                        pattern_matching_result_2 = 34
                        value_38 = match_value[0].fields[0]
                    
                    elif match_value[1].tag == 25:
                        if not equals(match_value[0], Json(3)):
                            pattern_matching_result_2 = 37
                            json_value_5 = match_value[0]
                            optional_type_delayed_5 = match_value[1].fields[0]
                        
                        else: 
                            pattern_matching_result_2 = 38
                        
                    
                    else: 
                        pattern_matching_result_2 = 38
                    
                
                elif match_value[0].tag == 2:
                    if match_value[1].tag == 7:
                        pattern_matching_result_2 = 2
                        value_9 = match_value[0].fields[0]
                    
                    elif match_value[1].tag == 20:
                        pattern_matching_result_2 = 24
                        generic_json = match_value[0]
                    
                    elif match_value[1].tag == 25:
                        if not equals(match_value[0], Json(3)):
                            pattern_matching_result_2 = 37
                            json_value_5 = match_value[0]
                            optional_type_delayed_5 = match_value[1].fields[0]
                        
                        else: 
                            pattern_matching_result_2 = 38
                        
                    
                    else: 
                        pattern_matching_result_2 = 38
                    
                
                elif match_value[0].tag == 3:
                    if match_value[1].tag == 2:
                        pattern_matching_result_2 = 22
                    
                    elif match_value[1].tag == 0:
                        pattern_matching_result_2 = 23
                    
                    elif match_value[1].tag == 20:
                        pattern_matching_result_2 = 24
                        generic_json = match_value[0]
                    
                    elif match_value[1].tag == 25:
                        pattern_matching_result_2 = 36
                    
                    else: 
                        pattern_matching_result_2 = 38
                    
                
                elif match_value[0].tag == 5:
                    if match_value[1].tag == 20:
                        pattern_matching_result_2 = 24
                        generic_json = match_value[0]
                    
                    elif match_value[1].tag == 38:
                        pattern_matching_result_2 = 35
                        get_types = match_value[1].fields[0]
                        values = match_value[0].fields[0]
                    
                    elif match_value[1].tag == 25:
                        if not equals(match_value[0], Json(3)):
                            pattern_matching_result_2 = 37
                            json_value_5 = match_value[0]
                            optional_type_delayed_5 = match_value[1].fields[0]
                        
                        else: 
                            pattern_matching_result_2 = 38
                        
                    
                    else: 
                        pattern_matching_result_2 = 38
                    
                
                elif match_value[1].tag == 20:
                    pattern_matching_result_2 = 24
                    generic_json = match_value[0]
                
                elif match_value[1].tag == 25:
                    if not equals(match_value[0], Json(3)):
                        pattern_matching_result_2 = 37
                        json_value_5 = match_value[0]
                        optional_type_delayed_5 = match_value[1].fields[0]
                    
                    else: 
                        pattern_matching_result_2 = 38
                    
                
                else: 
                    pattern_matching_result_2 = 38
                
                if pattern_matching_result_2 == 0:
                    return parse(value_7)
                
                elif pattern_matching_result_2 == 1:
                    return math.floor(value_8)
                
                elif pattern_matching_result_2 == 2:
                    return value_9
                
                elif pattern_matching_result_2 == 3:
                    return parse_1(value_10, 511, False, 32)
                
                elif pattern_matching_result_2 == 4:
                    return value_11
                
                elif pattern_matching_result_2 == 5:
                    return chr(value_12)
                
                elif pattern_matching_result_2 == 6:
                    return value_13
                
                elif pattern_matching_result_2 == 7:
                    return to_string(value_14)
                
                elif pattern_matching_result_2 == 8:
                    return Decimal(value_15)
                
                elif pattern_matching_result_2 == 9:
                    return Decimal(value_16)
                
                elif pattern_matching_result_2 == 10:
                    return Uri(value_17)
                
                elif pattern_matching_result_2 == 11:
                    return parse_1(value_18, 511, False, 16)
                
                elif pattern_matching_result_2 == 12:
                    return (int(value_19) + 0x8000 & 0xFFFF) - 0x8000
                
                elif pattern_matching_result_2 == 13:
                    return int(value_20+0x10000 if value_20 < 0 else value_20) & 0xFFFF
                
                elif pattern_matching_result_2 == 14:
                    return parse_1(value_21, 511, True, 16)
                
                elif pattern_matching_result_2 == 15:
                    return parse_1(value_22, 511, True, 32)
                
                elif pattern_matching_result_2 == 16:
                    return from_number(value_23, True)
                
                elif pattern_matching_result_2 == 17:
                    return parse_2(value_24, 511, True, 64)
                
                elif pattern_matching_result_2 == 18:
                    return math.floor(value_25)
                
                elif pattern_matching_result_2 == 19:
                    pattern_input : Tuple[TypeInfo_1, Any] = getl_elem_type()
                    underlying_type : TypeInfo_1 = pattern_input[0]
                    original_type : Any = pattern_input[1]
                    if underlying_type.tag == 6:
                        match_value_1 : Tuple[bool, int]
                        out_arg : int = 0
                        def arrow_90(input: Json=input, type_info: TypeInfo_1=type_info) -> int:
                            return out_arg
                        
                        def arrow_91(v: int, input: Json=input, type_info: TypeInfo_1=type_info) -> None:
                            nonlocal out_arg
                            out_arg = v or 0
                        
                        match_value_1 = (try_parse(value_26, 511, False, 32, FSharpRef(arrow_90, arrow_91)), out_arg)
                        if match_value_1[0]:
                            return match_value_1[1]
                        
                        else: 
                            arg20 : str = name_2(original_type)
                            return to_fail(printf("The value \u0027%s\u0027 is not valid for enum of type \u0027%s\u0027"))(value_26)(arg20)
                        
                    
                    elif underlying_type.tag == 12:
                        match_value_2 : Tuple[bool, Any]
                        out_arg_1 : Any = from_int(0)
                        def arrow_92(input: Json=input, type_info: TypeInfo_1=type_info) -> Any:
                            return out_arg_1
                        
                        def arrow_93(v_1: Any, input: Json=input, type_info: TypeInfo_1=type_info) -> None:
                            nonlocal out_arg_1
                            out_arg_1 = v_1
                        
                        match_value_2 = (try_parse_1(value_26, 511, False, 64, FSharpRef(arrow_92, arrow_93)), out_arg_1)
                        if match_value_2[0]:
                            return match_value_2[1]
                        
                        else: 
                            arg20_1 : str = name_2(original_type)
                            return to_fail(printf("The value \u0027%s\u0027 is not valid for enum of type \u0027%s\u0027"))(value_26)(arg20_1)
                        
                    
                    else: 
                        arg20_2 : str = name_2(original_type)
                        return to_fail(printf("The value \u0027%s\u0027 cannot be converted to enum of type \u0027%s\u0027"))(value_26)(arg20_2)
                    
                
                elif pattern_matching_result_2 == 20:
                    pattern_input_1 : Tuple[TypeInfo_1, Any] = get_elem_type()
                    return value_27
                
                elif pattern_matching_result_2 == 21:
                    elem_type : TypeInfo_1 = get_elem_type_1()
                    if elem_type.tag == 13:
                        return base64.b64decode(value_28)
                    
                    else: 
                        return to_fail(printf("Cannot convert arbitrary string \u0027%s\u0027 to %A"))(value_28)(elem_type)
                    
                
                elif pattern_matching_result_2 == 22:
                    return None
                
                elif pattern_matching_result_2 == 23:
                    return None
                
                elif pattern_matching_result_2 == 24:
                    return SimpleJson_toPlainObject(generic_json)
                
                elif pattern_matching_result_2 == 25:
                    return parse_2(value_29, 511, False, 64)
                
                elif pattern_matching_result_2 == 26:
                    return parse_1(value_30, 511, True, 8)
                
                elif pattern_matching_result_2 == 27:
                    return int(value_31+0x100 if value_31 < 0 else value_31) & 0xFF
                
                elif pattern_matching_result_2 == 28:
                    return (int(value_32) + 0x80 & 0xFF) - 0x80
                
                elif pattern_matching_result_2 == 29:
                    return parse_1(value_33, 511, False, 8)
                
                elif pattern_matching_result_2 == 30:
                    return parse_3(value_34)
                
                elif pattern_matching_result_2 == 31:
                    return from_int32(math.floor(value_35))
                
                elif pattern_matching_result_2 == 32:
                    return parse_4(value_36)
                
                elif pattern_matching_result_2 == 33:
                    return parse_5(value_37)
                
                elif pattern_matching_result_2 == 34:
                    return datetime.fromtimestamp(to_number(from_number(math.floor(value_38), False)) * 1000, 0)
                
                elif pattern_matching_result_2 == 35:
                    pattern_input_2 : Tuple[List[UnionCase], Any] = get_types()
                    union_type : Any = pattern_input_2[1]
                    cases : List[UnionCase] = pattern_input_2[0]
                    match_value_3 : FSharpList[Tuple[str, Json]] = to_list_1(values)
                    (pattern_matching_result_3, case_name, values_1, case_name_1, json) = (None, None, None, None, None)
                    if not is_empty(match_value_3):
                        if head(match_value_3)[1].tag == 4:
                            if is_empty(tail_1(match_value_3)):
                                pattern_matching_result_3 = 0
                                case_name = head(match_value_3)[0]
                                values_1 = head(match_value_3)[1].fields[0]
                            
                            else: 
                                pattern_matching_result_3 = 2
                            
                        
                        else: 
                            active_pattern_result906 : Optional[Json] = Convert__007CNonArray_007C__007C(head(match_value_3)[1])
                            if active_pattern_result906 is not None:
                                if is_empty(tail_1(match_value_3)):
                                    pattern_matching_result_3 = 1
                                    case_name_1 = head(match_value_3)[0]
                                    json = active_pattern_result906
                                
                                else: 
                                    pattern_matching_result_3 = 2
                                
                            
                            else: 
                                pattern_matching_result_3 = 2
                            
                        
                    
                    else: 
                        pattern_matching_result_3 = 2
                    
                    if pattern_matching_result_3 == 0:
                        def predicate(case: UnionCase, input: Json=input, type_info: TypeInfo_1=type_info) -> bool:
                            return case.CaseName == case_name
                        
                        _arg1 : Optional[UnionCase] = try_find_1(predicate, cases)
                        if _arg1 is not None:
                            def arrow_94(input: Json=input, type_info: TypeInfo_1=type_info) -> bool:
                                found_case : UnionCase = _arg1
                                return Convert_arrayLike(found_case.CaseTypes[0]) if (len(found_case.CaseTypes) == 1) else False
                            
                            if arrow_94():
                                found_case_1 : UnionCase = _arg1
                                return make_union(found_case_1.Info, [Convert_fromJsonAs(Json(4, values_1), found_case_1.CaseTypes[0])])
                            
                            else: 
                                (pattern_matching_result_4, found_case_3) = (None, None)
                                if _arg1 is not None:
                                    def arrow_95(input: Json=input, type_info: TypeInfo_1=type_info) -> bool:
                                        found_case_2 : UnionCase = _arg1
                                        return Convert_optional(found_case_2.CaseTypes[0]) if (len(found_case_2.CaseTypes) == 1) else False
                                    
                                    if arrow_95():
                                        pattern_matching_result_4 = 0
                                        found_case_3 = _arg1
                                    
                                    else: 
                                        pattern_matching_result_4 = 1
                                    
                                
                                else: 
                                    pattern_matching_result_4 = 1
                                
                                if pattern_matching_result_4 == 0:
                                    return make_union(found_case_3.Info, [Convert_fromJsonAs(Json(4, values_1), found_case_3.CaseTypes[0])])
                                
                                elif pattern_matching_result_4 == 1:
                                    if _arg1 is not None:
                                        found_case_4 : UnionCase = _arg1
                                        if (len(found_case_4.CaseTypes) != length(values_1)) if ((not Convert_arrayLike(found_case_4.CaseTypes[0])) if (len(found_case_4.CaseTypes) == 1) else False) else False:
                                            arg30_1 : int = length(values_1) or 0
                                            arg20_5 : int = len(found_case_4.CaseTypes) or 0
                                            to_fail(printf("Expected case \u0027%s\u0027 to have %d argument types but the JSON data only contained %d values"))(found_case_4.CaseName)(arg20_5)(arg30_1)
                                        
                                        def mapping(tupled_arg: Tuple[TypeInfo_1, Json], input: Json=input, type_info: TypeInfo_1=type_info) -> Any:
                                            return Convert_fromJsonAs(tupled_arg[1], tupled_arg[0])
                                        
                                        return make_union(found_case_4.Info, map_2(mapping, zip(found_case_4.CaseTypes, to_array(values_1)), None))
                                    
                                    else: 
                                        raise Exception("Match failure")
                                    
                                
                            
                        
                        else: 
                            def arrow_96(case_1: UnionCase, input: Json=input, type_info: TypeInfo_1=type_info) -> str:
                                return to_text(printf(" \u0027%s\u0027 "))(case_1.CaseName)
                            
                            expected_cases : str = join(", ", map_2(arrow_96, cases, None))
                            arg20_4 : str = name_2(union_type)
                            return to_fail(printf("Case %s was not valid for type \u0027%s\u0027, expected one of the cases [%s]"))(case_name)(arg20_4)(expected_cases)
                        
                    
                    elif pattern_matching_result_3 == 1:
                        def predicate_1(case_2: UnionCase, input: Json=input, type_info: TypeInfo_1=type_info) -> bool:
                            return case_2.CaseName == case_name_1
                        
                        _arg2 : Optional[UnionCase] = try_find_1(predicate_1, cases)
                        (pattern_matching_result_5, case_info, case_name_2, case_type) = (None, None, None, None)
                        if _arg2 is not None:
                            def arrow_99(input: Json=input, type_info: TypeInfo_1=type_info) -> bool:
                                test_expr : List[TypeInfo_1] = _arg2.CaseTypes
                                def arrow_98(x: TypeInfo_1, y: TypeInfo_1) -> bool:
                                    return equals(x, y)
                                
                                return (len(test_expr) == 1) if (not equals_with(arrow_98, test_expr, None)) else False
                            
                            if arrow_99():
                                pattern_matching_result_5 = 0
                                case_info = _arg2.Info
                                case_name_2 = _arg2.CaseName
                                case_type = _arg2.CaseTypes[0]
                            
                            else: 
                                pattern_matching_result_5 = 1
                            
                        
                        else: 
                            pattern_matching_result_5 = 1
                        
                        if pattern_matching_result_5 == 0:
                            return make_union(case_info, [Convert_fromJsonAs(json, case_type)])
                        
                        elif pattern_matching_result_5 == 1:
                            def arrow_97(case_3: UnionCase, input: Json=input, type_info: TypeInfo_1=type_info) -> str:
                                return to_text(printf(" \u0027%s\u0027 "))(case_3.CaseName)
                            
                            expected_cases_1 : str = join(", ", map_2(arrow_97, cases, None))
                            arg20_6 : str = name_2(union_type)
                            return to_fail(printf("Case %s was not valid for type \u0027%s\u0027, expected one of the cases [%s]"))(case_name_1)(arg20_6)(expected_cases_1)
                        
                    
                    elif pattern_matching_result_3 == 2:
                        if (count(values) == 2) if (contains_key("fields", values) if contains_key("tag", values) else False) else False:
                            match_value_4 : Tuple[Optional[Json], Optional[Json]] = (try_find("tag", values), try_find("fields", values))
                            (pattern_matching_result_6, case_index, field_values) = (None, None, None)
                            if match_value_4[0] is not None:
                                if match_value_4[0].tag == 0:
                                    if match_value_4[1] is not None:
                                        if match_value_4[1].tag == 4:
                                            pattern_matching_result_6 = 0
                                            case_index = match_value_4[0].fields[0]
                                            field_values = match_value_4[1].fields[0]
                                        
                                        else: 
                                            pattern_matching_result_6 = 1
                                        
                                    
                                    else: 
                                        pattern_matching_result_6 = 1
                                    
                                
                                else: 
                                    pattern_matching_result_6 = 1
                                
                            
                            else: 
                                pattern_matching_result_6 = 1
                            
                            if pattern_matching_result_6 == 0:
                                found_case_5 : UnionCase = cases[int(case_index)]
                                def mapping_1(index: int, value_44: Json, input: Json=input, type_info: TypeInfo_1=type_info) -> Any:
                                    return Convert_fromJsonAs(value_44, found_case_5.CaseTypes[index])
                                
                                return make_union(found_case_5.Info, map_indexed(mapping_1, to_array(field_values), None))
                            
                            elif pattern_matching_result_6 == 1:
                                arg20_7 : str = full_name(union_type)
                                arg10_9 : str = SimpleJson_toString(Json(5, values))
                                return to_fail(printf("Could not deserialize JSON(%s) into type %s"))(arg10_9)(arg20_7)
                            
                        
                        elif Convert_unionOfRecords(type_info):
                            def predicate_2(keyword: str, input: Json=input, type_info: TypeInfo_1=type_info) -> bool:
                                return contains_key(keyword, values)
                            
                            found_discriminator_key : Optional[str] = try_find_2(predicate_2, of_array(["__typename", "$typename", "$type"]))
                            if found_discriminator_key is not None:
                                discriminator_value_json : Json = find(found_discriminator_key, values)
                                if discriminator_value_json.tag == 1:
                                    discriminator_value : str = discriminator_value_json.fields[0]
                                    def predicate_3(case_4: UnionCase, input: Json=input, type_info: TypeInfo_1=type_info) -> bool:
                                        return case_4.CaseName.upper() == discriminator_value.upper()
                                    
                                    found_union_case : Optional[UnionCase] = try_find_3(predicate_3, cases)
                                    if found_union_case is not None:
                                        case_5 : UnionCase = found_union_case
                                        return make_union(case_5.Info, [Convert_fromJsonAs(Json(5, values), case_5.CaseTypes[0])])
                                    
                                    else: 
                                        arg10_11 : str = name_2(union_type)
                                        return to_fail(printf("Union of records of type \u0027%s\u0027 does not have a matching case \u0027%s\u0027"))(arg10_11)(discriminator_value)
                                    
                                
                                else: 
                                    arg10_12 : str = name_2(union_type)
                                    return to_fail(printf("Union of records of type \u0027%s\u0027 cannot be deserialized with the value of the discriminator key is not a string to match against a specific union case"))(arg10_12)
                                
                            
                            else: 
                                arg10_10 : str = name_2(union_type)
                                return to_fail(printf("Could not serialize the JSON object into the union of records of type %s because the JSON did not contain a known discriminator. Expected \u0027__typename\u0027, \u0027$typeName\u0027 or \u0027$type\u0027"))(arg10_10)
                            
                        
                        else: 
                            unexpected_json : str = json_1.dumps(match_value_3)
                            expected_type : str = json_1.dumps(cases)
                            return to_fail(printf("Expected JSON:\n%s\nto match the type\n%s"))(unexpected_json)(expected_type)
                        
                    
                
                elif pattern_matching_result_2 == 36:
                    return None
                
                elif pattern_matching_result_2 == 37:
                    return some(Convert_fromJsonAs(json_value_5, optional_type_delayed_5()))
                
                elif pattern_matching_result_2 == 38:
                    (pattern_matching_result_7, value_45, value_46, dict_1, case_name_4, get_types_2) = (None, None, None, None, None, None)
                    if match_value[0].tag == 1:
                        if match_value[1].tag == 19:
                            pattern_matching_result_7 = 0
                            value_45 = match_value[0].fields[0]
                        
                        elif match_value[1].tag == 38:
                            if Convert_isQuoted(match_value[0].fields[0]):
                                pattern_matching_result_7 = 3
                                case_name_4 = match_value[0].fields[0]
                                get_types_2 = match_value[1].fields[0]
                            
                            else: 
                                pattern_matching_result_7 = 4
                            
                        
                        else: 
                            pattern_matching_result_7 = 4
                        
                    
                    elif match_value[0].tag == 0:
                        if match_value[1].tag == 12:
                            pattern_matching_result_7 = 1
                            value_46 = match_value[0].fields[0]
                        
                        else: 
                            pattern_matching_result_7 = 4
                        
                    
                    elif match_value[0].tag == 5:
                        if match_value[1].tag == 12:
                            pattern_matching_result_7 = 2
                            dict_1 = match_value[0].fields[0]
                        
                        else: 
                            pattern_matching_result_7 = 4
                        
                    
                    else: 
                        pattern_matching_result_7 = 4
                    
                    if pattern_matching_result_7 == 0:
                        return parse_6(value_45)
                    
                    elif pattern_matching_result_7 == 1:
                        return from_integer(int(value_46), False, 2)
                    
                    elif pattern_matching_result_7 == 2:
                        def get(key: str, input: Json=input, type_info: TypeInfo_1=type_info) -> Optional[Json]:
                            return try_find(key, dict_1)
                        
                        get : Callable[[str], Optional[Json]] = get
                        def chooser(x_1: Optional[Json]=None, input: Json=input, type_info: TypeInfo_1=type_info) -> Optional[Json]:
                            return x_1
                        
                        _arg3 : FSharpList[Json] = choose(chooser, of_array([get("low"), get("high"), get("unsigned")]))
                        (pattern_matching_result_8, high, low) = (None, None, None)
                        if not is_empty(_arg3):
                            if head(_arg3).tag == 0:
                                if not is_empty(tail_1(_arg3)):
                                    if head(tail_1(_arg3)).tag == 0:
                                        if not is_empty(tail_1(tail_1(_arg3))):
                                            if head(tail_1(tail_1(_arg3))).tag == 2:
                                                if is_empty(tail_1(tail_1(tail_1(_arg3)))):
                                                    pattern_matching_result_8 = 0
                                                    high = head(tail_1(_arg3)).fields[0]
                                                    low = head(_arg3).fields[0]
                                                
                                                else: 
                                                    pattern_matching_result_8 = 1
                                                
                                            
                                            else: 
                                                pattern_matching_result_8 = 1
                                            
                                        
                                        else: 
                                            pattern_matching_result_8 = 1
                                        
                                    
                                    else: 
                                        pattern_matching_result_8 = 1
                                    
                                
                                else: 
                                    pattern_matching_result_8 = 1
                                
                            
                            else: 
                                pattern_matching_result_8 = 1
                            
                        
                        else: 
                            pattern_matching_result_8 = 1
                        
                        if pattern_matching_result_8 == 0:
                            return to_int64(concat([get_bytes_int32(int(low)), get_bytes_int32(int(high))], Uint8Array), 0)
                        
                        elif pattern_matching_result_8 == 1:
                            return to_fail(printf("Unable to construct int64 from object literal { low: int, high: int, unsigned: bool }"))
                        
                    
                    elif pattern_matching_result_7 == 3:
                        pattern_input_3 : Tuple[List[UnionCase], Any] = get_types_2()
                        case_types : List[UnionCase] = pattern_input_3[0]
                        def predicate_4(case_6: UnionCase, input: Json=input, type_info: TypeInfo_1=type_info) -> bool:
                            return case_6.CaseName == Convert_removeQuotes(case_name_4)
                        
                        _arg4 : Optional[UnionCase] = try_find_1(predicate_4, case_types)
                        if _arg4 is None:
                            def arrow_100(case_7: UnionCase, input: Json=input, type_info: TypeInfo_1=type_info) -> str:
                                return to_text(printf(" \u0027%s\u0027 "))(case_7.CaseName)
                            
                            expected_cases_2 : str = join(", ", map_2(arrow_100, case_types, None))
                            arg20_10 : str = name_2(pattern_input_3[1])
                            return to_fail(printf("Case %s was not valid for type \u0027%s\u0027, expected one of the cases [%s]"))(case_name_4)(arg20_10)(expected_cases_2)
                        
                        else: 
                            return make_union(_arg4.Info, [])
                        
                    
                    elif pattern_matching_result_7 == 4:
                        (pattern_matching_result_9, case_name_5, get_types_3, get_fields, serialized_record, case_value, get_types_4, element_type_delayed, values_4, element_type_delayed_1, values_5, element_type_delayed_2, linked_list, element_type_delayed_3, values_6, element_type_delayed_4, values_7, array_9, tuple_types_delayed, dict_2, get_types_5, get_types_6, tuples, get_types_7, tuples_1, dict_3, get_types_8, get_type, items, get_types_9, map, get_type_1) = (None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None)
                        if match_value[0].tag == 1:
                            if match_value[1].tag == 38:
                                pattern_matching_result_9 = 0
                                case_name_5 = match_value[0].fields[0]
                                get_types_3 = match_value[1].fields[0]
                            
                            elif match_value[1].tag == 37:
                                pattern_matching_result_9 = 1
                                get_fields = match_value[1].fields[0]
                                serialized_record = match_value[0].fields[0]
                            
                            elif match_value[1].tag == 22:
                                pattern_matching_result_9 = 15
                                get_type_1 = match_value[1].fields[0]
                            
                            else: 
                                pattern_matching_result_9 = 16
                            
                        
                        elif match_value[0].tag == 4:
                            if match_value[1].tag == 38:
                                pattern_matching_result_9 = 2
                                case_value = match_value[0].fields[0]
                                get_types_4 = match_value[1].fields[0]
                            
                            elif match_value[1].tag == 28:
                                pattern_matching_result_9 = 3
                                element_type_delayed = match_value[1].fields[0]
                                values_4 = match_value[0].fields[0]
                            
                            elif match_value[1].tag == 26:
                                pattern_matching_result_9 = 4
                                element_type_delayed_1 = match_value[1].fields[0]
                                values_5 = match_value[0].fields[0]
                            
                            elif match_value[1].tag == 27:
                                pattern_matching_result_9 = 6
                                element_type_delayed_3 = match_value[1].fields[0]
                                values_6 = match_value[0].fields[0]
                            
                            elif match_value[1].tag == 29:
                                pattern_matching_result_9 = 7
                                element_type_delayed_4 = match_value[1].fields[0]
                                values_7 = match_value[0].fields[0]
                            
                            elif match_value[1].tag == 30:
                                pattern_matching_result_9 = 8
                                array_9 = match_value[0].fields[0]
                                tuple_types_delayed = match_value[1].fields[0]
                            
                            elif match_value[1].tag == 31:
                                pattern_matching_result_9 = 10
                                get_types_6 = match_value[1].fields[0]
                                tuples = match_value[0].fields[0]
                            
                            elif match_value[1].tag == 32:
                                pattern_matching_result_9 = 11
                                get_types_7 = match_value[1].fields[0]
                                tuples_1 = match_value[0].fields[0]
                            
                            elif match_value[1].tag == 34:
                                pattern_matching_result_9 = 13
                                get_type = match_value[1].fields[0]
                                items = match_value[0].fields[0]
                            
                            elif match_value[1].tag == 22:
                                pattern_matching_result_9 = 15
                                get_type_1 = match_value[1].fields[0]
                            
                            else: 
                                pattern_matching_result_9 = 16
                            
                        
                        elif match_value[0].tag == 5:
                            if match_value[1].tag == 26:
                                pattern_matching_result_9 = 5
                                element_type_delayed_2 = match_value[1].fields[0]
                                linked_list = match_value[0].fields[0]
                            
                            elif match_value[1].tag == 37:
                                pattern_matching_result_9 = 9
                                dict_2 = match_value[0].fields[0]
                                get_types_5 = match_value[1].fields[0]
                            
                            elif match_value[1].tag == 32:
                                pattern_matching_result_9 = 12
                                dict_3 = match_value[0].fields[0]
                                get_types_8 = match_value[1].fields[0]
                            
                            elif match_value[1].tag == 31:
                                pattern_matching_result_9 = 14
                                get_types_9 = match_value[1].fields[0]
                                map = match_value[0].fields[0]
                            
                            elif match_value[1].tag == 22:
                                pattern_matching_result_9 = 15
                                get_type_1 = match_value[1].fields[0]
                            
                            else: 
                                pattern_matching_result_9 = 16
                            
                        
                        elif match_value[1].tag == 22:
                            pattern_matching_result_9 = 15
                            get_type_1 = match_value[1].fields[0]
                        
                        else: 
                            pattern_matching_result_9 = 16
                        
                        if pattern_matching_result_9 == 0:
                            pattern_input_4 : Tuple[List[UnionCase], Any] = get_types_3()
                            case_types_1 : List[UnionCase] = pattern_input_4[0]
                            def predicate_5(case_8: UnionCase, input: Json=input, type_info: TypeInfo_1=type_info) -> bool:
                                return case_8.CaseName == case_name_5
                            
                            _arg5 : Optional[UnionCase] = try_find_1(predicate_5, case_types_1)
                            if _arg5 is None:
                                def arrow_101(case_9: UnionCase, input: Json=input, type_info: TypeInfo_1=type_info) -> str:
                                    return to_text(printf(" \u0027%s\u0027 "))(case_9.CaseName)
                                
                                expected_cases_3 : str = join(", ", map_2(arrow_101, case_types_1, None))
                                arg20_11 : str = name_2(pattern_input_4[1])
                                return to_fail(printf("Case %s was not valid for type \u0027%s\u0027, expected one of the cases [%s]"))(case_name_5)(arg20_11)(expected_cases_3)
                            
                            else: 
                                return make_union(_arg5.Info, [])
                            
                        
                        elif pattern_matching_result_9 == 1:
                            input_mut = SimpleJson_parseNative(serialized_record)
                            type_info_mut = type_info
                            continue
                        
                        elif pattern_matching_result_9 == 2:
                            pattern_input_5 : Tuple[List[UnionCase], Any] = get_types_4()
                            cases_1 : List[UnionCase] = pattern_input_5[0]
                            (pattern_matching_result_10, case_name_6, case_name_8, values_3, otherwise_6) = (None, None, None, None, None)
                            if not is_empty(case_value):
                                if head(case_value).tag == 1:
                                    if is_empty(tail_1(case_value)):
                                        pattern_matching_result_10 = 0
                                        case_name_6 = head(case_value).fields[0]
                                    
                                    else: 
                                        pattern_matching_result_10 = 1
                                        case_name_8 = head(case_value).fields[0]
                                        values_3 = tail_1(case_value)
                                    
                                
                                else: 
                                    pattern_matching_result_10 = 2
                                    otherwise_6 = case_value
                                
                            
                            else: 
                                pattern_matching_result_10 = 2
                                otherwise_6 = case_value
                            
                            if pattern_matching_result_10 == 0:
                                def predicate_6(case_10: UnionCase, input: Json=input, type_info: TypeInfo_1=type_info) -> bool:
                                    return case_10.CaseName == case_name_6
                                
                                _arg6 : Optional[UnionCase] = try_find_1(predicate_6, cases_1)
                                if _arg6 is None:
                                    def arrow_102(case_11: UnionCase, input: Json=input, type_info: TypeInfo_1=type_info) -> str:
                                        return to_text(printf(" \u0027%s\u0027 "))(case_11.CaseName)
                                    
                                    expected_cases_4 : str = join(", ", map_2(arrow_102, cases_1, None))
                                    arg20_12 : str = name_2(pattern_input_5[1])
                                    return to_fail(printf("Case \u0027%s\u0027 was not valid for type \u0027%s\u0027, expected one of the cases [%s]"))(case_name_6)(arg20_12)(expected_cases_4)
                                
                                else: 
                                    case_name_7 : str = _arg6.CaseName
                                    case_info_types : List[TypeInfo_1] = _arg6.CaseTypes
                                    return make_union(_arg6.Info, [])
                                
                            
                            elif pattern_matching_result_10 == 1:
                                def predicate_7(case_12: UnionCase, input: Json=input, type_info: TypeInfo_1=type_info) -> bool:
                                    return case_12.CaseName == case_name_8
                                
                                _arg7 : Optional[UnionCase] = try_find_1(predicate_7, cases_1)
                                if _arg7 is not None:
                                    types : List[TypeInfo_1] = _arg7.CaseTypes
                                    found_case_name : str = _arg7.CaseName
                                    case_info_4 : Any = _arg7.Info
                                    if len(types) != length(values_3):
                                        to_fail(printf("The number of union case parameters for \u0027%s\u0027 is different"))(found_case_name)
                                    
                                    def mapping_2(tupled_arg_1: Tuple[TypeInfo_1, Json], input: Json=input, type_info: TypeInfo_1=type_info) -> Any:
                                        return Convert_fromJsonAs(tupled_arg_1[1], tupled_arg_1[0])
                                    
                                    return make_union(case_info_4, map_2(mapping_2, zip(types, to_array(values_3)), None))
                                
                                else: 
                                    def arrow_103(_arg1_1: UnionCase, input: Json=input, type_info: TypeInfo_1=type_info) -> str:
                                        return _arg1_1.CaseName
                                    
                                    expected_cases_5 : str = join(", ", map_2(arrow_103, cases_1, None))
                                    return to_fail(printf("Case %s was not valid, expected one of [%s]"))(case_name_8)(expected_cases_5)
                                
                            
                            elif pattern_matching_result_10 == 2:
                                unexpected_json_1 : str = JSON.stringify(otherwise_6)
                                expected_type_1 : str = JSON.stringify(cases_1)
                                return to_fail(printf("Expected JSON:\n%s\nto match the type\n%s"))(unexpected_json_1)(expected_type_1)
                            
                        
                        elif pattern_matching_result_9 == 3:
                            element_type : TypeInfo_1 = element_type_delayed()
                            def mapping_3(value_50: Json, input: Json=input, type_info: TypeInfo_1=type_info) -> Any:
                                return Convert_fromJsonAs(value_50, element_type)
                            
                            return to_array(map_3(mapping_3, values_4))
                        
                        elif pattern_matching_result_9 == 4:
                            element_type_1 : TypeInfo_1 = element_type_delayed_1()
                            def mapping_4(value_52: Json, input: Json=input, type_info: TypeInfo_1=type_info) -> Any:
                                return Convert_fromJsonAs(value_52, element_type_1)
                            
                            return map_3(mapping_4, values_5)
                        
                        elif pattern_matching_result_9 == 5:
                            element_type_2 : TypeInfo_1 = element_type_delayed_2()
                            def mapping_5(value_54: Json, input: Json=input, type_info: TypeInfo_1=type_info) -> Any:
                                return Convert_fromJsonAs(value_54, element_type_2)
                            
                            return map_3(mapping_5, Convert_flattenFable3Lists(linked_list))
                        
                        elif pattern_matching_result_9 == 6:
                            element_type_3 : TypeInfo_1 = element_type_delayed_3()
                            def mapping_6(value_56: Json, input: Json=input, type_info: TypeInfo_1=type_info) -> IComparable[Any]:
                                return Convert_fromJsonAs(value_56, element_type_3)
                            
                            class ObjectExpr105:
                                @property
                                def Compare(self) -> Any:
                                    def arrow_104(x_2: IComparable[Any], y_1: IComparable[Any]) -> int:
                                        return compare(x_2, y_1)
                                    
                                    return arrow_104
                                
                            return of_list(map_3(mapping_6, values_6), ObjectExpr105())
                        
                        elif pattern_matching_result_9 == 7:
                            element_type_4 : TypeInfo_1 = element_type_delayed_4()
                            def arrow_106(value_58: Json, input: Json=input, type_info: TypeInfo_1=type_info) -> Any:
                                return Convert_fromJsonAs(value_58, element_type_4)
                            
                            return map_3(arrow_106, values_7)
                        
                        elif pattern_matching_result_9 == 8:
                            def mapping_7(tupled_arg_2: Tuple[TypeInfo_1, Json], input: Json=input, type_info: TypeInfo_1=type_info) -> Any:
                                return Convert_fromJsonAs(tupled_arg_2[1], tupled_arg_2[0])
                            
                            return map_2(mapping_7, zip(tuple_types_delayed(), to_array(array_9)), None)
                        
                        elif pattern_matching_result_9 == 9:
                            pattern_input_6 : Tuple[List[RecordField], Any] = get_types_5()
                            record_type : Any = pattern_input_6[1]
                            fields : List[RecordField] = pattern_input_6[0]
                            def arrow_107(input: Json=input, type_info: TypeInfo_1=type_info) -> List[Any]:
                                values_8 : FSharpList[Tuple[str, Json]] = to_list_1(dict_2)
                                def mapping_10(_arg3_1: RecordField) -> Any:
                                    field_type : TypeInfo_1 = _arg3_1.FieldType
                                    field_name : str = _arg3_1.FieldName
                                    def predicate_8(tupled_arg_3: Tuple[str, Json], _arg3_1: RecordField=_arg3_1) -> bool:
                                        return field_name == tupled_arg_3[0]
                                    
                                    _arg8 : Optional[Tuple[str, Json]] = try_find_2(predicate_8, values_8)
                                    if _arg8 is None:
                                        if field_type.tag == 25:
                                            return None
                                        
                                        else: 
                                            dict_keys : str
                                            def mapping_8(arg: Tuple[str, Json], _arg3_1: RecordField=_arg3_1) -> str:
                                                return to_text(printf("\u0027%s\u0027"))(arg[0])
                                            
                                            arg10_24 : str = join(", ", map_3(mapping_8, to_list_1(dict_2)))
                                            dict_keys = to_text(printf("[ %s ]"))(arg10_24)
                                            record_fields : str
                                            def mapping_9(_arg2_1: RecordField, _arg3_1: RecordField=_arg3_1) -> str:
                                                name_1 : str = _arg2_1.FieldName
                                                if _arg2_1.FieldType.tag == 25:
                                                    return to_text(printf("optional(\u0027%s\u0027)"))(name_1)
                                                
                                                else: 
                                                    return to_text(printf("required(\u0027%s\u0027)"))(name_1)
                                                
                                            
                                            arg10_27 : str = join(", ", map_2(mapping_9, fields, None))
                                            record_fields = to_text(printf("[ %s ]"))(arg10_27)
                                            arg30_6 : str = name_2(record_type)
                                            return to_fail(printf("Could not find the required key \u0027%s\u0027 in the JSON object literal with keys %s to match with record type \u0027%s\u0027 that has fields %s"))(field_name)(dict_keys)(arg30_6)(record_fields)
                                        
                                    
                                    else: 
                                        key_2 : str = _arg8[0]
                                        return Convert_fromJsonAs(_arg8[1], field_type)
                                    
                                
                                return map_2(mapping_10, fields, None)
                            
                            return make_record(record_type, arrow_107())
                        
                        elif pattern_matching_result_9 == 10:
                            pattern_input_7 : Tuple[TypeInfo_1, TypeInfo_1] = get_types_6()
                            key_type : TypeInfo_1 = pattern_input_7[0]
                            def arrow_111(input: Json=input, type_info: TypeInfo_1=type_info) -> IEnumerable[Any]:
                                def arrow_110(key_value_pair: Json) -> IEnumerable[Any]:
                                    def arrow_109(__unit: Any=None) -> Callable[[], List[TypeInfo_1]]:
                                        a : List[TypeInfo_1] = [key_type, pattern_input_7[1]]
                                        def arrow_108(__unit: Any=None) -> List[TypeInfo_1]:
                                            return a
                                        
                                        return arrow_108
                                    
                                    return singleton_1(Convert_fromJsonAs(key_value_pair, TypeInfo_1(30, arrow_109())))
                                
                                return collect(arrow_110, tuples)
                            
                            pairs : FSharpList[Any] = to_list(delay(arrow_111))
                            if ((key_type.tag == 6) or (key_type.tag == 2)) or (key_type.tag == 7):
                                class ObjectExpr113:
                                    @property
                                    def Compare(self) -> Any:
                                        def arrow_112(x_3: str, y_2: str) -> int:
                                            return compare_primitives(x_3, y_2)
                                        
                                        return arrow_112
                                    
                                return of_list_1(pairs, ObjectExpr113())
                            
                            else: 
                                class ObjectExpr115:
                                    @property
                                    def Compare(self) -> Any:
                                        def arrow_114(x_4: IStructuralComparable, y_3: IStructuralComparable) -> int:
                                            return compare(x_4, y_3)
                                        
                                        return arrow_114
                                    
                                return of_list_1(pairs, ObjectExpr115())
                            
                        
                        elif pattern_matching_result_9 == 11:
                            pattern_input_8 : Tuple[TypeInfo_1, TypeInfo_1, Any] = get_types_7()
                            key_type_1 : TypeInfo_1 = pattern_input_8[0]
                            def arrow_118(input: Json=input, type_info: TypeInfo_1=type_info) -> IEnumerable[Any]:
                                def arrow_117(key_value_pair_1: Json) -> IEnumerable[Any]:
                                    def arrow_116(__unit: Any=None) -> List[TypeInfo_1]:
                                        return [key_type_1, pattern_input_8[1]]
                                    
                                    return singleton_1(Convert_fromJsonAs(key_value_pair_1, TypeInfo_1(30, arrow_116)))
                                
                                return collect(arrow_117, tuples_1)
                            
                            pairs_1 : FSharpList[Any] = to_list(delay(arrow_118))
                            class ObjectExpr121:
                                @property
                                def Equals(self) -> Any:
                                    def arrow_119(x_5: FSharpResult_2[Any, Any], y_4: FSharpResult_2[Any, Any]) -> bool:
                                        return equals(x_5, y_4)
                                    
                                    return arrow_119
                                
                                @property
                                def GetHashCode(self) -> Any:
                                    def arrow_120(x_5: FSharpResult_2[Any, Any]) -> int:
                                        return safe_hash(x_5)
                                    
                                    return arrow_120
                                
                            class ObjectExpr124:
                                @property
                                def Equals(self) -> Any:
                                    def arrow_122(x_6: dict[str, Any], y_5: dict[str, Any]) -> bool:
                                        return equals(x_6, y_5)
                                    
                                    return arrow_122
                                
                                @property
                                def GetHashCode(self) -> Any:
                                    def arrow_123(x_6: dict[str, Any]) -> int:
                                        return structural_hash(x_6)
                                    
                                    return arrow_123
                                
                            class ObjectExpr127:
                                @property
                                def Equals(self) -> Any:
                                    def arrow_125(x_7: IStructuralComparable, y_6: IStructuralComparable) -> bool:
                                        return equals(x_7, y_6)
                                    
                                    return arrow_125
                                
                                @property
                                def GetHashCode(self) -> Any:
                                    def arrow_126(x_7: IStructuralComparable) -> int:
                                        return structural_hash(x_7)
                                    
                                    return arrow_126
                                
                            output : Any = Dictionary([], ObjectExpr121()) if (key_type_1.tag == 38) else (Dictionary([], ObjectExpr124()) if (key_type_1.tag == 37) else Dictionary([], ObjectExpr127()))
                            with get_enumerator(pairs_1) as enumerator:
                                while enumerator.System_Collections_IEnumerator_MoveNext():
                                    for_loop_var : Tuple[IStructuralComparable, Any] = enumerator.System_Collections_Generic_IEnumerator_00601_get_Current()
                                    add_to_dict(output, for_loop_var[0], for_loop_var[1])
                            return output
                        
                        elif pattern_matching_result_9 == 12:
                            pattern_input_9 : Tuple[TypeInfo_1, TypeInfo_1, Any] = get_types_8()
                            key_type_2 : TypeInfo_1 = pattern_input_9[0]
                            def mapping_11(tupled_arg_4: Tuple[str, Json], input: Json=input, type_info: TypeInfo_1=type_info) -> Tuple[Any, Any]:
                                return (Convert_fromJsonAs(Json(1, tupled_arg_4[0]), key_type_2), Convert_fromJsonAs(tupled_arg_4[1], pattern_input_9[1]))
                            
                            pairs_2 : FSharpList[Tuple[Any, Any]] = map_3(mapping_11, to_list_1(dict_3))
                            class ObjectExpr130:
                                @property
                                def Equals(self) -> Any:
                                    def arrow_128(x_8: FSharpResult_2[Any, Any], y_7: FSharpResult_2[Any, Any]) -> bool:
                                        return equals(x_8, y_7)
                                    
                                    return arrow_128
                                
                                @property
                                def GetHashCode(self) -> Any:
                                    def arrow_129(x_8: FSharpResult_2[Any, Any]) -> int:
                                        return safe_hash(x_8)
                                    
                                    return arrow_129
                                
                            class ObjectExpr133:
                                @property
                                def Equals(self) -> Any:
                                    def arrow_131(x_9: dict[str, Any], y_8: dict[str, Any]) -> bool:
                                        return equals(x_9, y_8)
                                    
                                    return arrow_131
                                
                                @property
                                def GetHashCode(self) -> Any:
                                    def arrow_132(x_9: dict[str, Any]) -> int:
                                        return structural_hash(x_9)
                                    
                                    return arrow_132
                                
                            class ObjectExpr136:
                                @property
                                def Equals(self) -> Any:
                                    def arrow_134(x_10: IStructuralComparable, y_9: IStructuralComparable) -> bool:
                                        return equals(x_10, y_9)
                                    
                                    return arrow_134
                                
                                @property
                                def GetHashCode(self) -> Any:
                                    def arrow_135(x_10: IStructuralComparable) -> int:
                                        return structural_hash(x_10)
                                    
                                    return arrow_135
                                
                            output_1 : Any = Dictionary([], ObjectExpr130()) if (key_type_2.tag == 38) else (Dictionary([], ObjectExpr133()) if (key_type_2.tag == 37) else Dictionary([], ObjectExpr136()))
                            with get_enumerator(pairs_2) as enumerator_1:
                                while enumerator_1.System_Collections_IEnumerator_MoveNext():
                                    for_loop_var_1 : Tuple[Any, Any] = enumerator_1.System_Collections_Generic_IEnumerator_00601_get_Current()
                                    add_to_dict(output_1, for_loop_var_1[0], for_loop_var_1[1])
                            return output_1
                        
                        elif pattern_matching_result_9 == 13:
                            elem_type_1 : TypeInfo_1 = get_type()
                            class ObjectExpr139:
                                @property
                                def Equals(self) -> Any:
                                    def arrow_137(x_11: FSharpResult_2[Any, Any], y_10: FSharpResult_2[Any, Any]) -> bool:
                                        return equals(x_11, y_10)
                                    
                                    return arrow_137
                                
                                @property
                                def GetHashCode(self) -> Any:
                                    def arrow_138(x_11: FSharpResult_2[Any, Any]) -> int:
                                        return safe_hash(x_11)
                                    
                                    return arrow_138
                                
                            class ObjectExpr142:
                                @property
                                def Equals(self) -> Any:
                                    def arrow_140(x_12: dict[str, Any], y_11: dict[str, Any]) -> bool:
                                        return equals(x_12, y_11)
                                    
                                    return arrow_140
                                
                                @property
                                def GetHashCode(self) -> Any:
                                    def arrow_141(x_12: dict[str, Any]) -> int:
                                        return structural_hash(x_12)
                                    
                                    return arrow_141
                                
                            class ObjectExpr145:
                                @property
                                def Equals(self) -> Any:
                                    def arrow_143(x_13: IStructuralComparable, y_12: IStructuralComparable) -> bool:
                                        return equals(x_13, y_12)
                                    
                                    return arrow_143
                                
                                @property
                                def GetHashCode(self) -> Any:
                                    def arrow_144(x_13: IStructuralComparable) -> int:
                                        return structural_hash(x_13)
                                    
                                    return arrow_144
                                
                            hashset : Any = HashSet([], ObjectExpr139()) if (elem_type_1.tag == 38) else (HashSet([], ObjectExpr142()) if (elem_type_1.tag == 37) else HashSet([], ObjectExpr145()))
                            with get_enumerator(items) as enumerator_2:
                                while enumerator_2.System_Collections_IEnumerator_MoveNext():
                                    ignore(add_to_set(Convert_fromJsonAs(enumerator_2.System_Collections_Generic_IEnumerator_00601_get_Current(), elem_type_1), hashset))
                            return hashset
                        
                        elif pattern_matching_result_9 == 14:
                            pattern_input_10 : Tuple[TypeInfo_1, TypeInfo_1] = get_types_9()
                            value_type_5 : TypeInfo_1 = pattern_input_10[1]
                            key_type_3 : TypeInfo_1 = pattern_input_10[0]
                            match_value_5 : Tuple[Optional[Json], Optional[Json]] = (try_find("comparer", map), try_find("tree", map))
                            (pattern_matching_result_11, comparer_1, tree_1) = (None, None, None)
                            if match_value_5[0] is not None:
                                if match_value_5[0].tag == 5:
                                    if match_value_5[1] is not None:
                                        if match_value_5[1].tag == 4:
                                            def arrow_157(input: Json=input, type_info: TypeInfo_1=type_info) -> bool:
                                                tree : FSharpList[Json] = match_value_5[1].fields[0]
                                                return is_empty_1(match_value_5[0].fields[0])
                                            
                                            if arrow_157():
                                                pattern_matching_result_11 = 0
                                                comparer_1 = match_value_5[0].fields[0]
                                                tree_1 = match_value_5[1].fields[0]
                                            
                                            else: 
                                                pattern_matching_result_11 = 1
                                            
                                        
                                        else: 
                                            pattern_matching_result_11 = 1
                                        
                                    
                                    else: 
                                        pattern_matching_result_11 = 1
                                    
                                
                                else: 
                                    pattern_matching_result_11 = 1
                                
                            
                            else: 
                                pattern_matching_result_11 = 1
                            
                            if pattern_matching_result_11 == 0:
                                match_value_6 : Optional[Convert_InternalMap] = Convert_generateMap(Json(4, tree_1))
                                if match_value_6 is None:
                                    input_json : str = SimpleJson_toString(Json(4, tree_1))
                                    return to_fail(printf("Could not generate map from JSON\n %s"))(input_json)
                                
                                else: 
                                    def mapping_12(tupled_arg_5: Tuple[str, Json], input: Json=input, type_info: TypeInfo_1=type_info) -> Tuple[Any, Any]:
                                        key_6 : str = tupled_arg_5[0]
                                        return (Convert_fromJsonAs(Json(1, key_6), key_type_3) if (not Convert_isQuoted(key_6)) else Convert_fromJsonAs(SimpleJson_parseNative(key_6), key_type_3), Convert_fromJsonAs(tupled_arg_5[1], value_type_5))
                                    
                                    pairs_3 : FSharpList[Tuple[Any, Any]] = map_3(mapping_12, Convert_flattenMap(match_value_6))
                                    if ((key_type_3.tag == 6) or (key_type_3.tag == 2)) or (key_type_3.tag == 7):
                                        class ObjectExpr147:
                                            @property
                                            def Compare(self) -> Any:
                                                def arrow_146(x_14: str, y_13: str) -> int:
                                                    return compare_primitives(x_14, y_13)
                                                
                                                return arrow_146
                                            
                                        return of_list_1(pairs_3, ObjectExpr147())
                                    
                                    else: 
                                        class ObjectExpr149:
                                            @property
                                            def Compare(self) -> Any:
                                                def arrow_148(x_15: IStructuralComparable, y_14: IStructuralComparable) -> int:
                                                    return compare(x_15, y_14)
                                                
                                                return arrow_148
                                            
                                        return of_list_1(pairs_3, ObjectExpr149())
                                    
                                
                            
                            elif pattern_matching_result_11 == 1:
                                (pattern_matching_result_12, comparer_3, tree_3) = (None, None, None)
                                if match_value_5[0] is not None:
                                    if match_value_5[0].tag == 5:
                                        if match_value_5[1] is not None:
                                            if match_value_5[1].tag == 5:
                                                def arrow_156(input: Json=input, type_info: TypeInfo_1=type_info) -> bool:
                                                    tree_2 : Any = match_value_5[1].fields[0]
                                                    return is_empty_1(match_value_5[0].fields[0])
                                                
                                                if arrow_156():
                                                    pattern_matching_result_12 = 0
                                                    comparer_3 = match_value_5[0].fields[0]
                                                    tree_3 = match_value_5[1].fields[0]
                                                
                                                else: 
                                                    pattern_matching_result_12 = 1
                                                
                                            
                                            else: 
                                                pattern_matching_result_12 = 1
                                            
                                        
                                        else: 
                                            pattern_matching_result_12 = 1
                                        
                                    
                                    else: 
                                        pattern_matching_result_12 = 1
                                    
                                
                                else: 
                                    pattern_matching_result_12 = 1
                                
                                if pattern_matching_result_12 == 0:
                                    class ObjectExpr151:
                                        @property
                                        def Compare(self) -> Any:
                                            def arrow_150(x_16: str, y_15: str) -> int:
                                                return compare_primitives(x_16, y_15)
                                            
                                            return arrow_150
                                        
                                    input_mut = Json(5, of_list_1(Convert_flatteFable3Map(tree_3), ObjectExpr151()))
                                    type_info_mut = type_info
                                    continue
                                
                                elif pattern_matching_result_12 == 1:
                                    def mapping_13(tupled_arg_6: Tuple[str, Json], input: Json=input, type_info: TypeInfo_1=type_info) -> Tuple[str, Any]:
                                        key_7 : str = tupled_arg_6[0]
                                        return ((Convert_fromJsonAs(Json(1, key_7), key_type_3) if (True if is_primitive(key_type_3) else enum_union(key_type_3)) else Convert_fromJsonAs(SimpleJson_parseNative(key_7), key_type_3)) if (not Convert_isQuoted(key_7)) else Convert_fromJsonAs(SimpleJson_parseNative(key_7), key_type_3), Convert_fromJsonAs(tupled_arg_6[1], value_type_5))
                                    
                                    pairs_4 : FSharpList[Tuple[str, Any]] = map_3(mapping_13, to_list_1(map))
                                    if ((key_type_3.tag == 6) or (key_type_3.tag == 2)) or (key_type_3.tag == 7):
                                        class ObjectExpr153:
                                            @property
                                            def Compare(self) -> Any:
                                                def arrow_152(x_17: str, y_16: str) -> int:
                                                    return compare_primitives(x_17, y_16)
                                                
                                                return arrow_152
                                            
                                        return of_list_1(pairs_4, ObjectExpr153())
                                    
                                    else: 
                                        class ObjectExpr155:
                                            @property
                                            def Compare(self) -> Any:
                                                def arrow_154(x_18: IStructuralComparable, y_17: IStructuralComparable) -> int:
                                                    return compare(x_18, y_17)
                                                
                                                return arrow_154
                                            
                                        return of_list_1(pairs_4, ObjectExpr155())
                                    
                                
                            
                        
                        elif pattern_matching_result_9 == 15:
                            arg20_16 : str = full_name(get_type_1())
                            arg10_30 : str = SimpleJson_toString(input)
                            return to_fail(printf("Cannot convert %s to %s"))(arg10_30)(arg20_16)
                        
                        elif pattern_matching_result_9 == 16:
                            arg20_17 : str = JSON.stringify(type_info)
                            arg10_31 : str = SimpleJson_toString(input)
                            return to_fail(printf("Cannot convert %s to %s"))(arg10_31)(arg20_17)
                        
                    
                
            
        
        break


def Convert_fromJson(json: Json, type_info: TypeInfo_1) -> _T:
    return Convert_fromJsonAs(json, type_info)


def Convert_quoteText(input_text: str) -> str:
    return Convert_betweenQuotes(input_text)


def Convert_serialize(value_mut: Any, type_info_mut: TypeInfo_1) -> str:
    while True:
        (value, type_info) = (value_mut, type_info_mut)
        if type_info.tag == 2:
            content : str = value
            if content is None:
                return "null"
            
            else: 
                return Convert_quoteText(content)
            
        
        elif type_info.tag == 0:
            return "null"
        
        elif (type_info.tag == 9) or (type_info.tag == 8):
            if Number.is_na_n(value):
                return Convert_quoteText("NaN")
            
            else: 
                return to_string(value)
            
        
        elif type_info.tag == 1:
            return Convert_quoteText(value)
        
        elif (((((((type_info.tag == 13) or (type_info.tag == 14)) or (type_info.tag == 3)) or (type_info.tag == 4)) or (type_info.tag == 11)) or (type_info.tag == 36)) or (type_info.tag == 18)) or (type_info.tag == 6):
            return int32_to_string(value)
        
        elif (type_info.tag == 5) or (type_info.tag == 12):
            return Convert_betweenQuotes(int64_to_string(value))
        
        elif type_info.tag == 17:
            return Convert_betweenQuotes(int64_to_string(value))
        
        elif type_info.tag == 10:
            return Convert_betweenQuotes(to_string_1(value))
        
        elif type_info.tag == 7:
            if value:
                return "true"
            
            else: 
                return "false"
            
        
        elif type_info.tag == 19:
            def arrow_158(value: Any=value, type_info: TypeInfo_1=type_info) -> str:
                copy_of_struct : str = value
                return str(copy_of_struct)
            
            return Convert_betweenQuotes(arrow_158())
        
        elif type_info.tag == 21:
            return Convert_betweenQuotes(to_string(value))
        
        elif type_info.tag == 15:
            def arrow_159(value: Any=value, type_info: TypeInfo_1=type_info) -> str:
                copy_of_struct_1 : Any = value
                return to_string_2(copy_of_struct_1, "O")
            
            return Convert_betweenQuotes(arrow_159())
        
        elif type_info.tag == 16:
            def arrow_160(value: Any=value, type_info: TypeInfo_1=type_info) -> str:
                copy_of_struct_2 : Any = value
                return to_string_2(copy_of_struct_2, "O")
            
            return Convert_betweenQuotes(arrow_160())
        
        elif type_info.tag == 37:
            def mapping(field: RecordField, value: Any=value, type_info: TypeInfo_1=type_info) -> str:
                arg20 : str = Convert_serialize(get_record_field(value, field.PropertyInfo), field.FieldType)
                return to_text(printf("\"%s\": %s"))(field.FieldName)(arg20)
            
            return ("{" + join(", ", map_2(mapping, type_info.fields[0]()[0], None))) + "}"
        
        elif type_info.tag == 33:
            element_type : TypeInfo_1 = type_info.fields[0]()
            def mapping_1(element: Any=None, value: Any=value, type_info: TypeInfo_1=type_info) -> str:
                return Convert_serialize(element, element_type)
            
            return ("[" + join(", ", map_4(mapping_1, value))) + "]"
        
        elif type_info.tag == 34:
            element_type_1 : TypeInfo_1 = type_info.fields[0]()
            def mapping_2(element_1: Any=None, value: Any=value, type_info: TypeInfo_1=type_info) -> str:
                return Convert_serialize(element_1, element_type_1)
            
            return ("[" + join(", ", map_4(mapping_2, value))) + "]"
        
        elif type_info.tag == 27:
            element_type_2 : TypeInfo_1 = type_info.fields[0]()
            def mapping_3(element_2: IComparable[Any], value: Any=value, type_info: TypeInfo_1=type_info) -> str:
                return Convert_serialize(element_2, element_type_2)
            
            return ("[" + join(", ", map_4(mapping_3, value))) + "]"
        
        elif type_info.tag == 28:
            element_type_3 : TypeInfo_1 = type_info.fields[0]()
            def mapping_4(element_3: Any=None, value: Any=value, type_info: TypeInfo_1=type_info) -> str:
                return Convert_serialize(element_3, element_type_3)
            
            return ("[" + join(", ", map_2(mapping_4, value, None))) + "]"
        
        elif type_info.tag == 26:
            element_type_4 : TypeInfo_1 = type_info.fields[0]()
            def mapping_5(element_4: Any=None, value: Any=value, type_info: TypeInfo_1=type_info) -> str:
                return Convert_serialize(element_4, element_type_4)
            
            return ("[" + join(", ", map_3(mapping_5, value))) + "]"
        
        elif type_info.tag == 29:
            element_type_5 : TypeInfo_1 = type_info.fields[0]()
            def mapping_6(element_5: Any=None, value: Any=value, type_info: TypeInfo_1=type_info) -> str:
                return Convert_serialize(element_5, element_type_5)
            
            return ("[" + join(", ", map_2(mapping_6, to_array_1(value), None))) + "]"
        
        elif type_info.tag == 25:
            match_value : Optional[Any] = value
            if match_value is not None:
                value_mut = value_86(match_value)
                type_info_mut = type_info.fields[0]()
                continue
            
            else: 
                return "null"
            
        
        elif type_info.tag == 38:
            pattern_input_1 : Tuple[List[UnionCase], Any] = type_info.fields[0]()
            pattern_input_2 : Tuple[Any, List[Any]] = get_union_fields(value, pattern_input_1[1])
            used_case : Any = pattern_input_2[0]
            fields : List[Any] = pattern_input_2[1]
            def predicate(case: UnionCase, value: Any=value, type_info: TypeInfo_1=type_info) -> bool:
                return case.CaseName == name_2(used_case)
            
            case_types : List[TypeInfo_1] = find_1(predicate, pattern_input_1[0]).CaseTypes
            if True if enum_union(type_info) else (len(case_types) == 0):
                return Convert_betweenQuotes(name_2(used_case))
            
            elif len(case_types) == 1:
                return ((("{" + Convert_betweenQuotes(name_2(used_case))) + ": ") + Convert_serialize(fields[0], case_types[0])) + "}"
            
            else: 
                def mapping_7(index: int, case_type: TypeInfo_1, value: Any=value, type_info: TypeInfo_1=type_info) -> str:
                    return Convert_serialize(fields[index], case_type)
                
                serialized_fields_1 : str = join(", ", map_indexed(mapping_7, case_types, None))
                return (((("{" + Convert_betweenQuotes(name_2(used_case))) + ": ") + "[") + serialized_fields_1) + "] }"
            
        
        elif type_info.tag == 31:
            pattern_input_3 : Tuple[TypeInfo_1, TypeInfo_1] = type_info.fields[0]()
            key_type : TypeInfo_1 = pattern_input_3[0]
            def mapping_8(tupled_arg: Tuple[IComparable[Any], Any], value: Any=value, type_info: TypeInfo_1=type_info) -> str:
                serialized_key : str = Convert_serialize(tupled_arg[0], key_type)
                serialized_value : str = Convert_serialize(tupled_arg[1], pattern_input_3[1])
                if True if is_primitive(key_type) else enum_union(key_type):
                    if not Convert_isQuoted(serialized_key):
                        return (Convert_quoteText(serialized_key) + ": ") + serialized_value
                    
                    else: 
                        return (serialized_key + ": ") + serialized_value
                    
                
                else: 
                    return ((("[" + serialized_key) + ", ") + serialized_value) + "]"
                
            
            serialized_values : str = join(", ", map_2(mapping_8, to_array_2(value), None))
            if True if is_primitive(key_type) else enum_union(key_type):
                return ("{" + serialized_values) + "}"
            
            else: 
                return ("[" + serialized_values) + "]"
            
        
        elif type_info.tag == 32:
            pattern_input_4 : Tuple[TypeInfo_1, TypeInfo_1, Any] = type_info.fields[0]()
            key_type_1 : TypeInfo_1 = pattern_input_4[0]
            def mapping_9(pair: Any, value: Any=value, type_info: TypeInfo_1=type_info) -> str:
                pattern_input_5 : Tuple[IComparable[Any], Any] = (pair[0], pair[1])
                serialized_key_1 : str = Convert_serialize(pattern_input_5[0], key_type_1)
                serialized_value_1 : str = Convert_serialize(pattern_input_5[1], pattern_input_4[1])
                if True if is_primitive(key_type_1) else enum_union(key_type_1):
                    if not Convert_isQuoted(serialized_key_1):
                        return (Convert_betweenQuotes(serialized_key_1) + ": ") + serialized_value_1
                    
                    else: 
                        return (serialized_key_1 + ": ") + serialized_value_1
                    
                
                else: 
                    return ((("[" + serialized_key_1) + ", ") + serialized_value_1) + "]"
                
            
            serialized_values_1 : str = join(", ", map_4(mapping_9, value))
            if True if is_primitive(key_type_1) else enum_union(key_type_1):
                return ("{" + serialized_values_1) + "}"
            
            else: 
                return ("[" + serialized_values_1) + "]"
            
        
        elif type_info.tag == 30:
            tuple_types : List[TypeInfo_1] = type_info.fields[0]()
            if len(tuple_types) == 1:
                return ("[" + Convert_serialize(value, tuple_types[0])) + "]"
            
            else: 
                def mapping_10(index_1: int, element_6: Any=None, value: Any=value, type_info: TypeInfo_1=type_info) -> str:
                    return Convert_serialize(element_6, tuple_types[index_1])
                
                return ("[" + join(", ", map_indexed(mapping_10, value, None))) + "]"
            
        
        elif type_info.tag == 20:
            return json_1.dumps(value)
        
        elif type_info.tag == 22:
            return json_1.dumps(value)
        
        else: 
            return "null"
        
        break


