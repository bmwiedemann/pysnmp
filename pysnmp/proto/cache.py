#
# This file is part of pysnmp software.
#
# Copyright (c) 2005-2019, Ilya Etingof <etingof@gmail.com>
# License: https://www.pysnmp.com/pysnmp/license.html
#
from typing import Any, Callable
from pysnmp.proto import error


class Cache:
    def __init__(self):
        self.__cacheRepository = {}

    def add(self, index: int, **kwargs) -> int:
        self.__cacheRepository[index] = kwargs
        return index

    def pop(self, index: int):
        if index in self.__cacheRepository:
            cachedParams = self.__cacheRepository[index]
        else:
            return
        del self.__cacheRepository[index]
        return cachedParams

    def update(self, index: int, **kwargs):
        if index not in self.__cacheRepository:
            raise error.ProtocolError(
                'Cache miss on update for %s' % kwargs
            )
        self.__cacheRepository[index].update(kwargs)

    def expire(self, cbFun, cbCtx):
        for index, cachedParams in list(self.__cacheRepository.items()):
            if cbFun:
                if cbFun(index, cachedParams, cbCtx):
                    if index in self.__cacheRepository:
                        del self.__cacheRepository[index]
