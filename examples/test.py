from atherina import fuzz, fuzz_all
from typing import List, Dict, Set, Tuple
from dataclasses import dataclass

@fuzz
def foo(x: int, y: str) -> bool:
    return True

#@fuzz
def bar(a: int, b: float):
    if a > 100000 and a % 10000 == 67:
        return a / 0
    return a + b

#@fuzz
def baz(a: List[int] | str):
    if isinstance(a, str):
        assert len(a) > 5
        #if a[5] == "a":
        #    raise Exception
        return
    if isinstance(a, list):
        assert len(a) > 5
        if a[5] == 1:
            raise Exception
        return
    
    raise Exception("not supposed to get triggered")

#@fuzz
def qux(a: Dict[int, complex], b: Set[int], c: Tuple[int, float]):
    # if any(v.imag > 1000 for v in a.values()):
    #     raise Exception
    #     return
    # if sum(b) > 100:
    #     raise Exception
    if c[0] % 100 == 7:
        if c[1] > c[0]:
            raise Exception

@dataclass
class DC:
    x: int
    y: float
    z: Tuple[str, str | None]

@fuzz
def uses_dataclass(p: DC):
    if p.x > 1000 and p.y < -1000 and len(p.z[0]) > 1 and p.z[1] is None:
        raise Exception

# regular class with fully annotated __init__
class FullyAnnotated:
    def __init__(self, x: int, y: float):
        self.x = x
        self.y = y

#@fuzz
def uses_fully_annotated(obj: FullyAnnotated):
    if obj.x > 500 and obj.y < -500:
        raise Exception

# regular class with unannotated param — should raise UnsupportedTypeError
class PartiallyAnnotated:
    def __init__(self, x: int, y):  # y has no annotation
        self.x = x
        self.y = y

#@fuzz
def uses_partially_annotated(obj: PartiallyAnnotated):
    pass

# class with no __init__, only class-level annotations — uses setattr path
class NoInit:
    x: int
    y: str

#@fuzz
def uses_no_init(obj: NoInit):
    if obj.x > 500 and len(obj.y) > 2:
        raise Exception

if __name__ == "__main__":
    fuzz_all()