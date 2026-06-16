"""
core/extraction/use_cases.py
==============================
Tool: extract use cases from a document.

Uses prompt ``prompts/1_3_extraccion_casos_de_uso.md`` from
Lamb-Project/SE-rubric-evaluAItor (GPL-3.0).
"""

from __future__ import annotations

import os
import re
from pathlib import Path
from typing import Dict, List, Optional

from core.clients.dashscope_client import DashScopeClient

_REPO_ROOT = Path(__file__).parent.parent.parent
_PROMPT_FILE = _REPO_ROOT / "prompts" / "1_3_extraccion_casos_de_uso.md"

DEFAULT_MODEL = os.environ.get("DASHSCOPE_MODEL", "qwen3.6-plus")


def _load_prompt(prompt_path: Optional[Path] = None) -> str:
    path = prompt_path or _PROMPT_FILE
    if not path.is_file():
        raise FileNotFoundError(f"Prompt file not found: {path}")
    return path.read_text(encoding="utf-8")


def build_prompt(document: str, prompt_path: Optional[Path] = None) -> str:
    """Build the full LLM prompt by injecting *document* into the template."""
    template = _load_prompt(prompt_path)
    return template.replace("--{DOCUMENTO}--", document)


def extract_use_cases(
    document: str,
    client: Optional[DashScopeClient] = None,
    model: str = DEFAULT_MODEL,
    prompt_path: Optional[Path] = None,
) -> str:
    """Extract use cases from *document* using DashScope API.

    Parameters
    ----------
    document:
        Full text of the requirements document.
    client:
        Optional DashScopeClient instance. Created automatically if None.
    model:
        DashScope model name (default: qwen3.6-plus).
    prompt_path:
        Optional alternative prompt template path.

    Returns
    -------
    str
        Markdown-formatted use-case catalogue as produced by the LLM.

    Raises
    ------
    RuntimeError
        If the DashScope call fails or returns empty content.
    """
    if client is None:
        client = DashScopeClient()

    prompt = build_prompt(document, prompt_path)
    content = client.generate(
        model=model,
        prompt=prompt,
        temperature=0.0,
        max_tokens=4096,
    )
    if not content:
        raise RuntimeError("DashScope returned an empty response for use-case extraction.")
    return content


def parse_use_case_ids(use_cases_md: str) -> List[str]:
    """Extract use-case IDs (e.g. ``CU-001``) from Markdown output.

    Parameters
    ----------
    use_cases_md:
        Markdown text produced by :func:`extract_use_cases`.

    Returns
    -------
    list of str
        Sorted list of unique use-case IDs.
    """
    pattern = re.compile(r"\b(CU-\d+)\b", re.IGNORECASE)
    ids = {m.group(1).upper() for m in pattern.finditer(use_cases_md)}
    return sorted(ids)


def parse_diagram_detected(use_cases_md: str) -> bool:
    """Return ``True`` if the LLM reported detecting diagrams in the document.

    Parameters
    ----------
    use_cases_md:
        Markdown text produced by :func:`extract_use_cases`.
    """
    pattern = re.compile(
        r"Diagramas\s+detectados\s*:\s*S[ií]", re.IGNORECASE
    )
    return bool(pattern.search(use_cases_md))
