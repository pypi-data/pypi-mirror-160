from __future__ import annotations
from typing import (Optional, List, Tuple, TypeVar, Any)
from ..fable_library.async_builder import (singleton, Async)
from ..fable_library.option import default_arg
from ..fable_library.reflection import (TypeInfo, class_type)
from ..fable_library.string import (to_console, printf)
from ..fs_hafas_python.extensions.raw_request_ex import encode
from ..fs_hafas_python.extensions.raw_response import decode
from ..fs_hafas_python.lib.request import (HttpClient__ctor, HttpClient__Dispose, HttpClient__PostAsync)
from .extra_types import (HafasError, Log_Print, HafasError__ctor_Z384F8060)
from .types_raw_hafas_client import (Cfg, RawRequest, LocMatchRequest, RawResult, RawMatch, RawCommon, RawLoc, TripSearchRequest, RawOutCon, JourneyDetailsRequest, RawJny, StationBoardRequest, ReconstructionRequest, JourneyMatchRequest, LocGeoPosRequest, LocGeoReachRequest, RawPos, LocDetailsRequest, JourneyGeoPosRequest, HimSearchRequest, RawHim, LineMatchRequest, RawLine, ServerInfoRequest, SearchOnTripRequest, SvcReq, RawResponse, SvcRes)

_A_ = TypeVar("_A_")

def expr_312() -> TypeInfo:
    return class_type("FsHafas.Api.HafasRawClient", None, HafasRawClient)


class HafasRawClient:
    def __init__(self, endpoint: str, salt: str, cfg: Cfg, base_request: RawRequest) -> None:
        self.endpoint = endpoint
        self.salt = salt
        self.cfg = cfg
        self.base_request = base_request
        self.http_client = HttpClient__ctor()
    

HafasRawClient_reflection = expr_312

def HafasRawClient__ctor_6D5FF7F7(endpoint: str, salt: str, cfg: Cfg, base_request: RawRequest) -> HafasRawClient:
    return HafasRawClient(endpoint, salt, cfg, base_request)


def HafasRawClient__Dispose(__: HafasRawClient) -> None:
    HttpClient__Dispose(__.http_client)


def HafasRawClient__AsyncLocMatch_781FF3B0(__: HafasRawClient, lang: str, loc_match_request: LocMatchRequest) -> Async[Tuple[Optional[RawCommon], Optional[RawResult], Optional[List[RawLoc]]]]:
    def arrow_314(__: HafasRawClient=__, lang: str=lang, loc_match_request: LocMatchRequest=loc_match_request) -> Async[Tuple[Optional[RawCommon], Optional[RawResult], Optional[List[RawLoc]]]]:
        def arrow_313(_arg3: RawResult) -> Async[Tuple[Optional[RawCommon], Optional[RawResult], Optional[List[RawLoc]]]]:
            res : RawResult = _arg3
            match_value : Optional[RawMatch] = res.match
            if match_value is not None:
                match : RawMatch = match_value
                return singleton.Return((res.common, res, match.loc_l))
            
            else: 
                return singleton.Return((None, None, None))
            
        
        return singleton.Bind(HafasRawClient__asyncPost_737B0FC(__, HafasRawClient__makeRequest(__, "LocMatch", lang, loc_match_request)), arrow_313)
    
    return singleton.Delay(arrow_314)


def HafasRawClient__AsyncTripSearch_Z4D007EE(__: HafasRawClient, lang: str, trip_search_request: TripSearchRequest) -> Async[Tuple[Optional[RawCommon], Optional[RawResult], Optional[List[RawOutCon]]]]:
    def arrow_316(__: HafasRawClient=__, lang: str=lang, trip_search_request: TripSearchRequest=trip_search_request) -> Async[Tuple[Optional[RawCommon], Optional[RawResult], Optional[List[RawOutCon]]]]:
        def arrow_315(_arg4: RawResult) -> Async[Tuple[Optional[RawCommon], Optional[RawResult], Optional[List[RawOutCon]]]]:
            res : RawResult = _arg4
            return singleton.Return((res.common, res, res.out_con_l))
        
        return singleton.Bind(HafasRawClient__asyncPost_737B0FC(__, HafasRawClient__makeRequest(__, "TripSearch", lang, trip_search_request)), arrow_315)
    
    return singleton.Delay(arrow_316)


def HafasRawClient__AsyncJourneyDetails_73FB16B1(__: HafasRawClient, lang: str, journey_details_request: JourneyDetailsRequest) -> Async[Tuple[Optional[RawCommon], Optional[RawResult], Optional[RawJny]]]:
    def arrow_318(__: HafasRawClient=__, lang: str=lang, journey_details_request: JourneyDetailsRequest=journey_details_request) -> Async[Tuple[Optional[RawCommon], Optional[RawResult], Optional[RawJny]]]:
        def arrow_317(_arg5: RawResult) -> Async[Tuple[Optional[RawCommon], Optional[RawResult], Optional[RawJny]]]:
            res : RawResult = _arg5
            return singleton.Return((res.common, res, res.journey))
        
        return singleton.Bind(HafasRawClient__asyncPost_737B0FC(__, HafasRawClient__makeRequest(__, "JourneyDetails", lang, journey_details_request)), arrow_317)
    
    return singleton.Delay(arrow_318)


def HafasRawClient__AsyncStationBoard_3FCEEA3(__: HafasRawClient, lang: str, station_board_request: StationBoardRequest) -> Async[Tuple[Optional[RawCommon], Optional[RawResult], Optional[List[RawJny]]]]:
    def arrow_320(__: HafasRawClient=__, lang: str=lang, station_board_request: StationBoardRequest=station_board_request) -> Async[Tuple[Optional[RawCommon], Optional[RawResult], Optional[List[RawJny]]]]:
        def arrow_319(_arg6: RawResult) -> Async[Tuple[Optional[RawCommon], Optional[RawResult], Optional[List[RawJny]]]]:
            res : RawResult = _arg6
            return singleton.Return((res.common, res, res.jny_l))
        
        return singleton.Bind(HafasRawClient__asyncPost_737B0FC(__, HafasRawClient__makeRequest(__, "StationBoard", lang, station_board_request)), arrow_319)
    
    return singleton.Delay(arrow_320)


def HafasRawClient__AsyncReconstruction_Z19A33557(__: HafasRawClient, lang: str, reconstruction_request: ReconstructionRequest) -> Async[Tuple[Optional[RawCommon], Optional[RawResult], Optional[List[RawOutCon]]]]:
    def arrow_322(__: HafasRawClient=__, lang: str=lang, reconstruction_request: ReconstructionRequest=reconstruction_request) -> Async[Tuple[Optional[RawCommon], Optional[RawResult], Optional[List[RawOutCon]]]]:
        def arrow_321(_arg7: RawResult) -> Async[Tuple[Optional[RawCommon], Optional[RawResult], Optional[List[RawOutCon]]]]:
            res : RawResult = _arg7
            return singleton.Return((res.common, res, res.out_con_l))
        
        return singleton.Bind(HafasRawClient__asyncPost_737B0FC(__, HafasRawClient__makeRequest(__, "Reconstruction", lang, reconstruction_request)), arrow_321)
    
    return singleton.Delay(arrow_322)


def HafasRawClient__AsyncJourneyMatch_Z61E31480(__: HafasRawClient, lang: str, journey_match_request: JourneyMatchRequest) -> Async[Tuple[Optional[RawCommon], Optional[RawResult], Optional[List[RawJny]]]]:
    def arrow_324(__: HafasRawClient=__, lang: str=lang, journey_match_request: JourneyMatchRequest=journey_match_request) -> Async[Tuple[Optional[RawCommon], Optional[RawResult], Optional[List[RawJny]]]]:
        def arrow_323(_arg8: RawResult) -> Async[Tuple[Optional[RawCommon], Optional[RawResult], Optional[List[RawJny]]]]:
            res : RawResult = _arg8
            return singleton.Return((res.common, res, res.jny_l))
        
        return singleton.Bind(HafasRawClient__asyncPost_737B0FC(__, HafasRawClient__makeRequest(__, "JourneyMatch", lang, journey_match_request)), arrow_323)
    
    return singleton.Delay(arrow_324)


def HafasRawClient__AsyncLocGeoPos_3C0E4562(__: HafasRawClient, lang: str, loc_geo_pos_request: LocGeoPosRequest) -> Async[Tuple[Optional[RawCommon], Optional[RawResult], Optional[List[RawLoc]]]]:
    def arrow_326(__: HafasRawClient=__, lang: str=lang, loc_geo_pos_request: LocGeoPosRequest=loc_geo_pos_request) -> Async[Tuple[Optional[RawCommon], Optional[RawResult], Optional[List[RawLoc]]]]:
        def arrow_325(_arg9: RawResult) -> Async[Tuple[Optional[RawCommon], Optional[RawResult], Optional[List[RawLoc]]]]:
            res : RawResult = _arg9
            return singleton.Return((res.common, res, res.loc_l))
        
        return singleton.Bind(HafasRawClient__asyncPost_737B0FC(__, HafasRawClient__makeRequest(__, "LocGeoPos", lang, loc_geo_pos_request)), arrow_325)
    
    return singleton.Delay(arrow_326)


def HafasRawClient__AsyncLocGeoReach_320A81B3(__: HafasRawClient, lang: str, loc_geo_reach_request: LocGeoReachRequest) -> Async[Tuple[Optional[RawCommon], Optional[RawResult], List[RawPos]]]:
    def arrow_328(__: HafasRawClient=__, lang: str=lang, loc_geo_reach_request: LocGeoReachRequest=loc_geo_reach_request) -> Async[Tuple[Optional[RawCommon], Optional[RawResult], List[RawPos]]]:
        def arrow_327(_arg10: RawResult) -> Async[Tuple[Optional[RawCommon], Optional[RawResult], List[RawPos]]]:
            res : RawResult = _arg10
            match_value : Optional[List[RawPos]] = res.pos_l
            if match_value is not None:
                pos_l : List[RawPos] = match_value
                return singleton.Return((res.common, res, pos_l))
            
            else: 
                return singleton.Return((None, None, []))
            
        
        return singleton.Bind(HafasRawClient__asyncPost_737B0FC(__, HafasRawClient__makeRequest(__, "LocGeoReach", lang, loc_geo_reach_request)), arrow_327)
    
    return singleton.Delay(arrow_328)


def HafasRawClient__AsyncLocDetails_2FCF6141(__: HafasRawClient, lang: str, loc_details_request: LocDetailsRequest) -> Async[Tuple[Optional[RawCommon], Optional[RawResult], Optional[RawLoc]]]:
    def arrow_330(__: HafasRawClient=__, lang: str=lang, loc_details_request: LocDetailsRequest=loc_details_request) -> Async[Tuple[Optional[RawCommon], Optional[RawResult], Optional[RawLoc]]]:
        def arrow_329(_arg11: RawResult) -> Async[Tuple[Optional[RawCommon], Optional[RawResult], Optional[RawLoc]]]:
            res : RawResult = _arg11
            match_value : Optional[List[RawLoc]] = res.loc_l
            (pattern_matching_result, loc_l_1) = (None, None)
            if match_value is not None:
                if len(match_value) > 0:
                    pattern_matching_result = 0
                    loc_l_1 = match_value
                
                else: 
                    pattern_matching_result = 1
                
            
            else: 
                pattern_matching_result = 1
            
            if pattern_matching_result == 0:
                return singleton.Return((res.common, res, loc_l_1[0]))
            
            elif pattern_matching_result == 1:
                return singleton.Return((None, None, None))
            
        
        return singleton.Bind(HafasRawClient__asyncPost_737B0FC(__, HafasRawClient__makeRequest(__, "LocDetails", lang, loc_details_request)), arrow_329)
    
    return singleton.Delay(arrow_330)


def HafasRawClient__AsyncJourneyGeoPos_Z6DB7B6AE(__: HafasRawClient, lang: str, journey_geo_pos_request: JourneyGeoPosRequest) -> Async[Tuple[Optional[RawCommon], Optional[RawResult], Optional[List[RawJny]]]]:
    def arrow_332(__: HafasRawClient=__, lang: str=lang, journey_geo_pos_request: JourneyGeoPosRequest=journey_geo_pos_request) -> Async[Tuple[Optional[RawCommon], Optional[RawResult], Optional[List[RawJny]]]]:
        def arrow_331(_arg12: RawResult) -> Async[Tuple[Optional[RawCommon], Optional[RawResult], Optional[List[RawJny]]]]:
            res : RawResult = _arg12
            return singleton.Return((res.common, res, res.jny_l))
        
        return singleton.Bind(HafasRawClient__asyncPost_737B0FC(__, HafasRawClient__makeRequest(__, "JourneyGeoPos", lang, journey_geo_pos_request)), arrow_331)
    
    return singleton.Delay(arrow_332)


def HafasRawClient__AsyncHimSearch_Z6033479F(__: HafasRawClient, lang: str, him_search_request: HimSearchRequest) -> Async[Tuple[Optional[RawCommon], Optional[RawResult], Optional[List[RawHim]]]]:
    def arrow_334(__: HafasRawClient=__, lang: str=lang, him_search_request: HimSearchRequest=him_search_request) -> Async[Tuple[Optional[RawCommon], Optional[RawResult], Optional[List[RawHim]]]]:
        def arrow_333(_arg13: RawResult) -> Async[Tuple[Optional[RawCommon], Optional[RawResult], Optional[List[RawHim]]]]:
            res : RawResult = _arg13
            return singleton.Return((res.common, res, res.msg_l))
        
        return singleton.Bind(HafasRawClient__asyncPost_737B0FC(__, HafasRawClient__makeRequest(__, "HimSearch", lang, him_search_request)), arrow_333)
    
    return singleton.Delay(arrow_334)


def HafasRawClient__AsyncLineMatch_Z69AA7EA2(__: HafasRawClient, lang: str, line_match_request: LineMatchRequest) -> Async[Tuple[Optional[RawCommon], Optional[RawResult], Optional[List[RawLine]]]]:
    def arrow_336(__: HafasRawClient=__, lang: str=lang, line_match_request: LineMatchRequest=line_match_request) -> Async[Tuple[Optional[RawCommon], Optional[RawResult], Optional[List[RawLine]]]]:
        def arrow_335(_arg14: RawResult) -> Async[Tuple[Optional[RawCommon], Optional[RawResult], Optional[List[RawLine]]]]:
            res : RawResult = _arg14
            return singleton.Return((res.common, res, res.line_l))
        
        return singleton.Bind(HafasRawClient__asyncPost_737B0FC(__, HafasRawClient__makeRequest(__, "LineMatch", lang, line_match_request)), arrow_335)
    
    return singleton.Delay(arrow_336)


def HafasRawClient__AsyncServerInfo_Z684EE398(__: HafasRawClient, lang: str, server_info_request: ServerInfoRequest) -> Async[Tuple[Optional[RawCommon], Optional[RawResult]]]:
    def arrow_338(__: HafasRawClient=__, lang: str=lang, server_info_request: ServerInfoRequest=server_info_request) -> Async[Tuple[Optional[RawCommon], Optional[RawResult]]]:
        def arrow_337(_arg15: RawResult) -> Async[Tuple[Optional[RawCommon], Optional[RawResult]]]:
            res : RawResult = _arg15
            return singleton.Return((res.common, res))
        
        return singleton.Bind(HafasRawClient__asyncPost_737B0FC(__, HafasRawClient__makeRequest(__, "ServerInfo", lang, server_info_request)), arrow_337)
    
    return singleton.Delay(arrow_338)


def HafasRawClient__AsyncSearchOnTrip_5D40A373(__: HafasRawClient, lang: str, search_on_trip_request: SearchOnTripRequest) -> Async[Tuple[Optional[RawCommon], Optional[RawResult], Optional[List[RawOutCon]]]]:
    def arrow_340(__: HafasRawClient=__, lang: str=lang, search_on_trip_request: SearchOnTripRequest=search_on_trip_request) -> Async[Tuple[Optional[RawCommon], Optional[RawResult], Optional[List[RawOutCon]]]]:
        def arrow_339(_arg16: RawResult) -> Async[Tuple[Optional[RawCommon], Optional[RawResult], Optional[List[RawOutCon]]]]:
            res : RawResult = _arg16
            return singleton.Return((res.common, res, res.out_con_l))
        
        return singleton.Bind(HafasRawClient__asyncPost_737B0FC(__, HafasRawClient__makeRequest(__, "SearchOnTrip", lang, search_on_trip_request)), arrow_339)
    
    return singleton.Delay(arrow_340)


def HafasRawClient__toException_ZAAE3ECF(this: HafasRawClient, ex: HafasError) -> HafasError:
    return ex


def HafasRawClient__log(this: HafasRawClient, msg: str, o: _A_) -> None:
    Log_Print(msg, o)


def HafasRawClient__makeRequest(this: HafasRawClient, meth: str, lang: str, parameters: Any=None) -> RawRequest:
    input_record : RawRequest = this.base_request
    return RawRequest(lang, [SvcReq(this.cfg, meth, parameters)], input_record.client, input_record.ext, input_record.ver, input_record.auth)


def HafasRawClient__asyncPost_737B0FC(this: HafasRawClient, request: RawRequest) -> Async[RawResult]:
    json : str = encode(request)
    HafasRawClient__log(this, "request:", json)
    def arrow_356(this: HafasRawClient=this, request: RawRequest=request) -> Async[RawResult]:
        def arrow_355(_arg1: str) -> Async[RawResult]:
            result : str = _arg1
            HafasRawClient__log(this, "response:", result)
            def arrow_351(__unit: Any=None) -> Async[RawResult]:
                if len(result) == 0:
                    def arrow_341(__unit: Any=None) -> RawResult:
                        raise Exception("invalid response")
                    
                    return singleton.Return(arrow_341())
                
                else: 
                    response : RawResponse = decode(result)
                    svc_res_l : List[SvcRes] = default_arg(response.svc_res_l, [])
                    if len(svc_res_l) == 1:
                        svc_res : SvcRes = svc_res_l[0]
                        match_value : Tuple[Optional[str], Optional[str], Optional[RawResult]] = (svc_res.err, svc_res.err_txt, svc_res.res)
                        (pattern_matching_result, err_1, err_txt_1) = (None, None, None)
                        if match_value[0] is not None:
                            if match_value[1] is not None:
                                def arrow_345(__unit: Any=None) -> bool:
                                    err_txt : str = match_value[1]
                                    return match_value[0] != "OK"
                                
                                if arrow_345():
                                    pattern_matching_result = 0
                                    err_1 = match_value[0]
                                    err_txt_1 = match_value[1]
                                
                                else: 
                                    pattern_matching_result = 1
                                
                            
                            else: 
                                pattern_matching_result = 1
                            
                        
                        else: 
                            pattern_matching_result = 1
                        
                        if pattern_matching_result == 0:
                            def arrow_342(__unit: Any=None) -> RawResult:
                                raise HafasError__ctor_Z384F8060(err_1, err_txt_1)
                            
                            return singleton.Return(arrow_342())
                        
                        elif pattern_matching_result == 1:
                            (pattern_matching_result_1, err_3) = (None, None)
                            if match_value[0] is not None:
                                if match_value[0] != "OK":
                                    pattern_matching_result_1 = 0
                                    err_3 = match_value[0]
                                
                                else: 
                                    pattern_matching_result_1 = 1
                                
                            
                            else: 
                                pattern_matching_result_1 = 1
                            
                            if pattern_matching_result_1 == 0:
                                def arrow_343(__unit: Any=None) -> RawResult:
                                    raise HafasError__ctor_Z384F8060(err_3, err_3)
                                
                                return singleton.Return(arrow_343())
                            
                            elif pattern_matching_result_1 == 1:
                                if match_value[2] is not None:
                                    res : RawResult = match_value[2]
                                    return singleton.Return(res)
                                
                                else: 
                                    def arrow_344(__unit: Any=None) -> RawResult:
                                        raise Exception("invalid response")
                                    
                                    return singleton.Return(arrow_344())
                                
                            
                        
                    
                    else: 
                        match_value_1 : Tuple[Optional[str], Optional[str]] = (response.err, response.err_txt)
                        def arrow_347(__unit: Any=None) -> Async[RawResult]:
                            err_4 : str = match_value_1[0]
                            err_txt_2 : str = match_value_1[1]
                            def arrow_346(__unit: Any=None) -> RawResult:
                                raise HafasError__ctor_Z384F8060(err_4, err_txt_2)
                            
                            return singleton.Return(arrow_346())
                        
                        def arrow_349(__unit: Any=None) -> Async[RawResult]:
                            err_5 : str = match_value_1[0]
                            def arrow_348(__unit: Any=None) -> RawResult:
                                raise HafasError__ctor_Z384F8060(err_5, err_5)
                            
                            return singleton.Return(arrow_348())
                        
                        def arrow_350(__unit: Any=None) -> RawResult:
                            raise Exception("invalid response")
                        
                        return (arrow_347() if (match_value_1[1] is not None) else arrow_349()) if (match_value_1[0] is not None) else singleton.Return(arrow_350())
                    
                
            
            def arrow_354(_arg2: Exception) -> Async[RawResult]:
                if isinstance(_arg2, HafasError):
                    def arrow_352(__unit: Any=None) -> RawResult:
                        raise HafasRawClient__toException_ZAAE3ECF(this, _arg2)
                    
                    return singleton.Return(arrow_352())
                
                else: 
                    arg10_1 : str = str(_arg2)
                    to_console(printf("error: %s"))(arg10_1)
                    def arrow_353(__unit: Any=None) -> RawResult:
                        raise Exception("invalid response")
                    
                    return singleton.Return(arrow_353())
                
            
            return singleton.TryWith(singleton.Delay(arrow_351), arrow_354)
        
        return singleton.Bind(HttpClient__PostAsync(this.http_client, this.endpoint, this.salt, json), arrow_355)
    
    return singleton.Delay(arrow_356)


