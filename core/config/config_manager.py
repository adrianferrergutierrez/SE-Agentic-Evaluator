#!/usr/bin/env python3
"""
core/config/config_manager.py
===============================
Configuration management for Evaluaitor-Lamb.

Loads and validates rubric configuration from YAML files.
Supports default config and custom overrides.
"""

from __future__ import annotations

import logging
import os
from pathlib import Path
from typing import Any, Dict, List, Optional

import yaml
from pydantic import BaseModel, Field, field_validator

logger = logging.getLogger(__name__)

DEFAULT_CONFIG_PATH = Path(__file__).parents[2] / "configs" / "rubric_default.yaml"


class CriterionConfig(BaseModel):
    """Single rubric criterion configuration."""
    id: str
    name: str
    weight: float = Field(gt=0, le=1)
    prompt: str
    description: str = ""
    requires_vision: bool = False


class ModelsConfig(BaseModel):
    """LLM model configuration (legacy Ollama)."""
    text: str = "qwen3:32b"
    vision: str = "qwen3-vl:30b"


class ProviderConfig(BaseModel):
    """Cloud provider configuration (DashScope, etc.)."""
    type: str = "dashscope"
    region: str = "singapore"
    text_model: str = os.environ.get("DASHSCOPE_MODEL", "qwen3.6-plus")
    vision_model: str = os.environ.get("DASHSCOPE_VISION_MODEL", "qwen-vl-max")


class OptionsConfig(BaseModel):
    """Processing options."""
    multimodal: bool = True
    skip_existing: bool = False
    min_text_model_size: str = "14b"
    min_vision_model_size: str = "7b"
    enable_feedback: bool = False
    detailed_scoring: bool = False


class RubricConfig(BaseModel):
    """Full rubric configuration loaded from YAML."""
    version: str = "1.0"
    id: str = "default"
    description: str = ""
    models: Optional[ModelsConfig] = None
    provider: Optional[ProviderConfig] = Field(default_factory=ProviderConfig)
    rubric: Dict[str, List[CriterionConfig]]
    options: OptionsConfig = Field(default_factory=OptionsConfig)

    @field_validator("rubric")
    @classmethod
    def weights_must_sum_to_one(cls, v: Dict[str, List[CriterionConfig]]) -> Dict[str, List[CriterionConfig]]:
        criteria = v.get("criteria", [])
        total = sum(c.weight for c in criteria)
        if not (0.99 <= total <= 1.01):
            raise ValueError(f"Rubric weights must sum to ~1.0, got {total:.4f}")
        return v

    @property
    def criteria(self) -> List[CriterionConfig]:
        return self.rubric.get("criteria", [])

    @property
    def weights(self) -> Dict[str, float]:
        return {c.id: c.weight for c in self.criteria}

    @property
    def labels(self) -> Dict[str, str]:
        return {c.id: c.name for c in self.criteria}

    @property
    def prompt_map(self) -> Dict[str, str]:
        return {c.id: c.prompt for c in self.criteria}


class ConfigManager:
    """Manages loading and validation of rubric configurations."""

    def __init__(self, config_path: Optional[str | Path] = None):
        self.config_path = Path(config_path) if config_path else DEFAULT_CONFIG_PATH
        self._config: Optional[RubricConfig] = None

    def load(self) -> RubricConfig:
        """Load and validate configuration from YAML file.

        Raises
        ------
        FileNotFoundError
            If config file does not exist.
        yaml.YAMLError
            If YAML is malformed.
        ValueError
            If validation fails (e.g., weights don't sum to 1.0).
        """
        if not self.config_path.exists():
            raise FileNotFoundError(f"Config file not found: {self.config_path}")

        with open(self.config_path, "r", encoding="utf-8") as f:
            raw = yaml.safe_load(f)

        self._config = RubricConfig(**raw)
        logger.info(
            "Loaded config '%s' (%s) with %d criteria, weights sum=%.2f",
            self._config.id,
            self._config.description,
            len(self._config.criteria),
            sum(c.weight for c in self._config.criteria),
        )
        return self._config

    @property
    def config(self) -> RubricConfig:
        if self._config is None:
            return self.load()
        return self._config

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> RubricConfig:
        """Create config directly from dict (for testing or programmatic use)."""
        return RubricConfig(**data)
