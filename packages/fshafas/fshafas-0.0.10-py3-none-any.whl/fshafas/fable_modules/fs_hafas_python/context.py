from __future__ import annotations
from typing import (List, Any, Optional, Callable)
from ..fable_library.reflection import (TypeInfo, bool_type, record_type, array_type, obj_type, option_type, string_type, int32_type, class_type)
from ..fable_library.types import Record
from ..fable_library.util import curry
from .extra_types import (Icon, Icon_reflection, IndexMap_2)
from .types_hafas_client import (FeatureCollection, Line, Operator, Operator_reflection, Line_reflection, FeatureCollection_reflection, ProductType, JourneysOptions, Alternative, Journey, Leg, Movement, StopOver, Trip, Warning)
from .types_raw_hafas_client import (TripSearchRequest, RawCommon, RawJny, RawRem, RawIco, RawPoly, RawLoc, RawProd, RawOutCon, RawSec, RawOp, RawStop, RawHim, RawResult, RawResult_reflection, Cfg, RawRequest)

def expr_291() -> TypeInfo:
    return record_type("FsHafas.Endpoint.Options", [], Options, lambda: [("remarks", bool_type), ("stopovers", bool_type), ("polylines", bool_type), ("scheduled_days", bool_type), ("sub_stops", bool_type), ("entrances", bool_type), ("lines_of_stops", bool_type), ("first_class", bool_type)])


class Options(Record):
    def __init__(self, remarks: bool, stopovers: bool, polylines: bool, scheduled_days: bool, sub_stops: bool, entrances: bool, lines_of_stops: bool, first_class: bool) -> None:
        super().__init__()
        self.remarks = remarks
        self.stopovers = stopovers
        self.polylines = polylines
        self.scheduled_days = scheduled_days
        self.sub_stops = sub_stops
        self.entrances = entrances
        self.lines_of_stops = lines_of_stops
        self.first_class = first_class
    

Options_reflection = expr_291

def expr_292() -> TypeInfo:
    return record_type("FsHafas.Endpoint.CommonData", [], CommonData, lambda: [("operators", array_type(Operator_reflection())), ("locations", array_type(obj_type)), ("lines", array_type(Line_reflection())), ("hints", array_type(option_type(obj_type))), ("icons", array_type(Icon_reflection())), ("polylines", array_type(FeatureCollection_reflection()))])


class CommonData(Record):
    def __init__(self, operators: List[Operator], locations: List[Any], lines: List[Line], hints: List[Optional[Any]], icons: List[Icon], polylines: List[FeatureCollection]) -> None:
        super().__init__()
        self.operators = operators
        self.locations = locations
        self.lines = lines
        self.hints = hints
        self.icons = icons
        self.polylines = polylines
    

CommonData_reflection = expr_292

def expr_293() -> TypeInfo:
    return record_type("FsHafas.Endpoint.ParsedWhen", [], ParsedWhen, lambda: [("when", option_type(string_type)), ("planned_when", option_type(string_type)), ("prognosed_when", option_type(string_type)), ("delay", option_type(int32_type))])


class ParsedWhen(Record):
    def __init__(self, when: Optional[str], planned_when: Optional[str], prognosed_when: Optional[str], delay: Optional[int]) -> None:
        super().__init__()
        self.when = when
        self.planned_when = planned_when
        self.prognosed_when = prognosed_when
        self.delay = delay
    

ParsedWhen_reflection = expr_293

def expr_294() -> TypeInfo:
    return record_type("FsHafas.Endpoint.Platform", [], Platform, lambda: [("platform", option_type(string_type)), ("planned_platform", option_type(string_type)), ("prognosed_platform", option_type(string_type))])


class Platform(Record):
    def __init__(self, platform: Optional[str], planned_platform: Optional[str], prognosed_platform: Optional[str]) -> None:
        super().__init__()
        self.platform = platform
        self.planned_platform = planned_platform
        self.prognosed_platform = prognosed_platform
    

Platform_reflection = expr_294

def expr_295() -> TypeInfo:
    return class_type("FsHafas.Endpoint.Profile", None, Profile)


class Profile:
    def __init__(self, locale: str, timezone: str, format_station: Callable[[str], str], transform_journeys_query: Callable[[Optional[JourneysOptions], TripSearchRequest], TripSearchRequest], parse_common: Callable[[Context, RawCommon], CommonData], parse_arrival: Callable[[Context, RawJny], Alternative], parse_departure: Callable[[Context, RawJny], Alternative], parse_hint: Callable[[Context, RawRem], Optional[Any]], parse_icon: Callable[[Context, RawIco], Optional[Icon]], parse_polyline: Callable[[Context, RawPoly], FeatureCollection], parse_locations: Callable[[Context, List[RawLoc]], List[Any]], parse_line: Callable[[Context, RawProd], Line], parse_journey: Callable[[Context, RawOutCon], Journey], parse_journey_leg: Callable[[Context, RawSec, str], Leg], parse_movement: Callable[[Context, RawJny], Movement], parse_operator: Callable[[Context, RawOp], Operator], parse_platform: Callable[[Context, Optional[str], Optional[str], Optional[bool]], Platform], parse_stopover: Callable[[Context, RawStop, str], StopOver], parse_stopovers: Callable[[Context, Optional[List[RawStop]], str], Optional[List[StopOver]]], parse_trip: Callable[[Context, RawJny], Trip], parse_when: Callable[[Context, str, Optional[str], Optional[str], Optional[int], Optional[bool]], ParsedWhen], parse_date_time: Callable[[Context, str, Optional[str], Optional[int]], Optional[str]], parse_bitmask: Callable[[Context, int], IndexMap_2[str, bool]], parse_warning: Callable[[Context, RawHim], Warning]) -> None:
        self.salt_0040 = ""
        self.cfg_0040 = None
        self.base_request_0040 = None
        self.journeys_out_frwd_0040 = False
        self.departures_get_passlist_0040 = True
        self.departures_stb_fltr_equiv_0040 = True
        self.format_station_0040 = format_station
        self.transform_journeys_query_0040 = transform_journeys_query
        self.parse_common_0040 = parse_common
        self.parse_arrival_0040 = parse_arrival
        self.parse_departure_0040 = parse_departure
        self.parse_hint_0040 = parse_hint
        self.parse_icon_0040 = parse_icon
        self.parse_polyline_0040 = parse_polyline
        self.parse_locations_0040 = parse_locations
        self.parse_line_0040 = parse_line
        self.parse_journey_0040 = parse_journey
        self.parse_journey_leg_0040 = parse_journey_leg
        self.parse_movement_0040 = parse_movement
        self.parse_operator_0040 = parse_operator
        self.parse_platform_0040 = parse_platform
        self.parse_stopover_0040 = parse_stopover
        self.parse_stopovers_0040 = parse_stopovers
        self.parse_trip_0040 = parse_trip
        self.parse_when_0040 = parse_when
        self.parse_date_time_0040 = parse_date_time
        self.parse_bitmask_0040 = parse_bitmask
        self.parse_warning_0040 = parse_warning
        self._locale_0040 = locale
        self._timezone_0040 = timezone
        self._endpoint_0040 = ""
        self._products_0040 = []
        self._trip_0040 = None
        self._radar_0040 = None
        self._refreshJourney_0040 = None
        self._journeysFromTrip_0040 = None
        self._reachableFrom_0040 = None
        self._journeysWalkingSpeed_0040 = None
        self._tripsByName_0040 = None
        self._remarks_0040 = None
        self._remarksGetPolyline_0040 = None
        self._lines_0040 = None
    
    @property
    def locale(self) -> str:
        __ : Profile = self
        return Profile__get__locale(__)
    
    @property
    def timezone(self) -> str:
        __ : Profile = self
        return Profile__get__timezone(__)
    
    @property
    def endpoint(self) -> str:
        __ : Profile = self
        return Profile__get__endpoint(__)
    
    @property
    def products(self) -> List[ProductType]:
        __ : Profile = self
        return Profile__get__products(__)
    
    @property
    def trip(self) -> Optional[bool]:
        __ : Profile = self
        return Profile__get__trip(__)
    
    @property
    def radar(self) -> Optional[bool]:
        __ : Profile = self
        return Profile__get__radar(__)
    
    @property
    def refresh_journey(self) -> Optional[bool]:
        __ : Profile = self
        return Profile__get__refreshJourney(__)
    
    @property
    def journeys_from_trip(self) -> Optional[bool]:
        __ : Profile = self
        return Profile__get__journeysFromTrip(__)
    
    @property
    def reachable_from(self) -> Optional[bool]:
        __ : Profile = self
        return Profile__get__reachableFrom(__)
    
    @property
    def journeys_walking_speed(self) -> Optional[bool]:
        __ : Profile = self
        return Profile__get__journeysWalkingSpeed(__)
    
    @property
    def trips_by_name(self) -> Optional[bool]:
        __ : Profile = self
        return Profile__get__tripsByName(__)
    
    @property
    def remarks(self) -> Optional[bool]:
        __ : Profile = self
        return Profile__get__remarks(__)
    
    @property
    def remarks_get_polyline(self) -> Optional[bool]:
        __ : Profile = self
        return Profile__get__remarksGetPolyline(__)
    
    @property
    def lines(self) -> Optional[bool]:
        __ : Profile = self
        return Profile__get__lines(__)
    

Profile_reflection = expr_295

def Profile__ctor_35A3D895(locale: str, timezone: str, format_station: Callable[[str], str], transform_journeys_query: Callable[[Optional[JourneysOptions], TripSearchRequest], TripSearchRequest], parse_common: Callable[[Context, RawCommon], CommonData], parse_arrival: Callable[[Context, RawJny], Alternative], parse_departure: Callable[[Context, RawJny], Alternative], parse_hint: Callable[[Context, RawRem], Optional[Any]], parse_icon: Callable[[Context, RawIco], Optional[Icon]], parse_polyline: Callable[[Context, RawPoly], FeatureCollection], parse_locations: Callable[[Context, List[RawLoc]], List[Any]], parse_line: Callable[[Context, RawProd], Line], parse_journey: Callable[[Context, RawOutCon], Journey], parse_journey_leg: Callable[[Context, RawSec, str], Leg], parse_movement: Callable[[Context, RawJny], Movement], parse_operator: Callable[[Context, RawOp], Operator], parse_platform: Callable[[Context, Optional[str], Optional[str], Optional[bool]], Platform], parse_stopover: Callable[[Context, RawStop, str], StopOver], parse_stopovers: Callable[[Context, Optional[List[RawStop]], str], Optional[List[StopOver]]], parse_trip: Callable[[Context, RawJny], Trip], parse_when: Callable[[Context, str, Optional[str], Optional[str], Optional[int], Optional[bool]], ParsedWhen], parse_date_time: Callable[[Context, str, Optional[str], Optional[int]], Optional[str]], parse_bitmask: Callable[[Context, int], IndexMap_2[str, bool]], parse_warning: Callable[[Context, RawHim], Warning]) -> Profile:
    return Profile(locale, timezone, format_station, transform_journeys_query, parse_common, parse_arrival, parse_departure, parse_hint, parse_icon, parse_polyline, parse_locations, parse_line, parse_journey, parse_journey_leg, parse_movement, parse_operator, parse_platform, parse_stopover, parse_stopovers, parse_trip, parse_when, parse_date_time, parse_bitmask, parse_warning)


def expr_296() -> TypeInfo:
    return record_type("FsHafas.Endpoint.Context", [], Context, lambda: [("profile", Profile_reflection()), ("opt", Options_reflection()), ("common", CommonData_reflection()), ("res", RawResult_reflection())])


class Context(Record):
    def __init__(self, profile: Profile, opt: Options, common: CommonData, res: RawResult) -> None:
        super().__init__()
        self.profile = profile
        self.opt = opt
        self.common = common
        self.res = res
    

Context_reflection = expr_296

def Profile__get_salt(__: Profile) -> str:
    return __.salt_0040


def Profile__set_salt_Z721C83C5(__: Profile, v: str) -> None:
    __.salt_0040 = v


def Profile__get_cfg(__: Profile) -> Optional[Cfg]:
    return __.cfg_0040


def Profile__set_cfg_Z3219B2F8(__: Profile, v: Optional[Cfg]=None) -> None:
    __.cfg_0040 = v


def Profile__get_baseRequest(__: Profile) -> Optional[RawRequest]:
    return __.base_request_0040


def Profile__set_baseRequest_Z42C91061(__: Profile, v: Optional[RawRequest]=None) -> None:
    __.base_request_0040 = v


def Profile__get_journeysOutFrwd(__: Profile) -> bool:
    return __.journeys_out_frwd_0040


def Profile__set_journeysOutFrwd_Z1FBCCD16(__: Profile, v: bool) -> None:
    __.journeys_out_frwd_0040 = v


def Profile__get_departuresGetPasslist(__: Profile) -> bool:
    return __.departures_get_passlist_0040


def Profile__set_departuresGetPasslist_Z1FBCCD16(__: Profile, v: bool) -> None:
    __.departures_get_passlist_0040 = v


def Profile__get_departuresStbFltrEquiv(__: Profile) -> bool:
    return __.departures_stb_fltr_equiv_0040


def Profile__set_departuresStbFltrEquiv_Z1FBCCD16(__: Profile, v: bool) -> None:
    __.departures_stb_fltr_equiv_0040 = v


def Profile__get_formatStation(__: Profile) -> Callable[[str], str]:
    return __.format_station_0040


def Profile__set_formatStation_11D407F6(__: Profile, v: Callable[[str], str]) -> None:
    __.format_station_0040 = v


def Profile__get_transformJourneysQuery(__: Profile) -> Callable[[Optional[JourneysOptions], TripSearchRequest], TripSearchRequest]:
    return curry(2, __.transform_journeys_query_0040)


def Profile__set_transformJourneysQuery_4AA4AF64(__: Profile, v: Callable[[Optional[JourneysOptions], TripSearchRequest], TripSearchRequest]) -> None:
    __.transform_journeys_query_0040 = v


def Profile__get_parseCommon(__: Profile) -> Callable[[Context, RawCommon], CommonData]:
    return curry(2, __.parse_common_0040)


def Profile__set_parseCommon_7B6CA622(__: Profile, v: Callable[[Context, RawCommon], CommonData]) -> None:
    __.parse_common_0040 = v


def Profile__get_parseArrival(__: Profile) -> Callable[[Context, RawJny], Alternative]:
    return curry(2, __.parse_arrival_0040)


def Profile__set_parseArrival_537DC5A(__: Profile, v: Callable[[Context, RawJny], Alternative]) -> None:
    __.parse_arrival_0040 = v


def Profile__get_parseDeparture(__: Profile) -> Callable[[Context, RawJny], Alternative]:
    return curry(2, __.parse_departure_0040)


def Profile__set_parseDeparture_537DC5A(__: Profile, v: Callable[[Context, RawJny], Alternative]) -> None:
    __.parse_departure_0040 = v


def Profile__get_parseHint(__: Profile) -> Callable[[Context, RawRem], Optional[Any]]:
    return curry(2, __.parse_hint_0040)


def Profile__set_parseHint_2044943E(__: Profile, v: Callable[[Context, RawRem], Optional[Any]]) -> None:
    __.parse_hint_0040 = v


def Profile__get_parseIcon(__: Profile) -> Callable[[Context, RawIco], Optional[Icon]]:
    return curry(2, __.parse_icon_0040)


def Profile__set_parseIcon_ZB647E9B(__: Profile, v: Callable[[Context, RawIco], Optional[Icon]]) -> None:
    __.parse_icon_0040 = v


def Profile__get_parsePolyline(__: Profile) -> Callable[[Context, RawPoly], FeatureCollection]:
    return curry(2, __.parse_polyline_0040)


def Profile__set_parsePolyline_20B28720(__: Profile, v: Callable[[Context, RawPoly], FeatureCollection]) -> None:
    __.parse_polyline_0040 = v


def Profile__get_parseLocations(__: Profile) -> Callable[[Context, List[RawLoc]], List[Any]]:
    return curry(2, __.parse_locations_0040)


def Profile__set_parseLocations_Z27464599(__: Profile, v: Callable[[Context, List[RawLoc]], List[Any]]) -> None:
    __.parse_locations_0040 = v


def Profile__get_parseLine(__: Profile) -> Callable[[Context, RawProd], Line]:
    return curry(2, __.parse_line_0040)


def Profile__set_parseLine_718F82F(__: Profile, v: Callable[[Context, RawProd], Line]) -> None:
    __.parse_line_0040 = v


def Profile__get_parseJourney(__: Profile) -> Callable[[Context, RawOutCon], Journey]:
    return curry(2, __.parse_journey_0040)


def Profile__set_parseJourney_Z1F35F4C(__: Profile, v: Callable[[Context, RawOutCon], Journey]) -> None:
    __.parse_journey_0040 = v


def Profile__get_parseJourneyLeg(__: Profile) -> Callable[[Context, RawSec, str], Leg]:
    return curry(3, __.parse_journey_leg_0040)


def Profile__set_parseJourneyLeg_3913217E(__: Profile, v: Callable[[Context, RawSec, str], Leg]) -> None:
    __.parse_journey_leg_0040 = v


def Profile__get_parseMovement(__: Profile) -> Callable[[Context, RawJny], Movement]:
    return curry(2, __.parse_movement_0040)


def Profile__set_parseMovement_Z6A30A80A(__: Profile, v: Callable[[Context, RawJny], Movement]) -> None:
    __.parse_movement_0040 = v


def Profile__get_parseOperator(__: Profile) -> Callable[[Context, RawOp], Operator]:
    return curry(2, __.parse_operator_0040)


def Profile__set_parseOperator_1470F537(__: Profile, v: Callable[[Context, RawOp], Operator]) -> None:
    __.parse_operator_0040 = v


def Profile__get_parsePlatform(__: Profile) -> Callable[[Context, Optional[str], Optional[str], Optional[bool]], Platform]:
    return curry(4, __.parse_platform_0040)


def Profile__set_parsePlatform_5B26FC49(__: Profile, v: Callable[[Context, Optional[str], Optional[str], Optional[bool]], Platform]) -> None:
    __.parse_platform_0040 = v


def Profile__get_parseStopover(__: Profile) -> Callable[[Context, RawStop, str], StopOver]:
    return curry(3, __.parse_stopover_0040)


def Profile__set_parseStopover_Z23BF7DB5(__: Profile, v: Callable[[Context, RawStop, str], StopOver]) -> None:
    __.parse_stopover_0040 = v


def Profile__get_parseStopovers(__: Profile) -> Callable[[Context, Optional[List[RawStop]], str], Optional[List[StopOver]]]:
    return curry(3, __.parse_stopovers_0040)


def Profile__set_parseStopovers_Z70D915B5(__: Profile, v: Callable[[Context, Optional[List[RawStop]], str], Optional[List[StopOver]]]) -> None:
    __.parse_stopovers_0040 = v


def Profile__get_parseTrip(__: Profile) -> Callable[[Context, RawJny], Trip]:
    return curry(2, __.parse_trip_0040)


def Profile__set_parseTrip_Z4AA6F376(__: Profile, v: Callable[[Context, RawJny], Trip]) -> None:
    __.parse_trip_0040 = v


def Profile__get_parseWhen(__: Profile) -> Callable[[Context, str, Optional[str], Optional[str], Optional[int], Optional[bool]], ParsedWhen]:
    return curry(6, __.parse_when_0040)


def Profile__set_parseWhen_58E948D7(__: Profile, v: Callable[[Context, str, Optional[str], Optional[str], Optional[int], Optional[bool]], ParsedWhen]) -> None:
    __.parse_when_0040 = v


def Profile__get_parseDateTime(__: Profile) -> Callable[[Context, str, Optional[str], Optional[int]], Optional[str]]:
    return curry(4, __.parse_date_time_0040)


def Profile__set_parseDateTime_ZC71C28B(__: Profile, v: Callable[[Context, str, Optional[str], Optional[int]], Optional[str]]) -> None:
    __.parse_date_time_0040 = v


def Profile__get_parseBitmask(__: Profile) -> Callable[[Context, int], IndexMap_2[str, bool]]:
    return curry(2, __.parse_bitmask_0040)


def Profile__set_parseBitmask_797ABA12(__: Profile, v: Callable[[Context, int], IndexMap_2[str, bool]]) -> None:
    __.parse_bitmask_0040 = v


def Profile__get_parseWarning(__: Profile) -> Callable[[Context, RawHim], Warning]:
    return curry(2, __.parse_warning_0040)


def Profile__set_parseWarning_1F58EC2E(__: Profile, v: Callable[[Context, RawHim], Warning]) -> None:
    __.parse_warning_0040 = v


def Profile__get__locale(__: Profile) -> str:
    return __._locale_0040


def Profile__set__locale_Z721C83C5(__: Profile, v: str) -> None:
    __._locale_0040 = v


def Profile__get__timezone(__: Profile) -> str:
    return __._timezone_0040


def Profile__set__timezone_Z721C83C5(__: Profile, v: str) -> None:
    __._timezone_0040 = v


def Profile__get__endpoint(__: Profile) -> str:
    return __._endpoint_0040


def Profile__set__endpoint_Z721C83C5(__: Profile, v: str) -> None:
    __._endpoint_0040 = v


def Profile__get__products(__: Profile) -> List[ProductType]:
    return __._products_0040


def Profile__set__products_76A34681(__: Profile, v: List[ProductType]) -> None:
    __._products_0040 = v


def Profile__get__trip(__: Profile) -> Optional[bool]:
    return __._trip_0040


def Profile__set__trip_6FCE9E49(__: Profile, v: Optional[bool]=None) -> None:
    __._trip_0040 = v


def Profile__get__radar(__: Profile) -> Optional[bool]:
    return __._radar_0040


def Profile__set__radar_6FCE9E49(__: Profile, v: Optional[bool]=None) -> None:
    __._radar_0040 = v


def Profile__get__refreshJourney(__: Profile) -> Optional[bool]:
    return __._refreshJourney_0040


def Profile__set__refreshJourney_6FCE9E49(__: Profile, v: Optional[bool]=None) -> None:
    __._refreshJourney_0040 = v


def Profile__get__journeysFromTrip(__: Profile) -> Optional[bool]:
    return __._journeysFromTrip_0040


def Profile__set__journeysFromTrip_6FCE9E49(__: Profile, v: Optional[bool]=None) -> None:
    __._journeysFromTrip_0040 = v


def Profile__get__reachableFrom(__: Profile) -> Optional[bool]:
    return __._reachableFrom_0040


def Profile__set__reachableFrom_6FCE9E49(__: Profile, v: Optional[bool]=None) -> None:
    __._reachableFrom_0040 = v


def Profile__get__journeysWalkingSpeed(__: Profile) -> Optional[bool]:
    return __._journeysWalkingSpeed_0040


def Profile__set__journeysWalkingSpeed_6FCE9E49(__: Profile, v: Optional[bool]=None) -> None:
    __._journeysWalkingSpeed_0040 = v


def Profile__get__tripsByName(__: Profile) -> Optional[bool]:
    return __._tripsByName_0040


def Profile__set__tripsByName_6FCE9E49(__: Profile, v: Optional[bool]=None) -> None:
    __._tripsByName_0040 = v


def Profile__get__remarks(__: Profile) -> Optional[bool]:
    return __._remarks_0040


def Profile__set__remarks_6FCE9E49(__: Profile, v: Optional[bool]=None) -> None:
    __._remarks_0040 = v


def Profile__get__remarksGetPolyline(__: Profile) -> Optional[bool]:
    return __._remarksGetPolyline_0040


def Profile__set__remarksGetPolyline_6FCE9E49(__: Profile, v: Optional[bool]=None) -> None:
    __._remarksGetPolyline_0040 = v


def Profile__get__lines(__: Profile) -> Optional[bool]:
    return __._lines_0040


def Profile__set__lines_6FCE9E49(__: Profile, v: Optional[bool]=None) -> None:
    __._lines_0040 = v


