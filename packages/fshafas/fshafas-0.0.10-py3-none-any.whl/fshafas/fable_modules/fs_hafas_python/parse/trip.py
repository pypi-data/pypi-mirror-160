from __future__ import annotations
from typing import (List, Optional, Any)
from ...fable_library.date import now
from ...fable_library.string import (to_text, printf)
from ...fs_hafas_python.context import (Context, Profile__get_parseJourneyLeg)
from ...fs_hafas_python.lib.transformations import (RawDep_FromRawStopL, RawArr_FromRawStopL, ToTrip_FromLeg)
from ...fs_hafas_python.types_hafas_client import (Leg, Trip)
from ...fs_hafas_python.types_raw_hafas_client import (RawJny, RawStop, RawSec)

def parse_trip(ctx: Context, j: RawJny) -> Trip:
    match_value : Optional[List[RawStop]] = j.stop_l
    (pattern_matching_result, stop_l_1) = (None, None)
    if match_value is not None:
        if len(match_value) > 1:
            pattern_matching_result = 0
            stop_l_1 = match_value
        
        else: 
            pattern_matching_result = 1
        
    
    else: 
        pattern_matching_result = 1
    
    if pattern_matching_result == 0:
        raw_sec_l : RawSec = RawSec("JNY", None, RawDep_FromRawStopL(stop_l_1[0]), RawArr_FromRawStopL(stop_l_1[len(stop_l_1) - 1]), j, None, None, None)
        date_1 : str
        match_value_1 : Optional[str] = j.date
        if match_value_1 is None:
            dt : Any = now()
            arg30 : int = (dt.day) or 0
            arg20 : int = (dt.month) or 0
            arg10 : int = (dt.year) or 0
            date_1 = to_text(printf("%04d%02d%02d"))(arg10)(arg20)(arg30)
        
        else: 
            date_1 = match_value_1
        
        leg : Leg = Profile__get_parseJourneyLeg(ctx.profile)(ctx)(raw_sec_l)(date_1)
        match_value_2 : Optional[str] = leg.trip_id
        if match_value_2 is not None:
            return ToTrip_FromLeg(match_value_2, leg)
        
        else: 
            raise Exception("parseTrip failed")
        
    
    elif pattern_matching_result == 1:
        raise Exception("parseTrip failed")
    


