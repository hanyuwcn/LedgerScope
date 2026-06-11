import copy
from typing import List, Any

from src.config import DYNAMIC_PIPELINE_CONFIGS, messages
from .model_registry import PIPELINE_REGISTRY


class PipelineComposer:
    """Handles runtime lookups, component mixins, and factory instantiations."""

    @staticmethod
    def build_pipeline_by_keys(models: List[str]) -> List[Any]:
        """Resolves raw string keys and instantiates runtime objects."""
        pipeline = []
        for model_name in models:
            if model_name not in PIPELINE_REGISTRY:
                raise KeyError(messages.ERROR_PIPELINE_MODEL_NOT_REGISTERED.format(model=model_name))
            pipeline.append(PIPELINE_REGISTRY[model_name]())
        return pipeline

    @classmethod
    def build_named_scenario(cls, scenario_name: str, *extra_keys: str) -> List[Any]:
        """
        Builds a predefined pipeline scenario and dynamically appends
        additional model component mixins at runtime.
        """
        if scenario_name not in DYNAMIC_PIPELINE_CONFIGS:
            raise ValueError(messages.ERROR_PIPELINE_SCENARIO_DOES_NOT_EXIST.format(scenario=scenario_name))

        # Fetch the base scenario list of keys defensively using deepcopy
        compiled_keys = copy.deepcopy(list(DYNAMIC_PIPELINE_CONFIGS[scenario_name]))

        # Append any extra mixin keys passed via *args, protecting against duplicates
        for extra_key in extra_keys:
            if extra_key not in compiled_keys:
                compiled_keys.append(extra_key)

        return cls.build_pipeline_by_keys(compiled_keys)

    @classmethod
    def build_merged_scenarios(cls, scenarios: list[str]) -> list[Any]:
        """
        Merges multiple scenario configurations into a single unique pipeline.
        """
        merged_keys = []
        for scenario_name in scenarios:
            if scenario_name not in DYNAMIC_PIPELINE_CONFIGS:
                raise ValueError(messages.ERROR_PIPELINE_SCENARIO_DOES_NOT_EXIST.format(scenario=scenario_name))

            # Append new keys if they aren't already in the list
            for key in DYNAMIC_PIPELINE_CONFIGS[scenario_name]:
                if key not in merged_keys:
                    merged_keys.append(key)

        return cls.build_pipeline_by_keys(merged_keys)
