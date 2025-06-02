import atheris  # type: ignore
import argparse

with atheris.instrument_imports():
    import base92._base92python

DESCRIPTION = """Fuzzing tests for base92."""


def TestPythonEncode(data):
    base92._base92python.base92_encode(data)


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


if __name__ == "__main__":
    argparser = argparse.ArgumentParser(description=DESCRIPTION)
    argparser.add_argument("test", choices=["pyencode", "pydecode"])
    argparser.add_argument("pass_args", nargs="*")

    args, other_args = argparser.parse_known_args()

    # Leaving out the prog means the other args are not consumed
    # correctly.
    argv = [argparser.prog]
    argv.extend(other_args)

    # Add a default runs parameter if one is not already present.
    if not any(arg.startswith("-runs=") for arg in argv):
        argv.append("-runs=100000")

    # Run the fuzzer.
    if args.test == "pyencode":
        atheris.Setup(argv, TestPythonEncode)
        atheris.Fuzz()
    elif args.test == "pydecode":
        atheris.Setup(argv, TestPythonDecode)
        atheris.Fuzz()
    # TODO: figure out if I'm instrumenting the C extension properly.
