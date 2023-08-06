import os
import socket
from itertools import chain
from pathlib import Path

from tarn import StorageLevel

from .base import StorageCluster
from .hostname import StrHostName
from ..utils import PathLike

CONFIG = '.bev.yml'


def identity(x):
    return x


def wrap_levels(levels, cls, order=identity, **kwargs):
    return tuple(
        StorageLevel(
            order([cls(location.root, **kwargs) for location in level.locations]),
            write=level.write, replicate=level.replicate, name=level.name,
        )
        for level in _filter_levels(levels)
    )


def _filter_levels(levels):
    for level in levels:
        locations = [
            x for x in level.locations
            if not x.optional or x.root.exists()
        ]
        if locations:
            level = level.copy()
            level.locations = locations
            yield level


def choose_local(metas, func, default):
    for meta in metas:
        if func(meta):
            return meta.name

    return default


def default_choose(meta: StorageCluster):
    repo_key = 'BEV__REPOSITORY'
    if repo_key in os.environ:
        return meta.name == os.environ[repo_key]

    node = socket.gethostname()
    hosts = meta.hostname or [StrHostName(meta.name)]
    return any(h.match(node) for h in hosts)


def _find_root(path, marker):
    path = Path(path).resolve()
    for parent in chain([path], path.parents):
        if (parent / marker).exists():
            return parent


def find_repo_root(path: PathLike):
    return _find_root(path, CONFIG)


def find_vcs_root(path: PathLike):
    return _find_root(path, '.git')
