"""
core/analysis/traceability.py
===============================
Tool: analyse traceability between objectives and requirements.

Uses prompt ``prompts/2_1_analisis_trazabilidad.md`` from
Lamb-Project/SE-rubric-evaluAItor (GPL-3.0).
"""

from __future__ import annotations

from pathlib import Path
from typing import Optional

_REPO_ROOT = Path(__file__).parent.parent.parent
_PROMPT_FILE = _REPO_ROOT / "prompts" / "2_1_analisis_trazabilidad.md"


def _load_prompt(prompt_path: Optional[Path] = None) -> str:
    path = prompt_path or _PROMPT_FILE
    if not path.is_file():
        raise FileNotFoundError(f"Prompt file not found: {path}")
    return path.read_text(encoding="utf-8")


def build_prompt(
    objectives_md: str,
    requirements_md: str,
    prompt_path: Optional[Path] = None,
) -> str:
    """Build the traceability analysis prompt.

    Parameters
    ----------
    objectives_md:
        Markdown output from ``core/extraction/objectives.py``.
    requirements_md:
        Markdown output from ``core/extraction/requirements.py``.
    prompt_path:
        Optional alternative prompt template path.

    Returns
    -------
    str
        Rendered prompt ready to send to the LLM.
    """
    template = _load_prompt(prompt_path)
    prompt = template.replace("--{OBJETIVOS}--", objectives_md)
    prompt = prompt.replace("--{REQUISITOS}--", requirements_md)
    return prompt


def analyze_traceability(
    objectives_md: str,
    requirements_md: str,
    model: str = "qwen3",
    ollama_url: str = "http://localhost:11434/api/chat",
    prompt_path: Optional[Path] = None,
) -> str:
    """Analyse traceability between objectives and requirements.

    Parameters
    ----------
    objectives_md:
        Structured objectives (Markdown) produced by the extraction tool.
    requirements_md:
        Structured requirements (Markdown) produced by the extraction tool.
    model:
        Ollama model tag.
    ollama_url:
        Ollama API endpoint.
    prompt_path:
        Optional alternative prompt template path.

    Returns
    -------
    str
        Markdown traceability report as produced by the LLM.
    """
    try:
        import requests
    except ImportError as exc:
        raise ImportError("The 'requests' package is required.") from exc

    prompt = build_prompt(objectives_md, requirements_md, prompt_path)
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
        raise RuntimeError("LLM returned an empty response for traceability analysis.")
    return content
