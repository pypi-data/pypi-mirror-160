from __future__ import annotations
from datetime import timedelta
from typing import (ByteString, Any, List, Optional, Tuple)
from ...fable_library.array import (map, fold as fold_1, sum_by, choose)
from ...fable_library.date import (create, to_string)
from ...fable_library.int32 import parse
from ...fable_library.option import default_arg
from ...fable_library.range import range_double
from ...fable_library.seq import (to_array, fold)
from ...fable_library.string import substring
from ...fable_library.types import Uint8Array
from ...fs_hafas_python.context import (Context, Profile__get_parseJourneyLeg)
from ...fs_hafas_python.extra_types import (IndexMap_2, IndexMap_2__set_Item_541DA560, IndexMap_2__ctor_2B594)
from ...fs_hafas_python.lib.transformations import Default_Journey
from ...fs_hafas_python.types_hafas_client import (Leg, Cycle, Journey, FeatureCollection)
from ...fs_hafas_python.types_raw_hafas_client import (RawOutCon, RawSec, RawFreq)
from .common import msg_lto_remarks
from .polyline import distance_of_feature_collection

def mapping(x: int) -> int:
    value : int = (1 << (7 - x)) or 0
    return int(value+0x100 if value < 0 else value) & 0xFF


bytes : ByteString = map(mapping, to_array(range_double(0, 1, 7)), Uint8Array)

def parse_scheduled_days(ctx: Context, s_days: str, year: int) -> IndexMap_2[str, bool]:
    dt : Any = create(year, 1, 1)
    source : ByteString = bytes.fromhex(s_days)
    def folder_1(m: IndexMap_2[str, bool], d: int, ctx: Context=ctx, s_days: str=s_days, year: int=year) -> IndexMap_2[str, bool]:
        def folder(m_1: IndexMap_2[str, bool], b: int, m: IndexMap_2[str, bool]=m, d: int=d) -> IndexMap_2[str, bool]:
            nonlocal dt
            IndexMap_2__set_Item_541DA560(m_1, to_string(dt, "yyyy-MM-dd"), (d & b) != 0)
            dt = dt+timedelta(days=1)
            return m_1
        
        return fold_1(folder, m, bytes)
    
    return fold(folder_1, IndexMap_2__ctor_2B594(False), source)


def parse_journey(ctx: Context, j: RawOutCon) -> Journey:
    def mapping(l: RawSec, ctx: Context=ctx, j: RawOutCon=j) -> Leg:
        return Profile__get_parseJourneyLeg(ctx.profile)(ctx)(l)(j.date)
    
    legs : List[Leg] = map(mapping, j.sec_l, None)
    def arrow_438(ctx: Context=ctx, j: RawOutCon=j) -> List[Any]:
        value : List[Any] = []
        return default_arg(msg_lto_remarks(ctx, j.msg_l), value)
    
    remarks : Optional[List[Any]] = arrow_438() if ctx.opt.remarks else None
    scheduled_days : Optional[IndexMap_2[str, bool]]
    match_value : Tuple[bool, Optional[str]] = (ctx.opt.scheduled_days, j.s_days.s_days_b)
    (pattern_matching_result,) = (None,)
    if match_value[0]:
        if match_value[1] is not None:
            pattern_matching_result = 0
        
        else: 
            pattern_matching_result = 1
        
    
    else: 
        pattern_matching_result = 1
    
    if pattern_matching_result == 0:
        scheduled_days = parse_scheduled_days(ctx, match_value[1], parse(substring(j.date, 0, 4), 511, False, 32))
    
    elif pattern_matching_result == 1:
        scheduled_days = None
    
    def arrow_441(ctx: Context=ctx, j: RawOutCon=j) -> Optional[Cycle]:
        match_value_1 : Optional[RawFreq] = j.freq
        if match_value_1 is None:
            return None
        
        else: 
            freq : RawFreq = match_value_1
            match_value_2 : Tuple[Optional[int], Optional[int]] = (freq.min_c, freq.max_c)
            def arrow_439(__unit: Any=None) -> Optional[Cycle]:
                max_c : int = match_value_2[1] or 0
                min_c : int = match_value_2[0] or 0
                return Cycle(min_c * 60, max_c * 60, freq.num_c)
            
            def arrow_440(__unit: Any=None) -> Optional[Cycle]:
                min_c_1 : int = match_value_2[0] or 0
                return Cycle(min_c_1 * 60, None, None)
            
            return (arrow_439() if (match_value_2[1] is not None) else arrow_440()) if (match_value_2[0] is not None) else None
        
    
    return Journey(Default_Journey.type, legs, j.ctx_recon, remarks, Default_Journey.price, arrow_441(), scheduled_days)


def distance_of_journey(j: Journey) -> float:
    def arrow_442(fc: FeatureCollection, j: Journey=j) -> float:
        return distance_of_feature_collection(fc)
    
    def chooser(l: Leg, j: Journey=j) -> Optional[FeatureCollection]:
        return l.polyline
    
    class ObjectExpr445:
        @property
        def GetZero(self) -> Any:
            def arrow_443(__unit: Any=None) -> int:
                return 0
            
            return arrow_443
        
        @property
        def Add(self) -> Any:
            def arrow_444(x: float, y: float) -> float:
                return x + y
            
            return arrow_444
        
    return sum_by(arrow_442, choose(chooser, j.legs, None), ObjectExpr445())


