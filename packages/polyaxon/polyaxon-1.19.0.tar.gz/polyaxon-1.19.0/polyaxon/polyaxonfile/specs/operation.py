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

from collections.abc import Mapping
from typing import Dict

from polyaxon.exceptions import PolyaxonSchemaError
from polyaxon.polyaxonfile.specs import kinds
from polyaxon.polyaxonfile.specs.base import BaseSpecification
from polyaxon.polyflow import (
    V1IO,
    V1CompiledOperation,
    V1Component,
    V1Operation,
    V1Param,
    validate_run_patch,
)
from polyaxon.utils.list_utils import to_list


class OperationSpecification(BaseSpecification):
    """The polyaxonfile specification for operations."""

    _SPEC_KIND = kinds.OPERATION

    CONFIG = V1Operation

    @classmethod
    def compile_operation(
        cls,
        config: V1Operation,
        override: Dict = None,
        use_override_patch_strategy: bool = False,
    ) -> V1CompiledOperation:
        preset_patch_strategy = None
        if override:
            preset = OperationSpecification.read(override, is_preset=True)
            if use_override_patch_strategy and preset.patch_strategy:
                preset_patch_strategy = preset.patch_strategy

            config = config.patch(preset, preset.patch_strategy)
        # Patch run
        component = config.component  # type: V1Component
        if not component:
            raise PolyaxonSchemaError(
                "Compile operation received an invalid configuration: "
                "the component is missing. "
                "Please make sure that the polyaxonfile was correctly resolved "
                "before to calling this operation."
            )
        if config.run_patch:
            patch_strategy = (
                preset_patch_strategy
                if use_override_patch_strategy and preset_patch_strategy is not None
                else config.patch_strategy
            )
            component.run = component.run.patch(
                validate_run_patch(config.run_patch, component.run.kind),
                strategy=patch_strategy,
            )

        contexts = []

        def get_context_io(c_name: str, c_io: V1Param, is_list=None):
            if not c_io.context_only:
                return

            contexts.append(
                V1IO(
                    name=c_name,
                    to_init=c_io.to_init,
                    to_env=c_io.to_env,
                    connection=c_io.connection,
                    is_list=is_list,
                )
            )

        # Collect contexts io form params
        for p in config.params or {}:
            get_context_io(c_name=p, c_io=config.params[p])

        # Collect contexts io form joins
        for j in config.joins or []:
            for p in j.params or {}:
                get_context_io(c_name=p, c_io=j.params[p], is_list=True)

        patch_compiled = V1CompiledOperation(
            name=config.name,
            cost=config.cost,
            description=config.description,
            contexts=contexts,
            tags=config.tags,
            is_approved=config.is_approved,
            presets=config.presets,
            queue=config.queue,
            cache=config.cache,
            build=config.build,
            hooks=config.hooks,
            events=config.events,
            plugins=config.plugins,
            termination=config.termination,
            matrix=config.matrix,
            joins=config.joins,
            schedule=config.schedule,
            dependencies=config.dependencies,
            trigger=config.trigger,
            conditions=config.conditions,
            skip_on_upstream_skip=config.skip_on_upstream_skip,
        )

        values = [
            {cls.VERSION: config.version},
            component.to_dict(),
            {cls.KIND: kinds.COMPILED_OPERATION},
        ]
        compiled = V1CompiledOperation.read(values)  # type: V1CompiledOperation
        return compiled.patch(patch_compiled, strategy=config.patch_strategy)

    @classmethod
    def read(cls, values, partial: bool = False, is_preset: bool = False):
        if is_preset:
            if isinstance(values, cls.CONFIG):
                values.is_preset = True
                return values
            elif isinstance(values, Mapping):
                values[cls.IS_PRESET] = True
            else:
                values = to_list(values)
                values = [{cls.IS_PRESET: True}] + values

        return super().read(values, partial=partial or is_preset)
