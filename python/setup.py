import sys
import platform
import os

from setuptools import Extension, setup

# "The C extension interface is specific to CPython, and extension
# modules do not work on other Python implementations." -
# https://docs.python.org/3/extending/extending.html
supported_platform = platform.python_implementation() == "CPython"

attempt_compilation = (
    supported_platform and os.environ.get("FORCE_BASE92_PYTHON", "0") == "0"
)

ext_modules = []
if attempt_compilation:
    ext_modules.append(
        Extension(
            name="base92._base92compiled",
            sources=["src/base92/_base92extension.c"],
            # Don't fail the install if the extension fails to build.
            optional=True,
        )
    )

setup(
    ext_modules=ext_modules,
)
