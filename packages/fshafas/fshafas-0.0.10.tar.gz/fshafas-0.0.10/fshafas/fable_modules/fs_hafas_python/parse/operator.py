from __future__ import annotations
from ...fs_hafas_python.context import Context
from ...fs_hafas_python.lib.slug import slugify
from ...fs_hafas_python.types_hafas_client import Operator
from ...fs_hafas_python.types_raw_hafas_client import RawOp

def slug(s: str) -> str:
    return slugify(s)


default_operator : Operator = Operator("operator", "", "")

def parse_operator(ctx: Context, a: RawOp) -> Operator:
    name : str = a.name.strip()
    return Operator(default_operator.type, slug(name), name)


