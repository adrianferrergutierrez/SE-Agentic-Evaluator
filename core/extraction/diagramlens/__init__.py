# core.extraction.diagramlens – vision-based diagram description module
# Adapted from Lamb-Project/DiagramLens (GPL-3.0)
# Original: https://github.com/Lamb-Project/DiagramLens
#
# Copyright (C) Lamb-Project contributors.
# Modifications for Evaluaitor-Lamb: integrated as importable module.
# This file is part of Evaluaitor-Lamb and is distributed under GPL-3.0.

from .annotate import (
    find_image_refs_with_context,
    call_ollama,
    pre_categorize_with_context,
    load_categories_config,
    describe_diagram,
    process_markdown_document,
    DEFAULT_MODEL,
    DEFAULT_CATEGORIES_PATH,
)

__all__ = [
    "find_image_refs_with_context",
    "call_ollama",
    "pre_categorize_with_context",
    "load_categories_config",
    "describe_diagram",
    "process_markdown_document",
    "DEFAULT_MODEL",
    "DEFAULT_CATEGORIES_PATH",
]
