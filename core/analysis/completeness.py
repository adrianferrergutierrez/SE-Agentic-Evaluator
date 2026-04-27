"""
core/analysis/completeness.py
================================
Tool: analyse requirements completeness.

Uses prompt ``prompts/2_2_analisis_completitud.md`` from
Lamb-Project/SE-rubric-evaluAItor (GPL-3.0).
"""

from __future__ import annotations

from pathlib import Path
from typing import Optional

_REPO_ROOT = Path(__file__).parent.parent.parent
_PROMPT_FILE = _REPO_ROOT / "prompts" / "2_2_analisis_completitud.md"


def _load_prompt(prompt_path: Optional[Path] = None) -> str:
    path = prompt_path or _PROMPT_FILE
    if not path.is_file():
        raise FileNotFoundError(f"Prompt file not found: {path}")
    return path.read_text(encoding="utf-8")


def build_prompt(requirements_md: str, prompt_path: Optional[Path] = None) -> str:
    """Build the completeness analysis prompt.

    Parameters
    ----------
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
    return template.replace("--{REQUISITOS}--", requirements_md)


def analyze_completeness(
    requirements_md: str,
    model: str = "qwen2.5-coder:1.5b",
    ollama_url: str = "http://localhost:11434/api/chat",
    prompt_path: Optional[Path] = None,
) -> str:
    """Analyse the completeness of extracted requirements.

    Parameters
    ----------
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
        Markdown completeness report as produced by the LLM.
    """
    try:
        import requests
    except ImportError as exc:
        raise ImportError("The 'requests' package is required.") from exc

    prompt = build_prompt(requirements_md, prompt_path)
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
        raise RuntimeError("LLM returned an empty response for completeness analysis.")
    return content
