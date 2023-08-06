from __future__ import annotations
from array import array as array_3
from typing import (Optional, Tuple, Any, List, MutableSequence, Callable)
from ..fable_library.array import (map, append, choose, fold)
from ..fable_library.date import (create, now)
from ..fable_library.int32 import parse as parse_1
from ..fable_library.map import (FSharpMap__ContainsKey, FSharpMap__get_Item, FSharpMap__Add, FSharpMap__Remove, to_array, empty)
from ..fable_library.option import (map as map_1, to_array as to_array_1)
from ..fable_library.seq import fold as fold_1
from ..fable_library.string import (substring, to_console, printf)
from ..fable_library.types import Int32Array
from ..fable_library.util import compare_primitives
from ..fs_hafas_python.lib.transformations import (Default_Location, Default_Journey, Default_Journeys)
from ..fs_hafas_python.parse.arrival_or_departure import DEP
from ..fs_hafas_python.parse.common import get_element_at
from .context import (CommonData, Options, Profile, Context, Profile__get_parseCommon, Profile__get_parseLocations, Profile__get_parseMovement, Profile__get_parseJourney, Profile__get_parseTrip, Profile__get_parseWarning, Profile__get_parseDeparture, Profile__get_parseArrival, Profile__get_parseDateTime)
from .types_hafas_client import (Movement, Duration, Journey, Journeys, Trip, Line, Warning, Alternative, ServerInfo)
from .types_raw_hafas_client import (RawResult, RawCommon, RawLoc, RawJny, RawPos, RawOutCon, RawLine, RawDir, RawHim)

default_common_data : CommonData = CommonData([], [], [], [], [], [])

default_options : Options = Options(True, True, True, False, True, True, True, False)

def create_context(profile: Profile, opt: Options, res: RawResult) -> Context:
    return Context(profile, opt, default_common_data, res)


def parse_common(profile: Profile, opt: Options, common: Optional[RawCommon]=None, res: Optional[RawResult]=None) -> Optional[Context]:
    match_value : Tuple[Optional[RawResult], Optional[RawCommon]] = (res, common)
    if match_value[0] is not None:
        if match_value[1] is None:
            res_2 : RawResult = match_value[0]
            return create_context(profile, opt, res_2)
        
        else: 
            common_1 : RawCommon = match_value[1]
            res_1 : RawResult = match_value[0]
            ctx : Context = create_context(profile, opt, res_1)
            return Context(ctx.profile, ctx.opt, Profile__get_parseCommon(ctx.profile)(ctx)(common_1), ctx.res)
        
    
    else: 
        return None
    


def parse_location(loc_l: Optional[RawLoc]=None, ctx: Optional[Context]=None) -> Any:
    match_value : Tuple[Optional[Context], Optional[RawLoc]] = (ctx, loc_l)
    (pattern_matching_result, ctx_1, loc_l_1) = (None, None, None)
    if match_value[0] is not None:
        if match_value[1] is not None:
            pattern_matching_result = 0
            ctx_1 = match_value[0]
            loc_l_1 = match_value[1]
        
        else: 
            pattern_matching_result = 1
        
    
    else: 
        pattern_matching_result = 1
    
    if pattern_matching_result == 0:
        locs : List[Any] = Profile__get_parseLocations(ctx_1.profile)(ctx_1)([loc_l_1])
        return locs[0]
    
    elif pattern_matching_result == 1:
        return Default_Location
    


def parse_locations(loc_l: Optional[List[RawLoc]]=None, ctx: Optional[Context]=None) -> List[Any]:
    match_value : Tuple[Optional[List[RawLoc]], Optional[Context]] = (loc_l, ctx)
    (pattern_matching_result, ctx_1, loc_l_1) = (None, None, None)
    if match_value[0] is not None:
        if match_value[1] is not None:
            pattern_matching_result = 0
            ctx_1 = match_value[1]
            loc_l_1 = match_value[0]
        
        else: 
            pattern_matching_result = 1
        
    
    else: 
        pattern_matching_result = 1
    
    if pattern_matching_result == 0:
        return Profile__get_parseLocations(ctx_1.profile)(ctx_1)(loc_l_1)
    
    elif pattern_matching_result == 1:
        return []
    


def parse_locations_from_result(profile: Profile, loc_l: Optional[List[RawLoc]], options: Options, res: RawResult) -> List[Any]:
    return parse_locations(loc_l, parse_common(profile, options, res.common, res))


def parse_movements(jny_l: Optional[List[RawJny]]=None, ctx: Optional[Context]=None) -> List[Movement]:
    match_value : Tuple[Optional[Context], Optional[List[RawJny]]] = (ctx, jny_l)
    (pattern_matching_result, ctx_1, jny_l_1) = (None, None, None)
    if match_value[0] is not None:
        if match_value[1] is not None:
            pattern_matching_result = 0
            ctx_1 = match_value[0]
            jny_l_1 = match_value[1]
        
        else: 
            pattern_matching_result = 1
        
    
    else: 
        pattern_matching_result = 1
    
    if pattern_matching_result == 0:
        return map(Profile__get_parseMovement(ctx_1.profile)(ctx_1), jny_l_1, None)
    
    elif pattern_matching_result == 1:
        return []
    


def parse_movements_from_result(profile: Profile, jny_l: Optional[List[RawJny]], options: Options, res: RawResult) -> List[Movement]:
    return parse_movements(jny_l, parse_common(profile, options, res.common, res))


def add_to_map(m: Any, p: RawPos) -> Any:
    if FSharpMap__ContainsKey(m, p.dur):
        l : MutableSequence[int] = FSharpMap__get_Item(m, p.dur)
        return FSharpMap__Add(FSharpMap__Remove(m, p.dur), p.dur, append(l, array_3("i", [p.loc_x]), Int32Array))
    
    else: 
        return FSharpMap__Add(m, p.dur, array_3("i", [p.loc_x]))
    


def get_locations(ctx: Context, loc_xs: MutableSequence[int]) -> List[Any]:
    def chooser(x: Optional[Any]=None, ctx: Context=ctx, loc_xs: MutableSequence[int]=loc_xs) -> Optional[Any]:
        return x
    
    def mapping(locx: int, ctx: Context=ctx, loc_xs: MutableSequence[int]=loc_xs) -> Optional[Any]:
        return get_element_at(locx, ctx.common.locations)
    
    return choose(chooser, map(mapping, loc_xs, None), None)


def parse_durations(pos_l: List[RawPos], ctx: Optional[Context]=None) -> List[Duration]:
    if ctx is not None:
        ctx_1 : Context = ctx
        def mapping(tupled_arg: Tuple[int, MutableSequence[int]], pos_l: List[RawPos]=pos_l, ctx: Optional[Context]=ctx) -> Duration:
            return Duration(tupled_arg[0], get_locations(ctx_1, tupled_arg[1]))
        
        def arrow_473(m: Any, p: RawPos, pos_l: List[RawPos]=pos_l, ctx: Optional[Context]=ctx) -> Any:
            return add_to_map(m, p)
        
        class ObjectExpr475:
            @property
            def Compare(self) -> Any:
                def arrow_474(x: int, y: int) -> int:
                    return compare_primitives(x, y)
                
                return arrow_474
            
        return map(mapping, to_array(fold(arrow_473, empty(ObjectExpr475()), pos_l)), None)
    
    else: 
        return []
    


def parse_durations_from_result(profile: Profile, pos_l: List[RawPos], options: Options, res: RawResult) -> List[Duration]:
    return parse_durations(pos_l, parse_common(profile, options, res.common, res))


def parse_journey(out_con_l: Optional[List[RawOutCon]]=None, ctx: Optional[Context]=None) -> Journey:
    match_value : Tuple[Optional[Context], Optional[List[RawOutCon]]] = (ctx, out_con_l)
    (pattern_matching_result, ctx_2, out_con_l_2) = (None, None, None)
    if match_value[0] is not None:
        if match_value[1] is not None:
            def arrow_476(out_con_l: Optional[List[RawOutCon]]=out_con_l, ctx: Optional[Context]=ctx) -> bool:
                ctx_1 : Context = match_value[0]
                return len(match_value[1]) > 0
            
            if arrow_476():
                pattern_matching_result = 0
                ctx_2 = match_value[0]
                out_con_l_2 = match_value[1]
            
            else: 
                pattern_matching_result = 1
            
        
        else: 
            pattern_matching_result = 1
        
    
    else: 
        pattern_matching_result = 1
    
    if pattern_matching_result == 0:
        return Profile__get_parseJourney(ctx_2.profile)(ctx_2)(out_con_l_2[0])
    
    elif pattern_matching_result == 1:
        return Default_Journey
    


def parse_journeys_array(out_con_l: Optional[List[RawOutCon]]=None, ctx: Optional[Context]=None) -> List[Journey]:
    match_value : Tuple[Optional[Context], Optional[List[RawOutCon]]] = (ctx, out_con_l)
    (pattern_matching_result, ctx_1, out_con_l_1) = (None, None, None)
    if match_value[0] is not None:
        if match_value[1] is not None:
            pattern_matching_result = 0
            ctx_1 = match_value[0]
            out_con_l_1 = match_value[1]
        
        else: 
            pattern_matching_result = 1
        
    
    else: 
        pattern_matching_result = 1
    
    if pattern_matching_result == 0:
        def mapping(o: RawOutCon, out_con_l: Optional[List[RawOutCon]]=out_con_l, ctx: Optional[Context]=ctx) -> Journey:
            return Profile__get_parseJourney(ctx_1.profile)(ctx_1)(o)
        
        return map(mapping, out_con_l_1, None)
    
    elif pattern_matching_result == 1:
        return []
    


def parse_journeys_array_from_result(profile: Profile, out_con_l: Optional[List[RawOutCon]], options: Options, res: RawResult) -> List[Journey]:
    return parse_journeys_array(out_con_l, parse_common(profile, options, res.common, res))


def parse_journeys(out_con_l: Optional[List[RawOutCon]]=None, ctx: Optional[Context]=None) -> Journeys:
    match_value : Tuple[Optional[Context], Optional[List[RawOutCon]]] = (ctx, out_con_l)
    (pattern_matching_result, ctx_1, out_con_l_1) = (None, None, None)
    if match_value[0] is not None:
        if match_value[1] is not None:
            pattern_matching_result = 0
            ctx_1 = match_value[0]
            out_con_l_1 = match_value[1]
        
        else: 
            pattern_matching_result = 1
        
    
    else: 
        pattern_matching_result = 1
    
    if pattern_matching_result == 0:
        def mapping(o: RawOutCon, out_con_l: Optional[List[RawOutCon]]=out_con_l, ctx: Optional[Context]=ctx) -> Journey:
            return Profile__get_parseJourney(ctx_1.profile)(ctx_1)(o)
        
        def mapping_1(p: str, out_con_l: Optional[List[RawOutCon]]=out_con_l, ctx: Optional[Context]=ctx) -> int:
            return parse_1(p, 511, False, 32)
        
        return Journeys(ctx_1.res.out_ctx_scr_b, ctx_1.res.out_ctx_scr_f, map(mapping, out_con_l_1, None), map_1(mapping_1, ctx_1.res.planrt_ts))
    
    elif pattern_matching_result == 1:
        return Default_Journeys
    


def parse_journeys_from_result(profile: Profile, out_con_l: Optional[List[RawOutCon]], options: Options, res: RawResult) -> Journeys:
    return parse_journeys(out_con_l, parse_common(profile, options, res.common, res))


def parse_trip(journey: Optional[RawJny]=None, ctx: Optional[Context]=None) -> Trip:
    match_value : Tuple[Optional[Context], Optional[RawJny]] = (ctx, journey)
    (pattern_matching_result, ctx_1, journey_1) = (None, None, None)
    if match_value[0] is not None:
        if match_value[1] is not None:
            pattern_matching_result = 0
            ctx_1 = match_value[0]
            journey_1 = match_value[1]
        
        else: 
            pattern_matching_result = 1
        
    
    else: 
        pattern_matching_result = 1
    
    if pattern_matching_result == 0:
        return Profile__get_parseTrip(ctx_1.profile)(ctx_1)(journey_1)
    
    elif pattern_matching_result == 1:
        raise Exception("parseTrip failed")
    


def parse_trip_from_result(profile: Profile, journey: Optional[RawJny], options: Options, res: RawResult) -> Trip:
    return parse_trip(journey, parse_common(profile, options, res.common, res))


def parse_trips(journeys: Optional[List[RawJny]]=None, ctx: Optional[Context]=None) -> List[Trip]:
    match_value : Tuple[Optional[Context], Optional[List[RawJny]]] = (ctx, journeys)
    (pattern_matching_result, ctx_1, journeys_1) = (None, None, None)
    if match_value[0] is not None:
        if match_value[1] is not None:
            pattern_matching_result = 0
            ctx_1 = match_value[0]
            journeys_1 = match_value[1]
        
        else: 
            pattern_matching_result = 1
        
    
    else: 
        pattern_matching_result = 1
    
    if pattern_matching_result == 0:
        def mapping(j: RawJny, journeys: Optional[List[RawJny]]=journeys, ctx: Optional[Context]=ctx) -> Trip:
            return Profile__get_parseTrip(ctx_1.profile)(ctx_1)(j)
        
        return map(mapping, journeys_1, None)
    
    elif pattern_matching_result == 1:
        raise Exception("parseTrip failed")
    


def parse_line(l: RawLine, ctx: Context) -> Optional[Line]:
    dirl : List[RawDir]
    match_value : Optional[RawCommon] = ctx.res.common
    if match_value is None:
        dirl = []
    
    else: 
        match_value_1 : Optional[List[RawDir]] = match_value.dir_l
        dirl = [] if (match_value_1 is None) else match_value_1
    
    def mapping_1(d_2: RawDir, l: RawLine=l, ctx: Context=ctx) -> str:
        return d_2.txt
    
    def chooser(x: Optional[RawDir]=None, l: RawLine=l, ctx: Context=ctx) -> Optional[RawDir]:
        return x
    
    def mapping(d_1: int, l: RawLine=l, ctx: Context=ctx) -> Optional[RawDir]:
        return get_element_at(d_1, dirl)
    
    def folder(_arg1: MutableSequence[int], d: MutableSequence[int], l: RawLine=l, ctx: Context=ctx) -> MutableSequence[int]:
        return d
    
    directions : List[str] = map(mapping_1, choose(chooser, map(mapping, fold_1(folder, array_3("i", []), to_array_1(l.dir_ref_l)), None), None), None)
    match_value_2 : Optional[Line] = get_element_at(l.prod_x, ctx.common.lines)
    if match_value_2 is None:
        return None
    
    else: 
        line : Line = match_value_2
        return Line(line.type, line.id, line.name, line.admin_code, line.fahrt_nr, line.additional_name, line.product, line.public, line.mode, line.routes, line.operator, line.express, line.metro, line.night, line.nr, line.symbol, directions, line.product_name)
    


def parse_lines(lines: Optional[List[RawLine]]=None, ctx: Optional[Context]=None) -> List[Line]:
    match_value : Tuple[Optional[Context], Optional[List[RawLine]]] = (ctx, lines)
    if match_value[0] is not None:
        if match_value[1] is None:
            ctx_2 : Context = match_value[0]
            return []
        
        else: 
            ctx_1 : Context = match_value[0]
            lines_1 : List[RawLine] = match_value[1]
            def chooser(x: Optional[Line]=None, lines: Optional[List[RawLine]]=lines, ctx: Optional[Context]=ctx) -> Optional[Line]:
                return x
            
            def mapping(l: RawLine, lines: Optional[List[RawLine]]=lines, ctx: Optional[Context]=ctx) -> Optional[Line]:
                return parse_line(l, ctx_1)
            
            return choose(chooser, map(mapping, lines_1, None), None)
        
    
    else: 
        raise Exception("parseLines failed")
    


def parse_lines_from_result(profile: Profile, lines: Optional[List[RawLine]], options: Options, res: RawResult) -> List[Line]:
    return parse_lines(lines, parse_common(profile, options, res.common, res))


def parse_warnings(msg_l: Optional[List[RawHim]]=None, ctx: Optional[Context]=None) -> List[Warning]:
    match_value : Tuple[Optional[Context], Optional[List[RawHim]]] = (ctx, msg_l)
    (pattern_matching_result, ctx_1, msg_l_1) = (None, None, None)
    if match_value[0] is not None:
        if match_value[1] is not None:
            pattern_matching_result = 0
            ctx_1 = match_value[0]
            msg_l_1 = match_value[1]
        
        else: 
            pattern_matching_result = 1
        
    
    else: 
        pattern_matching_result = 1
    
    if pattern_matching_result == 0:
        def mapping(j: RawHim, msg_l: Optional[List[RawHim]]=msg_l, ctx: Optional[Context]=ctx) -> Warning:
            return Profile__get_parseWarning(ctx_1.profile)(ctx_1)(j)
        
        return map(mapping, msg_l_1, None)
    
    elif pattern_matching_result == 1:
        raise Exception("parseWarnings failed")
    


def parse_warnings_from_result(profile: Profile, msg_l: Optional[List[RawHim]], options: Options, res: RawResult) -> List[Warning]:
    return parse_warnings(msg_l, parse_common(profile, options, res.common, res))


def ParseIsoString(datetime: str) -> Any:
    return create(parse_1(substring(datetime, 0, 4), 511, False, 32), parse_1(substring(datetime, 5, 2), 511, False, 32), parse_1(substring(datetime, 8, 2), 511, False, 32), parse_1(substring(datetime, 11, 2), 511, False, 32), parse_1(substring(datetime, 14, 2), 511, False, 32), 0)


def parse_departures_arrivals(type: str, jny_l: Optional[List[RawJny]]=None, ctx: Optional[Context]=None) -> List[Alternative]:
    match_value_1 : Tuple[Optional[Context], Optional[List[RawJny]]] = (ctx, jny_l)
    (pattern_matching_result, ctx_1, jny_l_1) = (None, None, None)
    if match_value_1[0] is not None:
        if match_value_1[1] is not None:
            pattern_matching_result = 0
            ctx_1 = match_value_1[0]
            jny_l_1 = match_value_1[1]
        
        else: 
            pattern_matching_result = 1
        
    
    else: 
        pattern_matching_result = 1
    
    if pattern_matching_result == 0:
        try: 
            parse : Callable[[Context, RawJny], Alternative] = Profile__get_parseDeparture(ctx_1.profile) if (type == DEP) else Profile__get_parseArrival(ctx_1.profile)
            def mapping(jny: RawJny) -> Alternative:
                return parse(ctx_1)(jny)
            
            arr : List[Alternative] = map(mapping, jny_l_1, None)
            def projection(d: Alternative) -> Any:
                try: 
                    match_value : Optional[str] = d.when
                    return now() if (match_value is None) else ParseIsoString(match_value)
                
                except Exception as ex:
                    arg10 : str = str(ex)
                    to_console(printf("%s"))(arg10)
                    return now()
                
            
            return sorted(arr, key=projection)
        
        except Exception as ex_1:
            arg10_1 : str = str(ex_1)
            to_console(printf("%s"))(arg10_1)
            return []
        
    
    elif pattern_matching_result == 1:
        return []
    


def parse_departures_arrivals_from_result(profile: Profile, type: str, jny_l: Optional[List[RawJny]], options: Options, res: RawResult) -> List[Alternative]:
    return parse_departures_arrivals(type, jny_l, parse_common(profile, options, res.common, res))


def parse_server_info(res: Optional[RawResult]=None, ctx: Optional[Context]=None) -> ServerInfo:
    match_value : Tuple[Optional[Context], Optional[RawResult]] = (ctx, res)
    (pattern_matching_result, ctx_1, res_1) = (None, None, None)
    if match_value[0] is not None:
        if match_value[1] is not None:
            pattern_matching_result = 0
            ctx_1 = match_value[0]
            res_1 = match_value[1]
        
        else: 
            pattern_matching_result = 1
        
    
    else: 
        pattern_matching_result = 1
    
    if pattern_matching_result == 0:
        def arrow_477(res: Optional[RawResult]=res, ctx: Optional[Context]=ctx) -> Optional[str]:
            match_value_1 : Optional[str] = res_1.s_d
            if match_value_1 is None:
                return None
            
            else: 
                s_d : str = match_value_1
                return Profile__get_parseDateTime(ctx_1.profile)(ctx_1)(s_d)(res_1.s_t)(None)
            
        
        def mapping(p: str, res: Optional[RawResult]=res, ctx: Optional[Context]=ctx) -> int:
            return parse_1(p, 511, False, 32)
        
        return ServerInfo(res_1.hci_version, res_1.fp_b, res_1.fp_e, arrow_477(), map_1(mapping, res_1.planrt_ts))
    
    elif pattern_matching_result == 1:
        raise Exception("ServerInfo failed")
    


