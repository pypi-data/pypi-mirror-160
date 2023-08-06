from __future__ import annotations
from typing import (Optional, Callable, List, Any, Tuple, TypeVar)
from ..fable_library.array import (filter as filter_1, fold)
from ..fable_library.async_builder import (singleton, Async)
from ..fable_library.reflection import (TypeInfo, class_type)
from ..fable_library.util import IDisposable
from ..fs_hafas_python.format.format_request import (journey_request, reconstruction_request, search_on_trip_request, trip_request, station_board_request, location_request, loc_details_request, loc_geo_pos_request, loc_geo_reach_request, journey_geo_pos_request, journey_match_request, him_search_request, line_match_request, server_info_request)
from ..fs_hafas_python.lib.transformations import (MergeOptions_JourneysOptions, Default_Journey, MergeOptions_JourneysFromTripOptions, Default_Trip, MergeOptions_LocationsOptions, MergeOptions_NearByOptions)
from ..fs_hafas_python.parse.arrival_or_departure import (DEP, ARR)
from ..fs_hafas_python.parse.journey import distance_of_journey
from .context import (Profile__get_cfg, Profile__get_baseRequest, Profile__get_salt, Profile)
from .extra_types import (IndexMap_2, IndexMap_2__set_Item_541DA560, IndexMap_2__ctor_2B594, Log_Print)
from .hafas_raw_client import (HafasRawClient__Dispose, HafasRawClient__ctor_6D5FF7F7, HafasRawClient__AsyncTripSearch_Z4D007EE, HafasRawClient__AsyncReconstruction_Z19A33557, HafasRawClient__AsyncSearchOnTrip_5D40A373, HafasRawClient__AsyncJourneyDetails_73FB16B1, HafasRawClient__AsyncStationBoard_3FCEEA3, HafasRawClient__AsyncLocMatch_781FF3B0, HafasRawClient__AsyncLocDetails_2FCF6141, HafasRawClient__AsyncLocGeoPos_3C0E4562, HafasRawClient__AsyncLocGeoReach_320A81B3, HafasRawClient__AsyncJourneyGeoPos_Z6DB7B6AE, HafasRawClient__AsyncJourneyMatch_Z61E31480, HafasRawClient__AsyncHimSearch_Z6033479F, HafasRawClient__AsyncLineMatch_Z69AA7EA2, HafasRawClient__AsyncServerInfo_Z684EE398)
from .parser import (parse_journeys, parse_common, default_options, parse_journey, parse_journeys_array, parse_trip, parse_departures_arrivals, parse_locations, parse_location, parse_durations, parse_movements, parse_trips, parse_warnings, parse_lines, parse_server_info)
from .types_hafas_client import (ProductType, JourneysOptions, Journeys, RefreshJourneyOptions, Journey, StopOver, JourneysFromTripOptions, TripOptions, Trip, DeparturesArrivalsOptions, Alternative, LocationsOptions, StopOptions, Location, NearByOptions, ReachableFromOptions, Duration, BoundingBox, RadarOptions, Movement, TripsByNameOptions, RemarksOptions, Warning, LinesOptions, Line, ServerOptions, ServerInfo)
from .types_raw_hafas_client import (Cfg, RawRequest, TripSearchRequest, RawCommon, RawResult, RawOutCon, ReconstructionRequest, SearchOnTripRequest, JourneyDetailsRequest, RawJny, StationBoardRequest, LocMatchRequest, RawLoc, LocDetailsRequest, LocGeoPosRequest, LocGeoReachRequest, RawPos, JourneyGeoPosRequest, JourneyMatchRequest, HimSearchRequest, RawHim, LineMatchRequest, RawLine, ServerInfoRequest)

_A_ = TypeVar("_A_")

def expr_478() -> TypeInfo:
    return class_type("FsHafas.Api.HafasAsyncClient", None, HafasAsyncClient)


class HafasAsyncClient(IDisposable):
    def __init__(self, profile: Profile) -> None:
        self.profile = profile
        cfg_1 : Cfg
        match_value : Optional[Cfg] = Profile__get_cfg(self.profile)
        if match_value is None:
            raise Exception("profile.cfg")
        
        else: 
            cfg_1 = match_value
        
        base_request_1 : RawRequest
        match_value_1 : Optional[RawRequest] = Profile__get_baseRequest(self.profile)
        if match_value_1 is None:
            raise Exception("profile.baseRequest")
        
        else: 
            base_request_1 = match_value_1
        
        self.http_client = HafasRawClient__ctor_6D5FF7F7(self.profile.endpoint, Profile__get_salt(self.profile), cfg_1, base_request_1)
    
    def Dispose(self) -> None:
        __ : HafasAsyncClient = self
        HafasRawClient__Dispose(__.http_client)
    

HafasAsyncClient_reflection = expr_478

def HafasAsyncClient__ctor_Z3AB94A1B(profile: Profile) -> HafasAsyncClient:
    return HafasAsyncClient(profile)


def HafasAsyncClient_initSerializer() -> None:
    pass


def HafasAsyncClient_productsOfFilter(profile: Profile, filter: Callable[[ProductType], bool]) -> IndexMap_2[str, bool]:
    array_1 : List[ProductType] = filter_1(filter, profile.products)
    def folder(m: IndexMap_2[str, bool], p: ProductType, profile: Profile=profile, filter: Callable[[ProductType], bool]=filter) -> IndexMap_2[str, bool]:
        IndexMap_2__set_Item_541DA560(m, p.id, True)
        return m
    
    return fold(folder, IndexMap_2__ctor_2B594(False), array_1)


def HafasAsyncClient_productsOfMode(profile: Profile, mode: str) -> IndexMap_2[str, bool]:
    def arrow_479(p: ProductType, profile: Profile=profile, mode: str=mode) -> bool:
        return (p.name != "Tram") if (p.mode == mode) else False
    
    return HafasAsyncClient_productsOfFilter(profile, arrow_479)


def HafasAsyncClient__AsyncJourneys(__: HafasAsyncClient, from_: Any=None, to: Any=None, opt: Optional[JourneysOptions]=None) -> Async[Journeys]:
    def arrow_482(__: HafasAsyncClient=__, from_: Any=from_, to: Any=to, opt: Optional[JourneysOptions]=opt) -> Async[Journeys]:
        def arrow_480(__unit: Any=None) -> Async[Tuple[Optional[RawCommon], Optional[RawResult], Optional[List[RawOutCon]]]]:
            tupled_arg : Tuple[str, TripSearchRequest] = journey_request(__.profile, from_, to, opt)
            return HafasRawClient__AsyncTripSearch_Z4D007EE(__.http_client, tupled_arg[0], tupled_arg[1])
        
        def arrow_481(_arg1: Tuple[Optional[RawCommon], Optional[RawResult], Optional[List[RawOutCon]]]) -> Async[Journeys]:
            return singleton.Return(parse_journeys(_arg1[2], parse_common(__.profile, MergeOptions_JourneysOptions(default_options, opt), _arg1[0], _arg1[1])))
        
        return singleton.Bind(arrow_480(), arrow_481)
    
    return singleton.Delay(arrow_482)


def HafasAsyncClient__AsyncRefreshJourney(__: HafasAsyncClient, refresh_token: str, opt: Optional[RefreshJourneyOptions]=None) -> Async[Journey]:
    def arrow_485(__: HafasAsyncClient=__, refresh_token: str=refresh_token, opt: Optional[RefreshJourneyOptions]=opt) -> Async[Journey]:
        def arrow_483(__unit: Any=None) -> Async[Tuple[Optional[RawCommon], Optional[RawResult], Optional[List[RawOutCon]]]]:
            tupled_arg : Tuple[str, ReconstructionRequest] = reconstruction_request(__.profile, refresh_token, opt)
            return HafasRawClient__AsyncReconstruction_Z19A33557(__.http_client, tupled_arg[0], tupled_arg[1])
        
        def arrow_484(_arg2: Tuple[Optional[RawCommon], Optional[RawResult], Optional[List[RawOutCon]]]) -> Async[Journey]:
            return singleton.Return(parse_journey(_arg2[2], parse_common(__.profile, default_options, _arg2[0], _arg2[1])))
        
        return singleton.Bind(arrow_483(), arrow_484) if HafasAsyncClient__enabled_6FCE9E49(__, __.profile.refresh_journey) else singleton.Return(Default_Journey)
    
    return singleton.Delay(arrow_485)


def HafasAsyncClient__AsyncJourneysFromTrip(__: HafasAsyncClient, from_trip_id: str, previous_stop_over: StopOver, to: Any=None, opt: Optional[JourneysFromTripOptions]=None) -> Async[List[Journey]]:
    def arrow_488(__: HafasAsyncClient=__, from_trip_id: str=from_trip_id, previous_stop_over: StopOver=previous_stop_over, to: Any=to, opt: Optional[JourneysFromTripOptions]=opt) -> Async[List[Journey]]:
        def arrow_486(__unit: Any=None) -> Async[Tuple[Optional[RawCommon], Optional[RawResult], Optional[List[RawOutCon]]]]:
            tupled_arg : Tuple[str, SearchOnTripRequest] = search_on_trip_request(__.profile, from_trip_id, previous_stop_over, to, opt)
            return HafasRawClient__AsyncSearchOnTrip_5D40A373(__.http_client, tupled_arg[0], tupled_arg[1])
        
        def arrow_487(_arg3: Tuple[Optional[RawCommon], Optional[RawResult], Optional[List[RawOutCon]]]) -> Async[List[Journey]]:
            return singleton.Return(parse_journeys_array(_arg3[2], parse_common(__.profile, MergeOptions_JourneysFromTripOptions(default_options, opt), _arg3[0], _arg3[1])))
        
        return singleton.Bind(arrow_486(), arrow_487) if HafasAsyncClient__enabled_6FCE9E49(__, __.profile.journeys_from_trip) else singleton.Return([])
    
    return singleton.Delay(arrow_488)


def HafasAsyncClient__AsyncTrip(__: HafasAsyncClient, id: str, name: str, opt: Optional[TripOptions]=None) -> Async[Trip]:
    def arrow_491(__: HafasAsyncClient=__, id: str=id, name: str=name, opt: Optional[TripOptions]=opt) -> Async[Trip]:
        def arrow_489(__unit: Any=None) -> Async[Tuple[Optional[RawCommon], Optional[RawResult], Optional[RawJny]]]:
            tupled_arg : Tuple[str, JourneyDetailsRequest] = trip_request(__.profile, id, name, opt)
            return HafasRawClient__AsyncJourneyDetails_73FB16B1(__.http_client, tupled_arg[0], tupled_arg[1])
        
        def arrow_490(_arg4: Tuple[Optional[RawCommon], Optional[RawResult], Optional[RawJny]]) -> Async[Trip]:
            return singleton.Return(parse_trip(_arg4[2], parse_common(__.profile, default_options, _arg4[0], _arg4[1])))
        
        return singleton.Bind(arrow_489(), arrow_490) if HafasAsyncClient__enabled_6FCE9E49(__, __.profile.trip) else singleton.Return(Default_Trip)
    
    return singleton.Delay(arrow_491)


def HafasAsyncClient__AsyncDepartures(__: HafasAsyncClient, name: Any=None, opt: Optional[DeparturesArrivalsOptions]=None) -> Async[List[Alternative]]:
    def arrow_494(__: HafasAsyncClient=__, name: Any=name, opt: Optional[DeparturesArrivalsOptions]=opt) -> Async[List[Alternative]]:
        def arrow_492(__unit: Any=None) -> Async[Tuple[Optional[RawCommon], Optional[RawResult], Optional[List[RawJny]]]]:
            tupled_arg : Tuple[str, StationBoardRequest] = station_board_request(__.profile, DEP, name, opt)
            return HafasRawClient__AsyncStationBoard_3FCEEA3(__.http_client, tupled_arg[0], tupled_arg[1])
        
        def arrow_493(_arg5: Tuple[Optional[RawCommon], Optional[RawResult], Optional[List[RawJny]]]) -> Async[List[Alternative]]:
            return singleton.Return(parse_departures_arrivals(DEP, _arg5[2], parse_common(__.profile, default_options, _arg5[0], _arg5[1])))
        
        return singleton.Bind(arrow_492(), arrow_493)
    
    return singleton.Delay(arrow_494)


def HafasAsyncClient__AsyncArrivals(__: HafasAsyncClient, name: Any=None, opt: Optional[DeparturesArrivalsOptions]=None) -> Async[List[Alternative]]:
    def arrow_497(__: HafasAsyncClient=__, name: Any=name, opt: Optional[DeparturesArrivalsOptions]=opt) -> Async[List[Alternative]]:
        def arrow_495(__unit: Any=None) -> Async[Tuple[Optional[RawCommon], Optional[RawResult], Optional[List[RawJny]]]]:
            tupled_arg : Tuple[str, StationBoardRequest] = station_board_request(__.profile, ARR, name, opt)
            return HafasRawClient__AsyncStationBoard_3FCEEA3(__.http_client, tupled_arg[0], tupled_arg[1])
        
        def arrow_496(_arg6: Tuple[Optional[RawCommon], Optional[RawResult], Optional[List[RawJny]]]) -> Async[List[Alternative]]:
            return singleton.Return(parse_departures_arrivals(ARR, _arg6[2], parse_common(__.profile, default_options, _arg6[0], _arg6[1])))
        
        return singleton.Bind(arrow_495(), arrow_496)
    
    return singleton.Delay(arrow_497)


def HafasAsyncClient__AsyncLocations(__: HafasAsyncClient, name: str, opt: Optional[LocationsOptions]=None) -> Async[List[Any]]:
    def arrow_500(__: HafasAsyncClient=__, name: str=name, opt: Optional[LocationsOptions]=opt) -> Async[List[Any]]:
        def arrow_498(__unit: Any=None) -> Async[Tuple[Optional[RawCommon], Optional[RawResult], Optional[List[RawLoc]]]]:
            tupled_arg : Tuple[str, LocMatchRequest] = location_request(__.profile, name, opt)
            return HafasRawClient__AsyncLocMatch_781FF3B0(__.http_client, tupled_arg[0], tupled_arg[1])
        
        def arrow_499(_arg7: Tuple[Optional[RawCommon], Optional[RawResult], Optional[List[RawLoc]]]) -> Async[List[Any]]:
            return singleton.Return(parse_locations(_arg7[2], parse_common(__.profile, MergeOptions_LocationsOptions(default_options, opt), _arg7[0], _arg7[1])))
        
        return singleton.Bind(arrow_498(), arrow_499)
    
    return singleton.Delay(arrow_500)


def HafasAsyncClient__AsyncStop(__: HafasAsyncClient, stop: Any=None, opt: Optional[StopOptions]=None) -> Async[Any]:
    def arrow_503(__: HafasAsyncClient=__, stop: Any=stop, opt: Optional[StopOptions]=opt) -> Async[Any]:
        def arrow_501(__unit: Any=None) -> Async[Tuple[Optional[RawCommon], Optional[RawResult], Optional[RawLoc]]]:
            tupled_arg : Tuple[str, LocDetailsRequest] = loc_details_request(__.profile, stop, opt)
            return HafasRawClient__AsyncLocDetails_2FCF6141(__.http_client, tupled_arg[0], tupled_arg[1])
        
        def arrow_502(_arg8: Tuple[Optional[RawCommon], Optional[RawResult], Optional[RawLoc]]) -> Async[Any]:
            return singleton.Return(parse_location(_arg8[2], parse_common(__.profile, default_options, _arg8[0], _arg8[1])))
        
        return singleton.Bind(arrow_501(), arrow_502)
    
    return singleton.Delay(arrow_503)


def HafasAsyncClient__AsyncNearby(__: HafasAsyncClient, l: Location, opt: Optional[NearByOptions]=None) -> Async[List[Any]]:
    def arrow_506(__: HafasAsyncClient=__, l: Location=l, opt: Optional[NearByOptions]=opt) -> Async[List[Any]]:
        def arrow_504(__unit: Any=None) -> Async[Tuple[Optional[RawCommon], Optional[RawResult], Optional[List[RawLoc]]]]:
            tupled_arg : Tuple[str, LocGeoPosRequest] = loc_geo_pos_request(__.profile, l, opt)
            return HafasRawClient__AsyncLocGeoPos_3C0E4562(__.http_client, tupled_arg[0], tupled_arg[1])
        
        def arrow_505(_arg9: Tuple[Optional[RawCommon], Optional[RawResult], Optional[List[RawLoc]]]) -> Async[List[Any]]:
            return singleton.Return(parse_locations(_arg9[2], parse_common(__.profile, MergeOptions_NearByOptions(default_options, opt), _arg9[0], _arg9[1])))
        
        return singleton.Bind(arrow_504(), arrow_505)
    
    return singleton.Delay(arrow_506)


def HafasAsyncClient__AsyncReachableFrom(__: HafasAsyncClient, l: Location, opt: Optional[ReachableFromOptions]=None) -> Async[List[Duration]]:
    def arrow_509(__: HafasAsyncClient=__, l: Location=l, opt: Optional[ReachableFromOptions]=opt) -> Async[List[Duration]]:
        def arrow_507(__unit: Any=None) -> Async[Tuple[Optional[RawCommon], Optional[RawResult], List[RawPos]]]:
            tupled_arg : Tuple[str, LocGeoReachRequest] = loc_geo_reach_request(__.profile, l, opt)
            return HafasRawClient__AsyncLocGeoReach_320A81B3(__.http_client, tupled_arg[0], tupled_arg[1])
        
        def arrow_508(_arg10: Tuple[Optional[RawCommon], Optional[RawResult], List[RawPos]]) -> Async[List[Duration]]:
            return singleton.Return(parse_durations(_arg10[2], parse_common(__.profile, default_options, _arg10[0], _arg10[1])))
        
        return singleton.Bind(arrow_507(), arrow_508) if HafasAsyncClient__enabled_6FCE9E49(__, __.profile.reachable_from) else singleton.Return([])
    
    return singleton.Delay(arrow_509)


def HafasAsyncClient__AsyncRadar(__: HafasAsyncClient, rect: BoundingBox, opt: Optional[RadarOptions]=None) -> Async[List[Movement]]:
    def arrow_512(__: HafasAsyncClient=__, rect: BoundingBox=rect, opt: Optional[RadarOptions]=opt) -> Async[List[Movement]]:
        def arrow_510(__unit: Any=None) -> Async[Tuple[Optional[RawCommon], Optional[RawResult], Optional[List[RawJny]]]]:
            tupled_arg : Tuple[str, JourneyGeoPosRequest] = journey_geo_pos_request(__.profile, rect, opt)
            return HafasRawClient__AsyncJourneyGeoPos_Z6DB7B6AE(__.http_client, tupled_arg[0], tupled_arg[1])
        
        def arrow_511(_arg11: Tuple[Optional[RawCommon], Optional[RawResult], Optional[List[RawJny]]]) -> Async[List[Movement]]:
            return singleton.Return(parse_movements(_arg11[2], parse_common(__.profile, default_options, _arg11[0], _arg11[1])))
        
        return singleton.Bind(arrow_510(), arrow_511) if HafasAsyncClient__enabled_6FCE9E49(__, __.profile.radar) else singleton.Return([])
    
    return singleton.Delay(arrow_512)


def HafasAsyncClient__AsyncTripsByName(__: HafasAsyncClient, line_name: str, opt: Optional[TripsByNameOptions]=None) -> Async[List[Trip]]:
    def arrow_515(__: HafasAsyncClient=__, line_name: str=line_name, opt: Optional[TripsByNameOptions]=opt) -> Async[List[Trip]]:
        def arrow_513(__unit: Any=None) -> Async[Tuple[Optional[RawCommon], Optional[RawResult], Optional[List[RawJny]]]]:
            tupled_arg : Tuple[str, JourneyMatchRequest] = journey_match_request(__.profile, line_name, opt)
            return HafasRawClient__AsyncJourneyMatch_Z61E31480(__.http_client, tupled_arg[0], tupled_arg[1])
        
        def arrow_514(_arg12: Tuple[Optional[RawCommon], Optional[RawResult], Optional[List[RawJny]]]) -> Async[List[Trip]]:
            return singleton.Return(parse_trips(_arg12[2], parse_common(__.profile, default_options, _arg12[0], _arg12[1])))
        
        return singleton.Bind(arrow_513(), arrow_514) if HafasAsyncClient__enabled_6FCE9E49(__, __.profile.trips_by_name) else singleton.Return([])
    
    return singleton.Delay(arrow_515)


def HafasAsyncClient__AsyncRemarks_7D671456(__: HafasAsyncClient, opt: Optional[RemarksOptions]=None) -> Async[List[Warning]]:
    def arrow_518(__: HafasAsyncClient=__, opt: Optional[RemarksOptions]=opt) -> Async[List[Warning]]:
        def arrow_516(__unit: Any=None) -> Async[Tuple[Optional[RawCommon], Optional[RawResult], Optional[List[RawHim]]]]:
            tupled_arg : Tuple[str, HimSearchRequest] = him_search_request(__.profile, opt)
            return HafasRawClient__AsyncHimSearch_Z6033479F(__.http_client, tupled_arg[0], tupled_arg[1])
        
        def arrow_517(_arg13: Tuple[Optional[RawCommon], Optional[RawResult], Optional[List[RawHim]]]) -> Async[List[Warning]]:
            return singleton.Return(parse_warnings(_arg13[2], parse_common(__.profile, default_options, _arg13[0], _arg13[1])))
        
        return singleton.Bind(arrow_516(), arrow_517) if HafasAsyncClient__enabled_6FCE9E49(__, __.profile.remarks) else singleton.Return([])
    
    return singleton.Delay(arrow_518)


def HafasAsyncClient__AsyncLines(__: HafasAsyncClient, query: str, opt: Optional[LinesOptions]=None) -> Async[List[Line]]:
    def arrow_521(__: HafasAsyncClient=__, query: str=query, opt: Optional[LinesOptions]=opt) -> Async[List[Line]]:
        def arrow_519(__unit: Any=None) -> Async[Tuple[Optional[RawCommon], Optional[RawResult], Optional[List[RawLine]]]]:
            tupled_arg : Tuple[str, LineMatchRequest] = line_match_request(__.profile, query, opt)
            return HafasRawClient__AsyncLineMatch_Z69AA7EA2(__.http_client, tupled_arg[0], tupled_arg[1])
        
        def arrow_520(_arg14: Tuple[Optional[RawCommon], Optional[RawResult], Optional[List[RawLine]]]) -> Async[List[Line]]:
            return singleton.Return(parse_lines(_arg14[2], parse_common(__.profile, default_options, _arg14[0], _arg14[1])))
        
        return singleton.Bind(arrow_519(), arrow_520) if HafasAsyncClient__enabled_6FCE9E49(__, __.profile.lines) else singleton.Return([])
    
    return singleton.Delay(arrow_521)


def HafasAsyncClient__AsyncServerInfo_70DF6D02(__: HafasAsyncClient, opt: Optional[ServerOptions]=None) -> Async[ServerInfo]:
    def arrow_524(__: HafasAsyncClient=__, opt: Optional[ServerOptions]=opt) -> Async[ServerInfo]:
        def arrow_522(__unit: Any=None) -> Async[Tuple[Optional[RawCommon], Optional[RawResult]]]:
            tupled_arg : Tuple[str, ServerInfoRequest] = server_info_request(__.profile, opt)
            return HafasRawClient__AsyncServerInfo_Z684EE398(__.http_client, tupled_arg[0], tupled_arg[1])
        
        def arrow_523(_arg15: Tuple[Optional[RawCommon], Optional[RawResult]]) -> Async[ServerInfo]:
            res : Optional[RawResult] = _arg15[1]
            return singleton.Return(parse_server_info(res, parse_common(__.profile, default_options, _arg15[0], res)))
        
        return singleton.Bind(arrow_522(), arrow_523)
    
    return singleton.Delay(arrow_524)


def HafasAsyncClient__distanceOfJourney_1E546A4(__: HafasAsyncClient, j: Journey) -> float:
    return distance_of_journey(j)


def HafasAsyncClient__log(this: HafasAsyncClient, msg: str, o: _A_) -> None:
    Log_Print(msg, o)


def HafasAsyncClient__enabled_6FCE9E49(this: HafasAsyncClient, value: Optional[bool]=None) -> bool:
    if value is None:
        return False
    
    else: 
        return value
    


