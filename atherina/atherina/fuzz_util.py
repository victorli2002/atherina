import atheris
import dataclasses
import types
import typing
from typing import get_origin, get_args, Union

class UnsupportedTypeError(Exception):
    pass

def typed_data(fdp, typ):
    origin = get_origin(typ)
    args = get_args(typ)

    if typ is type(None):
        return None

    if typ is int:
        return fdp.ConsumeInt(32)

    if typ is bool:
        return fdp.ConsumeBool()

    if typ is float:
        return fdp.ConsumeFloat()

    if typ is str:
        return fdp.ConsumeUnicodeNoSurrogates(32)

    if origin is list:
        list_typ = args[0]
        n = fdp.ConsumeIntInRange(0, 100) # limit the length
        return [typed_data(fdp, list_typ) for _ in range(n)]

    if origin is Union or isinstance(typ, types.UnionType):
        idx = fdp.ConsumeIntInRange(0, len(args)-1)
        return typed_data(fdp, args[idx])

    if typ is complex:
        return complex(fdp.ConsumeFloat(), fdp.ConsumeFloat())

    if origin is tuple:
        return tuple(typed_data(fdp, a) for a in args)

    if origin is set:
        elem_typ = args[0]
        n = fdp.ConsumeIntInRange(0, 100)
        return {typed_data(fdp, elem_typ) for _ in range(n)}

    if origin is dict:
        key_typ, val_typ = args
        n = fdp.ConsumeIntInRange(0, 100)
        return {typed_data(fdp, key_typ): typed_data(fdp, val_typ) for _ in range(n)}

    if dataclasses.is_dataclass(typ) and isinstance(typ, type):
        hints = typing.get_type_hints(typ)
        kwargs = {name: typed_data(fdp, field_typ) for name, field_typ in hints.items()}
        return typ(**kwargs)

    raise UnsupportedTypeError(f"Unsupported type: {typ}")

def generateInput(input_bytes, arg_types):
    fdp = atheris.FuzzedDataProvider(input_bytes)
    kwargs = {k: typed_data(fdp, t) for k, t in arg_types.items()}
    return kwargs

def run_function(fn, kwargs):
    try:
        fn(**kwargs)
#     except UnsupportedTypeError:
#         return
    except AssertionError:
        return
    except Exception:
        print("-"*50)
        print("crash detected")
        print(f"function: {fn.__name__}")
        print(f"args: {kwargs}")
        raise
