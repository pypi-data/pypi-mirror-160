from __future__ import annotations
from abc import abstractmethod
from typing import (MutableSequence, Optional, List, Protocol, Any)
from ..fable_library.reflection import (TypeInfo, string_type, int32_type, array_type, bool_type, record_type, option_type, float64_type, obj_type, class_type)
from ..fable_library.types import Record
from .extra_types import (IndexMap_2, IndexMap_2_reflection, Icon, Icon_reflection)

def expr_240() -> TypeInfo:
    return record_type("FsHafas.Client.ProductType", [], ProductType, lambda: [("id", string_type), ("mode", string_type), ("name", string_type), ("short", string_type), ("bitmasks", array_type(int32_type)), ("default", bool_type)])


class ProductType(Record):
    def __init__(self, id: str, mode: str, name: str, short: str, bitmasks: MutableSequence[int], default: bool) -> None:
        super().__init__()
        self.id = id
        self.mode = mode
        self.name = name
        self.short = short
        self.bitmasks = bitmasks
        self.default = default
    

ProductType_reflection = expr_240

class Profile(Protocol):
    @property
    @abstractmethod
    def endpoint(self) -> str:
        ...
    
    @property
    @abstractmethod
    def journeys_from_trip(self) -> Optional[bool]:
        ...
    
    @property
    @abstractmethod
    def journeys_walking_speed(self) -> Optional[bool]:
        ...
    
    @property
    @abstractmethod
    def lines(self) -> Optional[bool]:
        ...
    
    @property
    @abstractmethod
    def locale(self) -> str:
        ...
    
    @property
    @abstractmethod
    def products(self) -> List[ProductType]:
        ...
    
    @property
    @abstractmethod
    def radar(self) -> Optional[bool]:
        ...
    
    @property
    @abstractmethod
    def reachable_from(self) -> Optional[bool]:
        ...
    
    @property
    @abstractmethod
    def refresh_journey(self) -> Optional[bool]:
        ...
    
    @property
    @abstractmethod
    def remarks(self) -> Optional[bool]:
        ...
    
    @property
    @abstractmethod
    def remarks_get_polyline(self) -> Optional[bool]:
        ...
    
    @property
    @abstractmethod
    def timezone(self) -> str:
        ...
    
    @property
    @abstractmethod
    def trip(self) -> Optional[bool]:
        ...
    
    @property
    @abstractmethod
    def trips_by_name(self) -> Optional[bool]:
        ...
    

def expr_241() -> TypeInfo:
    return record_type("FsHafas.Client.Location", [], Location, lambda: [("type", option_type(string_type)), ("id", option_type(string_type)), ("name", option_type(string_type)), ("poi", option_type(bool_type)), ("address", option_type(string_type)), ("longitude", option_type(float64_type)), ("latitude", option_type(float64_type)), ("altitude", option_type(float64_type)), ("distance", option_type(int32_type))])


class Location(Record):
    def __init__(self, type: Optional[str], id: Optional[str], name: Optional[str], poi: Optional[bool], address: Optional[str], longitude: Optional[float], latitude: Optional[float], altitude: Optional[float], distance: Optional[int]) -> None:
        super().__init__()
        self.type = type
        self.id = id
        self.name = name
        self.poi = poi
        self.address = address
        self.longitude = longitude
        self.latitude = latitude
        self.altitude = altitude
        self.distance = distance
    

Location_reflection = expr_241

def expr_242() -> TypeInfo:
    return record_type("FsHafas.Client.ReisezentrumOpeningHours", [], ReisezentrumOpeningHours, lambda: [("Mo", option_type(string_type)), ("Di", option_type(string_type)), ("Mi", option_type(string_type)), ("Do", option_type(string_type)), ("Fr", option_type(string_type)), ("Sa", option_type(string_type)), ("So", option_type(string_type))])


class ReisezentrumOpeningHours(Record):
    def __init__(self, Mo: Optional[str], Di: Optional[str], Mi: Optional[str], Do: Optional[str], Fr: Optional[str], Sa: Optional[str], So: Optional[str]) -> None:
        super().__init__()
        self.Mo = Mo
        self.Di = Di
        self.Mi = Mi
        self.Do = Do
        self.Fr = Fr
        self.Sa = Sa
        self.So = So
    

ReisezentrumOpeningHours_reflection = expr_242

def expr_243() -> TypeInfo:
    return record_type("FsHafas.Client.Station", [], Station, lambda: [("type", option_type(string_type)), ("id", option_type(string_type)), ("name", option_type(string_type)), ("station", option_type(Station_reflection())), ("location", option_type(Location_reflection())), ("products", option_type(IndexMap_2_reflection(string_type, bool_type))), ("lines", option_type(array_type(Line_reflection()))), ("is_meta", option_type(bool_type)), ("regions", option_type(array_type(string_type))), ("facilities", option_type(IndexMap_2_reflection(string_type, string_type))), ("reisezentrum_opening_hours", option_type(ReisezentrumOpeningHours_reflection())), ("stops", option_type(array_type(obj_type))), ("entrances", option_type(array_type(Location_reflection()))), ("transit_authority", option_type(string_type)), ("distance", option_type(int32_type))])


class Station(Record):
    def __init__(self, type: Optional[str], id: Optional[str], name: Optional[str], station: Optional[Station], location: Optional[Location], products: Optional[IndexMap_2[str, bool]], lines: Optional[List[Line]], is_meta: Optional[bool], regions: Optional[List[str]], facilities: Optional[IndexMap_2[str, str]], reisezentrum_opening_hours: Optional[ReisezentrumOpeningHours], stops: Optional[List[Any]], entrances: Optional[List[Location]], transit_authority: Optional[str], distance: Optional[int]) -> None:
        super().__init__()
        self.type = type
        self.id = id
        self.name = name
        self.station = station
        self.location = location
        self.products = products
        self.lines = lines
        self.is_meta = is_meta
        self.regions = regions
        self.facilities = facilities
        self.reisezentrum_opening_hours = reisezentrum_opening_hours
        self.stops = stops
        self.entrances = entrances
        self.transit_authority = transit_authority
        self.distance = distance
    

Station_reflection = expr_243

def expr_244() -> TypeInfo:
    return record_type("FsHafas.Client.Stop", [], Stop, lambda: [("type", option_type(string_type)), ("id", option_type(string_type)), ("name", option_type(string_type)), ("location", option_type(Location_reflection())), ("station", option_type(Station_reflection())), ("products", option_type(IndexMap_2_reflection(string_type, bool_type))), ("lines", option_type(array_type(Line_reflection()))), ("is_meta", option_type(bool_type)), ("reisezentrum_opening_hours", option_type(ReisezentrumOpeningHours_reflection())), ("ids", option_type(IndexMap_2_reflection(string_type, string_type))), ("load_factor", option_type(string_type)), ("entrances", option_type(array_type(Location_reflection()))), ("transit_authority", option_type(string_type)), ("distance", option_type(int32_type))])


class Stop(Record):
    def __init__(self, type: Optional[str], id: Optional[str], name: Optional[str], location: Optional[Location], station: Optional[Station], products: Optional[IndexMap_2[str, bool]], lines: Optional[List[Line]], is_meta: Optional[bool], reisezentrum_opening_hours: Optional[ReisezentrumOpeningHours], ids: Optional[IndexMap_2[str, str]], load_factor: Optional[str], entrances: Optional[List[Location]], transit_authority: Optional[str], distance: Optional[int]) -> None:
        super().__init__()
        self.type = type
        self.id = id
        self.name = name
        self.location = location
        self.station = station
        self.products = products
        self.lines = lines
        self.is_meta = is_meta
        self.reisezentrum_opening_hours = reisezentrum_opening_hours
        self.ids = ids
        self.load_factor = load_factor
        self.entrances = entrances
        self.transit_authority = transit_authority
        self.distance = distance
    

Stop_reflection = expr_244

def expr_245() -> TypeInfo:
    return record_type("FsHafas.Client.Region", [], Region, lambda: [("type", option_type(string_type)), ("id", string_type), ("name", string_type), ("stations", array_type(string_type))])


class Region(Record):
    def __init__(self, type: Optional[str], id: str, name: str, stations: List[str]) -> None:
        super().__init__()
        self.type = type
        self.id = id
        self.name = name
        self.stations = stations
    

Region_reflection = expr_245

def expr_246() -> TypeInfo:
    return record_type("FsHafas.Client.Line", [], Line, lambda: [("type", option_type(string_type)), ("id", option_type(string_type)), ("name", option_type(string_type)), ("admin_code", option_type(string_type)), ("fahrt_nr", option_type(string_type)), ("additional_name", option_type(string_type)), ("product", option_type(string_type)), ("public", option_type(bool_type)), ("mode", option_type(string_type)), ("routes", option_type(array_type(string_type))), ("operator", option_type(Operator_reflection())), ("express", option_type(bool_type)), ("metro", option_type(bool_type)), ("night", option_type(bool_type)), ("nr", option_type(int32_type)), ("symbol", option_type(string_type)), ("directions", option_type(array_type(string_type))), ("product_name", option_type(string_type))])


class Line(Record):
    def __init__(self, type: Optional[str], id: Optional[str], name: Optional[str], admin_code: Optional[str], fahrt_nr: Optional[str], additional_name: Optional[str], product: Optional[str], public: Optional[bool], mode: Optional[str], routes: Optional[List[str]], operator: Optional[Operator], express: Optional[bool], metro: Optional[bool], night: Optional[bool], nr: Optional[int], symbol: Optional[str], directions: Optional[List[str]], product_name: Optional[str]) -> None:
        super().__init__()
        self.type = type
        self.id = id
        self.name = name
        self.admin_code = admin_code
        self.fahrt_nr = fahrt_nr
        self.additional_name = additional_name
        self.product = product
        self.public = public
        self.mode = mode
        self.routes = routes
        self.operator = operator
        self.express = express
        self.metro = metro
        self.night = night
        self.nr = nr
        self.symbol = symbol
        self.directions = directions
        self.product_name = product_name
    

Line_reflection = expr_246

def expr_247() -> TypeInfo:
    return record_type("FsHafas.Client.Route", [], Route, lambda: [("type", option_type(string_type)), ("id", string_type), ("line", string_type), ("mode", string_type), ("stops", array_type(string_type))])


class Route(Record):
    def __init__(self, type: Optional[str], id: str, line: str, mode: str, stops: List[str]) -> None:
        super().__init__()
        self.type = type
        self.id = id
        self.line = line
        self.mode = mode
        self.stops = stops
    

Route_reflection = expr_247

def expr_248() -> TypeInfo:
    return record_type("FsHafas.Client.Cycle", [], Cycle, lambda: [("min", option_type(int32_type)), ("max", option_type(int32_type)), ("nr", option_type(int32_type))])


class Cycle(Record):
    def __init__(self, min: Optional[int], max: Optional[int], nr: Optional[int]) -> None:
        super().__init__()
        self.min = min
        self.max = max
        self.nr = nr
    

Cycle_reflection = expr_248

def expr_249() -> TypeInfo:
    return record_type("FsHafas.Client.ArrivalDeparture", [], ArrivalDeparture, lambda: [("arrival", option_type(float64_type)), ("departure", option_type(float64_type))])


class ArrivalDeparture(Record):
    def __init__(self, arrival: Optional[float], departure: Optional[float]) -> None:
        super().__init__()
        self.arrival = arrival
        self.departure = departure
    

ArrivalDeparture_reflection = expr_249

def expr_250() -> TypeInfo:
    return record_type("FsHafas.Client.Schedule", [], Schedule, lambda: [("type", option_type(string_type)), ("id", string_type), ("route", string_type), ("mode", string_type), ("sequence", array_type(ArrivalDeparture_reflection())), ("starts", array_type(string_type))])


class Schedule(Record):
    def __init__(self, type: Optional[str], id: str, route: str, mode: str, sequence: List[ArrivalDeparture], starts: List[str]) -> None:
        super().__init__()
        self.type = type
        self.id = id
        self.route = route
        self.mode = mode
        self.sequence = sequence
        self.starts = starts
    

Schedule_reflection = expr_250

def expr_251() -> TypeInfo:
    return record_type("FsHafas.Client.Operator", [], Operator, lambda: [("type", option_type(string_type)), ("id", string_type), ("name", string_type)])


class Operator(Record):
    def __init__(self, type: Optional[str], id: str, name: str) -> None:
        super().__init__()
        self.type = type
        self.id = id
        self.name = name
    

Operator_reflection = expr_251

def expr_252() -> TypeInfo:
    return record_type("FsHafas.Client.Hint", [], Hint, lambda: [("type", option_type(string_type)), ("code", option_type(string_type)), ("summary", option_type(string_type)), ("text", string_type), ("trip_id", option_type(string_type))])


class Hint(Record):
    def __init__(self, type: Optional[str], code: Optional[str], summary: Optional[str], text: str, trip_id: Optional[str]) -> None:
        super().__init__()
        self.type = type
        self.code = code
        self.summary = summary
        self.text = text
        self.trip_id = trip_id
    

Hint_reflection = expr_252

def expr_253() -> TypeInfo:
    return record_type("FsHafas.Client.Status", [], Status, lambda: [("type", option_type(string_type)), ("code", option_type(string_type)), ("summary", option_type(string_type)), ("text", string_type), ("trip_id", option_type(string_type))])


class Status(Record):
    def __init__(self, type: Optional[str], code: Optional[str], summary: Optional[str], text: str, trip_id: Optional[str]) -> None:
        super().__init__()
        self.type = type
        self.code = code
        self.summary = summary
        self.text = text
        self.trip_id = trip_id
    

Status_reflection = expr_253

def expr_254() -> TypeInfo:
    return record_type("FsHafas.Client.IcoCrd", [], IcoCrd, lambda: [("x", int32_type), ("y", int32_type), ("type", option_type(string_type))])


class IcoCrd(Record):
    def __init__(self, x: int, y: int, type: Optional[str]) -> None:
        super().__init__()
        self.x = x or 0
        self.y = y or 0
        self.type = type
    

IcoCrd_reflection = expr_254

def expr_255() -> TypeInfo:
    return record_type("FsHafas.Client.Edge", [], Edge, lambda: [("from_loc", option_type(obj_type)), ("to_loc", option_type(obj_type)), ("icon", option_type(Icon_reflection())), ("dir", option_type(int32_type)), ("ico_crd", option_type(IcoCrd_reflection()))])


class Edge(Record):
    def __init__(self, from_loc: Optional[Any], to_loc: Optional[Any], icon: Optional[Icon], dir: Optional[int], ico_crd: Optional[IcoCrd]) -> None:
        super().__init__()
        self.from_loc = from_loc
        self.to_loc = to_loc
        self.icon = icon
        self.dir = dir
        self.ico_crd = ico_crd
    

Edge_reflection = expr_255

def expr_256() -> TypeInfo:
    return record_type("FsHafas.Client.Event", [], Event, lambda: [("from_loc", option_type(obj_type)), ("to_loc", option_type(obj_type)), ("start", option_type(string_type)), ("end", option_type(string_type)), ("sections", option_type(array_type(string_type)))])


class Event(Record):
    def __init__(self, from_loc: Optional[Any], to_loc: Optional[Any], start: Optional[str], end: Optional[str], sections: Optional[List[str]]) -> None:
        super().__init__()
        self.from_loc = from_loc
        self.to_loc = to_loc
        self.start = start
        self.end = end
        self.sections = sections
    

Event_reflection = expr_256

def expr_257() -> TypeInfo:
    return record_type("FsHafas.Client.Warning", [], Warning, lambda: [("type", option_type(string_type)), ("id", option_type(string_type)), ("icon", option_type(Icon_reflection())), ("summary", option_type(string_type)), ("text", option_type(string_type)), ("category", option_type(string_type)), ("priority", option_type(int32_type)), ("products", option_type(IndexMap_2_reflection(string_type, bool_type))), ("edges", option_type(array_type(Edge_reflection()))), ("events", option_type(array_type(Event_reflection()))), ("valid_from", option_type(string_type)), ("valid_until", option_type(string_type)), ("modified", option_type(string_type)), ("company", option_type(string_type)), ("categories", option_type(array_type(int32_type))), ("affected_lines", option_type(array_type(Line_reflection()))), ("from_stops", option_type(array_type(obj_type))), ("to_stops", option_type(array_type(obj_type)))])


class Warning(Record):
    def __init__(self, type: Optional[str], id: Optional[str], icon: Optional[Icon], summary: Optional[str], text: Optional[str], category: Optional[str], priority: Optional[int], products: Optional[IndexMap_2[str, bool]], edges: Optional[List[Edge]], events: Optional[List[Event]], valid_from: Optional[str], valid_until: Optional[str], modified: Optional[str], company: Optional[str], categories: Optional[MutableSequence[int]], affected_lines: Optional[List[Line]], from_stops: Optional[List[Any]], to_stops: Optional[List[Any]]) -> None:
        super().__init__()
        self.type = type
        self.id = id
        self.icon = icon
        self.summary = summary
        self.text = text
        self.category = category
        self.priority = priority
        self.products = products
        self.edges = edges
        self.events = events
        self.valid_from = valid_from
        self.valid_until = valid_until
        self.modified = modified
        self.company = company
        self.categories = categories
        self.affected_lines = affected_lines
        self.from_stops = from_stops
        self.to_stops = to_stops
    

Warning_reflection = expr_257

def expr_258() -> TypeInfo:
    return record_type("FsHafas.Client.Geometry", [], Geometry, lambda: [("type", option_type(string_type)), ("coordinates", array_type(float64_type))])


class Geometry(Record):
    def __init__(self, type: Optional[str], coordinates: MutableSequence[float]) -> None:
        super().__init__()
        self.type = type
        self.coordinates = coordinates
    

Geometry_reflection = expr_258

def expr_259() -> TypeInfo:
    return record_type("FsHafas.Client.Feature", [], Feature, lambda: [("type", option_type(string_type)), ("properties", obj_type), ("geometry", Geometry_reflection())])


class Feature(Record):
    def __init__(self, type: Optional[str], properties: Any, geometry: Geometry) -> None:
        super().__init__()
        self.type = type
        self.properties = properties
        self.geometry = geometry
    

Feature_reflection = expr_259

def expr_260() -> TypeInfo:
    return record_type("FsHafas.Client.FeatureCollection", [], FeatureCollection, lambda: [("type", option_type(string_type)), ("features", array_type(Feature_reflection()))])


class FeatureCollection(Record):
    def __init__(self, type: Optional[str], features: List[Feature]) -> None:
        super().__init__()
        self.type = type
        self.features = features
    

FeatureCollection_reflection = expr_260

def expr_261() -> TypeInfo:
    return record_type("FsHafas.Client.StopOver", [], StopOver, lambda: [("stop", option_type(obj_type)), ("departure", option_type(string_type)), ("departure_delay", option_type(int32_type)), ("prognosed_departure", option_type(string_type)), ("planned_departure", option_type(string_type)), ("departure_platform", option_type(string_type)), ("prognosed_departure_platform", option_type(string_type)), ("planned_departure_platform", option_type(string_type)), ("arrival", option_type(string_type)), ("arrival_delay", option_type(int32_type)), ("prognosed_arrival", option_type(string_type)), ("planned_arrival", option_type(string_type)), ("arrival_platform", option_type(string_type)), ("prognosed_arrival_platform", option_type(string_type)), ("planned_arrival_platform", option_type(string_type)), ("remarks", option_type(array_type(obj_type))), ("pass_by", option_type(bool_type)), ("cancelled", option_type(bool_type))])


class StopOver(Record):
    def __init__(self, stop: Optional[Any], departure: Optional[str], departure_delay: Optional[int], prognosed_departure: Optional[str], planned_departure: Optional[str], departure_platform: Optional[str], prognosed_departure_platform: Optional[str], planned_departure_platform: Optional[str], arrival: Optional[str], arrival_delay: Optional[int], prognosed_arrival: Optional[str], planned_arrival: Optional[str], arrival_platform: Optional[str], prognosed_arrival_platform: Optional[str], planned_arrival_platform: Optional[str], remarks: Optional[List[Any]], pass_by: Optional[bool], cancelled: Optional[bool]) -> None:
        super().__init__()
        self.stop = stop
        self.departure = departure
        self.departure_delay = departure_delay
        self.prognosed_departure = prognosed_departure
        self.planned_departure = planned_departure
        self.departure_platform = departure_platform
        self.prognosed_departure_platform = prognosed_departure_platform
        self.planned_departure_platform = planned_departure_platform
        self.arrival = arrival
        self.arrival_delay = arrival_delay
        self.prognosed_arrival = prognosed_arrival
        self.planned_arrival = planned_arrival
        self.arrival_platform = arrival_platform
        self.prognosed_arrival_platform = prognosed_arrival_platform
        self.planned_arrival_platform = planned_arrival_platform
        self.remarks = remarks
        self.pass_by = pass_by
        self.cancelled = cancelled
    

StopOver_reflection = expr_261

def expr_262() -> TypeInfo:
    return record_type("FsHafas.Client.Trip", [], Trip, lambda: [("id", string_type), ("origin", option_type(obj_type)), ("destination", option_type(obj_type)), ("departure", option_type(string_type)), ("planned_departure", option_type(string_type)), ("prognosed_arrival", option_type(string_type)), ("departure_delay", option_type(int32_type)), ("departure_platform", option_type(string_type)), ("prognosed_departure_platform", option_type(string_type)), ("planned_departure_platform", option_type(string_type)), ("arrival", option_type(string_type)), ("planned_arrival", option_type(string_type)), ("prognosed_departure", option_type(string_type)), ("arrival_delay", option_type(int32_type)), ("arrival_platform", option_type(string_type)), ("prognosed_arrival_platform", option_type(string_type)), ("planned_arrival_platform", option_type(string_type)), ("stopovers", option_type(array_type(StopOver_reflection()))), ("schedule", option_type(float64_type)), ("price", option_type(Price_reflection())), ("operator", option_type(float64_type)), ("direction", option_type(string_type)), ("line", option_type(Line_reflection())), ("reachable", option_type(bool_type)), ("cancelled", option_type(bool_type)), ("walking", option_type(bool_type)), ("load_factor", option_type(string_type)), ("distance", option_type(int32_type)), ("public", option_type(bool_type)), ("transfer", option_type(bool_type)), ("cycle", option_type(Cycle_reflection())), ("alternatives", option_type(array_type(Alternative_reflection()))), ("polyline", option_type(FeatureCollection_reflection())), ("remarks", option_type(array_type(obj_type)))])


class Trip(Record):
    def __init__(self, id: str, origin: Optional[Any], destination: Optional[Any], departure: Optional[str], planned_departure: Optional[str], prognosed_arrival: Optional[str], departure_delay: Optional[int], departure_platform: Optional[str], prognosed_departure_platform: Optional[str], planned_departure_platform: Optional[str], arrival: Optional[str], planned_arrival: Optional[str], prognosed_departure: Optional[str], arrival_delay: Optional[int], arrival_platform: Optional[str], prognosed_arrival_platform: Optional[str], planned_arrival_platform: Optional[str], stopovers: Optional[List[StopOver]], schedule: Optional[float], price: Optional[Price], operator: Optional[float], direction: Optional[str], line: Optional[Line], reachable: Optional[bool], cancelled: Optional[bool], walking: Optional[bool], load_factor: Optional[str], distance: Optional[int], public: Optional[bool], transfer: Optional[bool], cycle: Optional[Cycle], alternatives: Optional[List[Alternative]], polyline: Optional[FeatureCollection], remarks: Optional[List[Any]]) -> None:
        super().__init__()
        self.id = id
        self.origin = origin
        self.destination = destination
        self.departure = departure
        self.planned_departure = planned_departure
        self.prognosed_arrival = prognosed_arrival
        self.departure_delay = departure_delay
        self.departure_platform = departure_platform
        self.prognosed_departure_platform = prognosed_departure_platform
        self.planned_departure_platform = planned_departure_platform
        self.arrival = arrival
        self.planned_arrival = planned_arrival
        self.prognosed_departure = prognosed_departure
        self.arrival_delay = arrival_delay
        self.arrival_platform = arrival_platform
        self.prognosed_arrival_platform = prognosed_arrival_platform
        self.planned_arrival_platform = planned_arrival_platform
        self.stopovers = stopovers
        self.schedule = schedule
        self.price = price
        self.operator = operator
        self.direction = direction
        self.line = line
        self.reachable = reachable
        self.cancelled = cancelled
        self.walking = walking
        self.load_factor = load_factor
        self.distance = distance
        self.public = public
        self.transfer = transfer
        self.cycle = cycle
        self.alternatives = alternatives
        self.polyline = polyline
        self.remarks = remarks
    

Trip_reflection = expr_262

def expr_263() -> TypeInfo:
    return record_type("FsHafas.Client.Price", [], Price, lambda: [("amount", float64_type), ("currency", string_type), ("hint", option_type(string_type))])


class Price(Record):
    def __init__(self, amount: float, currency: str, hint: Optional[str]) -> None:
        super().__init__()
        self.amount = amount
        self.currency = currency
        self.hint = hint
    

Price_reflection = expr_263

def expr_264() -> TypeInfo:
    return record_type("FsHafas.Client.Alternative", [], Alternative, lambda: [("trip_id", string_type), ("direction", option_type(string_type)), ("location", option_type(Location_reflection())), ("line", option_type(Line_reflection())), ("stop", option_type(obj_type)), ("when", option_type(string_type)), ("planned_when", option_type(string_type)), ("prognosed_when", option_type(string_type)), ("delay", option_type(int32_type)), ("platform", option_type(string_type)), ("planned_platform", option_type(string_type)), ("prognosed_platform", option_type(string_type)), ("remarks", option_type(array_type(obj_type))), ("cancelled", option_type(bool_type)), ("load_factor", option_type(string_type)), ("provenance", option_type(string_type)), ("previous_stopovers", option_type(array_type(StopOver_reflection()))), ("next_stopovers", option_type(array_type(StopOver_reflection()))), ("frames", option_type(array_type(Frame_reflection()))), ("polyline", option_type(FeatureCollection_reflection())), ("current_trip_position", option_type(Location_reflection())), ("origin", option_type(obj_type)), ("destination", option_type(obj_type))])


class Alternative(Record):
    def __init__(self, trip_id: str, direction: Optional[str], location: Optional[Location], line: Optional[Line], stop: Optional[Any], when: Optional[str], planned_when: Optional[str], prognosed_when: Optional[str], delay: Optional[int], platform: Optional[str], planned_platform: Optional[str], prognosed_platform: Optional[str], remarks: Optional[List[Any]], cancelled: Optional[bool], load_factor: Optional[str], provenance: Optional[str], previous_stopovers: Optional[List[StopOver]], next_stopovers: Optional[List[StopOver]], frames: Optional[List[Frame]], polyline: Optional[FeatureCollection], current_trip_position: Optional[Location], origin: Optional[Any], destination: Optional[Any]) -> None:
        super().__init__()
        self.trip_id = trip_id
        self.direction = direction
        self.location = location
        self.line = line
        self.stop = stop
        self.when = when
        self.planned_when = planned_when
        self.prognosed_when = prognosed_when
        self.delay = delay
        self.platform = platform
        self.planned_platform = planned_platform
        self.prognosed_platform = prognosed_platform
        self.remarks = remarks
        self.cancelled = cancelled
        self.load_factor = load_factor
        self.provenance = provenance
        self.previous_stopovers = previous_stopovers
        self.next_stopovers = next_stopovers
        self.frames = frames
        self.polyline = polyline
        self.current_trip_position = current_trip_position
        self.origin = origin
        self.destination = destination
    

Alternative_reflection = expr_264

def expr_265() -> TypeInfo:
    return record_type("FsHafas.Client.Leg", [], Leg, lambda: [("trip_id", option_type(string_type)), ("origin", option_type(obj_type)), ("destination", option_type(obj_type)), ("departure", option_type(string_type)), ("planned_departure", option_type(string_type)), ("prognosed_arrival", option_type(string_type)), ("departure_delay", option_type(int32_type)), ("departure_platform", option_type(string_type)), ("prognosed_departure_platform", option_type(string_type)), ("planned_departure_platform", option_type(string_type)), ("arrival", option_type(string_type)), ("planned_arrival", option_type(string_type)), ("prognosed_departure", option_type(string_type)), ("arrival_delay", option_type(int32_type)), ("arrival_platform", option_type(string_type)), ("prognosed_arrival_platform", option_type(string_type)), ("planned_arrival_platform", option_type(string_type)), ("stopovers", option_type(array_type(StopOver_reflection()))), ("schedule", option_type(float64_type)), ("price", option_type(Price_reflection())), ("operator", option_type(float64_type)), ("direction", option_type(string_type)), ("line", option_type(Line_reflection())), ("reachable", option_type(bool_type)), ("cancelled", option_type(bool_type)), ("walking", option_type(bool_type)), ("load_factor", option_type(string_type)), ("distance", option_type(int32_type)), ("public", option_type(bool_type)), ("transfer", option_type(bool_type)), ("cycle", option_type(Cycle_reflection())), ("alternatives", option_type(array_type(Alternative_reflection()))), ("polyline", option_type(FeatureCollection_reflection())), ("remarks", option_type(array_type(obj_type))), ("current_location", option_type(Location_reflection()))])


class Leg(Record):
    def __init__(self, trip_id: Optional[str], origin: Optional[Any], destination: Optional[Any], departure: Optional[str], planned_departure: Optional[str], prognosed_arrival: Optional[str], departure_delay: Optional[int], departure_platform: Optional[str], prognosed_departure_platform: Optional[str], planned_departure_platform: Optional[str], arrival: Optional[str], planned_arrival: Optional[str], prognosed_departure: Optional[str], arrival_delay: Optional[int], arrival_platform: Optional[str], prognosed_arrival_platform: Optional[str], planned_arrival_platform: Optional[str], stopovers: Optional[List[StopOver]], schedule: Optional[float], price: Optional[Price], operator: Optional[float], direction: Optional[str], line: Optional[Line], reachable: Optional[bool], cancelled: Optional[bool], walking: Optional[bool], load_factor: Optional[str], distance: Optional[int], public: Optional[bool], transfer: Optional[bool], cycle: Optional[Cycle], alternatives: Optional[List[Alternative]], polyline: Optional[FeatureCollection], remarks: Optional[List[Any]], current_location: Optional[Location]) -> None:
        super().__init__()
        self.trip_id = trip_id
        self.origin = origin
        self.destination = destination
        self.departure = departure
        self.planned_departure = planned_departure
        self.prognosed_arrival = prognosed_arrival
        self.departure_delay = departure_delay
        self.departure_platform = departure_platform
        self.prognosed_departure_platform = prognosed_departure_platform
        self.planned_departure_platform = planned_departure_platform
        self.arrival = arrival
        self.planned_arrival = planned_arrival
        self.prognosed_departure = prognosed_departure
        self.arrival_delay = arrival_delay
        self.arrival_platform = arrival_platform
        self.prognosed_arrival_platform = prognosed_arrival_platform
        self.planned_arrival_platform = planned_arrival_platform
        self.stopovers = stopovers
        self.schedule = schedule
        self.price = price
        self.operator = operator
        self.direction = direction
        self.line = line
        self.reachable = reachable
        self.cancelled = cancelled
        self.walking = walking
        self.load_factor = load_factor
        self.distance = distance
        self.public = public
        self.transfer = transfer
        self.cycle = cycle
        self.alternatives = alternatives
        self.polyline = polyline
        self.remarks = remarks
        self.current_location = current_location
    

Leg_reflection = expr_265

def expr_266() -> TypeInfo:
    return record_type("FsHafas.Client.Journey", [], Journey, lambda: [("type", option_type(string_type)), ("legs", array_type(Leg_reflection())), ("refresh_token", option_type(string_type)), ("remarks", option_type(array_type(obj_type))), ("price", option_type(Price_reflection())), ("cycle", option_type(Cycle_reflection())), ("scheduled_days", option_type(IndexMap_2_reflection(string_type, bool_type)))])


class Journey(Record):
    def __init__(self, type: Optional[str], legs: List[Leg], refresh_token: Optional[str], remarks: Optional[List[Any]], price: Optional[Price], cycle: Optional[Cycle], scheduled_days: Optional[IndexMap_2[str, bool]]) -> None:
        super().__init__()
        self.type = type
        self.legs = legs
        self.refresh_token = refresh_token
        self.remarks = remarks
        self.price = price
        self.cycle = cycle
        self.scheduled_days = scheduled_days
    

Journey_reflection = expr_266

def expr_267() -> TypeInfo:
    return record_type("FsHafas.Client.Journeys", [], Journeys, lambda: [("earlier_ref", option_type(string_type)), ("later_ref", option_type(string_type)), ("journeys", option_type(array_type(Journey_reflection()))), ("realtime_data_from", option_type(int32_type))])


class Journeys(Record):
    def __init__(self, earlier_ref: Optional[str], later_ref: Optional[str], journeys: Optional[List[Journey]], realtime_data_from: Optional[int]) -> None:
        super().__init__()
        self.earlier_ref = earlier_ref
        self.later_ref = later_ref
        self.journeys = journeys
        self.realtime_data_from = realtime_data_from
    

Journeys_reflection = expr_267

def expr_268() -> TypeInfo:
    return record_type("FsHafas.Client.Duration", [], Duration, lambda: [("duration", int32_type), ("stations", array_type(obj_type))])


class Duration(Record):
    def __init__(self, duration: int, stations: List[Any]) -> None:
        super().__init__()
        self.duration = duration or 0
        self.stations = stations
    

Duration_reflection = expr_268

def expr_269() -> TypeInfo:
    return record_type("FsHafas.Client.Frame", [], Frame, lambda: [("origin", obj_type), ("destination", obj_type), ("t", option_type(int32_type))])


class Frame(Record):
    def __init__(self, origin: Any, destination: Any, t: Optional[int]) -> None:
        super().__init__()
        self.origin = origin
        self.destination = destination
        self.t = t
    

Frame_reflection = expr_269

def expr_270() -> TypeInfo:
    return record_type("FsHafas.Client.Movement", [], Movement, lambda: [("direction", option_type(string_type)), ("trip_id", option_type(string_type)), ("line", option_type(Line_reflection())), ("location", option_type(Location_reflection())), ("next_stopovers", option_type(array_type(StopOver_reflection()))), ("frames", option_type(array_type(Frame_reflection()))), ("polyline", option_type(FeatureCollection_reflection()))])


class Movement(Record):
    def __init__(self, direction: Optional[str], trip_id: Optional[str], line: Optional[Line], location: Optional[Location], next_stopovers: Optional[List[StopOver]], frames: Optional[List[Frame]], polyline: Optional[FeatureCollection]) -> None:
        super().__init__()
        self.direction = direction
        self.trip_id = trip_id
        self.line = line
        self.location = location
        self.next_stopovers = next_stopovers
        self.frames = frames
        self.polyline = polyline
    

Movement_reflection = expr_270

def expr_271() -> TypeInfo:
    return record_type("FsHafas.Client.ServerInfo", [], ServerInfo, lambda: [("hci_version", option_type(string_type)), ("timetable_start", option_type(string_type)), ("timetable_end", option_type(string_type)), ("server_time", option_type(string_type)), ("realtime_data_updated_at", option_type(int32_type))])


class ServerInfo(Record):
    def __init__(self, hci_version: Optional[str], timetable_start: Optional[str], timetable_end: Optional[str], server_time: Optional[str], realtime_data_updated_at: Optional[int]) -> None:
        super().__init__()
        self.hci_version = hci_version
        self.timetable_start = timetable_start
        self.timetable_end = timetable_end
        self.server_time = server_time
        self.realtime_data_updated_at = realtime_data_updated_at
    

ServerInfo_reflection = expr_271

def expr_272() -> TypeInfo:
    return record_type("FsHafas.Client.LoyaltyCard", [], LoyaltyCard, lambda: [("type", option_type(string_type)), ("discount", option_type(int32_type)), ("class_", option_type(int32_type))])


class LoyaltyCard(Record):
    def __init__(self, type: Optional[str], discount: Optional[int], class_: Optional[int]) -> None:
        super().__init__()
        self.type = type
        self.discount = discount
        self.class_ = class_
    

LoyaltyCard_reflection = expr_272

def expr_273() -> TypeInfo:
    return record_type("FsHafas.Client.JourneysOptions", [], JourneysOptions, lambda: [("departure", option_type(class_type("System.DateTime"))), ("arrival", option_type(class_type("System.DateTime"))), ("earlier_than", option_type(string_type)), ("later_than", option_type(string_type)), ("results", option_type(int32_type)), ("via", option_type(string_type)), ("stopovers", option_type(bool_type)), ("transfers", option_type(int32_type)), ("transfer_time", option_type(int32_type)), ("accessibility", option_type(string_type)), ("bike", option_type(bool_type)), ("products", option_type(IndexMap_2_reflection(string_type, bool_type))), ("tickets", option_type(bool_type)), ("polylines", option_type(bool_type)), ("sub_stops", option_type(bool_type)), ("entrances", option_type(bool_type)), ("remarks", option_type(bool_type)), ("walking_speed", option_type(string_type)), ("start_with_walking", option_type(bool_type)), ("language", option_type(string_type)), ("scheduled_days", option_type(bool_type)), ("first_class", option_type(bool_type)), ("age", option_type(int32_type)), ("loyalty_card", option_type(LoyaltyCard_reflection())), ("when", option_type(class_type("System.DateTime")))])


class JourneysOptions(Record):
    def __init__(self, departure: Optional[Any], arrival: Optional[Any], earlier_than: Optional[str], later_than: Optional[str], results: Optional[int], via: Optional[str], stopovers: Optional[bool], transfers: Optional[int], transfer_time: Optional[int], accessibility: Optional[str], bike: Optional[bool], products: Optional[IndexMap_2[str, bool]], tickets: Optional[bool], polylines: Optional[bool], sub_stops: Optional[bool], entrances: Optional[bool], remarks: Optional[bool], walking_speed: Optional[str], start_with_walking: Optional[bool], language: Optional[str], scheduled_days: Optional[bool], first_class: Optional[bool], age: Optional[int], loyalty_card: Optional[LoyaltyCard], when: Optional[Any]) -> None:
        super().__init__()
        self.departure = departure
        self.arrival = arrival
        self.earlier_than = earlier_than
        self.later_than = later_than
        self.results = results
        self.via = via
        self.stopovers = stopovers
        self.transfers = transfers
        self.transfer_time = transfer_time
        self.accessibility = accessibility
        self.bike = bike
        self.products = products
        self.tickets = tickets
        self.polylines = polylines
        self.sub_stops = sub_stops
        self.entrances = entrances
        self.remarks = remarks
        self.walking_speed = walking_speed
        self.start_with_walking = start_with_walking
        self.language = language
        self.scheduled_days = scheduled_days
        self.first_class = first_class
        self.age = age
        self.loyalty_card = loyalty_card
        self.when = when
    

JourneysOptions_reflection = expr_273

def expr_274() -> TypeInfo:
    return record_type("FsHafas.Client.JourneysFromTripOptions", [], JourneysFromTripOptions, lambda: [("stopovers", option_type(bool_type)), ("transfer_time", option_type(int32_type)), ("accessibility", option_type(string_type)), ("tickets", option_type(bool_type)), ("polylines", option_type(bool_type)), ("sub_stops", option_type(bool_type)), ("entrances", option_type(bool_type)), ("remarks", option_type(bool_type)), ("products", option_type(IndexMap_2_reflection(string_type, bool_type)))])


class JourneysFromTripOptions(Record):
    def __init__(self, stopovers: Optional[bool], transfer_time: Optional[int], accessibility: Optional[str], tickets: Optional[bool], polylines: Optional[bool], sub_stops: Optional[bool], entrances: Optional[bool], remarks: Optional[bool], products: Optional[IndexMap_2[str, bool]]) -> None:
        super().__init__()
        self.stopovers = stopovers
        self.transfer_time = transfer_time
        self.accessibility = accessibility
        self.tickets = tickets
        self.polylines = polylines
        self.sub_stops = sub_stops
        self.entrances = entrances
        self.remarks = remarks
        self.products = products
    

JourneysFromTripOptions_reflection = expr_274

def expr_275() -> TypeInfo:
    return record_type("FsHafas.Client.LocationsOptions", [], LocationsOptions, lambda: [("fuzzy", option_type(bool_type)), ("results", option_type(int32_type)), ("stops", option_type(bool_type)), ("addresses", option_type(bool_type)), ("poi", option_type(bool_type)), ("sub_stops", option_type(bool_type)), ("entrances", option_type(bool_type)), ("lines_of_stops", option_type(bool_type)), ("language", option_type(string_type))])


class LocationsOptions(Record):
    def __init__(self, fuzzy: Optional[bool], results: Optional[int], stops: Optional[bool], addresses: Optional[bool], poi: Optional[bool], sub_stops: Optional[bool], entrances: Optional[bool], lines_of_stops: Optional[bool], language: Optional[str]) -> None:
        super().__init__()
        self.fuzzy = fuzzy
        self.results = results
        self.stops = stops
        self.addresses = addresses
        self.poi = poi
        self.sub_stops = sub_stops
        self.entrances = entrances
        self.lines_of_stops = lines_of_stops
        self.language = language
    

LocationsOptions_reflection = expr_275

def expr_276() -> TypeInfo:
    return record_type("FsHafas.Client.TripOptions", [], TripOptions, lambda: [("stopovers", option_type(bool_type)), ("polyline", option_type(bool_type)), ("sub_stops", option_type(bool_type)), ("entrances", option_type(bool_type)), ("remarks", option_type(bool_type)), ("language", option_type(string_type))])


class TripOptions(Record):
    def __init__(self, stopovers: Optional[bool], polyline: Optional[bool], sub_stops: Optional[bool], entrances: Optional[bool], remarks: Optional[bool], language: Optional[str]) -> None:
        super().__init__()
        self.stopovers = stopovers
        self.polyline = polyline
        self.sub_stops = sub_stops
        self.entrances = entrances
        self.remarks = remarks
        self.language = language
    

TripOptions_reflection = expr_276

def expr_277() -> TypeInfo:
    return record_type("FsHafas.Client.StopOptions", [], StopOptions, lambda: [("lines_of_stops", option_type(bool_type)), ("sub_stops", option_type(bool_type)), ("entrances", option_type(bool_type)), ("remarks", option_type(bool_type)), ("language", option_type(string_type))])


class StopOptions(Record):
    def __init__(self, lines_of_stops: Optional[bool], sub_stops: Optional[bool], entrances: Optional[bool], remarks: Optional[bool], language: Optional[str]) -> None:
        super().__init__()
        self.lines_of_stops = lines_of_stops
        self.sub_stops = sub_stops
        self.entrances = entrances
        self.remarks = remarks
        self.language = language
    

StopOptions_reflection = expr_277

def expr_278() -> TypeInfo:
    return record_type("FsHafas.Client.DeparturesArrivalsOptions", [], DeparturesArrivalsOptions, lambda: [("when", option_type(class_type("System.DateTime"))), ("direction", option_type(string_type)), ("line", option_type(string_type)), ("duration", option_type(int32_type)), ("results", option_type(int32_type)), ("sub_stops", option_type(bool_type)), ("entrances", option_type(bool_type)), ("lines_of_stops", option_type(bool_type)), ("remarks", option_type(bool_type)), ("stopovers", option_type(bool_type)), ("include_related_stations", option_type(bool_type)), ("products", option_type(IndexMap_2_reflection(string_type, bool_type))), ("language", option_type(string_type))])


class DeparturesArrivalsOptions(Record):
    def __init__(self, when: Optional[Any], direction: Optional[str], line: Optional[str], duration: Optional[int], results: Optional[int], sub_stops: Optional[bool], entrances: Optional[bool], lines_of_stops: Optional[bool], remarks: Optional[bool], stopovers: Optional[bool], include_related_stations: Optional[bool], products: Optional[IndexMap_2[str, bool]], language: Optional[str]) -> None:
        super().__init__()
        self.when = when
        self.direction = direction
        self.line = line
        self.duration = duration
        self.results = results
        self.sub_stops = sub_stops
        self.entrances = entrances
        self.lines_of_stops = lines_of_stops
        self.remarks = remarks
        self.stopovers = stopovers
        self.include_related_stations = include_related_stations
        self.products = products
        self.language = language
    

DeparturesArrivalsOptions_reflection = expr_278

def expr_279() -> TypeInfo:
    return record_type("FsHafas.Client.RefreshJourneyOptions", [], RefreshJourneyOptions, lambda: [("stopovers", option_type(bool_type)), ("polylines", option_type(bool_type)), ("tickets", option_type(bool_type)), ("sub_stops", option_type(bool_type)), ("entrances", option_type(bool_type)), ("remarks", option_type(bool_type)), ("language", option_type(string_type))])


class RefreshJourneyOptions(Record):
    def __init__(self, stopovers: Optional[bool], polylines: Optional[bool], tickets: Optional[bool], sub_stops: Optional[bool], entrances: Optional[bool], remarks: Optional[bool], language: Optional[str]) -> None:
        super().__init__()
        self.stopovers = stopovers
        self.polylines = polylines
        self.tickets = tickets
        self.sub_stops = sub_stops
        self.entrances = entrances
        self.remarks = remarks
        self.language = language
    

RefreshJourneyOptions_reflection = expr_279

def expr_280() -> TypeInfo:
    return record_type("FsHafas.Client.NearByOptions", [], NearByOptions, lambda: [("results", option_type(int32_type)), ("distance", option_type(int32_type)), ("poi", option_type(bool_type)), ("stops", option_type(bool_type)), ("products", option_type(IndexMap_2_reflection(string_type, bool_type))), ("sub_stops", option_type(bool_type)), ("entrances", option_type(bool_type)), ("lines_of_stops", option_type(bool_type)), ("language", option_type(string_type))])


class NearByOptions(Record):
    def __init__(self, results: Optional[int], distance: Optional[int], poi: Optional[bool], stops: Optional[bool], products: Optional[IndexMap_2[str, bool]], sub_stops: Optional[bool], entrances: Optional[bool], lines_of_stops: Optional[bool], language: Optional[str]) -> None:
        super().__init__()
        self.results = results
        self.distance = distance
        self.poi = poi
        self.stops = stops
        self.products = products
        self.sub_stops = sub_stops
        self.entrances = entrances
        self.lines_of_stops = lines_of_stops
        self.language = language
    

NearByOptions_reflection = expr_280

def expr_281() -> TypeInfo:
    return record_type("FsHafas.Client.ReachableFromOptions", [], ReachableFromOptions, lambda: [("when", option_type(class_type("System.DateTime"))), ("max_transfers", option_type(int32_type)), ("max_duration", option_type(int32_type)), ("products", option_type(IndexMap_2_reflection(string_type, bool_type))), ("sub_stops", option_type(bool_type)), ("entrances", option_type(bool_type)), ("polylines", option_type(bool_type))])


class ReachableFromOptions(Record):
    def __init__(self, when: Optional[Any], max_transfers: Optional[int], max_duration: Optional[int], products: Optional[IndexMap_2[str, bool]], sub_stops: Optional[bool], entrances: Optional[bool], polylines: Optional[bool]) -> None:
        super().__init__()
        self.when = when
        self.max_transfers = max_transfers
        self.max_duration = max_duration
        self.products = products
        self.sub_stops = sub_stops
        self.entrances = entrances
        self.polylines = polylines
    

ReachableFromOptions_reflection = expr_281

def expr_282() -> TypeInfo:
    return record_type("FsHafas.Client.BoundingBox", [], BoundingBox, lambda: [("north", float64_type), ("west", float64_type), ("south", float64_type), ("east", float64_type)])


class BoundingBox(Record):
    def __init__(self, north: float, west: float, south: float, east: float) -> None:
        super().__init__()
        self.north = north
        self.west = west
        self.south = south
        self.east = east
    

BoundingBox_reflection = expr_282

def expr_283() -> TypeInfo:
    return record_type("FsHafas.Client.RadarOptions", [], RadarOptions, lambda: [("results", option_type(int32_type)), ("frames", option_type(int32_type)), ("products", option_type(IndexMap_2_reflection(string_type, bool_type))), ("duration", option_type(int32_type)), ("sub_stops", option_type(bool_type)), ("entrances", option_type(bool_type)), ("polylines", option_type(bool_type)), ("when", option_type(class_type("System.DateTime")))])


class RadarOptions(Record):
    def __init__(self, results: Optional[int], frames: Optional[int], products: Optional[IndexMap_2[str, bool]], duration: Optional[int], sub_stops: Optional[bool], entrances: Optional[bool], polylines: Optional[bool], when: Optional[Any]) -> None:
        super().__init__()
        self.results = results
        self.frames = frames
        self.products = products
        self.duration = duration
        self.sub_stops = sub_stops
        self.entrances = entrances
        self.polylines = polylines
        self.when = when
    

RadarOptions_reflection = expr_283

def expr_284() -> TypeInfo:
    return record_type("FsHafas.Client.Filter", [], Filter, lambda: [("type", option_type(string_type)), ("mode", string_type), ("value", string_type)])


class Filter(Record):
    def __init__(self, type: Optional[str], mode: str, value: str) -> None:
        super().__init__()
        self.type = type
        self.mode = mode
        self.value = value
    

Filter_reflection = expr_284

def expr_285() -> TypeInfo:
    return record_type("FsHafas.Client.TripsByNameOptions", [], TripsByNameOptions, lambda: [("when", option_type(class_type("System.DateTime"))), ("from_when", option_type(class_type("System.DateTime"))), ("until_when", option_type(class_type("System.DateTime"))), ("only_currently_running", option_type(bool_type)), ("products", option_type(IndexMap_2_reflection(string_type, bool_type))), ("currently_stopping_at", option_type(obj_type)), ("line_name", option_type(string_type)), ("operator_names", option_type(array_type(string_type))), ("additional_filters", option_type(array_type(Filter_reflection())))])


class TripsByNameOptions(Record):
    def __init__(self, when: Optional[Any], from_when: Optional[Any], until_when: Optional[Any], only_currently_running: Optional[bool], products: Optional[IndexMap_2[str, bool]], currently_stopping_at: Optional[Any], line_name: Optional[str], operator_names: Optional[List[str]], additional_filters: Optional[List[Filter]]) -> None:
        super().__init__()
        self.when = when
        self.from_when = from_when
        self.until_when = until_when
        self.only_currently_running = only_currently_running
        self.products = products
        self.currently_stopping_at = currently_stopping_at
        self.line_name = line_name
        self.operator_names = operator_names
        self.additional_filters = additional_filters
    

TripsByNameOptions_reflection = expr_285

def expr_286() -> TypeInfo:
    return record_type("FsHafas.Client.RemarksOptions", [], RemarksOptions, lambda: [("from_", option_type(class_type("System.DateTime"))), ("to", option_type(class_type("System.DateTime"))), ("results", option_type(int32_type)), ("products", option_type(IndexMap_2_reflection(string_type, bool_type))), ("polylines", option_type(bool_type)), ("language", option_type(string_type))])


class RemarksOptions(Record):
    def __init__(self, from_: Optional[Any], to: Optional[Any], results: Optional[int], products: Optional[IndexMap_2[str, bool]], polylines: Optional[bool], language: Optional[str]) -> None:
        super().__init__()
        self.from_ = from_
        self.to = to
        self.results = results
        self.products = products
        self.polylines = polylines
        self.language = language
    

RemarksOptions_reflection = expr_286

def expr_287() -> TypeInfo:
    return record_type("FsHafas.Client.LinesOptions", [], LinesOptions, lambda: [("language", option_type(string_type))])


class LinesOptions(Record):
    def __init__(self, language: Optional[str]=None) -> None:
        super().__init__()
        self.language = language
    

LinesOptions_reflection = expr_287

def expr_288() -> TypeInfo:
    return record_type("FsHafas.Client.ServerOptions", [], ServerOptions, lambda: [("version_info", option_type(bool_type)), ("language", option_type(string_type))])


class ServerOptions(Record):
    def __init__(self, version_info: Optional[bool], language: Optional[str]) -> None:
        super().__init__()
        self.version_info = version_info
        self.language = language
    

ServerOptions_reflection = expr_288

class HafasClient(Protocol):
    @abstractmethod
    def arrivals(self, __arg0: Any, __arg1: Optional[DeparturesArrivalsOptions]) -> Promise_1[List[Alternative]]:
        ...
    
    @abstractmethod
    def departures(self, __arg0: Any, __arg1: Optional[DeparturesArrivalsOptions]) -> Promise_1[List[Alternative]]:
        ...
    
    @abstractmethod
    def journeys(self, __arg0: Any, __arg1: Any, __arg2: Optional[JourneysOptions]) -> Promise_1[Journeys]:
        ...
    
    @abstractmethod
    def journeys_from_trip(self, __arg0: str, __arg1: StopOver, __arg2: Any, __arg3: Optional[JourneysFromTripOptions]) -> Promise_1[List[Journey]]:
        ...
    
    @abstractmethod
    def lines(self, __arg0: str, __arg1: Optional[LinesOptions]) -> Promise_1[List[Line]]:
        ...
    
    @abstractmethod
    def locations(self, __arg0: str, __arg1: Optional[LocationsOptions]) -> Promise_1[List[Any]]:
        ...
    
    @abstractmethod
    def nearby(self, __arg0: Location, __arg1: Optional[NearByOptions]) -> Promise_1[List[Any]]:
        ...
    
    @abstractmethod
    def radar(self, __arg0: BoundingBox, __arg1: Optional[RadarOptions]) -> Promise_1[List[Movement]]:
        ...
    
    @abstractmethod
    def reachable_from(self, __arg0: Location, __arg1: Optional[ReachableFromOptions]) -> Promise_1[List[Duration]]:
        ...
    
    @abstractmethod
    def refresh_journey(self, __arg0: str, __arg1: Optional[RefreshJourneyOptions]) -> Promise_1[Journey]:
        ...
    
    @abstractmethod
    def remarks(self, __arg0: Optional[RemarksOptions]) -> Promise_1[List[Warning]]:
        ...
    
    @abstractmethod
    def server_info(self, __arg0: Optional[ServerOptions]) -> Promise_1[ServerInfo]:
        ...
    
    @abstractmethod
    def stop(self, __arg0: Any, __arg1: Optional[StopOptions]) -> Promise_1[Any]:
        ...
    
    @abstractmethod
    def trip(self, __arg0: str, __arg1: str, __arg2: Optional[TripOptions]) -> Promise_1[Trip]:
        ...
    
    @abstractmethod
    def trips_by_name(self, __arg0: str, __arg1: Optional[TripsByNameOptions]) -> Promise_1[List[Trip]]:
        ...
    

