import atheris  # type: ignore
import sys

with atheris.instrument_imports():
    import base92._base92python


def TestPythonEncode(data):
    base92._base92python.base92_encode(data)


atheris.Setup(sys.argv, TestPythonEncode)
atheris.Fuzz()
