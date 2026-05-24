from typing import List, Any

from src.config import DYNAMIC_PIPELINE_CONFIGS
from .model_registry import MODEL_REGISTRY


class PipelineComposer:
    """Handles runtime lookups, component mixins, and factory instantiations."""

    @staticmethod
    def build_pipeline_by_keys(model_keys: List[str]) -> List[Any]:
        """Resolves raw string keys and instantiates runtime objects."""
        instantiated_objects = []
        for key in model_keys:
            if key not in MODEL_REGISTRY:
                raise KeyError(f"Model key '{key}' is not registered in MODEL_REGISTRY.")
            instantiated_objects.append(MODEL_REGISTRY[key]())
        return instantiated_objects

    @classmethod
    def build_named_scenario(cls, scenario_name: str, *extra_keys: str) -> List[Any]:
        """
        Builds a predefined pipeline scenario and dynamically appends
        additional model component mixins at runtime.
        """
        if scenario_name not in DYNAMIC_PIPELINE_CONFIGS:
            raise ValueError(f"Scenario configuration '{scenario_name}' does not exist.")

        # 1. Fetch the base scenario list of keys: ['advertising_efficiency', 'cogs', 'revenue', 'profit']
        compiled_keys = list(DYNAMIC_PIPELINE_CONFIGS[scenario_name])

        # 2. Append any extra mixin keys passed via *args, protecting against duplicates
        for extra_key in extra_keys:
            if extra_key not in compiled_keys:
                compiled_keys.append(extra_key)

        # 3. Pass the fully combined list straight to the instantiation engine
        return cls.build_pipeline_by_keys(compiled_keys)
