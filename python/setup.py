import os
from setuptools import setup, Extension

CFLAGS = os.environ.get('CFLAGS', '').split()
LFLAGS = os.environ.get('LFLAGS', '').split()

setup(
    name='base92',
    version='1.0.3',
    author='thenoviceoof',
    author_email='thenoviceoof@gmail.com',
    packages=['base92'],
    scripts=[],
    url='https://github.com/thenoviceoof/base92',
    license='LICENSE.txt',
    description='A library to create base92 encoded strings',
    long_description=open('README.txt').read(),
    install_requires=[],
    ext_modules = [
        Extension(
            'base92.base92_extension',
            include_dirs=['base92'],
            define_macros=def_macros,
            sources=['base92/base92_extension.c'],
            library_dirs=[],
            libraries=[],
            extra_link_args=LFLAGS,
            extra_compile_args=CFLAGS,
        ),
     ],
)
