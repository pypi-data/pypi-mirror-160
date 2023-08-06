# -*- coding: utf-8 -*-


import pytcm

from pygitm.git import add, checkout, commit, pull, push
from pygitm.options import (
    AddOptions,
    CheckoutOptions,
    CommitOptions,
    PullOptions,
    PushOptions,
)


class Workspace:
    def __init__(self, cwd: str) -> None:
        self._cwd = cwd

    def add(self, opts: AddOptions) -> pytcm.CommandResult:
        add(opts, self._cwd)

    def push(self, opts: PushOptions) -> pytcm.CommandResult:
        push(opts, self._cwd)

    def pull(self, opts: PullOptions) -> pytcm.CommandResult:
        pull(opts, self._cwd)

    def checkout(self, opts: CheckoutOptions) -> pytcm.CommandResult:
        checkout(opts, self._cwd)

    def commit(self, opts: CommitOptions) -> pytcm.CommandResult:
        commit(opts, self._cwd)
