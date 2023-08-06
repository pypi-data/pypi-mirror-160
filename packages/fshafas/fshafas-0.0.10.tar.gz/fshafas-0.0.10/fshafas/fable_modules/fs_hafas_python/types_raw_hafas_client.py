from __future__ import annotations
from typing import (MutableSequence, Optional, List, Any)
from ..fable_library.reflection import (TypeInfo, string_type, record_type, int32_type, option_type, array_type, bool_type, obj_type)
from ..fable_library.types import Record

def expr_161() -> TypeInfo:
    return record_type("FsHafas.Raw.RawPltf", [], RawPltf, lambda: [("type", string_type), ("txt", string_type)])


class RawPltf(Record):
    def __init__(self, type: str, txt: str) -> None:
        super().__init__()
        self.type = type
        self.txt = txt
    

RawPltf_reflection = expr_161

def expr_162() -> TypeInfo:
    return record_type("FsHafas.Raw.RawTrnCmpSX", [], RawTrnCmpSX, lambda: [("tc_m", option_type(int32_type)), ("tcoc_x", option_type(array_type(int32_type)))])


class RawTrnCmpSX(Record):
    def __init__(self, tc_m: Optional[int], tcoc_x: Optional[MutableSequence[int]]) -> None:
        super().__init__()
        self.tc_m = tc_m
        self.tcoc_x = tcoc_x
    

RawTrnCmpSX_reflection = expr_162

def expr_163() -> TypeInfo:
    return record_type("FsHafas.Raw.RawDep", [], RawDep, lambda: [("loc_x", option_type(int32_type)), ("idx", option_type(int32_type)), ("d_prod_x", option_type(int32_type)), ("d_platf_s", option_type(string_type)), ("d_in_r", option_type(bool_type)), ("d_time_s", option_type(string_type)), ("d_prog_type", option_type(string_type)), ("d_trn_cmp_sx", option_type(RawTrnCmpSX_reflection())), ("d_tzoffset", option_type(int32_type)), ("type", option_type(string_type)), ("d_time_r", option_type(string_type)), ("d_cncl", option_type(bool_type)), ("d_pltf_s", option_type(RawPltf_reflection())), ("d_platf_r", option_type(string_type)), ("d_pltf_r", option_type(RawPltf_reflection()))])


class RawDep(Record):
    def __init__(self, loc_x: Optional[int], idx: Optional[int], d_prod_x: Optional[int], d_platf_s: Optional[str], d_in_r: Optional[bool], d_time_s: Optional[str], d_prog_type: Optional[str], d_trn_cmp_sx: Optional[RawTrnCmpSX], d_tzoffset: Optional[int], type: Optional[str], d_time_r: Optional[str], d_cncl: Optional[bool], d_pltf_s: Optional[RawPltf], d_platf_r: Optional[str], d_pltf_r: Optional[RawPltf]) -> None:
        super().__init__()
        self.loc_x = loc_x
        self.idx = idx
        self.d_prod_x = d_prod_x
        self.d_platf_s = d_platf_s
        self.d_in_r = d_in_r
        self.d_time_s = d_time_s
        self.d_prog_type = d_prog_type
        self.d_trn_cmp_sx = d_trn_cmp_sx
        self.d_tzoffset = d_tzoffset
        self.type = type
        self.d_time_r = d_time_r
        self.d_cncl = d_cncl
        self.d_pltf_s = d_pltf_s
        self.d_platf_r = d_platf_r
        self.d_pltf_r = d_pltf_r
    

RawDep_reflection = expr_163

def expr_164() -> TypeInfo:
    return record_type("FsHafas.Raw.RawArr", [], RawArr, lambda: [("loc_x", option_type(int32_type)), ("idx", option_type(int32_type)), ("a_platf_s", option_type(string_type)), ("a_out_r", option_type(bool_type)), ("a_time_s", option_type(string_type)), ("a_prog_type", option_type(string_type)), ("a_tzoffset", option_type(int32_type)), ("type", option_type(string_type)), ("a_time_r", option_type(string_type)), ("a_cncl", option_type(bool_type)), ("a_pltf_s", option_type(RawPltf_reflection())), ("a_platf_r", option_type(string_type)), ("a_pltf_r", option_type(RawPltf_reflection())), ("prod_l", option_type(array_type(RawProd_reflection())))])


class RawArr(Record):
    def __init__(self, loc_x: Optional[int], idx: Optional[int], a_platf_s: Optional[str], a_out_r: Optional[bool], a_time_s: Optional[str], a_prog_type: Optional[str], a_tzoffset: Optional[int], type: Optional[str], a_time_r: Optional[str], a_cncl: Optional[bool], a_pltf_s: Optional[RawPltf], a_platf_r: Optional[str], a_pltf_r: Optional[RawPltf], prod_l: Optional[List[RawProd]]) -> None:
        super().__init__()
        self.loc_x = loc_x
        self.idx = idx
        self.a_platf_s = a_platf_s
        self.a_out_r = a_out_r
        self.a_time_s = a_time_s
        self.a_prog_type = a_prog_type
        self.a_tzoffset = a_tzoffset
        self.type = type
        self.a_time_r = a_time_r
        self.a_cncl = a_cncl
        self.a_pltf_s = a_pltf_s
        self.a_platf_r = a_platf_r
        self.a_pltf_r = a_pltf_r
        self.prod_l = prod_l
    

RawArr_reflection = expr_164

def expr_165() -> TypeInfo:
    return record_type("FsHafas.Raw.PubCh", [], PubCh, lambda: [("name", string_type), ("f_date", string_type), ("f_time", string_type), ("t_date", string_type), ("t_time", string_type)])


class PubCh(Record):
    def __init__(self, name: str, f_date: str, f_time: str, t_date: str, t_time: str) -> None:
        super().__init__()
        self.name = name
        self.f_date = f_date
        self.f_time = f_time
        self.t_date = t_date
        self.t_time = t_time
    

PubCh_reflection = expr_165

def expr_166() -> TypeInfo:
    return record_type("FsHafas.Raw.RawHim", [], RawHim, lambda: [("hid", string_type), ("act", bool_type), ("pub", option_type(string_type)), ("head", option_type(string_type)), ("lead", option_type(string_type)), ("text", option_type(string_type)), ("tckr", option_type(string_type)), ("ico_x", int32_type), ("prio", int32_type), ("f_loc_x", option_type(int32_type)), ("t_loc_x", option_type(int32_type)), ("prod", option_type(int32_type)), ("l_mod_date", option_type(string_type)), ("l_mod_time", option_type(string_type)), ("s_date", option_type(string_type)), ("s_time", option_type(string_type)), ("e_date", option_type(string_type)), ("e_time", option_type(string_type)), ("cat", option_type(int32_type)), ("pub_ch_l", array_type(PubCh_reflection())), ("edge_ref_l", option_type(array_type(int32_type))), ("region_ref_l", option_type(array_type(int32_type))), ("cat_ref_l", option_type(array_type(int32_type))), ("event_ref_l", option_type(array_type(int32_type))), ("aff_prod_ref_l", option_type(array_type(int32_type))), ("comp", option_type(string_type))])


class RawHim(Record):
    def __init__(self, hid: str, act: bool, pub: Optional[str], head: Optional[str], lead: Optional[str], text: Optional[str], tckr: Optional[str], ico_x: int, prio: int, f_loc_x: Optional[int], t_loc_x: Optional[int], prod: Optional[int], l_mod_date: Optional[str], l_mod_time: Optional[str], s_date: Optional[str], s_time: Optional[str], e_date: Optional[str], e_time: Optional[str], cat: Optional[int], pub_ch_l: List[PubCh], edge_ref_l: Optional[MutableSequence[int]], region_ref_l: Optional[MutableSequence[int]], cat_ref_l: Optional[MutableSequence[int]], event_ref_l: Optional[MutableSequence[int]], aff_prod_ref_l: Optional[MutableSequence[int]], comp: Optional[str]) -> None:
        super().__init__()
        self.hid = hid
        self.act = act
        self.pub = pub
        self.head = head
        self.lead = lead
        self.text = text
        self.tckr = tckr
        self.ico_x = ico_x or 0
        self.prio = prio or 0
        self.f_loc_x = f_loc_x
        self.t_loc_x = t_loc_x
        self.prod = prod
        self.l_mod_date = l_mod_date
        self.l_mod_time = l_mod_time
        self.s_date = s_date
        self.s_time = s_time
        self.e_date = e_date
        self.e_time = e_time
        self.cat = cat
        self.pub_ch_l = pub_ch_l
        self.edge_ref_l = edge_ref_l
        self.region_ref_l = region_ref_l
        self.cat_ref_l = cat_ref_l
        self.event_ref_l = event_ref_l
        self.aff_prod_ref_l = aff_prod_ref_l
        self.comp = comp
    

RawHim_reflection = expr_166

def expr_167() -> TypeInfo:
    return record_type("FsHafas.Raw.RawMsg", [], RawMsg, lambda: [("type", string_type), ("rem_x", option_type(int32_type)), ("f_loc_x", option_type(int32_type)), ("t_loc_x", option_type(int32_type)), ("f_idx", option_type(int32_type)), ("t_idx", option_type(int32_type)), ("him_x", option_type(int32_type)), ("tag_l", option_type(array_type(string_type)))])


class RawMsg(Record):
    def __init__(self, type: str, rem_x: Optional[int], f_loc_x: Optional[int], t_loc_x: Optional[int], f_idx: Optional[int], t_idx: Optional[int], him_x: Optional[int], tag_l: Optional[List[str]]) -> None:
        super().__init__()
        self.type = type
        self.rem_x = rem_x
        self.f_loc_x = f_loc_x
        self.t_loc_x = t_loc_x
        self.f_idx = f_idx
        self.t_idx = t_idx
        self.him_x = him_x
        self.tag_l = tag_l
    

RawMsg_reflection = expr_167

def expr_168() -> TypeInfo:
    return record_type("FsHafas.Raw.RawRem", [], RawRem, lambda: [("type", string_type), ("code", string_type), ("prio", option_type(int32_type)), ("ico_x", option_type(int32_type)), ("txt_n", option_type(string_type)), ("txt_s", option_type(string_type)), ("jid", option_type(string_type))])


class RawRem(Record):
    def __init__(self, type: str, code: str, prio: Optional[int], ico_x: Optional[int], txt_n: Optional[str], txt_s: Optional[str], jid: Optional[str]) -> None:
        super().__init__()
        self.type = type
        self.code = code
        self.prio = prio
        self.ico_x = ico_x
        self.txt_n = txt_n
        self.txt_s = txt_s
        self.jid = jid
    

RawRem_reflection = expr_168

def expr_169() -> TypeInfo:
    return record_type("FsHafas.Raw.RawStop", [], RawStop, lambda: [("loc_x", int32_type), ("idx", option_type(int32_type)), ("d_prod_x", option_type(int32_type)), ("d_in_r", option_type(bool_type)), ("d_time_s", option_type(string_type)), ("d_time_r", option_type(string_type)), ("d_tzoffset", option_type(int32_type)), ("d_cncl", option_type(bool_type)), ("d_in_s", option_type(bool_type)), ("d_platf_s", option_type(string_type)), ("d_pltf_s", option_type(RawPltf_reflection())), ("d_platf_r", option_type(string_type)), ("d_pltf_r", option_type(RawPltf_reflection())), ("d_prog_type", option_type(string_type)), ("d_dir_txt", option_type(string_type)), ("d_dir_flg", option_type(string_type)), ("d_trn_cmp_sx", option_type(RawTrnCmpSX_reflection())), ("a_prod_x", option_type(int32_type)), ("a_platf_s", option_type(string_type)), ("a_pltf_s", option_type(RawPltf_reflection())), ("a_platf_r", option_type(string_type)), ("a_pltf_r", option_type(RawPltf_reflection())), ("a_out_r", option_type(bool_type)), ("a_time_s", option_type(string_type)), ("a_time_r", option_type(string_type)), ("a_tzoffset", option_type(int32_type)), ("a_cncl", option_type(bool_type)), ("a_out_s", option_type(bool_type)), ("a_platf_ch", option_type(bool_type)), ("a_prog_type", option_type(string_type)), ("type", option_type(string_type)), ("msg_l", option_type(array_type(RawMsg_reflection()))), ("rem_l", option_type(array_type(RawRem_reflection())))])


class RawStop(Record):
    def __init__(self, loc_x: int, idx: Optional[int], d_prod_x: Optional[int], d_in_r: Optional[bool], d_time_s: Optional[str], d_time_r: Optional[str], d_tzoffset: Optional[int], d_cncl: Optional[bool], d_in_s: Optional[bool], d_platf_s: Optional[str], d_pltf_s: Optional[RawPltf], d_platf_r: Optional[str], d_pltf_r: Optional[RawPltf], d_prog_type: Optional[str], d_dir_txt: Optional[str], d_dir_flg: Optional[str], d_trn_cmp_sx: Optional[RawTrnCmpSX], a_prod_x: Optional[int], a_platf_s: Optional[str], a_pltf_s: Optional[RawPltf], a_platf_r: Optional[str], a_pltf_r: Optional[RawPltf], a_out_r: Optional[bool], a_time_s: Optional[str], a_time_r: Optional[str], a_tzoffset: Optional[int], a_cncl: Optional[bool], a_out_s: Optional[bool], a_platf_ch: Optional[bool], a_prog_type: Optional[str], type: Optional[str], msg_l: Optional[List[RawMsg]], rem_l: Optional[List[RawRem]]) -> None:
        super().__init__()
        self.loc_x = loc_x or 0
        self.idx = idx
        self.d_prod_x = d_prod_x
        self.d_in_r = d_in_r
        self.d_time_s = d_time_s
        self.d_time_r = d_time_r
        self.d_tzoffset = d_tzoffset
        self.d_cncl = d_cncl
        self.d_in_s = d_in_s
        self.d_platf_s = d_platf_s
        self.d_pltf_s = d_pltf_s
        self.d_platf_r = d_platf_r
        self.d_pltf_r = d_pltf_r
        self.d_prog_type = d_prog_type
        self.d_dir_txt = d_dir_txt
        self.d_dir_flg = d_dir_flg
        self.d_trn_cmp_sx = d_trn_cmp_sx
        self.a_prod_x = a_prod_x
        self.a_platf_s = a_platf_s
        self.a_pltf_s = a_pltf_s
        self.a_platf_r = a_platf_r
        self.a_pltf_r = a_pltf_r
        self.a_out_r = a_out_r
        self.a_time_s = a_time_s
        self.a_time_r = a_time_r
        self.a_tzoffset = a_tzoffset
        self.a_cncl = a_cncl
        self.a_out_s = a_out_s
        self.a_platf_ch = a_platf_ch
        self.a_prog_type = a_prog_type
        self.type = type
        self.msg_l = msg_l
        self.rem_l = rem_l
    

RawStop_reflection = expr_169

def expr_170() -> TypeInfo:
    return record_type("FsHafas.Raw.PpLocRef", [], PpLocRef, lambda: [("pp_idx", int32_type), ("loc_x", int32_type)])


class PpLocRef(Record):
    def __init__(self, pp_idx: int, loc_x: int) -> None:
        super().__init__()
        self.pp_idx = pp_idx or 0
        self.loc_x = loc_x or 0
    

PpLocRef_reflection = expr_170

def expr_171() -> TypeInfo:
    return record_type("FsHafas.Raw.RawPoly", [], RawPoly, lambda: [("delta", bool_type), ("dim", int32_type), ("type", option_type(string_type)), ("crd_enc_yx", string_type), ("crd_enc_z", option_type(string_type)), ("crd_enc_s", string_type), ("crd_enc_f", string_type), ("pp_loc_ref_l", option_type(array_type(PpLocRef_reflection())))])


class RawPoly(Record):
    def __init__(self, delta: bool, dim: int, type: Optional[str], crd_enc_yx: str, crd_enc_z: Optional[str], crd_enc_s: str, crd_enc_f: str, pp_loc_ref_l: Optional[List[PpLocRef]]) -> None:
        super().__init__()
        self.delta = delta
        self.dim = dim or 0
        self.type = type
        self.crd_enc_yx = crd_enc_yx
        self.crd_enc_z = crd_enc_z
        self.crd_enc_s = crd_enc_s
        self.crd_enc_f = crd_enc_f
        self.pp_loc_ref_l = pp_loc_ref_l
    

RawPoly_reflection = expr_171

def expr_172() -> TypeInfo:
    return record_type("FsHafas.Raw.PolyG", [], PolyG, lambda: [("poly_xl", array_type(int32_type))])


class PolyG(Record):
    def __init__(self, poly_xl: MutableSequence[int]=None) -> None:
        super().__init__()
        self.poly_xl = poly_xl
    

PolyG_reflection = expr_172

def expr_173() -> TypeInfo:
    return record_type("FsHafas.Raw.RawAni", [], RawAni, lambda: [("m_sec", array_type(int32_type)), ("proc", array_type(int32_type)), ("proc_abs", option_type(array_type(int32_type))), ("f_loc_x", array_type(int32_type)), ("t_loc_x", array_type(int32_type)), ("dir_geo", array_type(int32_type)), ("stc_output_x", array_type(int32_type)), ("poly_g", option_type(PolyG_reflection())), ("state", array_type(string_type)), ("poly", option_type(RawPoly_reflection()))])


class RawAni(Record):
    def __init__(self, m_sec: MutableSequence[int], proc: MutableSequence[int], proc_abs: Optional[MutableSequence[int]], f_loc_x: MutableSequence[int], t_loc_x: MutableSequence[int], dir_geo: MutableSequence[int], stc_output_x: MutableSequence[int], poly_g: Optional[PolyG], state: List[str], poly: Optional[RawPoly]) -> None:
        super().__init__()
        self.m_sec = m_sec
        self.proc = proc
        self.proc_abs = proc_abs
        self.f_loc_x = f_loc_x
        self.t_loc_x = t_loc_x
        self.dir_geo = dir_geo
        self.stc_output_x = stc_output_x
        self.poly_g = poly_g
        self.state = state
        self.poly = poly
    

RawAni_reflection = expr_173

def expr_174() -> TypeInfo:
    return record_type("FsHafas.Raw.RawSDays", [], RawSDays, lambda: [("f_loc_x", option_type(int32_type)), ("t_loc_x", option_type(int32_type)), ("s_days_r", option_type(string_type)), ("s_days_i", option_type(string_type)), ("s_days_b", option_type(string_type))])


class RawSDays(Record):
    def __init__(self, f_loc_x: Optional[int], t_loc_x: Optional[int], s_days_r: Optional[str], s_days_i: Optional[str], s_days_b: Optional[str]) -> None:
        super().__init__()
        self.f_loc_x = f_loc_x
        self.t_loc_x = t_loc_x
        self.s_days_r = s_days_r
        self.s_days_i = s_days_i
        self.s_days_b = s_days_b
    

RawSDays_reflection = expr_174

def expr_175() -> TypeInfo:
    return record_type("FsHafas.Raw.RawPolyG", [], RawPolyG, lambda: [("poly_xl", array_type(int32_type))])


class RawPolyG(Record):
    def __init__(self, poly_xl: MutableSequence[int]=None) -> None:
        super().__init__()
        self.poly_xl = poly_xl
    

RawPolyG_reflection = expr_175

def expr_176() -> TypeInfo:
    return record_type("FsHafas.Raw.RawCrd", [], RawCrd, lambda: [("x", int32_type), ("y", int32_type), ("z", option_type(int32_type))])


class RawCrd(Record):
    def __init__(self, x: int, y: int, z: Optional[int]) -> None:
        super().__init__()
        self.x = x or 0
        self.y = y or 0
        self.z = z
    

RawCrd_reflection = expr_176

def expr_177() -> TypeInfo:
    return record_type("FsHafas.Raw.RawFreq", [], RawFreq, lambda: [("jny_l", option_type(array_type(RawJny_reflection()))), ("min_c", option_type(int32_type)), ("max_c", option_type(int32_type)), ("num_c", option_type(int32_type))])


class RawFreq(Record):
    def __init__(self, jny_l: Optional[List[RawJny]], min_c: Optional[int], max_c: Optional[int], num_c: Optional[int]) -> None:
        super().__init__()
        self.jny_l = jny_l
        self.min_c = min_c
        self.max_c = max_c
        self.num_c = num_c
    

RawFreq_reflection = expr_177

def expr_178() -> TypeInfo:
    return record_type("FsHafas.Raw.RawJny", [], RawJny, lambda: [("jid", string_type), ("prod_x", int32_type), ("dir_txt", option_type(string_type)), ("status", option_type(string_type)), ("is_rchbl", option_type(bool_type)), ("ctx_recon", option_type(string_type)), ("rem_l", option_type(array_type(RawRem_reflection()))), ("msg_l", option_type(array_type(RawMsg_reflection()))), ("stb_stop", option_type(RawStop_reflection())), ("subscr", option_type(string_type)), ("poly", option_type(RawPoly_reflection())), ("stop_l", option_type(array_type(RawStop_reflection()))), ("date", option_type(string_type)), ("s_days_l", option_type(array_type(RawSDays_reflection()))), ("d_trn_cmp_sx", option_type(RawTrnCmpSX_reflection())), ("poly_g", option_type(RawPolyG_reflection())), ("ani", option_type(RawAni_reflection())), ("pos", option_type(RawCrd_reflection())), ("freq", option_type(RawFreq_reflection())), ("prod_l", option_type(array_type(RawProd_reflection())))])


class RawJny(Record):
    def __init__(self, jid: str, prod_x: int, dir_txt: Optional[str], status: Optional[str], is_rchbl: Optional[bool], ctx_recon: Optional[str], rem_l: Optional[List[RawRem]], msg_l: Optional[List[RawMsg]], stb_stop: Optional[RawStop], subscr: Optional[str], poly: Optional[RawPoly], stop_l: Optional[List[RawStop]], date: Optional[str], s_days_l: Optional[List[RawSDays]], d_trn_cmp_sx: Optional[RawTrnCmpSX], poly_g: Optional[RawPolyG], ani: Optional[RawAni], pos: Optional[RawCrd], freq: Optional[RawFreq], prod_l: Optional[List[RawProd]]) -> None:
        super().__init__()
        self.jid = jid
        self.prod_x = prod_x or 0
        self.dir_txt = dir_txt
        self.status = status
        self.is_rchbl = is_rchbl
        self.ctx_recon = ctx_recon
        self.rem_l = rem_l
        self.msg_l = msg_l
        self.stb_stop = stb_stop
        self.subscr = subscr
        self.poly = poly
        self.stop_l = stop_l
        self.date = date
        self.s_days_l = s_days_l
        self.d_trn_cmp_sx = d_trn_cmp_sx
        self.poly_g = poly_g
        self.ani = ani
        self.pos = pos
        self.freq = freq
        self.prod_l = prod_l
    

RawJny_reflection = expr_178

def expr_179() -> TypeInfo:
    return record_type("FsHafas.Raw.RawGis", [], RawGis, lambda: [("dist", option_type(int32_type)), ("dur_s", option_type(string_type)), ("dir_geo", option_type(int32_type)), ("ctx", option_type(string_type)), ("gis_prvr", option_type(string_type)), ("get_descr", option_type(bool_type)), ("get_poly", option_type(bool_type)), ("msg_l", option_type(array_type(RawMsg_reflection())))])


class RawGis(Record):
    def __init__(self, dist: Optional[int], dur_s: Optional[str], dir_geo: Optional[int], ctx: Optional[str], gis_prvr: Optional[str], get_descr: Optional[bool], get_poly: Optional[bool], msg_l: Optional[List[RawMsg]]) -> None:
        super().__init__()
        self.dist = dist
        self.dur_s = dur_s
        self.dir_geo = dir_geo
        self.ctx = ctx
        self.gis_prvr = gis_prvr
        self.get_descr = get_descr
        self.get_poly = get_poly
        self.msg_l = msg_l
    

RawGis_reflection = expr_179

def expr_180() -> TypeInfo:
    return record_type("FsHafas.Raw.RawSec", [], RawSec, lambda: [("type", string_type), ("ico_x", option_type(int32_type)), ("dep", RawDep_reflection()), ("arr", RawArr_reflection()), ("jny", option_type(RawJny_reflection())), ("res_state", option_type(string_type)), ("res_recommendation", option_type(string_type)), ("gis", option_type(RawGis_reflection()))])


class RawSec(Record):
    def __init__(self, type: str, ico_x: Optional[int], dep: RawDep, arr: RawArr, jny: Optional[RawJny], res_state: Optional[str], res_recommendation: Optional[str], gis: Optional[RawGis]) -> None:
        super().__init__()
        self.type = type
        self.ico_x = ico_x
        self.dep = dep
        self.arr = arr
        self.jny = jny
        self.res_state = res_state
        self.res_recommendation = res_recommendation
        self.gis = gis
    

RawSec_reflection = expr_180

def expr_181() -> TypeInfo:
    return record_type("FsHafas.Raw.RawSotCtxt", [], RawSotCtxt, lambda: [("cn_loc_x", option_type(int32_type)), ("calc_date", string_type), ("jid", option_type(string_type)), ("loc_mode", string_type), ("p_loc_x", option_type(int32_type)), ("req_mode", string_type), ("sect_x", option_type(int32_type)), ("calc_time", string_type)])


class RawSotCtxt(Record):
    def __init__(self, cn_loc_x: Optional[int], calc_date: str, jid: Optional[str], loc_mode: str, p_loc_x: Optional[int], req_mode: str, sect_x: Optional[int], calc_time: str) -> None:
        super().__init__()
        self.cn_loc_x = cn_loc_x
        self.calc_date = calc_date
        self.jid = jid
        self.loc_mode = loc_mode
        self.p_loc_x = p_loc_x
        self.req_mode = req_mode
        self.sect_x = sect_x
        self.calc_time = calc_time
    

RawSotCtxt_reflection = expr_181

def expr_182() -> TypeInfo:
    return record_type("FsHafas.Raw.Content", [], Content, lambda: [("type", string_type), ("content", string_type)])


class Content(Record):
    def __init__(self, type: str, content: str) -> None:
        super().__init__()
        self.type = type
        self.content = content
    

Content_reflection = expr_182

def expr_183() -> TypeInfo:
    return record_type("FsHafas.Raw.ExtCont", [], ExtCont, lambda: [("content", Content_reflection())])


class ExtCont(Record):
    def __init__(self, content: Content=None) -> None:
        super().__init__()
        self.content = content
    

ExtCont_reflection = expr_183

def expr_184() -> TypeInfo:
    return record_type("FsHafas.Raw.RawTicket", [], RawTicket, lambda: [("name", string_type), ("prc", int32_type), ("cur", string_type), ("ext_cont", ExtCont_reflection())])


class RawTicket(Record):
    def __init__(self, name: str, prc: int, cur: str, ext_cont: ExtCont) -> None:
        super().__init__()
        self.name = name
        self.prc = prc or 0
        self.cur = cur
        self.ext_cont = ext_cont
    

RawTicket_reflection = expr_184

def expr_185() -> TypeInfo:
    return record_type("FsHafas.Raw.RawPrice", [], RawPrice, lambda: [("amount", option_type(int32_type))])


class RawPrice(Record):
    def __init__(self, amount: Optional[int]=None) -> None:
        super().__init__()
        self.amount = amount
    

RawPrice_reflection = expr_185

def expr_186() -> TypeInfo:
    return record_type("FsHafas.Raw.RawFare", [], RawFare, lambda: [("price", option_type(RawPrice_reflection())), ("is_from_price", option_type(bool_type)), ("is_bookable", option_type(bool_type)), ("is_upsell", option_type(bool_type)), ("target_ctx", option_type(string_type)), ("button_text", option_type(string_type)), ("name", option_type(string_type)), ("ticket_l", option_type(array_type(RawTicket_reflection())))])


class RawFare(Record):
    def __init__(self, price: Optional[RawPrice], is_from_price: Optional[bool], is_bookable: Optional[bool], is_upsell: Optional[bool], target_ctx: Optional[str], button_text: Optional[str], name: Optional[str], ticket_l: Optional[List[RawTicket]]) -> None:
        super().__init__()
        self.price = price
        self.is_from_price = is_from_price
        self.is_bookable = is_bookable
        self.is_upsell = is_upsell
        self.target_ctx = target_ctx
        self.button_text = button_text
        self.name = name
        self.ticket_l = ticket_l
    

RawFare_reflection = expr_186

def expr_187() -> TypeInfo:
    return record_type("FsHafas.Raw.RawFareSet", [], RawFareSet, lambda: [("desc", option_type(string_type)), ("fare_l", array_type(RawFare_reflection()))])


class RawFareSet(Record):
    def __init__(self, desc: Optional[str], fare_l: List[RawFare]) -> None:
        super().__init__()
        self.desc = desc
        self.fare_l = fare_l
    

RawFareSet_reflection = expr_187

def expr_188() -> TypeInfo:
    return record_type("FsHafas.Raw.RawTrfRes", [], RawTrfRes, lambda: [("status_code", option_type(string_type)), ("fare_set_l", array_type(RawFareSet_reflection()))])


class RawTrfRes(Record):
    def __init__(self, status_code: Optional[str], fare_set_l: List[RawFareSet]) -> None:
        super().__init__()
        self.status_code = status_code
        self.fare_set_l = fare_set_l
    

RawTrfRes_reflection = expr_188

def expr_189() -> TypeInfo:
    return record_type("FsHafas.Raw.RawOutCon", [], RawOutCon, lambda: [("cid", string_type), ("date", string_type), ("dur", string_type), ("chg", int32_type), ("s_days", RawSDays_reflection()), ("dep", RawDep_reflection()), ("arr", RawArr_reflection()), ("sec_l", array_type(RawSec_reflection())), ("ctx_recon", option_type(string_type)), ("trf_res", option_type(RawTrfRes_reflection())), ("con_subscr", string_type), ("res_state", option_type(string_type)), ("res_recommendation", option_type(string_type)), ("rec_state", string_type), ("sot_rating", option_type(int32_type)), ("is_sot_con", option_type(bool_type)), ("show_arslink", option_type(bool_type)), ("sot_ctxt", option_type(RawSotCtxt_reflection())), ("cksum", string_type), ("msg_l", option_type(array_type(RawMsg_reflection()))), ("freq", option_type(RawFreq_reflection()))])


class RawOutCon(Record):
    def __init__(self, cid: str, date: str, dur: str, chg: int, s_days: RawSDays, dep: RawDep, arr: RawArr, sec_l: List[RawSec], ctx_recon: Optional[str], trf_res: Optional[RawTrfRes], con_subscr: str, res_state: Optional[str], res_recommendation: Optional[str], rec_state: str, sot_rating: Optional[int], is_sot_con: Optional[bool], show_arslink: Optional[bool], sot_ctxt: Optional[RawSotCtxt], cksum: str, msg_l: Optional[List[RawMsg]], freq: Optional[RawFreq]) -> None:
        super().__init__()
        self.cid = cid
        self.date = date
        self.dur = dur
        self.chg = chg or 0
        self.s_days = s_days
        self.dep = dep
        self.arr = arr
        self.sec_l = sec_l
        self.ctx_recon = ctx_recon
        self.trf_res = trf_res
        self.con_subscr = con_subscr
        self.res_state = res_state
        self.res_recommendation = res_recommendation
        self.rec_state = rec_state
        self.sot_rating = sot_rating
        self.is_sot_con = is_sot_con
        self.show_arslink = show_arslink
        self.sot_ctxt = sot_ctxt
        self.cksum = cksum
        self.msg_l = msg_l
        self.freq = freq
    

RawOutCon_reflection = expr_189

def expr_190() -> TypeInfo:
    return record_type("FsHafas.Raw.RawItem", [], RawItem, lambda: [("col", int32_type), ("row", int32_type), ("msg_l", option_type(array_type(RawMsg_reflection()))), ("rem_l", option_type(array_type(int32_type)))])


class RawItem(Record):
    def __init__(self, col: int, row: int, msg_l: Optional[List[RawMsg]], rem_l: Optional[MutableSequence[int]]) -> None:
        super().__init__()
        self.col = col or 0
        self.row = row or 0
        self.msg_l = msg_l
        self.rem_l = rem_l
    

RawItem_reflection = expr_190

def expr_191() -> TypeInfo:
    return record_type("FsHafas.Raw.RawGrid", [], RawGrid, lambda: [("n_cols", int32_type), ("n_rows", int32_type), ("item_l", array_type(RawItem_reflection())), ("type", string_type), ("title", string_type)])


class RawGrid(Record):
    def __init__(self, n_cols: int, n_rows: int, item_l: List[RawItem], type: str, title: str) -> None:
        super().__init__()
        self.n_cols = n_cols or 0
        self.n_rows = n_rows or 0
        self.item_l = item_l
        self.type = type
        self.title = title
    

RawGrid_reflection = expr_191

def expr_192() -> TypeInfo:
    return record_type("FsHafas.Raw.RawLoc", [], RawLoc, lambda: [("lid", option_type(string_type)), ("type", option_type(string_type)), ("name", string_type), ("ico_x", option_type(int32_type)), ("ext_id", option_type(string_type)), ("state", string_type), ("crd", option_type(RawCrd_reflection())), ("p_cls", option_type(int32_type)), ("entry", option_type(bool_type)), ("m_mast_loc_x", option_type(int32_type)), ("p_ref_l", option_type(array_type(int32_type))), ("wt", option_type(int32_type)), ("entry_loc_l", option_type(array_type(int32_type))), ("stop_loc_l", option_type(array_type(int32_type))), ("msg_l", option_type(array_type(RawMsg_reflection()))), ("grid_l", option_type(array_type(RawGrid_reflection()))), ("is_main_mast", option_type(bool_type)), ("meta", option_type(bool_type)), ("dist", option_type(int32_type)), ("dur", option_type(int32_type))])


class RawLoc(Record):
    def __init__(self, lid: Optional[str], type: Optional[str], name: str, ico_x: Optional[int], ext_id: Optional[str], state: str, crd: Optional[RawCrd], p_cls: Optional[int], entry: Optional[bool], m_mast_loc_x: Optional[int], p_ref_l: Optional[MutableSequence[int]], wt: Optional[int], entry_loc_l: Optional[MutableSequence[int]], stop_loc_l: Optional[MutableSequence[int]], msg_l: Optional[List[RawMsg]], grid_l: Optional[List[RawGrid]], is_main_mast: Optional[bool], meta: Optional[bool], dist: Optional[int], dur: Optional[int]) -> None:
        super().__init__()
        self.lid = lid
        self.type = type
        self.name = name
        self.ico_x = ico_x
        self.ext_id = ext_id
        self.state = state
        self.crd = crd
        self.p_cls = p_cls
        self.entry = entry
        self.m_mast_loc_x = m_mast_loc_x
        self.p_ref_l = p_ref_l
        self.wt = wt
        self.entry_loc_l = entry_loc_l
        self.stop_loc_l = stop_loc_l
        self.msg_l = msg_l
        self.grid_l = grid_l
        self.is_main_mast = is_main_mast
        self.meta = meta
        self.dist = dist
        self.dur = dur
    

RawLoc_reflection = expr_192

def expr_193() -> TypeInfo:
    return record_type("FsHafas.Raw.RawProdCtx", [], RawProdCtx, lambda: [("name", option_type(string_type)), ("num", option_type(string_type)), ("match_id", option_type(string_type)), ("cat_out", option_type(string_type)), ("cat_out_s", option_type(string_type)), ("cat_out_l", option_type(string_type)), ("cat_in", option_type(string_type)), ("cat_code", option_type(string_type)), ("admin", option_type(string_type)), ("line_id", option_type(string_type))])


class RawProdCtx(Record):
    def __init__(self, name: Optional[str], num: Optional[str], match_id: Optional[str], cat_out: Optional[str], cat_out_s: Optional[str], cat_out_l: Optional[str], cat_in: Optional[str], cat_code: Optional[str], admin: Optional[str], line_id: Optional[str]) -> None:
        super().__init__()
        self.name = name
        self.num = num
        self.match_id = match_id
        self.cat_out = cat_out
        self.cat_out_s = cat_out_s
        self.cat_out_l = cat_out_l
        self.cat_in = cat_in
        self.cat_code = cat_code
        self.admin = admin
        self.line_id = line_id
    

RawProdCtx_reflection = expr_193

def expr_194() -> TypeInfo:
    return record_type("FsHafas.Raw.RawOp", [], RawOp, lambda: [("name", string_type), ("ico_x", int32_type)])


class RawOp(Record):
    def __init__(self, name: str, ico_x: int) -> None:
        super().__init__()
        self.name = name
        self.ico_x = ico_x or 0
    

RawOp_reflection = expr_194

def expr_195() -> TypeInfo:
    return record_type("FsHafas.Raw.RawProd", [], RawProd, lambda: [("name", option_type(string_type)), ("number", option_type(string_type)), ("ico_x", option_type(int32_type)), ("opr_x", option_type(int32_type)), ("prod_ctx", option_type(RawProdCtx_reflection())), ("cls", option_type(int32_type)), ("line", option_type(string_type)), ("add_name", option_type(string_type)), ("f_loc_x", option_type(int32_type)), ("t_loc_x", option_type(int32_type)), ("prod_x", option_type(int32_type)), ("f_idx", option_type(int32_type)), ("t_idx", option_type(int32_type))])


class RawProd(Record):
    def __init__(self, name: Optional[str], number: Optional[str], ico_x: Optional[int], opr_x: Optional[int], prod_ctx: Optional[RawProdCtx], cls: Optional[int], line: Optional[str], add_name: Optional[str], f_loc_x: Optional[int], t_loc_x: Optional[int], prod_x: Optional[int], f_idx: Optional[int], t_idx: Optional[int]) -> None:
        super().__init__()
        self.name = name
        self.number = number
        self.ico_x = ico_x
        self.opr_x = opr_x
        self.prod_ctx = prod_ctx
        self.cls = cls
        self.line = line
        self.add_name = add_name
        self.f_loc_x = f_loc_x
        self.t_loc_x = t_loc_x
        self.prod_x = prod_x
        self.f_idx = f_idx
        self.t_idx = t_idx
    

RawProd_reflection = expr_195

def expr_196() -> TypeInfo:
    return record_type("FsHafas.Raw.RawRGB", [], RawRGB, lambda: [("r", option_type(int32_type)), ("g", int32_type), ("b", int32_type)])


class RawRGB(Record):
    def __init__(self, r: Optional[int], g: int, b: int) -> None:
        super().__init__()
        self.r = r
        self.g = g or 0
        self.b = b or 0
    

RawRGB_reflection = expr_196

def expr_197() -> TypeInfo:
    return record_type("FsHafas.Raw.RawIco", [], RawIco, lambda: [("res", option_type(string_type)), ("txt", option_type(string_type)), ("text", option_type(string_type)), ("txt_s", option_type(string_type)), ("fg", option_type(RawRGB_reflection())), ("bg", option_type(RawRGB_reflection()))])


class RawIco(Record):
    def __init__(self, res: Optional[str], txt: Optional[str], text: Optional[str], txt_s: Optional[str], fg: Optional[RawRGB], bg: Optional[RawRGB]) -> None:
        super().__init__()
        self.res = res
        self.txt = txt
        self.text = text
        self.txt_s = txt_s
        self.fg = fg
        self.bg = bg
    

RawIco_reflection = expr_197

def expr_198() -> TypeInfo:
    return record_type("FsHafas.Raw.RawDir", [], RawDir, lambda: [("txt", string_type), ("flg", option_type(string_type))])


class RawDir(Record):
    def __init__(self, txt: str, flg: Optional[str]) -> None:
        super().__init__()
        self.txt = txt
        self.flg = flg
    

RawDir_reflection = expr_198

def expr_199() -> TypeInfo:
    return record_type("FsHafas.Raw.RawTcoc", [], RawTcoc, lambda: [("c", string_type), ("r", option_type(int32_type))])


class RawTcoc(Record):
    def __init__(self, c: str, r: Optional[int]) -> None:
        super().__init__()
        self.c = c
        self.r = r
    

RawTcoc_reflection = expr_199

def expr_200() -> TypeInfo:
    return record_type("FsHafas.Raw.RawHimMsgCat", [], RawHimMsgCat, lambda: [("id", int32_type)])


class RawHimMsgCat(Record):
    def __init__(self, id: int=None) -> None:
        super().__init__()
        self.id = id or 0
    

RawHimMsgCat_reflection = expr_200

def expr_201() -> TypeInfo:
    return record_type("FsHafas.Raw.IcoCrd", [], IcoCrd, lambda: [("x", int32_type), ("y", int32_type), ("type", option_type(string_type))])


class IcoCrd(Record):
    def __init__(self, x: int, y: int, type: Optional[str]) -> None:
        super().__init__()
        self.x = x or 0
        self.y = y or 0
        self.type = type
    

IcoCrd_reflection = expr_201

def expr_202() -> TypeInfo:
    return record_type("FsHafas.Raw.RawHimMsgEdge", [], RawHimMsgEdge, lambda: [("f_loc_x", option_type(int32_type)), ("t_loc_x", option_type(int32_type)), ("dir", option_type(int32_type)), ("ico_crd", IcoCrd_reflection()), ("msg_ref_l", option_type(array_type(int32_type))), ("ico_x", option_type(int32_type))])


class RawHimMsgEdge(Record):
    def __init__(self, f_loc_x: Optional[int], t_loc_x: Optional[int], dir: Optional[int], ico_crd: IcoCrd, msg_ref_l: Optional[MutableSequence[int]], ico_x: Optional[int]) -> None:
        super().__init__()
        self.f_loc_x = f_loc_x
        self.t_loc_x = t_loc_x
        self.dir = dir
        self.ico_crd = ico_crd
        self.msg_ref_l = msg_ref_l
        self.ico_x = ico_x
    

RawHimMsgEdge_reflection = expr_202

def expr_203() -> TypeInfo:
    return record_type("FsHafas.Raw.RawHimMsgEvent", [], RawHimMsgEvent, lambda: [("f_loc_x", option_type(int32_type)), ("t_loc_x", option_type(int32_type)), ("f_date", string_type), ("f_time", string_type), ("t_date", string_type), ("t_time", string_type)])


class RawHimMsgEvent(Record):
    def __init__(self, f_loc_x: Optional[int], t_loc_x: Optional[int], f_date: str, f_time: str, t_date: str, t_time: str) -> None:
        super().__init__()
        self.f_loc_x = f_loc_x
        self.t_loc_x = t_loc_x
        self.f_date = f_date
        self.f_time = f_time
        self.t_date = t_date
        self.t_time = t_time
    

RawHimMsgEvent_reflection = expr_203

def expr_204() -> TypeInfo:
    return record_type("FsHafas.Raw.RawCommon", [], RawCommon, lambda: [("loc_l", option_type(array_type(RawLoc_reflection()))), ("prod_l", option_type(array_type(RawProd_reflection()))), ("rem_l", option_type(array_type(RawRem_reflection()))), ("ico_l", option_type(array_type(RawIco_reflection()))), ("op_l", option_type(array_type(RawOp_reflection()))), ("max_c", option_type(int32_type)), ("num_c", option_type(int32_type)), ("him_l", option_type(array_type(RawHim_reflection()))), ("poly_l", option_type(array_type(RawPoly_reflection()))), ("dir_l", option_type(array_type(RawDir_reflection()))), ("tcoc_l", option_type(array_type(RawTcoc_reflection()))), ("him_msg_cat_l", option_type(array_type(RawHimMsgCat_reflection()))), ("him_msg_edge_l", option_type(array_type(RawHimMsgEdge_reflection()))), ("him_msg_event_l", option_type(array_type(RawHimMsgEvent_reflection())))])


class RawCommon(Record):
    def __init__(self, loc_l: Optional[List[RawLoc]], prod_l: Optional[List[RawProd]], rem_l: Optional[List[RawRem]], ico_l: Optional[List[RawIco]], op_l: Optional[List[RawOp]], max_c: Optional[int], num_c: Optional[int], him_l: Optional[List[RawHim]], poly_l: Optional[List[RawPoly]], dir_l: Optional[List[RawDir]], tcoc_l: Optional[List[RawTcoc]], him_msg_cat_l: Optional[List[RawHimMsgCat]], him_msg_edge_l: Optional[List[RawHimMsgEdge]], him_msg_event_l: Optional[List[RawHimMsgEvent]]) -> None:
        super().__init__()
        self.loc_l = loc_l
        self.prod_l = prod_l
        self.rem_l = rem_l
        self.ico_l = ico_l
        self.op_l = op_l
        self.max_c = max_c
        self.num_c = num_c
        self.him_l = him_l
        self.poly_l = poly_l
        self.dir_l = dir_l
        self.tcoc_l = tcoc_l
        self.him_msg_cat_l = him_msg_cat_l
        self.him_msg_edge_l = him_msg_edge_l
        self.him_msg_event_l = him_msg_event_l
    

RawCommon_reflection = expr_204

def expr_205() -> TypeInfo:
    return record_type("FsHafas.Raw.RawMatch", [], RawMatch, lambda: [("field", option_type(string_type)), ("state", option_type(string_type)), ("loc_l", option_type(array_type(RawLoc_reflection())))])


class RawMatch(Record):
    def __init__(self, field: Optional[str], state: Optional[str], loc_l: Optional[List[RawLoc]]) -> None:
        super().__init__()
        self.field = field
        self.state = state
        self.loc_l = loc_l
    

RawMatch_reflection = expr_205

def expr_206() -> TypeInfo:
    return record_type("FsHafas.Raw.RawPos", [], RawPos, lambda: [("loc_x", int32_type), ("dur", int32_type)])


class RawPos(Record):
    def __init__(self, loc_x: int, dur: int) -> None:
        super().__init__()
        self.loc_x = loc_x or 0
        self.dur = dur or 0
    

RawPos_reflection = expr_206

def expr_207() -> TypeInfo:
    return record_type("FsHafas.Raw.RawLine", [], RawLine, lambda: [("line_id", option_type(string_type)), ("prod_x", int32_type), ("dir_ref_l", option_type(array_type(int32_type))), ("jny_l", option_type(array_type(RawJny_reflection())))])


class RawLine(Record):
    def __init__(self, line_id: Optional[str], prod_x: int, dir_ref_l: Optional[MutableSequence[int]], jny_l: Optional[List[RawJny]]) -> None:
        super().__init__()
        self.line_id = line_id
        self.prod_x = prod_x or 0
        self.dir_ref_l = dir_ref_l
        self.jny_l = jny_l
    

RawLine_reflection = expr_207

def expr_208() -> TypeInfo:
    return record_type("FsHafas.Raw.RawResult", [], RawResult, lambda: [("common", option_type(RawCommon_reflection())), ("msg_l", option_type(array_type(RawHim_reflection()))), ("type", option_type(string_type)), ("jny_l", option_type(array_type(RawJny_reflection()))), ("out_con_l", option_type(array_type(RawOutCon_reflection()))), ("out_ctx_scr_b", option_type(string_type)), ("out_ctx_scr_f", option_type(string_type)), ("planrt_ts", option_type(string_type)), ("match", option_type(RawMatch_reflection())), ("loc_l", option_type(array_type(RawLoc_reflection()))), ("journey", option_type(RawJny_reflection())), ("hci_version", option_type(string_type)), ("fp_e", option_type(string_type)), ("s_d", option_type(string_type)), ("s_t", option_type(string_type)), ("fp_b", option_type(string_type)), ("pos_l", option_type(array_type(RawPos_reflection()))), ("line_l", option_type(array_type(RawLine_reflection())))])


class RawResult(Record):
    def __init__(self, common: Optional[RawCommon], msg_l: Optional[List[RawHim]], type: Optional[str], jny_l: Optional[List[RawJny]], out_con_l: Optional[List[RawOutCon]], out_ctx_scr_b: Optional[str], out_ctx_scr_f: Optional[str], planrt_ts: Optional[str], match: Optional[RawMatch], loc_l: Optional[List[RawLoc]], journey: Optional[RawJny], hci_version: Optional[str], fp_e: Optional[str], s_d: Optional[str], s_t: Optional[str], fp_b: Optional[str], pos_l: Optional[List[RawPos]], line_l: Optional[List[RawLine]]) -> None:
        super().__init__()
        self.common = common
        self.msg_l = msg_l
        self.type = type
        self.jny_l = jny_l
        self.out_con_l = out_con_l
        self.out_ctx_scr_b = out_ctx_scr_b
        self.out_ctx_scr_f = out_ctx_scr_f
        self.planrt_ts = planrt_ts
        self.match = match
        self.loc_l = loc_l
        self.journey = journey
        self.hci_version = hci_version
        self.fp_e = fp_e
        self.s_d = s_d
        self.s_t = s_t
        self.fp_b = fp_b
        self.pos_l = pos_l
        self.line_l = line_l
    

RawResult_reflection = expr_208

def expr_209() -> TypeInfo:
    return record_type("FsHafas.Raw.SvcRes", [], SvcRes, lambda: [("meth", string_type), ("err", option_type(string_type)), ("err_txt", option_type(string_type)), ("res", option_type(RawResult_reflection()))])


class SvcRes(Record):
    def __init__(self, meth: str, err: Optional[str], err_txt: Optional[str], res: Optional[RawResult]) -> None:
        super().__init__()
        self.meth = meth
        self.err = err
        self.err_txt = err_txt
        self.res = res
    

SvcRes_reflection = expr_209

def expr_210() -> TypeInfo:
    return record_type("FsHafas.Raw.RawResponse", [], RawResponse, lambda: [("ver", string_type), ("lang", string_type), ("id", option_type(string_type)), ("err", option_type(string_type)), ("err_txt", option_type(string_type)), ("svc_res_l", option_type(array_type(SvcRes_reflection())))])


class RawResponse(Record):
    def __init__(self, ver: str, lang: str, id: Optional[str], err: Optional[str], err_txt: Optional[str], svc_res_l: Optional[List[SvcRes]]) -> None:
        super().__init__()
        self.ver = ver
        self.lang = lang
        self.id = id
        self.err = err
        self.err_txt = err_txt
        self.svc_res_l = svc_res_l
    

RawResponse_reflection = expr_210

def expr_211() -> TypeInfo:
    return record_type("FsHafas.Raw.Cfg", [], Cfg, lambda: [("poly_enc", string_type), ("rt_mode", option_type(string_type))])


class Cfg(Record):
    def __init__(self, poly_enc: str, rt_mode: Optional[str]) -> None:
        super().__init__()
        self.poly_enc = poly_enc
        self.rt_mode = rt_mode
    

Cfg_reflection = expr_211

def expr_212() -> TypeInfo:
    return record_type("FsHafas.Raw.Loc", [], Loc, lambda: [("type", string_type), ("name", option_type(string_type)), ("lid", option_type(string_type))])


class Loc(Record):
    def __init__(self, type: str, name: Optional[str], lid: Optional[str]) -> None:
        super().__init__()
        self.type = type
        self.name = name
        self.lid = lid
    

Loc_reflection = expr_212

def expr_213() -> TypeInfo:
    return record_type("FsHafas.Raw.LocViaInput", [], LocViaInput, lambda: [("loc", Loc_reflection())])


class LocViaInput(Record):
    def __init__(self, loc: Loc=None) -> None:
        super().__init__()
        self.loc = loc
    

LocViaInput_reflection = expr_213

def expr_214() -> TypeInfo:
    return record_type("FsHafas.Raw.LocMatchInput", [], LocMatchInput, lambda: [("loc", Loc_reflection()), ("max_loc", int32_type), ("field", string_type)])


class LocMatchInput(Record):
    def __init__(self, loc: Loc, max_loc: int, field: str) -> None:
        super().__init__()
        self.loc = loc
        self.max_loc = max_loc or 0
        self.field = field
    

LocMatchInput_reflection = expr_214

def expr_215() -> TypeInfo:
    return record_type("FsHafas.Raw.LocMatchRequest", [], LocMatchRequest, lambda: [("input", LocMatchInput_reflection())])


class LocMatchRequest(Record):
    def __init__(self, input: LocMatchInput=None) -> None:
        super().__init__()
        self.input = input
    

LocMatchRequest_reflection = expr_215

def expr_216() -> TypeInfo:
    return record_type("FsHafas.Raw.LineMatchRequest", [], LineMatchRequest, lambda: [("input", string_type)])


class LineMatchRequest(Record):
    def __init__(self, input: str=None) -> None:
        super().__init__()
        self.input = input
    

LineMatchRequest_reflection = expr_216

def expr_217() -> TypeInfo:
    return record_type("FsHafas.Raw.JourneyDetailsRequest", [], JourneyDetailsRequest, lambda: [("jid", string_type), ("name", string_type), ("get_polyline", bool_type)])


class JourneyDetailsRequest(Record):
    def __init__(self, jid: str, name: str, get_polyline: bool) -> None:
        super().__init__()
        self.jid = jid
        self.name = name
        self.get_polyline = get_polyline
    

JourneyDetailsRequest_reflection = expr_217

def expr_218() -> TypeInfo:
    return record_type("FsHafas.Raw.JnyFltr", [], JnyFltr, lambda: [("type", string_type), ("mode", string_type), ("value", option_type(string_type)), ("meta", option_type(string_type))])


class JnyFltr(Record):
    def __init__(self, type: str, mode: str, value: Optional[str], meta: Optional[str]) -> None:
        super().__init__()
        self.type = type
        self.mode = mode
        self.value = value
        self.meta = meta
    

JnyFltr_reflection = expr_218

def expr_219() -> TypeInfo:
    return record_type("FsHafas.Raw.TvlrProf", [], TvlrProf, lambda: [("type", string_type), ("redtn_card", option_type(int32_type))])


class TvlrProf(Record):
    def __init__(self, type: str, redtn_card: Optional[int]) -> None:
        super().__init__()
        self.type = type
        self.redtn_card = redtn_card
    

TvlrProf_reflection = expr_219

def expr_220() -> TypeInfo:
    return record_type("FsHafas.Raw.TrfReq", [], TrfReq, lambda: [("jny_cl", int32_type), ("tvlr_prof", array_type(TvlrProf_reflection())), ("c_type", string_type)])


class TrfReq(Record):
    def __init__(self, jny_cl: int, tvlr_prof: List[TvlrProf], c_type: str) -> None:
        super().__init__()
        self.jny_cl = jny_cl or 0
        self.tvlr_prof = tvlr_prof
        self.c_type = c_type
    

TrfReq_reflection = expr_220

def expr_221() -> TypeInfo:
    return record_type("FsHafas.Raw.StationBoardRequest", [], StationBoardRequest, lambda: [("type", string_type), ("date", string_type), ("time", string_type), ("stb_loc", Loc_reflection()), ("jny_fltr_l", array_type(JnyFltr_reflection())), ("dur", int32_type)])


class StationBoardRequest(Record):
    def __init__(self, type: str, date: str, time: str, stb_loc: Loc, jny_fltr_l: List[JnyFltr], dur: int) -> None:
        super().__init__()
        self.type = type
        self.date = date
        self.time = time
        self.stb_loc = stb_loc
        self.jny_fltr_l = jny_fltr_l
        self.dur = dur or 0
    

StationBoardRequest_reflection = expr_221

def expr_222() -> TypeInfo:
    return record_type("FsHafas.Raw.HimSearchRequest", [], HimSearchRequest, lambda: [("him_fltr_l", array_type(JnyFltr_reflection())), ("get_polyline", bool_type), ("max_num", int32_type), ("date_b", string_type), ("time_b", string_type)])


class HimSearchRequest(Record):
    def __init__(self, him_fltr_l: List[JnyFltr], get_polyline: bool, max_num: int, date_b: str, time_b: str) -> None:
        super().__init__()
        self.him_fltr_l = him_fltr_l
        self.get_polyline = get_polyline
        self.max_num = max_num or 0
        self.date_b = date_b
        self.time_b = time_b
    

HimSearchRequest_reflection = expr_222

def expr_223() -> TypeInfo:
    return record_type("FsHafas.Raw.ReconstructionRequest", [], ReconstructionRequest, lambda: [("get_ist", bool_type), ("get_passlist", bool_type), ("get_polyline", bool_type), ("get_tariff", bool_type), ("ctx_recon", option_type(string_type))])


class ReconstructionRequest(Record):
    def __init__(self, get_ist: bool, get_passlist: bool, get_polyline: bool, get_tariff: bool, ctx_recon: Optional[str]) -> None:
        super().__init__()
        self.get_ist = get_ist
        self.get_passlist = get_passlist
        self.get_polyline = get_polyline
        self.get_tariff = get_tariff
        self.ctx_recon = ctx_recon
    

ReconstructionRequest_reflection = expr_223

def expr_224() -> TypeInfo:
    return record_type("FsHafas.Raw.LocData", [], LocData, lambda: [("loc", Loc_reflection()), ("type", string_type), ("date", string_type), ("time", string_type)])


class LocData(Record):
    def __init__(self, loc: Loc, type: str, date: str, time: str) -> None:
        super().__init__()
        self.loc = loc
        self.type = type
        self.date = date
        self.time = time
    

LocData_reflection = expr_224

def expr_225() -> TypeInfo:
    return record_type("FsHafas.Raw.SearchOnTripRequest", [], SearchOnTripRequest, lambda: [("sot_mode", string_type), ("jid", string_type), ("loc_data", LocData_reflection()), ("arr_loc_l", array_type(Loc_reflection())), ("jny_fltr_l", array_type(JnyFltr_reflection())), ("get_passlist", bool_type), ("get_polyline", bool_type), ("min_chg_time", int32_type), ("get_tariff", bool_type)])


class SearchOnTripRequest(Record):
    def __init__(self, sot_mode: str, jid: str, loc_data: LocData, arr_loc_l: List[Loc], jny_fltr_l: List[JnyFltr], get_passlist: bool, get_polyline: bool, min_chg_time: int, get_tariff: bool) -> None:
        super().__init__()
        self.sot_mode = sot_mode
        self.jid = jid
        self.loc_data = loc_data
        self.arr_loc_l = arr_loc_l
        self.jny_fltr_l = jny_fltr_l
        self.get_passlist = get_passlist
        self.get_polyline = get_polyline
        self.min_chg_time = min_chg_time or 0
        self.get_tariff = get_tariff
    

SearchOnTripRequest_reflection = expr_225

def expr_226() -> TypeInfo:
    return record_type("FsHafas.Raw.TripSearchRequest", [], TripSearchRequest, lambda: [("get_passlist", bool_type), ("max_chg", int32_type), ("min_chg_time", int32_type), ("dep_loc_l", array_type(Loc_reflection())), ("via_loc_l", option_type(array_type(LocViaInput_reflection()))), ("arr_loc_l", array_type(Loc_reflection())), ("jny_fltr_l", array_type(JnyFltr_reflection())), ("gis_fltr_l", array_type(JnyFltr_reflection())), ("get_tariff", bool_type), ("ushrp", bool_type), ("get_pt", bool_type), ("get_iv", bool_type), ("get_polyline", bool_type), ("out_date", string_type), ("out_time", string_type), ("num_f", int32_type), ("out_frwd", bool_type), ("trf_req", option_type(TrfReq_reflection()))])


class TripSearchRequest(Record):
    def __init__(self, get_passlist: bool, max_chg: int, min_chg_time: int, dep_loc_l: List[Loc], via_loc_l: Optional[List[LocViaInput]], arr_loc_l: List[Loc], jny_fltr_l: List[JnyFltr], gis_fltr_l: List[JnyFltr], get_tariff: bool, ushrp: bool, get_pt: bool, get_iv: bool, get_polyline: bool, out_date: str, out_time: str, num_f: int, out_frwd: bool, trf_req: Optional[TrfReq]) -> None:
        super().__init__()
        self.get_passlist = get_passlist
        self.max_chg = max_chg or 0
        self.min_chg_time = min_chg_time or 0
        self.dep_loc_l = dep_loc_l
        self.via_loc_l = via_loc_l
        self.arr_loc_l = arr_loc_l
        self.jny_fltr_l = jny_fltr_l
        self.gis_fltr_l = gis_fltr_l
        self.get_tariff = get_tariff
        self.ushrp = ushrp
        self.get_pt = get_pt
        self.get_iv = get_iv
        self.get_polyline = get_polyline
        self.out_date = out_date
        self.out_time = out_time
        self.num_f = num_f or 0
        self.out_frwd = out_frwd
        self.trf_req = trf_req
    

TripSearchRequest_reflection = expr_226

def expr_227() -> TypeInfo:
    return record_type("FsHafas.Raw.JourneyMatchRequest", [], JourneyMatchRequest, lambda: [("input", string_type), ("date", option_type(string_type))])


class JourneyMatchRequest(Record):
    def __init__(self, input: str, date: Optional[str]) -> None:
        super().__init__()
        self.input = input
        self.date = date
    

JourneyMatchRequest_reflection = expr_227

def expr_228() -> TypeInfo:
    return record_type("FsHafas.Raw.RawcCrd", [], RawcCrd, lambda: [("x", int32_type), ("y", int32_type)])


class RawcCrd(Record):
    def __init__(self, x: int, y: int) -> None:
        super().__init__()
        self.x = x or 0
        self.y = y or 0
    

RawcCrd_reflection = expr_228

def expr_229() -> TypeInfo:
    return record_type("FsHafas.Raw.RawRing", [], RawRing, lambda: [("c_crd", RawcCrd_reflection()), ("max_dist", int32_type), ("min_dist", int32_type)])


class RawRing(Record):
    def __init__(self, c_crd: RawcCrd, max_dist: int, min_dist: int) -> None:
        super().__init__()
        self.c_crd = c_crd
        self.max_dist = max_dist or 0
        self.min_dist = min_dist or 0
    

RawRing_reflection = expr_229

def expr_230() -> TypeInfo:
    return record_type("FsHafas.Raw.LocGeoPosRequest", [], LocGeoPosRequest, lambda: [("ring", RawRing_reflection()), ("loc_fltr_l", array_type(JnyFltr_reflection())), ("get_pois", bool_type), ("get_stops", bool_type), ("max_loc", int32_type)])


class LocGeoPosRequest(Record):
    def __init__(self, ring: RawRing, loc_fltr_l: List[JnyFltr], get_pois: bool, get_stops: bool, max_loc: int) -> None:
        super().__init__()
        self.ring = ring
        self.loc_fltr_l = loc_fltr_l
        self.get_pois = get_pois
        self.get_stops = get_stops
        self.max_loc = max_loc or 0
    

LocGeoPosRequest_reflection = expr_230

def expr_231() -> TypeInfo:
    return record_type("FsHafas.Raw.LocGeoReachRequest", [], LocGeoReachRequest, lambda: [("loc", Loc_reflection()), ("max_dur", int32_type), ("max_chg", int32_type), ("date", string_type), ("time", string_type), ("period", int32_type), ("jny_fltr_l", array_type(JnyFltr_reflection()))])


class LocGeoReachRequest(Record):
    def __init__(self, loc: Loc, max_dur: int, max_chg: int, date: str, time: str, period: int, jny_fltr_l: List[JnyFltr]) -> None:
        super().__init__()
        self.loc = loc
        self.max_dur = max_dur or 0
        self.max_chg = max_chg or 0
        self.date = date
        self.time = time
        self.period = period or 0
        self.jny_fltr_l = jny_fltr_l
    

LocGeoReachRequest_reflection = expr_231

def expr_232() -> TypeInfo:
    return record_type("FsHafas.Raw.LocDetailsRequest", [], LocDetailsRequest, lambda: [("loc_l", array_type(Loc_reflection()))])


class LocDetailsRequest(Record):
    def __init__(self, loc_l: List[Loc]=None) -> None:
        super().__init__()
        self.loc_l = loc_l
    

LocDetailsRequest_reflection = expr_232

def expr_233() -> TypeInfo:
    return record_type("FsHafas.Raw.ServerInfoRequest", [], ServerInfoRequest, lambda: [("get_version_info", bool_type)])


class ServerInfoRequest(Record):
    def __init__(self, get_version_info: bool=None) -> None:
        super().__init__()
        self.get_version_info = get_version_info
    

ServerInfoRequest_reflection = expr_233

def expr_234() -> TypeInfo:
    return record_type("FsHafas.Raw.RawRect", [], RawRect, lambda: [("ll_crd", RawCrd_reflection()), ("ur_crd", RawCrd_reflection())])


class RawRect(Record):
    def __init__(self, ll_crd: RawCrd, ur_crd: RawCrd) -> None:
        super().__init__()
        self.ll_crd = ll_crd
        self.ur_crd = ur_crd
    

RawRect_reflection = expr_234

def expr_235() -> TypeInfo:
    return record_type("FsHafas.Raw.JourneyGeoPosRequest", [], JourneyGeoPosRequest, lambda: [("max_jny", int32_type), ("only_rt", bool_type), ("date", string_type), ("time", string_type), ("rect", RawRect_reflection()), ("per_size", int32_type), ("per_step", int32_type), ("age_of_report", bool_type), ("jny_fltr_l", array_type(JnyFltr_reflection())), ("train_pos_mode", string_type)])


class JourneyGeoPosRequest(Record):
    def __init__(self, max_jny: int, only_rt: bool, date: str, time: str, rect: RawRect, per_size: int, per_step: int, age_of_report: bool, jny_fltr_l: List[JnyFltr], train_pos_mode: str) -> None:
        super().__init__()
        self.max_jny = max_jny or 0
        self.only_rt = only_rt
        self.date = date
        self.time = time
        self.rect = rect
        self.per_size = per_size or 0
        self.per_step = per_step or 0
        self.age_of_report = age_of_report
        self.jny_fltr_l = jny_fltr_l
        self.train_pos_mode = train_pos_mode
    

JourneyGeoPosRequest_reflection = expr_235

def expr_236() -> TypeInfo:
    return record_type("FsHafas.Raw.SvcReq", [], SvcReq, lambda: [("cfg", Cfg_reflection()), ("meth", string_type), ("req", obj_type)])


class SvcReq(Record):
    def __init__(self, cfg: Cfg, meth: str, req: Any) -> None:
        super().__init__()
        self.cfg = cfg
        self.meth = meth
        self.req = req
    

SvcReq_reflection = expr_236

def expr_237() -> TypeInfo:
    return record_type("FsHafas.Raw.RawRequestClient", [], RawRequestClient, lambda: [("id", string_type), ("v", string_type), ("type", string_type), ("name", string_type)])


class RawRequestClient(Record):
    def __init__(self, id: str, v: str, type: str, name: str) -> None:
        super().__init__()
        self.id = id
        self.v = v
        self.type = type
        self.name = name
    

RawRequestClient_reflection = expr_237

def expr_238() -> TypeInfo:
    return record_type("FsHafas.Raw.RawRequestAuth", [], RawRequestAuth, lambda: [("type", string_type), ("aid", string_type)])


class RawRequestAuth(Record):
    def __init__(self, type: str, aid: str) -> None:
        super().__init__()
        self.type = type
        self.aid = aid
    

RawRequestAuth_reflection = expr_238

def expr_239() -> TypeInfo:
    return record_type("FsHafas.Raw.RawRequest", [], RawRequest, lambda: [("lang", string_type), ("svc_req_l", array_type(SvcReq_reflection())), ("client", RawRequestClient_reflection()), ("ext", string_type), ("ver", string_type), ("auth", RawRequestAuth_reflection())])


class RawRequest(Record):
    def __init__(self, lang: str, svc_req_l: List[SvcReq], client: RawRequestClient, ext: str, ver: str, auth: RawRequestAuth) -> None:
        super().__init__()
        self.lang = lang
        self.svc_req_l = svc_req_l
        self.client = client
        self.ext = ext
        self.ver = ver
        self.auth = auth
    

RawRequest_reflection = expr_239

