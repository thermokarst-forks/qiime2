# ----------------------------------------------------------------------------
# Copyright (c) 2016--, QIIME 2 development team.
#
# Distributed under the terms of the Modified BSD License.
#
# The full license is in the file COPYING.txt, distributed with this software.
# ----------------------------------------------------------------------------

from typing import Generic, TypeVar, GenericMeta

T = TypeVar('T')

class ResourceMeta(GenericMeta):
    """
    | I think the tl;dr is "please don't do that".
                                    - Guido van Rossum BDFL

    This will be replaced with something else depending on the outcome of:
        https://github.com/python/typing/issues/263

    """
    _registry = {}

    def __new__(cls, name, bases, dct, pattern=None):
        # I assume a singleton factory is necessary as MyPy and Python are
        # nominally typed, so the same expression should yield the same
        # instance
        if pattern not in cls._registry:
            # Just return the value outright at runtime (should be str)
            dct['__new__'] = lambda cls, value: value
            cls._registry[pattern] = super().__new__(cls, name, bases, dct)

        return cls._registry[pattern]

    def __init__(self, name, bases, dct, pattern=None):
        # The particular resource pattern that we want to keep track of
        # for runtime coercion
        self.__pattern__ = pattern

    def __getitem__(self, pattern):
        return self.__class__(self.__name__, self.__bases__,
                              dict(self.__dict__), pattern=pattern)


class FilePath(str, Generic[T], metaclass=ResourceMeta):
    pass


class DirectoryPath(str, Generic[T], metaclass=ResourceMeta):
    pass

#
# class Object(Generic[T], metaclass=ResourceMeta):
#     pass
