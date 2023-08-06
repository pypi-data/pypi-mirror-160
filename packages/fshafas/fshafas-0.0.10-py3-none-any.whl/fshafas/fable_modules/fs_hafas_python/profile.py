from __future__ import annotations
from typing import (Optional, Any, List)
from ..fs_hafas_python.parse.arrival_or_departure import (parse_arrival, parse_departure)
from ..fs_hafas_python.parse.common import parse_common
from ..fs_hafas_python.parse.date_time import parse_date_time
from ..fs_hafas_python.parse.hint import parse_hint
from ..fs_hafas_python.parse.icon import parse_icon
from ..fs_hafas_python.parse.journey import parse_journey
from ..fs_hafas_python.parse.journey_leg import (parse_journey_leg, parse_platform)
from ..fs_hafas_python.parse.line import parse_line
from ..fs_hafas_python.parse.location import parse_locations
from ..fs_hafas_python.parse.movement import parse_movement
from ..fs_hafas_python.parse.operator import parse_operator
from ..fs_hafas_python.parse.polyline import parse_polyline
from ..fs_hafas_python.parse.products_bitmask import parse_bitmask
from ..fs_hafas_python.parse.stopover import (parse_stopover, parse_stopovers)
from ..fs_hafas_python.parse.trip import parse_trip
from ..fs_hafas_python.parse.warning import parse_warning
from ..fs_hafas_python.parse.when import parse_when
from .context import (Profile__ctor_35A3D895, Context, CommonData, Platform, ParsedWhen, Profile)
from .extra_types import (Icon, IndexMap_2)
from .types_hafas_client import (JourneysOptions, Alternative, FeatureCollection, Line, Journey, Leg, Movement, Operator, StopOver, Trip, Warning)
from .types_raw_hafas_client import (TripSearchRequest, RawCommon, RawJny, RawRem, RawIco, RawPoly, RawLoc, RawProd, RawOutCon, RawSec, RawOp, RawStop, RawHim)

def default_profile() -> Profile:
    def arrow_451(x: str) -> str:
        return x
    
    def arrow_452(_arg1: Optional[JourneysOptions], q: TripSearchRequest) -> TripSearchRequest:
        return q
    
    def arrow_453(ctx: Context, c: RawCommon) -> CommonData:
        return parse_common(ctx, c)
    
    def arrow_454(ctx_1: Context, d: RawJny) -> Alternative:
        return parse_arrival(ctx_1, d)
    
    def arrow_455(ctx_2: Context, d_1: RawJny) -> Alternative:
        return parse_departure(ctx_2, d_1)
    
    def arrow_456(ctx_3: Context, h: RawRem) -> Optional[Any]:
        return parse_hint(ctx_3, h)
    
    def arrow_457(ctx_4: Context, i: RawIco) -> Optional[Icon]:
        return parse_icon(ctx_4, i)
    
    def arrow_458(ctx_5: Context, poly: RawPoly) -> FeatureCollection:
        return parse_polyline(ctx_5, poly)
    
    def arrow_459(ctx_6: Context, loc_l: List[RawLoc]) -> List[Any]:
        return parse_locations(ctx_6, loc_l)
    
    def arrow_460(ctx_7: Context, p: RawProd) -> Line:
        return parse_line(ctx_7, p)
    
    def arrow_461(ctx_8: Context, j: RawOutCon) -> Journey:
        return parse_journey(ctx_8, j)
    
    def arrow_462(ctx_9: Context, pt: RawSec, date: str) -> Leg:
        return parse_journey_leg(ctx_9, pt, date)
    
    def arrow_463(ctx_10: Context, m: RawJny) -> Movement:
        return parse_movement(ctx_10, m)
    
    def arrow_464(ctx_11: Context, a: RawOp) -> Operator:
        return parse_operator(ctx_11, a)
    
    def arrow_465(ctx_12: Context, platf_s: Optional[str]=None, platf_r: Optional[str]=None, cncl: Optional[bool]=None) -> Platform:
        return parse_platform(ctx_12, platf_s, platf_r, cncl)
    
    def arrow_466(ctx_13: Context, st: RawStop, date_1: str) -> StopOver:
        return parse_stopover(ctx_13, st, date_1)
    
    def arrow_467(ctx_14: Context, stop_l: Optional[List[RawStop]], date_2: str) -> Optional[List[StopOver]]:
        return parse_stopovers(ctx_14, stop_l, date_2)
    
    def arrow_468(ctx_15: Context, j_1: RawJny) -> Trip:
        return parse_trip(ctx_15, j_1)
    
    def arrow_469(ctx_16: Context, date_3: str, time_s: Optional[str]=None, time_r: Optional[str]=None, tz_offset: Optional[int]=None, cncl_1: Optional[bool]=None) -> ParsedWhen:
        return parse_when(ctx_16, date_3, time_s, time_r, tz_offset, cncl_1)
    
    def arrow_470(ctx_17: Context, date_4: str, time: Optional[str]=None, tz_offset_1: Optional[int]=None) -> Optional[str]:
        return parse_date_time(ctx_17, date_4, time, tz_offset_1)
    
    def arrow_471(ctx_18: Context, bitmask: int) -> IndexMap_2[str, bool]:
        return parse_bitmask(ctx_18, bitmask)
    
    def arrow_472(ctx_19: Context, w: RawHim) -> Warning:
        return parse_warning(ctx_19, w)
    
    return Profile__ctor_35A3D895("de-DE", "Europe/Berlin", arrow_451, arrow_452, arrow_453, arrow_454, arrow_455, arrow_456, arrow_457, arrow_458, arrow_459, arrow_460, arrow_461, arrow_462, arrow_463, arrow_464, arrow_465, arrow_466, arrow_467, arrow_468, arrow_469, arrow_470, arrow_471, arrow_472)


