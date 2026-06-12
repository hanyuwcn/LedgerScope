"""
LedgerScope Pipeline Orchestration Layer.

Handles the composition of pipelines by unifying Models and Auditors
into a singular execution registry.
"""

from .model_composer import PipelineComposer
from .model_registry import PIPELINE_REGISTRY

__all__ = ["PipelineComposer", "PIPELINE_REGISTRY"]
