# -*- coding: utf-8 -*-
# This file is part of Quark-Engine - https://github.com/quark-engine/quark-engine
# See the file 'LICENSE' for copying permission.

from ctypes import Union
from email.generator import Generator
from typing import List

from quark.script import Method


class Frida:
    def __init__(self) -> None:
        pass

    def hookMethod(
        self,
        method: Union[Method, str],
        overloadFilter: str = "",
        watchArgs: bool = False
    ):
        pass

    def getParamValues(self, method) -> Generator[str, None, None]:
        pass

    def getBacktrace(self, method) -> Generator[List[str], None, None]:
        pass