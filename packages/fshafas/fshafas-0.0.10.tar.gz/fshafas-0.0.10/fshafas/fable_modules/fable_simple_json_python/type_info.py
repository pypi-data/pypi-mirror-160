from __future__ import annotations
from typing import (Any, List)
from ..fable_library.reflection import (TypeInfo as TypeInfo_1, string_type, class_type, record_type, array_type, unit_type, lambda_type, tuple_type, union_type)
from ..fable_library.types import (Record, Union)

def expr_0() -> TypeInfo_1:
    return record_type("Fable.SimpleJson.Python.RecordField", [], RecordField, lambda: [("FieldName", string_type), ("FieldType", TypeInfo_reflection()), ("PropertyInfo", class_type("System.Reflection.PropertyInfo"))])


class RecordField(Record):
    def __init__(self, FieldName: str, FieldType: TypeInfo, PropertyInfo: Any) -> None:
        super().__init__()
        self.FieldName = FieldName
        self.FieldType = FieldType
        self.PropertyInfo = PropertyInfo
    

RecordField_reflection = expr_0

def expr_1() -> TypeInfo_1:
    return record_type("Fable.SimpleJson.Python.UnionCase", [], UnionCase, lambda: [("CaseName", string_type), ("CaseTypes", array_type(TypeInfo_reflection())), ("Info", class_type("Microsoft.FSharp.Reflection.UnionCaseInfo"))])


class UnionCase(Record):
    def __init__(self, CaseName: str, CaseTypes: List[TypeInfo], Info: Any) -> None:
        super().__init__()
        self.CaseName = CaseName
        self.CaseTypes = CaseTypes
        self.Info = Info
    

UnionCase_reflection = expr_1

def expr_2() -> TypeInfo_1:
    return union_type("Fable.SimpleJson.Python.TypeInfo", [], TypeInfo, lambda: [[], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [("Item", lambda_type(unit_type, class_type("System.Type")))], [("Item", lambda_type(unit_type, TypeInfo_reflection()))], [("Item", lambda_type(unit_type, TypeInfo_reflection()))], [("Item", lambda_type(unit_type, TypeInfo_reflection()))], [("Item", lambda_type(unit_type, TypeInfo_reflection()))], [("Item", lambda_type(unit_type, TypeInfo_reflection()))], [("Item", lambda_type(unit_type, TypeInfo_reflection()))], [("Item", lambda_type(unit_type, TypeInfo_reflection()))], [("Item", lambda_type(unit_type, array_type(TypeInfo_reflection())))], [("Item", lambda_type(unit_type, tuple_type(TypeInfo_reflection(), TypeInfo_reflection())))], [("Item", lambda_type(unit_type, tuple_type(TypeInfo_reflection(), TypeInfo_reflection(), class_type("System.Type"))))], [("Item", lambda_type(unit_type, TypeInfo_reflection()))], [("Item", lambda_type(unit_type, TypeInfo_reflection()))], [("Item", lambda_type(unit_type, array_type(TypeInfo_reflection())))], [("Item", lambda_type(unit_type, tuple_type(TypeInfo_reflection(), class_type("System.Type"))))], [("Item", lambda_type(unit_type, tuple_type(array_type(RecordField_reflection()), class_type("System.Type"))))], [("Item", lambda_type(unit_type, tuple_type(array_type(UnionCase_reflection()), class_type("System.Type"))))]])


class TypeInfo(Union):
    def __init__(self, tag: int, *fields: Any) -> None:
        super().__init__()
        self.tag : int = tag or 0
        self.fields : List[Any] = list(fields)
    
    @staticmethod
    def cases() -> List[str]:
        return ["Unit", "Char", "String", "UInt16", "UInt32", "UInt64", "Int32", "Bool", "Float32", "Float", "Decimal", "Short", "Long", "Byte", "SByte", "DateTime", "DateTimeOffset", "BigInt", "TimeSpan", "Guid", "Object", "Uri", "Any", "Async", "Promise", "Option", "List", "Set", "Array", "Seq", "Tuple", "Map", "Dictionary", "ResizeArray", "HashSet", "Func", "Enum", "Record", "Union"]
    

TypeInfo_reflection = expr_2

