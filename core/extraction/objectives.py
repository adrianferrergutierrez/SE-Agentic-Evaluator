"""
core/extraction/objectives.py
==============================
Tool: extract project objectives from a document.

Uses prompt ``prompts/1_1_extraccion_objetivos.md`` from
Lamb-Project/SE-rubric-evaluAItor (GPL-3.0).

The tool loads the prompt template, substitutes the document content,
and invokes the configured LLM backend (Ollama by default) to produce
a structured Markdown list of objectives (OBJ-X format).
"""

from __future__ import annotations

import re
from pathlib import Path
from typing import Dict, List, Optional

# Default path to the prompt template relative to this file's repo root
_REPO_ROOT = Path(__file__).parent.parent.parent
_PROMPT_FILE = _REPO_ROOT / "prompts" / "1_1_extraccion_objetivos.md"


def _load_prompt(prompt_path: Optional[Path] = None) -> str:
    """Load the objectives extraction prompt template."""
    path = prompt_path or _PROMPT_FILE
    if not path.is_file():
        raise FileNotFoundError(f"Prompt file not found: {path}")
    return path.read_text(encoding="utf-8")


def build_prompt(document: str, prompt_path: Optional[Path] = None) -> str:
    """Build the full LLM prompt by injecting *document* into the template.

    Parameters
    ----------
    document:
        Full text content of the document to analyse.
    prompt_path:
        Optional override for the prompt template path.

    Returns
    -------
    str
        Rendered prompt ready to send to the LLM.
    """
    template = _load_prompt(prompt_path)
    return template.replace("--{DOCUMENTO}--", document)


def extract_objectives(
    document: str,
    model: str = "qwen3",
    ollama_url: str = "http://localhost:11434/api/chat",
    prompt_path: Optional[Path] = None,
) -> str:
    """Extract project objectives from *document* using a local LLM.

    Parameters
    ----------
    document:
        Full text of the requirements document (Markdown or plain text).
    model:
        Ollama model tag (text-only; no vision required for this tool).
    ollama_url:
        Ollama API endpoint.
    prompt_path:
        Optional path to an alternative prompt template.

    Returns
    -------
    str
        Markdown-formatted list of objectives (``# Objetivos del Proyecto``
        section) as produced by the LLM.

    Raises
    ------
    ImportError
        If ``requests`` is not installed.
    RuntimeError
        If the Ollama call fails.
    """
    try:
        import requests
    except ImportError as exc:
        raise ImportError("The 'requests' package is required.") from exc

    prompt = build_prompt(document, prompt_path)

    payload = {
        "model": model,
        "messages": [{"role": "user", "content": prompt}],
        "options": {"temperature": 0.0},
        "stream": False,
    }

    resp = requests.post(ollama_url, json=payload, timeout=300)
    resp.raise_for_status()
    data = resp.json()
    content = data.get("message", {}).get("content", "").strip()
    if not content:
        raise RuntimeError("LLM returned an empty response for objectives extraction.")
    return content


def parse_objective_ids(objectives_md: str) -> List[str]:
    """Extract objective IDs (e.g. ``OBJ-1``, ``OBJ-2.1``) from Markdown output.

    Parameters
    ----------
    objectives_md:
        Markdown text produced by :func:`extract_objectives`.

    Returns
    -------
    list of str
        Sorted list of unique objective IDs found in the text.
    """
    pattern = re.compile(r"\b(OBJ-\d+(?:\.\d+)*)\b", re.IGNORECASE)
    ids = {m.group(1).upper() for m in pattern.finditer(objectives_md)}
    return sorted(ids)
