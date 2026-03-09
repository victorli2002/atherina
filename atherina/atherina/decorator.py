import inspect
from typing import get_type_hints, Callable
        
FUZZ_TARGETS = []

def fuzz(fn: Callable) -> Callable:
    sig = inspect.signature(fn)
    hints = get_type_hints(fn)

    arg_types = {
        name: hints.get(name, None)
        for name in sig.parameters
    }
    
    FUZZ_TARGETS.append({
        "fn": fn,
        "arg_types": arg_types,
    })
    return fn
    