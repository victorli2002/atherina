from type_fuzzer import fuzz, fuzz_all
from typing import List, Dict, Set, Tuple

@fuzz
def foo(x: int, y: str) -> bool:
    return True

#@fuzz
def bar(a: int, b: float):
    if a > 100000 and a % 10000 == 67:
        return a / 0
    return a + b

#@fuzz
def bazz(a: List[int] | str):
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

@fuzz
def qux(a: Dict[int, complex], b: Set[int], c: Tuple[int, float]):
    # if any(v.imag > 1000 for v in a.values()):
    #     raise Exception
    #     return
    # if sum(b) > 100:
    #     raise Exception
    if c[0] % 100 == 7:
        if c[1] > c[0]:
            raise Exception

if __name__ == "__main__":
    fuzz_all()