from atherina import fuzz, fuzz_all
from typing import List, Dict, Set, Tuple
from dataclasses import dataclass

#@fuzz
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

#@fuzz
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

# regular class with unannotated param should raise UnsupportedTypeError
class PartiallyAnnotated:
    def __init__(self, x: int, y):  # y has no annotation
        self.x = x
        self.y = y

#@fuzz
def uses_partially_annotated(obj: PartiallyAnnotated):
    pass

# class with no __init__
class NoInit:
    x: int
    y: str

#@fuzz
def uses_no_init(obj: NoInit):
    if obj.x > 500 and len(obj.y) > 2:
        raise Exception

#Stress test
#Easy bug: ZeroDivisionError when adjustment != None and adjustment.imag == 0.0
#Medium bug: ZeroDivisionError when a sector_weight val[0] == 0.0 and the order is active
#Hard bug: Exception when strict=True, min_qty > 0, and at least one order has qty == 0
@dataclass
class Order:
    qty: int
    price: float
    tag: Tuple[str, str | None]
    active: bool

#easy one found first - instant

#medium one found in less than 5 min
#30335  REDUCE cov: 28 ft: 149 corp: 31/989b lim: 226 exec/s: 1596 rss: 40Mb L: 213/213 MS: 4 ChangeByte-InsertRepeatedBytes-CrossOver-InsertRepeatedBytes-

#hard one also found in less than 5 min
#@fuzz(ignore=[ZeroDivisionError])
#20987  REDUCE cov: 31 ft: 150 corp: 25/588b lim: 163 exec/s: 1499 rss: 40Mb L: 131/154 MS: 1 EraseBytes-
def process_orders(
    orders: List[Order],
    sector_weights: Dict[str, Tuple[float, int]],   #sector -> (weight, cap)
    risk_bounds: Tuple[int, float, bool],   #(min_qty, max_exposure, strict)
    priority_set: Set[int],
    adjustment: complex | None,
) -> float:
    gross = 0.0
    for order in orders:
        if order.active and order.qty > 0:
            gross += order.qty * order.price

    #Medium Bug
    weighted = 0.0
    for order in orders:
        sector = order.tag[0]
        if sector in sector_weights:
            w, cap = sector_weights[sector]
            if order.active and order.qty <= cap:
                weighted += (order.qty * order.price) / w

    #Hard Bug
    min_qty, max_exposure, strict = risk_bounds
    if strict and gross > max_exposure:
        for order in orders:
            if order.qty < min_qty:
                raise Exception(
                    f"order qty {order.qty} violates minimum {min_qty}"
                )

    #Easy Bug
    if adjustment is not None:
        #phase = adjustment.real / adjustment.imag
        assert True
        
    score = sum(p * p for p in priority_set if p > 0)
    sub_totals: Dict[str, float] = {}
    for order in orders:
        sub = order.tag[1]
        if sub is not None:
            sub_totals[sub] = sub_totals.get(sub, 0.0) + order.qty * order.price

    return weighted + score


if __name__ == "__main__":
    fuzz_all()