from __future__ import annotations
from typing import (List, Any, Optional, TypeVar, Callable, MutableSequence, Tuple)
from ...fable_library.array import (map, choose, append)
from ...fable_library.option import (default_arg, some)
from ...fs_hafas_python.context import (Context, CommonData, Profile__get_parseOperator, Profile__get_parseLine, Profile__get_parseHint, Profile__get_parseIcon, Profile__get_parsePolyline, Profile__get_parseLocations)
from ...fs_hafas_python.extra_types import Icon
from ...fs_hafas_python.types_hafas_client import (Operator, Line, FeatureCollection)
from ...fs_hafas_python.types_raw_hafas_client import (RawCommon, RawOp, RawProd, RawRem, RawIco, RawPoly, RawMsg)

_A = TypeVar("_A")

_B = TypeVar("_B")

def update_operators(ctx: Context, ops: List[Operator]) -> Context:
    def arrow_358(ctx: Context=ctx, ops: List[Operator]=ops) -> CommonData:
        input_record : CommonData = ctx.common
        return CommonData(ops, input_record.locations, input_record.lines, input_record.hints, input_record.icons, input_record.polylines)
    
    return Context(ctx.profile, ctx.opt, arrow_358(), ctx.res)


def update_lines(ctx: Context, lines: List[Line]) -> Context:
    def arrow_359(ctx: Context=ctx, lines: List[Line]=lines) -> CommonData:
        input_record : CommonData = ctx.common
        return CommonData(input_record.operators, input_record.locations, lines, input_record.hints, input_record.icons, input_record.polylines)
    
    return Context(ctx.profile, ctx.opt, arrow_359(), ctx.res)


def parse_common(ctx: Context, c: RawCommon) -> CommonData:
    def mapping(op: RawOp, ctx: Context=ctx, c: RawCommon=c) -> Operator:
        return Profile__get_parseOperator(ctx.profile)(ctx)(op)
    
    ctx1 : Context = update_operators(ctx, map(mapping, default_arg(c.op_l, []), None))
    def mapping_1(p: RawProd, ctx: Context=ctx, c: RawCommon=c) -> Line:
        return Profile__get_parseLine(ctx1.profile)(ctx1)(p)
    
    ctx2 : Context = update_lines(ctx, map(mapping_1, default_arg(c.prod_l, []), None))
    def mapping_2(p_1: RawRem, ctx: Context=ctx, c: RawCommon=c) -> Optional[Any]:
        return Profile__get_parseHint(ctx2.profile)(ctx2)(p_1)
    
    hints : List[Optional[Any]] = map(mapping_2, default_arg(c.rem_l, []), None)
    def chooser(x: Optional[Icon]=None, ctx: Context=ctx, c: RawCommon=c) -> Optional[Icon]:
        return x
    
    def mapping_3(i: RawIco, ctx: Context=ctx, c: RawCommon=c) -> Optional[Icon]:
        return Profile__get_parseIcon(ctx2.profile)(ctx2)(i)
    
    icons : List[Icon] = choose(chooser, map(mapping_3, default_arg(c.ico_l, []), None), None)
    def mapping_4(p_2: RawPoly, ctx: Context=ctx, c: RawCommon=c) -> FeatureCollection:
        return Profile__get_parsePolyline(ctx2.profile)(ctx2)(p_2)
    
    polylines : List[FeatureCollection] = map(mapping_4, default_arg(c.poly_l, []), None)
    return CommonData(ctx2.common.operators, Profile__get_parseLocations(ctx2.profile)(ctx2)(default_arg(c.loc_l, [])), ctx2.common.lines, hints, icons, polylines)


def get_element_at(index: int, arr: List[_A]) -> Optional[_A]:
    if index < len(arr):
        return some(arr[index])
    
    else: 
        return None
    


def get_element_at_some(index: Optional[int], arr: List[_A]) -> Optional[_A]:
    (pattern_matching_result, index_2) = (None, None)
    if index is not None:
        if index < len(arr):
            pattern_matching_result = 0
            index_2 = index
        
        else: 
            pattern_matching_result = 1
        
    
    else: 
        pattern_matching_result = 1
    
    if pattern_matching_result == 0:
        return some(arr[index_2])
    
    elif pattern_matching_result == 1:
        return None
    


def get_array(common: Optional[RawCommon], getter: Callable[[RawCommon], Optional[List[_A]]]) -> List[_A]:
    if common is None:
        return []
    
    else: 
        match_value : Optional[List[_A]] = getter(common)
        if match_value is None:
            return []
        
        else: 
            return match_value
        
    


def map_index_array(common: Optional[RawCommon], get_target_array: Callable[[RawCommon], Optional[List[_A]]], index_arr: Optional[MutableSequence[int]]=None) -> List[_A]:
    elements : List[_A] = get_array(common, get_target_array)
    if index_arr is None:
        return []
    
    else: 
        def chooser(x: Optional[_A]=None, common: Optional[RawCommon]=common, get_target_array: Callable[[RawCommon], Optional[List[_A]]]=get_target_array, index_arr: Optional[MutableSequence[int]]=index_arr) -> Optional[_A]:
            return x
        
        def mapping(i: int, common: Optional[RawCommon]=common, get_target_array: Callable[[RawCommon], Optional[List[_A]]]=get_target_array, index_arr: Optional[MutableSequence[int]]=index_arr) -> Optional[_A]:
            return get_element_at(i, elements)
        
        return choose(chooser, map(mapping, index_arr, None), None)
    


def append_some_array(arr1: Optional[List[_A]]=None, arr2: Optional[List[_A]]=None) -> Optional[List[_A]]:
    match_value : Tuple[Optional[List[_A]], Optional[List[_A]]] = (arr1, arr2)
    if match_value[0] is None:
        if match_value[1] is not None:
            arr2_2 : List[_A] = match_value[1]
            return arr2_2
        
        else: 
            return None
        
    
    elif match_value[1] is None:
        arr1_2 : List[_A] = match_value[0]
        return arr1_2
    
    else: 
        arr1_1 : List[_A] = match_value[0]
        arr2_1 : List[_A] = match_value[1]
        return append(arr1_1, arr2_1, None)
    


def map_array(target_array: List[_B], get_index: Callable[[_A], Optional[int]], source_array: Optional[List[_A]]=None) -> List[_B]:
    if source_array is None:
        return []
    
    else: 
        def chooser(x: Optional[_B]=None, target_array: List[_B]=target_array, get_index: Callable[[_A], Optional[int]]=get_index, source_array: Optional[List[_A]]=source_array) -> Optional[_B]:
            return x
        
        def mapping(elt: Optional[_A]=None, target_array: List[_B]=target_array, get_index: Callable[[_A], Optional[int]]=get_index, source_array: Optional[List[_A]]=source_array) -> Optional[_B]:
            return get_element_at_some(get_index(elt), target_array)
        
        return choose(chooser, map(mapping, source_array, None), None)
    


def to_option(arr: List[_A]) -> Optional[List[_A]]:
    if len(arr) > 0:
        return arr
    
    else: 
        return None
    


def msg_lto_remarks(ctx: Context, msg_l: Optional[List[RawMsg]]=None) -> Optional[List[Any]]:
    def chooser(x_1: Optional[Any]=None, ctx: Context=ctx, msg_l: Optional[List[RawMsg]]=msg_l) -> Optional[Any]:
        return x_1
    
    def get_index(x: RawMsg, ctx: Context=ctx, msg_l: Optional[List[RawMsg]]=msg_l) -> Optional[int]:
        return x.rem_x
    
    return to_option(choose(chooser, map_array(ctx.common.hints, get_index, msg_l), None))


