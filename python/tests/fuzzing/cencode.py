import atheris  # type: ignore
import sys

with atheris.instrument_imports():
    import base92._base92compiled


def TestCompiledEncode(data):
    base92._base92compiled.base92_encode(data)


atheris.Setup(sys.argv, TestCompiledEncode)
atheris.Fuzz()
