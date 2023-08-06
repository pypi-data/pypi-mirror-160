from typing import (TypeVar, Callable, Any, Optional)
from .util import (IEqualityComparer, structural_hash, equals, physical_hash, IComparer, compare)

_T = TypeVar("_T")

_T_ = TypeVar("_T_")

def HashIdentity_FromFunctions(hash_1: Callable[[_T], int], eq: Callable[[_T, _T], bool]) -> IEqualityComparer[Any]:
    class ObjectExpr1(IEqualityComparer[Any]):
        def Equals(self, x: _T_, y: _T_, hash_1: Callable[[_T], int]=hash_1, eq: Callable[[_T, _T], bool]=eq) -> bool:
            return eq(x, y)
        
        def GetHashCode(self, x_1: Optional[_T_]=None, hash_1: Callable[[_T], int]=hash_1, eq: Callable[[_T, _T], bool]=eq) -> int:
            return hash_1(x_1)
        
    return ObjectExpr1()


def HashIdentity_Structural() -> IEqualityComparer[Any]:
    def arrow_2(obj: Optional[_T]=None) -> int:
        return structural_hash(obj)
    
    def arrow_3(e1: _T, e2: _T) -> bool:
        return equals(e1, e2)
    
    return HashIdentity_FromFunctions(arrow_2, arrow_3)


def HashIdentity_Reference() -> IEqualityComparer[Any]:
    def arrow_4(obj: Optional[_T]=None) -> int:
        return physical_hash(obj)
    
    def arrow_5(e1: _T, e2: _T) -> bool:
        return e1 is e2
    
    return HashIdentity_FromFunctions(arrow_4, arrow_5)


def ComparisonIdentity_FromFunction(comparer: Callable[[_T, _T], int]) -> IComparer[_T]:
    class ObjectExpr6(IComparer[_T_]):
        def Compare(self, x: _T_, y: _T_, comparer: Callable[[_T, _T], int]=comparer) -> int:
            return comparer(x, y)
        
    return ObjectExpr6()


def ComparisonIdentity_Structural() -> IComparer[_T]:
    def arrow_7(e1: _T, e2: _T) -> int:
        return compare(e1, e2)
    
    return ComparisonIdentity_FromFunction(arrow_7)


