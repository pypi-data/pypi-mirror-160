from __future__ import annotations
from typing import (Any, Optional, Tuple, List, TypeVar, Callable)
from ..fable_library.array import (map, for_all)
from ..fable_library.mutable_map import Dictionary
from ..fable_library.reflection import (full_name, is_record, name, get_record_elements, get_generics, is_union, get_union_case_fields, get_union_cases, is_function, get_function_elements, is_array, get_element_type, is_tuple, get_tuple_elements, is_enum, get_enum_underlying_type, equals)
from ..fable_library.seq import (to_array, delay, append, singleton, collect)
from ..fable_library.string import trim_start
from ..fable_library.util import (IEnumerable, Lazy, structural_hash)
from .type_info import (TypeInfo, RecordField, UnionCase)

_A_ = TypeVar("_A_")

def _007CPrimitiveType_007C__007C(prim_type: Any) -> Optional[TypeInfo]:
    match_value : str = full_name(prim_type)
    (pattern_matching_result,) = (None,)
    if match_value == "System.String":
        pattern_matching_result = 0
    
    elif match_value == "System.Char":
        pattern_matching_result = 1
    
    elif match_value == "System.Int16":
        pattern_matching_result = 2
    
    elif match_value == "System.Int32":
        pattern_matching_result = 3
    
    elif match_value == "Microsoft.FSharp.Core.int64`1":
        pattern_matching_result = 4
    
    elif match_value == "System.Int64":
        pattern_matching_result = 4
    
    elif match_value == "System.UInt16":
        pattern_matching_result = 5
    
    elif match_value == "System.UInt32":
        pattern_matching_result = 6
    
    elif match_value == "System.UInt64":
        pattern_matching_result = 7
    
    elif match_value == "System.DateTime":
        pattern_matching_result = 8
    
    elif match_value == "System.TimeSpan":
        pattern_matching_result = 9
    
    elif match_value == "System.DateTimeOffset":
        pattern_matching_result = 10
    
    elif match_value == "System.Boolean":
        pattern_matching_result = 11
    
    elif match_value == "System.Single":
        pattern_matching_result = 12
    
    elif match_value == "System.Double":
        pattern_matching_result = 13
    
    elif match_value == "Microsoft.FSharp.Core.decimal`1":
        pattern_matching_result = 14
    
    elif match_value == "System.Decimal":
        pattern_matching_result = 14
    
    elif match_value == "System.Numerics.BigInteger":
        pattern_matching_result = 15
    
    elif match_value == "Microsoft.FSharp.Core.Unit":
        pattern_matching_result = 16
    
    elif match_value == "System.Guid":
        pattern_matching_result = 17
    
    elif match_value == "System.Byte":
        pattern_matching_result = 18
    
    elif match_value == "System.SByte":
        pattern_matching_result = 19
    
    elif match_value == "System.Object":
        pattern_matching_result = 20
    
    elif match_value == "System.Uri":
        pattern_matching_result = 21
    
    else: 
        pattern_matching_result = 22
    
    if pattern_matching_result == 0:
        return TypeInfo(2)
    
    elif pattern_matching_result == 1:
        return TypeInfo(1)
    
    elif pattern_matching_result == 2:
        return TypeInfo(11)
    
    elif pattern_matching_result == 3:
        return TypeInfo(6)
    
    elif pattern_matching_result == 4:
        return TypeInfo(12)
    
    elif pattern_matching_result == 5:
        return TypeInfo(3)
    
    elif pattern_matching_result == 6:
        return TypeInfo(4)
    
    elif pattern_matching_result == 7:
        return TypeInfo(5)
    
    elif pattern_matching_result == 8:
        return TypeInfo(15)
    
    elif pattern_matching_result == 9:
        return TypeInfo(18)
    
    elif pattern_matching_result == 10:
        return TypeInfo(16)
    
    elif pattern_matching_result == 11:
        return TypeInfo(7)
    
    elif pattern_matching_result == 12:
        return TypeInfo(8)
    
    elif pattern_matching_result == 13:
        return TypeInfo(9)
    
    elif pattern_matching_result == 14:
        return TypeInfo(10)
    
    elif pattern_matching_result == 15:
        return TypeInfo(17)
    
    elif pattern_matching_result == 16:
        return TypeInfo(0)
    
    elif pattern_matching_result == 17:
        return TypeInfo(19)
    
    elif pattern_matching_result == 18:
        return TypeInfo(13)
    
    elif pattern_matching_result == 19:
        return TypeInfo(14)
    
    elif pattern_matching_result == 20:
        return TypeInfo(20)
    
    elif pattern_matching_result == 21:
        return TypeInfo(21)
    
    elif pattern_matching_result == 22:
        return None
    


def _007CRecordType_007C__007C(t: Any) -> Optional[List[Tuple[Any, str, Any]]]:
    if is_record(t):
        def mapping(field: Any, t: Any=t) -> Tuple[Any, str, Any]:
            return (field, name(field), field[1])
        
        return map(mapping, get_record_elements(t), None)
    
    else: 
        return None
    


def _007CSetType_007C__007C(t: Any) -> Optional[Any]:
    if trim_start(full_name(t), "$").find("Microsoft.FSharp.Collections.FSharpSet`1") == 0:
        return get_generics(t)[0]
    
    else: 
        return None
    


def _007CNullable_007C__007C(t: Any) -> Optional[Any]:
    if trim_start(full_name(t), "$").find("System.Nullable`1") == 0:
        return get_generics(t)[0]
    
    else: 
        return None
    


def _007CUnionType_007C__007C(t: Any) -> Optional[List[Tuple[str, Any, List[Any]]]]:
    if is_union(t):
        def mapping_1(info: Any, t: Any=t) -> Tuple[str, Any, List[Any]]:
            def mapping(prop: Any, info: Any=info) -> Any:
                return prop[1]
            
            return (name(info), info, map(mapping, get_union_case_fields(info), None))
        
        return map(mapping_1, get_union_cases(t), None)
    
    else: 
        return None
    


def _007CMapType_007C__007C(t: Any) -> Optional[Tuple[Any, Any]]:
    if trim_start(full_name(t), "$").find("Microsoft.FSharp.Collections.FSharpMap`2") == 0:
        gen_args : List[Any] = get_generics(t)
        return (gen_args[0], gen_args[1])
    
    else: 
        return None
    


def _007CListType_007C__007C(t: Any) -> Optional[Any]:
    if trim_start(full_name(t), "$").find("Microsoft.FSharp.Collections.FSharpList`1") == 0:
        return get_generics(t)[0]
    
    else: 
        return None
    


def flatten_func_types(type_def: Any) -> List[Any]:
    def arrow_8(type_def: Any=type_def) -> IEnumerable[Any]:
        if is_function(type_def):
            pattern_input : Tuple[Any, Any] = get_function_elements(type_def)
            def arrow_7(__unit: Any=None) -> IEnumerable[Any]:
                return flatten_func_types(pattern_input[1])
            
            return append(flatten_func_types(pattern_input[0]), delay(arrow_7))
        
        else: 
            return singleton(type_def)
        
    
    return to_array(delay(arrow_8))


def _007CFuncType_007C__007C(t: Any) -> Optional[List[Any]]:
    if is_function(t):
        return flatten_func_types(t)
    
    else: 
        return None
    


def _007CArrayType_007C__007C(t: Any) -> Optional[Any]:
    if is_array(t):
        return get_element_type(t)
    
    else: 
        return None
    


def _007COptionType_007C__007C(t: Any) -> Optional[Any]:
    if trim_start(full_name(t), "$").find("Microsoft.FSharp.Core.FSharpOption`1") == 0:
        return get_generics(t)[0]
    
    else: 
        return None
    


def _007CTupleType_007C__007C(t: Any) -> Optional[List[Any]]:
    if is_tuple(t):
        return get_tuple_elements(t)
    
    else: 
        return None
    


def _007CSeqType_007C__007C(t: Any) -> Optional[Any]:
    if trim_start(full_name(t), "$").find("System.Collections.Generic.IEnumerable`1") == 0:
        return get_generics(t)[0]
    
    else: 
        return None
    


def _007CDictionaryType_007C__007C(t: Any) -> Optional[Tuple[Any, Any]]:
    if trim_start(full_name(t), "$").find("System.Collections.Generic.Dictionary") == 0:
        gen_args : List[Any] = get_generics(t)
        return (gen_args[0], gen_args[1])
    
    else: 
        return None
    


def _007CResizeArrayType_007C__007C(t: Any) -> Optional[Any]:
    if trim_start(full_name(t), "$").find("System.Collections.Generic.List") == 0:
        return get_generics(t)[0]
    
    else: 
        return None
    


def _007CHashSetType_007C__007C(t: Any) -> Optional[Any]:
    if trim_start(full_name(t), "$").find("System.Collections.Generic.HashSet") == 0:
        return get_generics(t)[0]
    
    else: 
        return None
    


def _007CAsyncType_007C__007C(t: Any) -> Optional[Any]:
    if trim_start(full_name(t), "$").find("Microsoft.FSharp.Control.FSharpAsync`1") == 0:
        return get_generics(t)[0]
    
    else: 
        return None
    


def _007CPromiseType_007C__007C(t: Any) -> Optional[Any]:
    if trim_start(full_name(t), "$").find("Fable.Core.JS.Promise`1") == 0:
        return get_generics(t)[0]
    
    else: 
        return None
    


def lazy_to_delayed(l: Any, unit_var0: None) -> _A_:
    return l.Value


def _007CEnumType_007C__007C(t: Any) -> Optional[Any]:
    if is_enum(t):
        return get_enum_underlying_type(t)
    
    else: 
        return None
    


def _createTypeInfo(resolved_type: Any) -> TypeInfo:
    active_pattern_result571 : Optional[TypeInfo] = _007CPrimitiveType_007C__007C(resolved_type)
    if active_pattern_result571 is not None:
        type_info : TypeInfo = active_pattern_result571
        return type_info
    
    else: 
        active_pattern_result570 : Optional[List[Any]] = _007CFuncType_007C__007C(resolved_type)
        if active_pattern_result570 is not None:
            types : List[Any] = active_pattern_result570
            def arrow_14(resolved_type: Any=resolved_type) -> Callable[[], List[TypeInfo]]:
                def arrow_12(__unit: Any=None) -> List[TypeInfo]:
                    def arrow_11(resolved_type_1: Any) -> TypeInfo:
                        return create_type_info(resolved_type_1)
                    
                    return map(arrow_11, types, None)
                
                l : Any = Lazy(arrow_12)
                def arrow_13(__unit: Any=None) -> List[TypeInfo]:
                    return lazy_to_delayed(l, None)
                
                return arrow_13
            
            return TypeInfo(35, arrow_14())
        
        else: 
            active_pattern_result569 : Optional[List[Tuple[Any, str, Any]]] = _007CRecordType_007C__007C(resolved_type)
            if active_pattern_result569 is not None:
                fields : List[Tuple[Any, str, Any]] = active_pattern_result569
                def arrow_17(resolved_type: Any=resolved_type) -> Tuple[List[RecordField], Any]:
                    def arrow_16(__unit: Any=None) -> IEnumerable[RecordField]:
                        def arrow_15(match_value: Tuple[Any, str, Any]) -> IEnumerable[RecordField]:
                            return singleton(RecordField(match_value[1], create_type_info(match_value[2]), match_value[0]))
                        
                        return collect(arrow_15, fields)
                    
                    return (to_array(delay(arrow_16)), resolved_type)
                
                return TypeInfo(37, arrow_17)
            
            else: 
                active_pattern_result568 : Optional[List[Tuple[str, Any, List[Any]]]] = _007CUnionType_007C__007C(resolved_type)
                if active_pattern_result568 is not None:
                    cases : List[Tuple[str, Any, List[Any]]] = active_pattern_result568
                    def arrow_21(resolved_type: Any=resolved_type) -> Tuple[List[UnionCase], Any]:
                        def arrow_20(__unit: Any=None) -> IEnumerable[UnionCase]:
                            def arrow_19(match_value_1: Tuple[str, Any, List[Any]]) -> IEnumerable[UnionCase]:
                                def arrow_18(resolved_type_2: Any) -> TypeInfo:
                                    return create_type_info(resolved_type_2)
                                
                                return singleton(UnionCase(match_value_1[0], map(arrow_18, match_value_1[2], None), match_value_1[1]))
                            
                            return collect(arrow_19, cases)
                        
                        return (to_array(delay(arrow_20)), resolved_type)
                    
                    l_1 : Any = Lazy(arrow_21)
                    def arrow_22(resolved_type: Any=resolved_type) -> Tuple[List[UnionCase], Any]:
                        return lazy_to_delayed(l_1, None)
                    
                    return TypeInfo(38, arrow_22)
                
                else: 
                    active_pattern_result567 : Optional[Any] = _007CEnumType_007C__007C(resolved_type)
                    if active_pattern_result567 is not None:
                        elem_type : Any = active_pattern_result567
                        def arrow_25(resolved_type: Any=resolved_type) -> Callable[[], Tuple[TypeInfo, Any]]:
                            def arrow_23(__unit: Any=None) -> Tuple[TypeInfo, Any]:
                                return (create_type_info(elem_type), resolved_type)
                            
                            l_2 : Any = Lazy(arrow_23)
                            def arrow_24(__unit: Any=None) -> Tuple[TypeInfo, Any]:
                                return lazy_to_delayed(l_2, None)
                            
                            return arrow_24
                        
                        return TypeInfo(36, arrow_25())
                    
                    else: 
                        active_pattern_result566 : Optional[Any] = _007CListType_007C__007C(resolved_type)
                        if active_pattern_result566 is not None:
                            elem_type_1 : Any = active_pattern_result566
                            def arrow_26(resolved_type: Any=resolved_type) -> TypeInfo:
                                return create_type_info(elem_type_1)
                            
                            return TypeInfo(26, arrow_26)
                        
                        else: 
                            active_pattern_result565 : Optional[Any] = _007CResizeArrayType_007C__007C(resolved_type)
                            if active_pattern_result565 is not None:
                                elem_type_2 : Any = active_pattern_result565
                                def arrow_29(resolved_type: Any=resolved_type) -> Callable[[], TypeInfo]:
                                    def arrow_27(__unit: Any=None) -> TypeInfo:
                                        return create_type_info(elem_type_2)
                                    
                                    l_3 : Any = Lazy(arrow_27)
                                    def arrow_28(__unit: Any=None) -> TypeInfo:
                                        return lazy_to_delayed(l_3, None)
                                    
                                    return arrow_28
                                
                                return TypeInfo(33, arrow_29())
                            
                            else: 
                                active_pattern_result564 : Optional[Any] = _007CHashSetType_007C__007C(resolved_type)
                                if active_pattern_result564 is not None:
                                    elem_type_3 : Any = active_pattern_result564
                                    def arrow_32(resolved_type: Any=resolved_type) -> Callable[[], TypeInfo]:
                                        def arrow_30(__unit: Any=None) -> TypeInfo:
                                            return create_type_info(elem_type_3)
                                        
                                        l_4 : Any = Lazy(arrow_30)
                                        def arrow_31(__unit: Any=None) -> TypeInfo:
                                            return lazy_to_delayed(l_4, None)
                                        
                                        return arrow_31
                                    
                                    return TypeInfo(34, arrow_32())
                                
                                else: 
                                    active_pattern_result563 : Optional[Any] = _007CArrayType_007C__007C(resolved_type)
                                    if active_pattern_result563 is not None:
                                        elem_type_4 : Any = active_pattern_result563
                                        def arrow_35(resolved_type: Any=resolved_type) -> Callable[[], TypeInfo]:
                                            def arrow_33(__unit: Any=None) -> TypeInfo:
                                                return create_type_info(elem_type_4)
                                            
                                            l_5 : Any = Lazy(arrow_33)
                                            def arrow_34(__unit: Any=None) -> TypeInfo:
                                                return lazy_to_delayed(l_5, None)
                                            
                                            return arrow_34
                                        
                                        return TypeInfo(28, arrow_35())
                                    
                                    else: 
                                        active_pattern_result562 : Optional[List[Any]] = _007CTupleType_007C__007C(resolved_type)
                                        if active_pattern_result562 is not None:
                                            types_1 : List[Any] = active_pattern_result562
                                            def arrow_39(resolved_type: Any=resolved_type) -> Callable[[], List[TypeInfo]]:
                                                def arrow_37(__unit: Any=None) -> List[TypeInfo]:
                                                    def arrow_36(resolved_type_3: Any) -> TypeInfo:
                                                        return create_type_info(resolved_type_3)
                                                    
                                                    return map(arrow_36, types_1, None)
                                                
                                                l_6 : Any = Lazy(arrow_37)
                                                def arrow_38(__unit: Any=None) -> List[TypeInfo]:
                                                    return lazy_to_delayed(l_6, None)
                                                
                                                return arrow_38
                                            
                                            return TypeInfo(30, arrow_39())
                                        
                                        else: 
                                            active_pattern_result561 : Optional[Any] = _007COptionType_007C__007C(resolved_type)
                                            if active_pattern_result561 is not None:
                                                elem_type_5 : Any = active_pattern_result561
                                                def arrow_40(resolved_type: Any=resolved_type) -> TypeInfo:
                                                    return create_type_info(elem_type_5)
                                                
                                                return TypeInfo(25, arrow_40)
                                            
                                            else: 
                                                active_pattern_result560 : Optional[Any] = _007CNullable_007C__007C(resolved_type)
                                                if active_pattern_result560 is not None:
                                                    elem_type_6 : Any = active_pattern_result560
                                                    def arrow_43(resolved_type: Any=resolved_type) -> Callable[[], TypeInfo]:
                                                        def arrow_41(__unit: Any=None) -> TypeInfo:
                                                            return create_type_info(elem_type_6)
                                                        
                                                        l_7 : Any = Lazy(arrow_41)
                                                        def arrow_42(__unit: Any=None) -> TypeInfo:
                                                            return lazy_to_delayed(l_7, None)
                                                        
                                                        return arrow_42
                                                    
                                                    return TypeInfo(25, arrow_43())
                                                
                                                else: 
                                                    active_pattern_result559 : Optional[Any] = _007CSetType_007C__007C(resolved_type)
                                                    if active_pattern_result559 is not None:
                                                        elem_type_7 : Any = active_pattern_result559
                                                        def arrow_46(resolved_type: Any=resolved_type) -> Callable[[], TypeInfo]:
                                                            def arrow_44(__unit: Any=None) -> TypeInfo:
                                                                return create_type_info(elem_type_7)
                                                            
                                                            l_8 : Any = Lazy(arrow_44)
                                                            def arrow_45(__unit: Any=None) -> TypeInfo:
                                                                return lazy_to_delayed(l_8, None)
                                                            
                                                            return arrow_45
                                                        
                                                        return TypeInfo(27, arrow_46())
                                                    
                                                    else: 
                                                        active_pattern_result558 : Optional[Tuple[Any, Any]] = _007CMapType_007C__007C(resolved_type)
                                                        if active_pattern_result558 is not None:
                                                            key_type : Any = active_pattern_result558[0]
                                                            value_type : Any = active_pattern_result558[1]
                                                            def arrow_51(resolved_type: Any=resolved_type) -> Callable[[], Tuple[TypeInfo, TypeInfo]]:
                                                                def arrow_47(__unit: Any=None) -> Tuple[TypeInfo, TypeInfo]:
                                                                    return (create_type_info(key_type), create_type_info(value_type))
                                                                
                                                                l_9 : Any = Lazy(arrow_47)
                                                                def arrow_50(__unit: Any=None) -> Tuple[TypeInfo, TypeInfo]:
                                                                    return lazy_to_delayed(l_9, None)
                                                                
                                                                return arrow_50
                                                            
                                                            return TypeInfo(31, arrow_51())
                                                        
                                                        else: 
                                                            active_pattern_result557 : Optional[Tuple[Any, Any]] = _007CDictionaryType_007C__007C(resolved_type)
                                                            if active_pattern_result557 is not None:
                                                                key_type_1 : Any = active_pattern_result557[0]
                                                                value_type_1 : Any = active_pattern_result557[1]
                                                                def arrow_54(resolved_type: Any=resolved_type) -> Callable[[], Tuple[TypeInfo, TypeInfo, Any]]:
                                                                    def arrow_52(__unit: Any=None) -> Tuple[TypeInfo, TypeInfo, Any]:
                                                                        return (create_type_info(key_type_1), create_type_info(value_type_1), value_type_1)
                                                                    
                                                                    l_10 : Any = Lazy(arrow_52)
                                                                    def arrow_53(__unit: Any=None) -> Tuple[TypeInfo, TypeInfo, Any]:
                                                                        return lazy_to_delayed(l_10, None)
                                                                    
                                                                    return arrow_53
                                                                
                                                                return TypeInfo(32, arrow_54())
                                                            
                                                            else: 
                                                                active_pattern_result556 : Optional[Any] = _007CSeqType_007C__007C(resolved_type)
                                                                if active_pattern_result556 is not None:
                                                                    elem_type_8 : Any = active_pattern_result556
                                                                    def arrow_57(resolved_type: Any=resolved_type) -> Callable[[], TypeInfo]:
                                                                        def arrow_55(__unit: Any=None) -> TypeInfo:
                                                                            return create_type_info(elem_type_8)
                                                                        
                                                                        l_11 : Any = Lazy(arrow_55)
                                                                        def arrow_56(__unit: Any=None) -> TypeInfo:
                                                                            return lazy_to_delayed(l_11, None)
                                                                        
                                                                        return arrow_56
                                                                    
                                                                    return TypeInfo(29, arrow_57())
                                                                
                                                                else: 
                                                                    active_pattern_result555 : Optional[Any] = _007CAsyncType_007C__007C(resolved_type)
                                                                    if active_pattern_result555 is not None:
                                                                        elem_type_9 : Any = active_pattern_result555
                                                                        def arrow_60(resolved_type: Any=resolved_type) -> Callable[[], TypeInfo]:
                                                                            def arrow_58(__unit: Any=None) -> TypeInfo:
                                                                                return create_type_info(elem_type_9)
                                                                            
                                                                            l_12 : Any = Lazy(arrow_58)
                                                                            def arrow_59(__unit: Any=None) -> TypeInfo:
                                                                                return lazy_to_delayed(l_12, None)
                                                                            
                                                                            return arrow_59
                                                                        
                                                                        return TypeInfo(23, arrow_60())
                                                                    
                                                                    else: 
                                                                        active_pattern_result554 : Optional[Any] = _007CPromiseType_007C__007C(resolved_type)
                                                                        if active_pattern_result554 is not None:
                                                                            elem_type_10 : Any = active_pattern_result554
                                                                            def arrow_63(resolved_type: Any=resolved_type) -> Callable[[], TypeInfo]:
                                                                                def arrow_61(__unit: Any=None) -> TypeInfo:
                                                                                    return create_type_info(elem_type_10)
                                                                                
                                                                                l_13 : Any = Lazy(arrow_61)
                                                                                def arrow_62(__unit: Any=None) -> TypeInfo:
                                                                                    return lazy_to_delayed(l_13, None)
                                                                                
                                                                                return arrow_62
                                                                            
                                                                            return TypeInfo(24, arrow_63())
                                                                        
                                                                        else: 
                                                                            def arrow_66(resolved_type: Any=resolved_type) -> Callable[[], Any]:
                                                                                def arrow_64(__unit: Any=None) -> Any:
                                                                                    return resolved_type
                                                                                
                                                                                l_14 : Any = Lazy(arrow_64)
                                                                                def arrow_65(__unit: Any=None) -> Any:
                                                                                    return lazy_to_delayed(l_14, None)
                                                                                
                                                                                return arrow_65
                                                                            
                                                                            return TypeInfo(22, arrow_66())
                                                                        
                                                                    
                                                                
                                                            
                                                        
                                                    
                                                
                                            
                                        
                                    
                                
                            
                        
                    
                
            
        
    


class ObjectExpr69:
    @property
    def Equals(self) -> Any:
        def arrow_67(x: Any, y: Any) -> bool:
            return equals(x, y)
        
        return arrow_67
    
    @property
    def GetHashCode(self) -> Any:
        def arrow_68(x: Any) -> int:
            return structural_hash(x)
        
        return arrow_68
    

type_info_cache : Any = Dictionary([], ObjectExpr69())

def create_type_info(resolved_type: Any) -> TypeInfo:
    return _createTypeInfo(resolved_type)


def is_primitive(_arg1: TypeInfo) -> bool:
    if (((((((((((((((((_arg1.tag == 0) or (_arg1.tag == 2)) or (_arg1.tag == 3)) or (_arg1.tag == 4)) or (_arg1.tag == 5)) or (_arg1.tag == 6)) or (_arg1.tag == 7)) or (_arg1.tag == 8)) or (_arg1.tag == 9)) or (_arg1.tag == 10)) or (_arg1.tag == 11)) or (_arg1.tag == 12)) or (_arg1.tag == 13)) or (_arg1.tag == 15)) or (_arg1.tag == 16)) or (_arg1.tag == 17)) or (_arg1.tag == 19)) or (_arg1.tag == 25):
        return True
    
    else: 
        return False
    


def enum_union(_arg1: TypeInfo) -> bool:
    if _arg1.tag == 38:
        def predicate(case: UnionCase, _arg1: TypeInfo=_arg1) -> bool:
            return len(case.CaseTypes) == 0
        
        return for_all(predicate, _arg1.fields[0]()[0])
    
    else: 
        return False
    


