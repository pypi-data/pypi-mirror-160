from ctypes import CDLL, c_int

sub_errno = None


def load_ctypes_library(name, signatures):
    lib = CDLL(name, use_errno=True)
    if not lib:
        raise ImportError(f"Can't import {name}")
    # Add function signatures
    for funcname, signature in signatures.items():
        function = getattr(lib, funcname, None)
        if function:
            argtypes, restype = signature
            function.argtypes = argtypes
            if restype:
                function.restype = restype
    return lib
