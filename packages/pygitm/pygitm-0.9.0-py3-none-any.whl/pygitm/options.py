from dataclasses import dataclass
from typing import List

import pytcm


@dataclass
class CloneOptions:
    COMMAND = pytcm.Positional("clone")

    repository: str
    directory: str = ...
    branch: str = ...
    verbose: bool = ...
    quiet: bool = ...
    single_branch: bool = ...
    depth: int = ...

    def to_list(self) -> List[pytcm.Option]:
        return [
            self.COMMAND,
            pytcm.Implicit("--branch", self.branch),
            pytcm.Implicit("--depth", self.depth),
            pytcm.Flag("--verbose", self.verbose),
            pytcm.Flag("--quiet", self.quiet),
            pytcm.Flag("--single-branch", self.single_branch),
            pytcm.Positional(self.repository),
            pytcm.Positional(self.directory),
        ]


@dataclass
class AddOptions:
    COMMAND = pytcm.Positional("add")

    verbose: bool = ...
    pathspec: List[str] = ...

    def to_list(self) -> List[pytcm.Option]:
        pathspec = []
        if self.pathspec is not ...:
            pathspec = [pytcm.Positional(p) for p in self.pathspec]

        opts = [self.COMMAND, self.verbose]
        opts.extend(pathspec)

        return opts


@dataclass
class PushOptions:
    COMMAND = pytcm.Positional("push")

    all_branches: bool = ...
    tags: bool = ...
    force: bool = ...
    delete: bool = ...
    verbose: bool = ...
    set_upstream: bool = ...
    repository: str = ...
    refspec: str = ...

    def to_list(self) -> List[pytcm.Option]:
        return [
            self.COMMAND,
            pytcm.Flag("--all", self.all_branches),
            pytcm.Flag("--tags", self.tags),
            pytcm.Flag("--force", self.force),
            pytcm.Flag("--delete", self.delete),
            pytcm.Flag("--verbose", self.verbose),
            pytcm.Flag("--set-upstream", self.set_upstream),
            pytcm.Positional(self.repository),
            pytcm.Positional(self.refspec),
        ]


@dataclass
class PullOptions:
    COMMAND = pytcm.Positional("pull")

    all_remotes: bool = ...
    unshallow: bool = ...
    update_shallow: bool = ...
    tags: bool = ...
    verbose: bool = ...
    quiet: bool = ...
    repository: str = ...
    refspec: str = ...

    def to_list(self) -> List[pytcm.Option]:
        return [
            self.COMMAND,
            pytcm.Flag("--all", self.all_remotes),
            pytcm.Flag("--unshallow", self.unshallow),
            pytcm.Flag("--update-shallow", self.update_shallow),
            pytcm.Flag("--tags", self.tags),
            pytcm.Flag("--verbose", self.verbose),
            pytcm.Flag("--quiet", self.quiet),
            pytcm.Positional(self.repository),
            pytcm.Positional(self.refspec),
        ]


@dataclass
class CheckoutOptions:
    COMMAND = pytcm.Positional("checkout")

    branch: str
    ref_branch: str = ...
    quiet: bool = ...
    force: bool = ...
    new_branch: bool = ...

    def to_list(self) -> List[pytcm.Option]:
        return [
            self.COMMAND,
            pytcm.Flag("--quiet", self.quiet),
            pytcm.Flag("--force", self.force),
            pytcm.Flag("-b", self.new_branch),
            pytcm.Positional(self.ref_branch),
            pytcm.Positional(self.branch),
        ]


@dataclass
class CommitOptions:
    COMMAND = pytcm.Positional("commit")

    message: str
    all_files: bool = ...
    allow_empty_message: bool = ...
    file_message: str = ...
    commit: str = ...

    def to_list(self) -> List[pytcm.Option]:
        return [
            self.COMMAND,
            pytcm.Flag("--all", self.all_files),
            pytcm.Flag("--allow-empty-message", self.allow_empty_message),
            pytcm.Implicit("-m", self.message),
            pytcm.Implicit("-F", self.file_message),
            pytcm.Positional(self.commit),
        ]
