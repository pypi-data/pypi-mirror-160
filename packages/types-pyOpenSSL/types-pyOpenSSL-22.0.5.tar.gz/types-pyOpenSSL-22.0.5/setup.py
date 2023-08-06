from setuptools import setup

name = "types-pyOpenSSL"
description = "Typing stubs for pyOpenSSL"
long_description = '''
## Typing stubs for pyOpenSSL

This is a PEP 561 type stub package for the `pyOpenSSL` package.
It can be used by type-checking tools like mypy, PyCharm, pytype etc. to check code
that uses `pyOpenSSL`. The source for this package can be found at
https://github.com/python/typeshed/tree/master/stubs/pyOpenSSL. All fixes for
types and metadata should be contributed there.

See https://github.com/python/typeshed/blob/master/README.md for more details.
This package was generated from typeshed commit `32bac7280efc36a17c32c620f61b8e9c93bf1106`.
'''.lstrip()

setup(name=name,
      version="22.0.5",
      description=description,
      long_description=long_description,
      long_description_content_type="text/markdown",
      url="https://github.com/python/typeshed",
      project_urls={
          "GitHub": "https://github.com/python/typeshed",
          "Changes": "https://github.com/typeshed-internal/stub_uploader/blob/main/data/changelogs/pyOpenSSL.md",
          "Issue tracker": "https://github.com/python/typeshed/issues",
          "Chat": "https://gitter.im/python/typing",
      },
      install_requires=['types-cryptography'],
      packages=['OpenSSL-stubs'],
      package_data={'OpenSSL-stubs': ['SSL.pyi', '__init__.pyi', 'crypto.pyi', 'METADATA.toml']},
      license="Apache-2.0 license",
      classifiers=[
          "License :: OSI Approved :: Apache Software License",
          "Programming Language :: Python :: 3",
          "Typing :: Stubs Only",
      ]
)
