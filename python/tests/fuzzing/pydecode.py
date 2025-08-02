import atheris  # type: ignore
import sys

with atheris.instrument_imports():
    import base92._base92python


def TestPythonDecode(data):
    try:
        base92._base92python.base92_decode(data)
    except ValueError as exception:
        # Ignore errors that we throw.
        if exception.args[0] not in (
            "1 character is not a valid base92 encoding",
            "Invalid base92 character",
            "Invalid base92 string",
        ):
            raise


atheris.Setup(sys.argv, TestPythonDecode)
atheris.Fuzz()
