from __future__ import annotations
from typing import List
from ...fable_library.array import (fold, exists)
from ...fs_hafas_python.context import Context
from ...fs_hafas_python.extra_types import (IndexMap_2, IndexMap_2__set_Item_541DA560, IndexMap_2__ctor_2B594)
from ...fs_hafas_python.types_hafas_client import ProductType

def parse_bitmask(ctx: Context, bitmask: int) -> IndexMap_2[str, bool]:
    array_1 : List[ProductType] = ctx.profile.products
    def folder(m: IndexMap_2[str, bool], p: ProductType, ctx: Context=ctx, bitmask: int=bitmask) -> IndexMap_2[str, bool]:
        def predicate(b: int, m: IndexMap_2[str, bool]=m, p: ProductType=p) -> bool:
            return (b & bitmask) != 0
        
        IndexMap_2__set_Item_541DA560(m, p.id, exists(predicate, p.bitmasks))
        return m
    
    return fold(folder, IndexMap_2__ctor_2B594(False), array_1)


