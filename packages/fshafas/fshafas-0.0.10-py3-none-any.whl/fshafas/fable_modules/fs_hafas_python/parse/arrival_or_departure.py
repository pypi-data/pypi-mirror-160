from __future__ import annotations
from typing import (Optional, Tuple, Any, Callable, List)
from ...fable_library.array import (filter as filter_1, try_head)
from ...fable_library.option import (value as value_1, map, default_arg, to_array)
from ...fable_library.seq import fold
from ...fs_hafas_python.context import (Context, Profile__get_parseWhen, ParsedWhen, Profile__get_parsePlatform, Platform, Profile__get_parseStopovers, Profile__get_parseLocations)
from ...fs_hafas_python.lib.transformations import (RawDep_FromRawStopL, RawArr_FromRawStopL, U2StationStop_FromSomeU3StationStopLocation, Default_Location, Default_Alternative)
from ...fs_hafas_python.types_hafas_client import (StopOver, Location, Alternative)
from ...fs_hafas_python.types_raw_hafas_client import (RawJny, RawPltf, RawDep, RawArr, RawCrd, RawProd, RawCommon, RawLoc, RawMsg, RawStop)
from .common import (get_element_at_some, msg_lto_remarks, append_some_array, get_element_at)

DEP : str = "DEP"

ARR : str = "ARR"

def parse_departure_arrival(type: str, ctx: Context, d: RawJny) -> Alternative:
    pattern_input : Tuple[Optional[int], Optional[str], Optional[str], Optional[int], Optional[bool], Optional[str], Optional[str], Optional[RawPltf], Optional[RawPltf]]
    if type == DEP:
        dep : RawDep = RawDep_FromRawStopL(value_1(d.stb_stop))
        pattern_input = (dep.loc_x, dep.d_time_s, dep.d_time_r, dep.d_tzoffset, dep.d_cncl, dep.d_platf_s, dep.d_platf_r, dep.d_pltf_s, dep.d_pltf_r)
    
    else: 
        arr : RawArr = RawArr_FromRawStopL(value_1(d.stb_stop))
        pattern_input = (arr.loc_x, arr.a_time_s, arr.a_time_r, arr.a_tzoffset, arr.a_cncl, arr.a_platf_s, arr.a_platf_r, arr.a_pltf_s, arr.a_pltf_r)
    
    x_cncl : Optional[bool] = pattern_input[4]
    stop : Optional[Any] = U2StationStop_FromSomeU3StationStopLocation(get_element_at_some(pattern_input[0], ctx.common.locations))
    w : ParsedWhen = Profile__get_parseWhen(ctx.profile)(ctx)(value_1(d.date))(pattern_input[1])(pattern_input[2])(pattern_input[3])(x_cncl)
    def match_platf_s(a_platf_s: Optional[str]=None, a_pltf_s: Optional[RawPltf]=None, type: str=type, ctx: Context=ctx, d: RawJny=d) -> Optional[str]:
        if a_platf_s is None:
            if a_pltf_s is not None:
                return a_pltf_s.txt
            
            else: 
                return None
            
        
        else: 
            return a_platf_s
        
    
    platf_s_1 : Optional[str] = match_platf_s(pattern_input[5], pattern_input[7])
    platf_r : Optional[str] = match_platf_s(pattern_input[6], pattern_input[8])
    plt : Platform = Profile__get_parsePlatform(ctx.profile)(ctx)(platf_s_1)(platf_r)(x_cncl)
    def mapping(st: List[StopOver], type: str=type, ctx: Context=ctx, d: RawJny=d) -> List[StopOver]:
        def filter(s: StopOver, st: List[StopOver]=st) -> bool:
            match_value : Optional[bool] = s.pass_by
            if match_value is None:
                return True
            
            else: 
                return not match_value
            
        
        return filter_1(filter, st)
    
    stopovers : Optional[List[StopOver]] = map(mapping, Profile__get_parseStopovers(ctx.profile)(ctx)(d.stop_l)(value_1(d.date)))
    current_trip_position : Optional[Location]
    match_value_1 : Optional[RawCrd] = d.pos
    if match_value_1 is None:
        current_trip_position = None
    
    else: 
        pos : RawCrd = match_value_1
        current_trip_position = Location(Default_Location.type, Default_Location.id, Default_Location.name, Default_Location.poi, Default_Location.address, pos.x / 1000000, pos.y / 1000000, Default_Location.altitude, Default_Location.distance)
    
    destination : Optional[Any]
    if type == DEP:
        match_value_2 : Tuple[Optional[List[RawProd]], Optional[RawCommon]] = (d.prod_l, ctx.res.common)
        (pattern_matching_result, common_1, prod_l_1) = (None, None, None)
        if match_value_2[0] is not None:
            if match_value_2[1] is not None:
                def arrow_365(type: str=type, ctx: Context=ctx, d: RawJny=d) -> bool:
                    common : RawCommon = match_value_2[1]
                    return (common.loc_l is not None) if (len(match_value_2[0]) > 0) else False
                
                if arrow_365():
                    pattern_matching_result = 0
                    common_1 = match_value_2[1]
                    prod_l_1 = match_value_2[0]
                
                else: 
                    pattern_matching_result = 1
                
            
            else: 
                pattern_matching_result = 1
            
        
        else: 
            pattern_matching_result = 1
        
        if pattern_matching_result == 0:
            loc : Optional[RawLoc] = get_element_at_some(prod_l_1[0].t_loc_x, value_1(common_1.loc_l))
            destination = try_head(Profile__get_parseLocations(ctx.profile)(ctx)([value_1(loc)]))
        
        elif pattern_matching_result == 1:
            destination = None
        
    
    else: 
        destination = None
    
    origin : Optional[Any]
    if type == ARR:
        match_value_3 : Tuple[Optional[List[RawProd]], Optional[RawCommon]] = (d.prod_l, ctx.res.common)
        (pattern_matching_result_1, common_3, prod_l_3) = (None, None, None)
        if match_value_3[0] is not None:
            if match_value_3[1] is not None:
                def arrow_367(type: str=type, ctx: Context=ctx, d: RawJny=d) -> bool:
                    common_2 : RawCommon = match_value_3[1]
                    return (common_2.loc_l is not None) if (len(match_value_3[0]) > 0) else False
                
                if arrow_367():
                    pattern_matching_result_1 = 0
                    common_3 = match_value_3[1]
                    prod_l_3 = match_value_3[0]
                
                else: 
                    pattern_matching_result_1 = 1
                
            
            else: 
                pattern_matching_result_1 = 1
            
        
        else: 
            pattern_matching_result_1 = 1
        
        if pattern_matching_result_1 == 0:
            loc_1 : Optional[RawLoc] = get_element_at_some(prod_l_3[0].f_loc_x, value_1(common_3.loc_l))
            origin = try_head(Profile__get_parseLocations(ctx.profile)(ctx)([value_1(loc_1)]))
        
        elif pattern_matching_result_1 == 1:
            origin = None
        
    
    else: 
        origin = None
    
    def arrow_371(type: str=type, ctx: Context=ctx, d: RawJny=d) -> List[Any]:
        value : List[Any] = []
        def folder(_arg1: Optional[List[RawMsg]], s_1: RawStop) -> Optional[List[RawMsg]]:
            return s_1.msg_l
        
        return default_arg(msg_lto_remarks(ctx, append_some_array(d.msg_l, fold(folder, None, to_array(d.stb_stop)))), value)
    
    remarks : Optional[List[Any]] = arrow_371() if ctx.opt.remarks else None
    return Alternative(d.jid, d.dir_txt, Default_Alternative.location, get_element_at(d.prod_x, ctx.common.lines), stop, w.when, w.planned_when, w.prognosed_when, w.delay, plt.platform, plt.planned_platform, plt.prognosed_platform, remarks, value_1(d.stb_stop).d_cncl, Default_Alternative.load_factor, None, Default_Alternative.previous_stopovers, stopovers, Default_Alternative.frames, Default_Alternative.polyline, current_trip_position, origin, destination)


def parse_departure(ctx: Context, d: RawJny) -> Alternative:
    return parse_departure_arrival(DEP, ctx, d)


def parse_arrival(ctx: Context, d: RawJny) -> Alternative:
    return parse_departure_arrival(ARR, ctx, d)


