import atheris
import sys
from atherina.decorator import FUZZ_TARGETS

with atheris.instrument_imports():
    import atherina.fuzz_util as fuzz_util
    
def TestOneInput(data):
    for func in FUZZ_TARGETS:
        fn = func['fn']
        arg_types = func['arg_types']
        
        kwargs = fuzz_util.generateInput(data, arg_types)
        #sys.stderr.write(f"Debug: fn={fn} kwargs={kwargs}\n")
        fuzz_util.run_function(fn, kwargs)
    #sys.stderr.flush()

def fuzz_all():
    print(FUZZ_TARGETS)
    if FUZZ_TARGETS == []:
        return
    atheris.Setup(sys.argv, TestOneInput)
    atheris.Fuzz()