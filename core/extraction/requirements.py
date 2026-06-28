"""
core/extraction/requirements.py
=================================
Tool: extract information requirements (IRQ) and non-functional
requirements (NFR) from a document.

Uses prompt ``prompts/1_2_extraccion_requisitos.md`` from
Lamb-Project/SE-rubric-evaluAItor (GPL-3.0).
"""

from __future__ import annotations

import os
import re
from pathlib import Path
from typing import Dict, List, Optional

from core.clients.base import BaseLLMClient
from core.clients import get_client

_REPO_ROOT = Path(__file__).parent.parent.parent
_PROMPT_FILE = _REPO_ROOT / "prompts" / "1_2_extraccion_requisitos.md"

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


def extract_requirements(
    document: str,
    client: Optional[BaseLLMClient] = None,
    model: str = DEFAULT_MODEL,
    prompt_path: Optional[Path] = None,
) -> str:
    """Extract structured requirements (IRQ + NFR) from *document*.

    Parameters
    ----------
    document:
        Full text of the requirements document.
    client:
        Optional BaseLLMClient instance. Created automatically if None.
    model:
        DashScope model name (default: qwen3.6-plus).
    prompt_path:
        Optional alternative prompt template path.

    Returns
    -------
    str
        Markdown-formatted requirements list as produced by the LLM.

    Raises
    ------
    RuntimeError
        If the DashScope call fails or returns empty content.
    """
    if client is None:
        client = get_client()

    prompt = build_prompt(document, prompt_path)
    content = client.generate(
        model=model,
        prompt=prompt,
        temperature=0.0,
        max_tokens=4096,
    )
    if not content:
        raise RuntimeError("DashScope returned an empty response for requirements extraction.")
    return content


def parse_requirement_ids(requirements_md: str) -> Dict[str, List[str]]:
    """Extract requirement IDs from Markdown output.

    Parameters
    ----------
    requirements_md:
        Markdown text produced by :func:`extract_requirements`.

    Returns
    -------
    dict
        ``{"IRQ": [...], "NFR": [...]}`` with sorted unique IDs.
    """
    irq_pattern = re.compile(r"\b(IRQ-\d+)\b", re.IGNORECASE)
    nfr_pattern = re.compile(r"\b(NFR-\d+)\b", re.IGNORECASE)

    irqs = sorted({m.group(1).upper() for m in irq_pattern.finditer(requirements_md)})
    nfrs = sorted({m.group(1).upper() for m in nfr_pattern.finditer(requirements_md)})
    return {"IRQ": irqs, "NFR": nfrs}


def parse_objective_associations(requirements_md: str) -> Dict[str, List[str]]:
    """Parse which objectives each requirement is associated with.

    Looks for lines like ``- **Objetivos asociados:** OBJ-1, OBJ-2`` in
    the Markdown output from :func:`extract_requirements`.

    Parameters
    ----------
    requirements_md:
        Markdown text produced by :func:`extract_requirements`.

    Returns
    -------
    dict
        Mapping ``{ "IRQ-1": ["OBJ-1", "OBJ-2"], "NFR-3": ["OBJ-4"], … }``.
    """
    associations: Dict[str, List[str]] = {}

    # Find requirement blocks and their objective associations
    req_block_pattern = re.compile(
        r"###\s+((?:IRQ|NFR)-\d+)[^\n]*\n(.*?)(?=###|\Z)", re.DOTALL | re.IGNORECASE
    )
    obj_line_pattern = re.compile(
        r"(?:Objetivos?\s+asociados?):\s*(OBJ-\d+(?:\.\d+)?(?:,\s*OBJ-\d+(?:\.\d+)?)*)",
        re.IGNORECASE,
    )

    for block_match in req_block_pattern.finditer(requirements_md):
        req_id = block_match.group(1).upper()
        block_text = block_match.group(2)
        obj_match = obj_line_pattern.search(block_text)
        if obj_match:
            raw = obj_match.group(1)
            objs = [o.strip().upper() for o in raw.split(",") if o.strip()]
            associations[req_id] = objs
        else:
            associations[req_id] = []

    return associations
