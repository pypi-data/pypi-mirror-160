from __future__ import annotations
from typing import (Optional, Any, Tuple)
from ...fable_library.date import op_subtraction
from ...fable_library.option import (to_array, default_arg)
from ...fable_library.seq import exists
from ...fable_library.time_span import total_seconds
from ...fable_library.util import round
from ...fs_hafas_python.context import (ParsedWhen, Context)
from .date_time import parse_date_time_ex

default_when : ParsedWhen = ParsedWhen(None, None, None, None)

def parse_when(ctx: Context, date: str, time_s: Optional[str]=None, time_r: Optional[str]=None, tz_offset: Optional[int]=None, cncl: Optional[bool]=None) -> ParsedWhen:
    pattern_input : Tuple[Optional[Any], Optional[str]] = parse_date_time_ex(ctx.profile, date, time_s, tz_offset)
    str_planned : Optional[str] = pattern_input[1]
    pattern_input_1 : Tuple[Optional[Any], Optional[str]] = parse_date_time_ex(ctx.profile, date, time_r, tz_offset)
    str_prognosed : Optional[str] = pattern_input_1[1]
    delay : Optional[int]
    match_value : Tuple[Optional[Any], Optional[Any]] = (pattern_input_1[0], pattern_input[0])
    (pattern_matching_result, planned, prognosed) = (None, None, None)
    if match_value[0] is not None:
        if match_value[1] is not None:
            pattern_matching_result = 0
            planned = match_value[1]
            prognosed = match_value[0]
        
        else: 
            pattern_matching_result = 1
        
    
    else: 
        pattern_matching_result = 1
    
    if pattern_matching_result == 0:
        def arrow_357(ctx: Context=ctx, date: str=date, time_s: Optional[str]=time_s, time_r: Optional[str]=time_r, tz_offset: Optional[int]=tz_offset, cncl: Optional[bool]=cncl) -> float:
            copy_of_struct : Any = op_subtraction(prognosed, planned)
            return total_seconds(copy_of_struct)
        
        delay = int(round(arrow_357()))
    
    elif pattern_matching_result == 1:
        delay = None
    
    def predicate(x: bool, ctx: Context=ctx, date: str=date, time_s: Optional[str]=time_s, time_r: Optional[str]=time_r, tz_offset: Optional[int]=tz_offset, cncl: Optional[bool]=cncl) -> bool:
        return x
    
    if exists(predicate, to_array(cncl)):
        return ParsedWhen(None, str_planned, str_prognosed, delay)
    
    else: 
        return ParsedWhen(default_arg(str_prognosed, str_planned), str_planned, None, delay)
    


