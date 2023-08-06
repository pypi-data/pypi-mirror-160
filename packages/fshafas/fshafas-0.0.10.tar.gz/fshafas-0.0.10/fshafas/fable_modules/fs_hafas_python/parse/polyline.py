from __future__ import annotations
from array import array as array_3
import polyline
import math
from typing import (MutableSequence, List, Optional, Any, Tuple)
from ...fable_library.array import (try_find, map, sum, map_indexed as map_indexed_1)
from ...fable_library.option import value
from ...fable_library.seq import (to_array, map_indexed)
from ...fable_library.types import Float64Array
from ...fable_library.util import round as round_1
from ...fs_hafas_python.context import Context
from ...fs_hafas_python.types_hafas_client import (FeatureCollection, Stop, Geometry, Feature)
from ...fs_hafas_python.types_raw_hafas_client import (RawPoly, PpLocRef)
from .common import get_element_at

def decode(s: str) -> List[MutableSequence[float]]:
    return []


def round(f: float) -> float:
    return round_1(f, 5)


default_feature_collection : FeatureCollection = FeatureCollection("FeatureCollection", [])

def get_stop(ctx: Context, p: RawPoly, i: int) -> Any:
    match_value : Optional[List[PpLocRef]] = p.pp_loc_ref_l
    if match_value is None:
        pass
    
    else: 
        def predicate(p_loc_ref_l: PpLocRef, ctx: Context=ctx, p: RawPoly=p, i: int=i) -> bool:
            return p_loc_ref_l.pp_idx == i
        
        match_value_1 : Optional[PpLocRef] = try_find(predicate, match_value)
        if match_value_1 is None:
            pass
        
        else: 
            match_value_2 : Optional[Any] = get_element_at(match_value_1.loc_x, ctx.common.locations)
            (pattern_matching_result, s) = (None, None)
            if match_value_2 is not None:
                if isinstance(value(match_value_2), Stop):
                    pattern_matching_result = 0
                    s = value(match_value_2)
                
                else: 
                    pattern_matching_result = 1
                
            
            else: 
                pattern_matching_result = 1
            
            if pattern_matching_result == 0:
                return s
            
        
    


def parse_polyline(ctx: Context, poly: RawPoly) -> FeatureCollection:
    def mapping(i: int, p: MutableSequence[float], ctx: Context=ctx, poly: RawPoly=poly) -> Feature:
        return Feature("Feature", get_stop(ctx, poly, i), Geometry("Point", array_3("d", [round(p[1]), round(p[0])])))
    
    return FeatureCollection(default_feature_collection.type, to_array(map_indexed(mapping, polyline.decode(poly.crd_enc_yx))))


def calculate_distance(p1latitude: float, p1longitude: float, p2latitude: float, p2longitude: float) -> float:
    d_lat : float = ((p2latitude - p1latitude) * 3.141592653589793) / 180
    d_lon : float = ((p2longitude - p1longitude) * 3.141592653589793) / 180
    lat1 : float = (p1latitude * 3.141592653589793) / 180
    lat2 : float = (p2latitude * 3.141592653589793) / 180
    a : float = (math.sin(d_lat / 2) * math.sin(d_lat / 2)) + (((math.sin(d_lon / 2) * math.sin(d_lon / 2)) * math.cos(lat1)) * math.cos(lat2))
    return 6371 * (2 * math.atan2(math.sqrt(a), math.sqrt(1 - a)))


def distance_of_feature_collection(fc: FeatureCollection) -> float:
    def mapping(f: Feature, fc: FeatureCollection=fc) -> Tuple[float, float]:
        return (f.geometry.coordinates[1], f.geometry.coordinates[0])
    
    lat_lon_points : List[Tuple[float, float]] = map(mapping, fc.features, None)
    def mapping_1(i: int, _arg1: Tuple[float, float], fc: FeatureCollection=fc) -> float:
        if i > 0:
            prev : Tuple[float, float] = lat_lon_points[i - 1]
            curr : Tuple[float, float] = lat_lon_points[i]
            return calculate_distance(prev[0], prev[1], curr[0], curr[1])
        
        else: 
            return 0
        
    
    class ObjectExpr437:
        @property
        def GetZero(self) -> Any:
            def arrow_435(__unit: Any=None) -> int:
                return 0
            
            return arrow_435
        
        @property
        def Add(self) -> Any:
            def arrow_436(x: float, y: float) -> float:
                return x + y
            
            return arrow_436
        
    return sum(map_indexed_1(mapping_1, lat_lon_points, Float64Array), ObjectExpr437())


