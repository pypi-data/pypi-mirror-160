# -*- coding: utf-8 -*-

import pytcm

from pygitm.git import clone
from pygitm.options import CloneOptions


class Repository:
    def __init__(self, cwd: str) -> None:
        self._cwd = cwd

    def clone(self, opts: CloneOptions) -> pytcm.CommandResult:
        return clone(opts, self._cwd)
