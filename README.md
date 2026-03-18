An automatic fuzzing workflow based on Atheris that uses type hints to generate inputs.

Requires Linux (atheris does not support macOS/Windows natively).

## Installation

```bash
python -m pip install atherina/
```

## Usage

Decorate functions with `@fuzz`, then call `fuzz_all()` to run the fuzzer against all decorated functions.

```python
from type_fuzzer import fuzz, fuzz_all
from typing import List

@fuzz
def my_func(x: int, y: str) -> bool:
    ...

if __name__ == "__main__":
    fuzz_all()
```

See [examples/test.py](examples/test.py) for a full example.
