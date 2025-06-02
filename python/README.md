# base92

A Python library for encoding byte-strings into strings easily
typeable on a standard US 101-key keyboard (ASCII), with strictly
better information density than base64 or base85 encodings. See
`docs/encoding.md` for more encoding details.

## Installation

[This package is available via
pypi](https://pypi.org/project/base92/). As such, it should be
available via the normal channels, like `pip` (`pip install base92`).

If pypi is not available, you can use this repository to build or
install:

```
pip install $PATH_TO_REPO
```

## Usage

Fire up your favorite python::

```
>>> import base92
>>> base92.decode(base92.encode('hello world'))
'hello world'
>>> base92.encode('\x61\xf2\x05\x99\x42')
'DJ8gER!'
```

## Performance

As of v2.0, installation under CPython will attempt to build a C
version of the base92 module and use it instead. If the build fails,
the module will fall back to a pure Python version.

The C version is approximately 100x faster than the pure Python
version (comparable to the speed of the builtin `base64`
module). There are more details on run time performance in
`docs/performance.md`.

Other Pythons do not support the C extension inteface (pypy, etc; [see
documentation](https://docs.python.org/3/extending/extending.html)).

It is possible to force the package to be installed with the pure
Python version (add `FORCE_BASE92_PYTHON=1` to your shell environment
when installing). I don't anticipate this option being necessary; if
your environment does not support compilation, setuptools should
continue installing the pure python package.

## Development

I will assume you're using [`uv`](https://github.com/astral-sh/uv).

If you're making a significant change that may impact encoding
outputs, you may want to generate a million example mappings before
making your changes (which are not checked in, since the resulting
file is hundreds of megabytes):

```
uv run python3 tests/generate_exhaustive.py
```

Once you've made your change, run the tests/type
checker/autoformatter:

```
uv run tox
```

To check against the earlier exhaustive examples:

```
RUN_EXHAUSTIVE_TESTS=1 uv run tox
```

To run this against a fuzzer
([atheris](https://github.com/google/atheris)):

```
# Install libfuzzer. Below is an example for Debian/Ubuntu; I just
# grabbed the biggest number.
sudo apt install libfuzzer-19-dev
# Run the fuzzer.
# Replace the $LIBRARY with one of:
#  - asan
#  - ubsan
# Replace the $FUNCTION with one of:
#  - pyencode
#  - pydecode
LD_PRELOAD="$(uv run python -c "import atheris; print(atheris.path())")/$LIBRARY_with_fuzzer.so" uv run python3 tests/fuzzing.py $FUNCTION -runs=100000
```

For some reason, `asan` finds a number of memory leaks. It is unclear
where they could be coming from, especially since the leak size
changes. My best guess is that the return value is sometimes not being
freed before leaks are checked.

If you've made changes to the C extension, kindly autoformat it with
`clang-format`:

```
clang-format -i src/base92/_base92extension.c
```

You may need to source `clang-format` from wherever you get your
software.

## Other languages

- The C repo is currently tied to this one.
- [pixa-pics/Base92](https://github.com/pixa-pics/Base92) is a JS version of this protocol.
- At some point there was a [Go package](https://pkg.go.dev/github.com/surefootedwi/go-encoding/base92), but the Github repo now 404's (as of 2025-06). Unclear if it was based on my work or not.
