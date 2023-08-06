#!/usr/bin/python
#
# Copyright 2018-2022 Polyaxon, Inc.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#      http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import os

from typing import List, Optional, Tuple, Union

from polyaxon.auxiliaries import V1PolyaxonInitContainer
from polyaxon.containers.names import (
    INIT_ARTIFACTS_CONTAINER_PREFIX,
    generate_container_name,
)
from polyaxon.contexts import paths as ctx_paths
from polyaxon.exceptions import PolypodException
from polyaxon.k8s import k8s_schemas
from polyaxon.polypod.common import constants
from polyaxon.polypod.common.containers import patch_container
from polyaxon.polypod.common.env_vars import (
    get_connection_env_var,
    get_env_from_config_map,
    get_env_from_secret,
    get_items_from_config_map,
    get_items_from_secret,
)
from polyaxon.polypod.common.mounts import (
    get_connections_context_mount,
    get_mount_from_resource,
    get_mount_from_store,
)
from polyaxon.polypod.common.volumes import get_volume_name
from polyaxon.schemas.types import V1ArtifactsType, V1ConnectionType
from polyaxon.utils.list_utils import to_list


def get_or_create_args(path):
    return 'if [ ! -d "{path}" ]; then mkdir -m 0777 -p {path}; fi;'.format(path=path)


def cp_mount_args(path_from, path_to, is_file: bool, sync_fw: bool) -> str:
    sync_fw_flag = (
        "polyaxon initializer fswatch --path={};".format(path_to) if sync_fw else ""
    )
    if is_file:
        return "if [ -f {path_from} ]; then cp {path_from} {path_to}; {sync_fw_flag} fi;".format(
            path_from=path_from,
            path_to=path_to,
            sync_fw_flag=sync_fw_flag,
        )
    return (
        'if [ -d {path_from} ] && [ "$(ls -A {path_from})" ]; '
        "then cp -R {path_from}/* {path_to}; {sync_fw_flag} fi;".format(
            path_from=path_from,
            path_to=path_to,
            sync_fw_flag=sync_fw_flag,
        )
    )


def cp_store_args(
    backend: str,
    path_from: str,
    path_to: str,
    is_file: bool,
    check_path: bool,
    sync_fw: bool,
) -> str:
    args = []
    if is_file:
        args.append("--is-file")
    if sync_fw:
        args.append("--sync-fw")
    if check_path:
        args.append("--check-path")
    return "polyaxon initializer path --connection-kind={} --path-from={} --path-to={} {};".format(
        backend, path_from, path_to, " ".join(args)
    )


def get_volume_args(
    store: V1ConnectionType,
    mount_path: str,
    artifacts: V1ArtifactsType,
    paths: Union[List[str], List[Tuple[str, str]]],
    sync_fw: bool = False,
) -> str:
    files = []
    dirs = []
    paths = to_list(paths, check_none=True)
    if artifacts:
        files = artifacts.files or files
        dirs = artifacts.dirs or dirs
    # Default behavior is to pull all bucket
    if not files and not dirs and not paths:
        dirs = [""]
    args = []
    base_path_from = store.store_path

    def _copy():
        if isinstance(p, (list, tuple)):
            path_from = os.path.join(base_path_from, p[0])
            path_to = os.path.join(mount_path, p[1])
            _p = p[1]
        else:
            path_from = os.path.join(base_path_from, p)
            path_to = os.path.join(mount_path, p)
            _p = p

        # Create folders
        if is_file or check_path:
            # If we are initializing a file we need to create the base folder
            _p = os.path.split(_p)[0]
        base_path_to = os.path.join(mount_path, _p)
        # We need to check that the path exists first
        args.append(get_or_create_args(path=base_path_to))

        # copy to context
        if store.is_wasb:
            args.append(
                cp_store_args(
                    backend="wasb",
                    path_from=path_from,
                    path_to=path_to,
                    is_file=is_file,
                    sync_fw=sync_fw,
                    check_path=check_path,
                )
            )
        elif store.is_s3:
            args.append(
                cp_store_args(
                    backend="s3",
                    path_from=path_from,
                    path_to=path_to,
                    is_file=is_file,
                    sync_fw=sync_fw,
                    check_path=check_path,
                )
            )
        elif store.is_gcs:
            args.append(
                cp_store_args(
                    backend="gcs",
                    path_from=path_from,
                    path_to=path_to,
                    is_file=is_file,
                    sync_fw=sync_fw,
                    check_path=check_path,
                )
            )
        else:
            if check_path:
                args.append(
                    cp_store_args(
                        backend=store.kind,
                        path_from=path_from,
                        path_to=path_to,
                        is_file=is_file,
                        sync_fw=sync_fw,
                        check_path=check_path,
                    )
                )
            else:
                args.append(
                    cp_mount_args(
                        path_from=path_from,
                        path_to=path_to,
                        is_file=is_file,
                        sync_fw=sync_fw,
                    )
                )

    check_path = False
    is_file = True
    for p in files:
        _copy()

    is_file = False
    for p in dirs:
        # We need to check that the path exists first
        _copy()

    check_path = True
    for p in paths:
        _copy()

    return " ".join(args)


def get_base_store_container(
    container: Optional[k8s_schemas.V1Container],
    container_name: str,
    polyaxon_init: V1PolyaxonInitContainer,
    store: V1ConnectionType,
    env: List[k8s_schemas.V1EnvVar],
    env_from: List[k8s_schemas.V1EnvFromSource],
    volume_mounts: List[k8s_schemas.V1VolumeMount],
    args: List[str],
    command: List[str] = None,
) -> Optional[k8s_schemas.V1Container]:
    env = env or []
    env_from = env_from or []
    volume_mounts = volume_mounts or []

    # Artifact store needs to allow init the contexts as well, so the store is not required
    if not store:
        raise PolypodException("Init store container requires a store")
    secret = None
    if store.is_bucket:
        secret = store.get_secret()
        volume_mounts = volume_mounts + to_list(
            get_mount_from_resource(resource=secret), check_none=True
        )
        env = env + to_list(get_items_from_secret(secret=secret), check_none=True)
        env_from = env_from + to_list(
            get_env_from_secret(secret=secret), check_none=True
        )
        env += to_list(
            get_connection_env_var(connection=store, secret=secret), check_none=True
        )

        config_map = store.get_config_map()
        volume_mounts = volume_mounts + to_list(
            get_mount_from_resource(resource=config_map), check_none=True
        )
        env = env + to_list(
            get_items_from_config_map(config_map=config_map), check_none=True
        )
        env_from = env_from + to_list(
            get_env_from_config_map(config_map=config_map), check_none=True
        )
    else:
        volume_mounts = volume_mounts + to_list(
            get_mount_from_store(store=store), check_none=True
        )
        env += to_list(
            get_connection_env_var(connection=store, secret=secret), check_none=True
        )

    return patch_container(
        container=container,
        name=container_name,
        image=polyaxon_init.get_image(),
        image_pull_policy=polyaxon_init.image_pull_policy,
        command=command or ["/bin/sh", "-c"],
        args=args,
        env=env,
        env_from=env_from,
        resources=polyaxon_init.get_resources(),
        volume_mounts=volume_mounts,
    )


def get_store_container(
    polyaxon_init: V1PolyaxonInitContainer,
    connection: V1ConnectionType,
    artifacts: V1ArtifactsType,
    paths: Union[List[str], List[Tuple[str, str]]],
    container: Optional[k8s_schemas.V1Container] = None,
    env: List[k8s_schemas.V1EnvVar] = None,
    mount_path: str = None,
    is_default_artifacts_store: bool = False,
) -> Optional[k8s_schemas.V1Container]:
    container_name = generate_container_name(
        INIT_ARTIFACTS_CONTAINER_PREFIX, connection.name
    )
    if not container:
        container = k8s_schemas.V1Container(name=container_name)

    volume_name = (
        get_volume_name(mount_path) if mount_path else constants.VOLUME_MOUNT_ARTIFACTS
    )
    volume_mount_path = mount_path or ctx_paths.CONTEXT_MOUNT_ARTIFACTS
    volume_mounts = [
        get_connections_context_mount(name=volume_name, mount_path=volume_mount_path)
    ]
    mount_path = mount_path or (
        ctx_paths.CONTEXT_MOUNT_ARTIFACTS
        if is_default_artifacts_store
        else ctx_paths.CONTEXT_MOUNT_ARTIFACTS_FORMAT.format(connection.name)
    )

    return get_base_store_container(
        container=container,
        container_name=container_name,
        polyaxon_init=polyaxon_init,
        store=connection,
        env=env,
        env_from=[],
        volume_mounts=volume_mounts,
        args=[
            get_volume_args(
                store=connection,
                mount_path=mount_path,
                artifacts=artifacts,
                paths=paths,
            )
        ],
    )
