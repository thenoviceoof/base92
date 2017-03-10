import os
import platform
from setuptools import find_packages, setup, Extension

CFLAGS = os.environ.get('CFLAGS', '').split()
LFLAGS = os.environ.get('LFLAGS', '').split()
def_macros = []

extensions = []
if platform.system() != 'Windows':
    extensions.append(Extension(
        'base92.base92_extension',
        include_dirs=['python/base92'],
        define_macros=def_macros,
        sources=['python/base92/base92_extension.c'],
        library_dirs=[],
        libraries=[],
        extra_link_args=LFLAGS,
        extra_compile_args=CFLAGS,
    ))

setup(
    name='base92',
    version='1.0.3',
    author='thenoviceoof',
    author_email='thenoviceoof@gmail.com',
    packages=find_packages(where='python/'),
    package_dir={'': 'python/'},
    scripts=[],
    url='https://github.com/thenoviceoof/base92',
    license='LICENSE.txt',
    description='A library to create base92 encoded strings',
    long_description=open('python/README.txt').read(),
    install_requires=[],
    ext_modules = extensions,
)
