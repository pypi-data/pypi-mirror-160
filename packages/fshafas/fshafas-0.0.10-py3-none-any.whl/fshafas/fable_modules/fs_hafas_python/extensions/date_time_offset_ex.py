from __future__ import annotations
from datetime import timedelta
import datetime
from dateutil import tz as tz_1
from typing import (Any, Optional, Tuple)
from ...fable_library.date import create
from ...fable_library.reflection import (TypeInfo, class_type)
from ...fable_library.string import (to_console, printf)
from ...fs_hafas_python.context import Profile

def expr_290() -> TypeInfo:
    return class_type("FsHafas.Extensions.DateTimeOffsetEx.DateTimeOffsetEx", None, DateTimeOffsetEx)


class DateTimeOffsetEx:
    def __init__(self, dt: Any, tzoffset_arg: Optional[int]=None, tz_arg: Optional[str]=None) -> None:
        self.dt = dt
        self.tzoffset_arg = tzoffset_arg
        self.tz_arg = tz_arg
    

DateTimeOffsetEx_reflection = expr_290

def DateTimeOffsetEx__ctor_26581FE8(dt: Any, tzoffset_arg: Optional[int]=None, tz_arg: Optional[str]=None) -> DateTimeOffsetEx:
    return DateTimeOffsetEx(dt, tzoffset_arg, tz_arg)


def DateTimeOffsetEx__get_DateTime(__: DateTimeOffsetEx) -> Any:
    return DateTimeOffsetEx__getDateTime(__)


def DateTimeOffsetEx__AddDays_5E38073B(__: DateTimeOffsetEx, days: float) -> DateTimeOffsetEx:
    return DateTimeOffsetEx__ctor_26581FE8(__.dt+timedelta(days=int(days)), __.tzoffset_arg, __.tz_arg)


def DateTimeOffsetEx__getDateTime(this: DateTimeOffsetEx) -> Any:
    match_value : Tuple[Optional[int], Optional[str]] = (this.tzoffset_arg, this.tz_arg)
    if match_value[0] is not None:
        tzoffset_arg : int = match_value[0] or 0
        return datetime.datetime((this.dt.year), (this.dt.month), (this.dt.day), (this.dt.hour), (this.dt.minute), (this.dt.second), tzinfo=(tz_1.tzoffset(None, tzoffset_arg)))
    
    elif match_value[1] is not None:
        tz : str = match_value[1]
        return datetime.datetime((this.dt.year), (this.dt.month), (this.dt.day), (this.dt.hour), (this.dt.minute), (this.dt.second), tzinfo=(tz_1.gettz(tz)))
    
    else: 
        return datetime.datetime((this.dt.year), (this.dt.month), (this.dt.day), (this.dt.hour), (this.dt.minute), (this.dt.second), tzinfo=(tz_1.gettz("Europe/Berlin")))
    


def parse_date_time_with_offset(profile: Profile, year: int, month: int, day: int, hour: int, minute: int, seconds: int, tz_offset: Optional[int]=None) -> DateTimeOffsetEx:
    try: 
        dt : Any = create(year, month, day, hour, minute, seconds)
        return DateTimeOffsetEx__ctor_26581FE8(dt, None, None) if (tz_offset is None) else DateTimeOffsetEx__ctor_26581FE8(dt, tz_offset * 60, None)
    
    except Exception as ex:
        arg10 : str = str(ex)
        to_console(printf("error parseDateTimeWithOffset: %s"))(arg10)
        raise Exception(str(ex))
    


def ToIsoString(dto: DateTimeOffsetEx) -> str:
    dt : Any = DateTimeOffsetEx__get_DateTime(dto)
    return dt.isoformat()


