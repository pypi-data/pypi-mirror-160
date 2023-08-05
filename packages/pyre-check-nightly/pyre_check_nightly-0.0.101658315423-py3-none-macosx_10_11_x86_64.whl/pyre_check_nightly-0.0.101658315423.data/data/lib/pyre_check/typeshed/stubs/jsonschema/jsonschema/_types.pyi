from typing import Callable, Iterable, Mapping

def is_array(checker, instance) -> bool: ...
def is_bool(checker, instance) -> bool: ...
def is_integer(checker, instance) -> bool: ...
def is_null(checker, instance) -> bool: ...
def is_number(checker, instance) -> bool: ...
def is_object(checker, instance) -> bool: ...
def is_string(checker, instance) -> bool: ...
def is_any(checker, instance) -> bool: ...

class TypeChecker:
    def __init__(self, type_checkers: Mapping[str, Callable[[object], bool]] = ...) -> None: ...
    def is_type(self, instance, type: str) -> bool: ...
    def redefine(self, type: str, fn: Callable[..., bool]) -> TypeChecker: ...
    def redefine_many(self, definitions=...) -> TypeChecker: ...
    def remove(self, *types: Iterable[str]) -> TypeChecker: ...

draft3_type_checker: TypeChecker
draft4_type_checker: TypeChecker
draft6_type_checker: TypeChecker
draft7_type_checker: TypeChecker
draft201909_type_checker: TypeChecker
draft202012_type_checker: TypeChecker
