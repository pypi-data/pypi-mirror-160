from typing import Union

import yaml

from bev.config import find_repo_root, CONFIG, load_config
from bev.utils import RepositoryNotFound
from tarn.config import CONFIG_NAME as STORAGE_CONFIG_NAME, root_params, StorageConfig
from tarn.utils import mkdir


def init(repository: str = '.', permissions: str = None, group: Union[int, str] = None):
    root = find_repo_root(repository)
    if root is None:
        raise RepositoryNotFound(f'{CONFIG} files not found in current folder\'s parents')

    return init_config(load_config(root / CONFIG), permissions, group)


def init_config(config, permissions, group):
    local, meta = config.local, config.meta
    if meta.hash is None:
        raise ValueError('The config\'s `meta` must contain a `hash` key')

    levels = list(local.storage) + list(local.cache)

    for level in levels:
        for location in level.locations:
            storage_root = location.root
            if not storage_root.exists():
                mkdir(storage_root, permissions, group, parents=True)

            conf_path = storage_root / STORAGE_CONFIG_NAME
            if not conf_path.exists():
                with open(conf_path, 'w') as file:
                    yaml.safe_dump(StorageConfig(hash=meta.hash).dict(exclude_defaults=True), file)


def get_root_params(levels, permissions, group):
    for level in levels:
        for entry in level.locations:
            if entry.root.exists():
                return root_params(entry.root)

    if permissions is None:
        permissions = input('Folder permissions:')
    if isinstance(permissions, str):
        permissions = int(permissions, base=8)
    assert 0 <= permissions <= 0o777
    if group is None:
        group = input('Folder group:')
    return permissions, group
