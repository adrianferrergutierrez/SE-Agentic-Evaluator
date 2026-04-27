"""
core/analysis/smart.py
========================
Helper: evaluate project objectives against the SMART criteria.

SMART stands for:
  - **S**pecific  – Is the objective well-defined and focused?
  - **M**easurable – Can achievement be measured?
  - **A**chievable – Is it realistic given context?
  - **R**elevant   – Does it align with the project/problem scope?
  - **T**ime-bound – Is there a deadline or milestone?

This module provides both a *heuristic* checker (regex/keyword-based,
no LLM required) and an LLM-based scorer for richer analysis.
"""

from __future__ import annotations

import re
from dataclasses import dataclass, field
from typing import Dict, List, Optional


# ---------------------------------------------------------------------------
# Heuristic SMART signals
# ---------------------------------------------------------------------------

# Keywords/patterns that *suggest* each dimension is addressed
_SMART_SIGNALS: Dict[str, List[str]] = {
    "specific": [
        r"\b(específico|específica|concreto|claramente|definido|define)\b",
        r"\b(specific|clearly|defined|focused)\b",
    ],
    "measurable": [
        r"\b(medir|medible|cuantificar|porcentaje|tasa|métrica|indicador)\b",
        r"\b(measure|measurable|quantify|percentage|rate|metric|indicator|kpi)\b",
        r"\d+\s*%",
        r"\b\d+\s*(veces|usuarios|documentos|horas?)\b",
    ],
    "achievable": [
        r"\b(viable|factible|alcanzable|realista|posible)\b",
        r"\b(achievable|feasible|realistic|attainable)\b",
    ],
    "relevant": [
        r"\b(relevante|alineado|acorde|contexto|necesidad)\b",
        r"\b(relevant|aligned|context|need|purpose)\b",
    ],
    "time_bound": [
        r"\b(plazo|fecha|semana|mes|año|trimestre|semestre|calendario)\b",
        r"\b(deadline|by|within|week|month|year|quarter|semester|schedule)\b",
        r"\b(al\s+final(izar)?|antes\s+de|para\s+el)\b",
    ],
}


@dataclass
class SmartScore:
    """SMART score for a single objective.

    Each dimension is ``True`` if at least one heuristic signal was found.
    """
    objective_id: str
    objective_text: str
    specific: bool = False
    measurable: bool = False
    achievable: bool = False
    relevant: bool = False
    time_bound: bool = False
    notes: List[str] = field(default_factory=list)

    @property
    def score(self) -> int:
        """Number of SMART dimensions satisfied (0–5)."""
        return sum(
            [self.specific, self.measurable, self.achievable, self.relevant, self.time_bound]
        )

    @property
    def label(self) -> str:
        if self.score >= 5:
            return "Fully SMART"
        if self.score >= 3:
            return "Partially SMART"
        return "Not SMART"

    def as_markdown(self) -> str:
        dims = {
            "S": ("Specific", self.specific),
            "M": ("Measurable", self.measurable),
            "A": ("Achievable", self.achievable),
            "R": ("Relevant", self.relevant),
            "T": ("Time-bound", self.time_bound),
        }
        checks = " | ".join(
            f"{'✅' if ok else '❌'} {letter} ({name})"
            for letter, (name, ok) in dims.items()
        )
        notes_str = ("\n  ".join(self.notes)) if self.notes else "—"
        return (
            f"**{self.objective_id}** ({self.label} – {self.score}/5)\n"
            f"  {checks}\n"
            f"  Notes: {notes_str}\n"
        )


def _check_signals(text: str, dimension: str) -> bool:
    patterns = _SMART_SIGNALS.get(dimension, [])
    for pat in patterns:
        if re.search(pat, text, re.IGNORECASE):
            return True
    return False


def evaluate_smart_heuristic(
    objective_id: str, objective_text: str
) -> SmartScore:
    """Heuristically score a single objective against SMART criteria.

    This function uses keyword/regex signals and does **not** call an LLM.
    Use it as a fast first-pass filter.

    Parameters
    ----------
    objective_id:
        Identifier such as ``"OBJ-1"`` or ``"OBJ-2.3"``.
    objective_text:
        Full description of the objective.

    Returns
    -------
    SmartScore
        Heuristic SMART evaluation result.
    """
    result = SmartScore(objective_id=objective_id, objective_text=objective_text)

    result.specific = _check_signals(objective_text, "specific")
    result.measurable = _check_signals(objective_text, "measurable")
    result.achievable = _check_signals(objective_text, "achievable")
    result.relevant = _check_signals(objective_text, "relevant")
    result.time_bound = _check_signals(objective_text, "time_bound")

    if not result.measurable:
        result.notes.append("No se detectaron métricas medibles. Añade KPIs, porcentajes u otras magnitudes cuantificables.")
    if not result.time_bound:
        result.notes.append("Sin indicadores temporales. Añade un plazo concreto o un hito de referencia.")
    if not result.specific:
        result.notes.append("El objetivo puede ser demasiado vago. Añade alcance y restricciones específicas.")

    return result


def evaluate_objectives_smart(
    objectives_text: str,
) -> List[SmartScore]:
    """Evaluate all objectives extracted from a structured Markdown block.

    Expects the format produced by ``core/extraction/objectives.py``::

        ## OBJ-1: Title
        **Descripción:** Full objective text…

    Parameters
    ----------
    objectives_text:
        Markdown produced by the objectives extraction tool.

    Returns
    -------
    list of SmartScore
        One entry per identified objective.
    """
    # Split on objective headers (## OBJ-X: ...)
    header_pattern = re.compile(
        r"^##\s+(OBJ-\d+(?:\.\d+)*):\s*(.+)", re.IGNORECASE | re.MULTILINE
    )
    desc_pattern = re.compile(r"\*\*Descripci[oó]n:\*\*\s*(.+)", re.IGNORECASE)

    headers = list(header_pattern.finditer(objectives_text))
    scores: List[SmartScore] = []

    for i, h in enumerate(headers):
        obj_id = h.group(1).upper()
        title = h.group(2).strip()
        # Extract block text until next header
        block_start = h.end()
        block_end = headers[i + 1].start() if i + 1 < len(headers) else len(objectives_text)
        block = objectives_text[block_start:block_end]

        # Try to extract description, fall back to title
        desc_match = desc_pattern.search(block)
        text_to_score = (desc_match.group(1) if desc_match else "") + " " + title

        score = evaluate_smart_heuristic(obj_id, text_to_score)
        scores.append(score)

    return scores


def smart_summary_markdown(scores: List[SmartScore]) -> str:
    """Produce a Markdown summary of SMART evaluation results.

    Parameters
    ----------
    scores:
        List of :class:`SmartScore` instances from
        :func:`evaluate_objectives_smart`.

    Returns
    -------
    str
        Formatted Markdown report.
    """
    fully = sum(1 for s in scores if s.score == 5)
    partial = sum(1 for s in scores if 1 <= s.score < 5)
    none_ = sum(1 for s in scores if s.score == 0)

    lines = [
        "# SMART Objectives Evaluation\n\n",
        f"**Total objectives evaluated:** {len(scores)}\n",
        f"- ✅ Fully SMART (5/5): {fully}\n",
        f"- ⚠️ Partially SMART (1–4/5): {partial}\n",
        f"- ❌ Not SMART (0/5): {none_}\n\n",
        "## Per-Objective Results\n\n",
    ]
    for s in scores:
        lines.append(s.as_markdown())
        lines.append("\n")
    return "".join(lines)
