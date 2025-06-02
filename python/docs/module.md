# C Module

We have both pure Python and a C extension. The C extension has much
better performance, but build tools might not be available everywhere.

Ideally, we could support both implementations, preferentially
building and using the faster C implementation, while keeping pure
Python as a fallback.

A query brings up some candidates:

- NumPy. I am sure the configuration of this project is horrendously complicated, and isn't the entire point of NumPy the compiled extensions?
- [lxml](https://github.com/lxml/lxml/blob/master/setup.py): setup is somewhat obscured by the use of Cython.
- [pyyaml](https://github.com/yaml/pyyaml/blob/main/setup.py): setup is somewhat obscured by the use of Cython.
- [markupsafe](https://github.com/pallets/markupsafe/blob/main/setup.py): this project is small enough that it's clear exactly how this works.

However, where in the world does the `ve_build_ext` code come from? It
has a concerning number of special cases involved; is there a tutorial
I missed which tells one how to define this?

A query for "class ve_build_ext(build_ext):" later, [I found a blog
post from
2012](https://nedbatchelder.com/blog/201212/skipping_c_extensions.html)
which notes that this same class has been proliferating for a while,
with a comment noting it's from 2003. Additionally, the comments note
that there's a much simpler optional=True param for distutils, which
was at some point folded into setuptools, and which [still exists on
the current day
Extension](https://setuptools.pypa.io/en/latest/userguide/ext_modules.html#extension-api-reference).
