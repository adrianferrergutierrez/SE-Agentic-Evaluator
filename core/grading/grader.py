#!/usr/bin/env python3
"""
core/grading/grader.py
========================
Deterministic grading utilities.

Objetivo:
  Evitar errores por alucinación en agregaciones numéricas.  El agente
  **nunca** debe calcular la nota final directamente; en su lugar debe
  delegar en este módulo.

Funciones principales
---------------------
- ``mean(values)``                  – media aritmética de una lista de notas.
- ``weighted_score(items)``         – nota final ponderada.
- ``ScoreExtractor``                – extrae puntuaciones de texto Markdown.
- ``RubricGrader``                  – aplica la rúbrica por defecto del proyecto.

Uso CLI
-------
  python core/grading/grader.py --scores 7 8.5 9
  python core/grading/grader.py --criteria-json criteria.json
  python core/grading/grader.py --eval-md 3_1_eval.md:objetivos 3_4_eval.md:casos_uso

Salida
------
  JSON por stdout con ``mean_xbar`` y/o ``weighted_final``.

Lógica migrada de:
  Lamb-Project/SE-rubric-evaluAItor utils/report_generator.py
  Lamb-Project/SE-rubric-evaluAItor utils/text_parser.py
  (GPL-3.0)
"""

from __future__ import annotations

import argparse
import json
import logging
import re
from dataclasses import dataclass, field
from datetime import datetime
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple

logger = logging.getLogger(__name__)


# ---------------------------------------------------------------------------
# Core math (pure functions)
# ---------------------------------------------------------------------------

def mean(values: List[float]) -> float:
    """Return the arithmetic mean of *values*.

    Parameters
    ----------
    values:
        Non-empty list of numeric scores.

    Raises
    ------
    ValueError
        If *values* is empty.
    """
    if not values:
        raise ValueError("No scores provided")
    return sum(values) / len(values)


def weighted_score(items: List[Dict[str, Any]]) -> float:
    """Return a weighted average score.

    Parameters
    ----------
    items:
        List of dicts, each with keys ``"name"`` (str), ``"score"``
        (float) and ``"weight"`` (float).  Weights are normalised
        internally so they can sum to 1.0 *or* 100.

    Raises
    ------
    ValueError
        If *items* is empty or total weight is zero.
    """
    if not items:
        raise ValueError("No criteria items provided")

    total_w = sum(float(i["weight"]) for i in items)
    if total_w <= 0:
        raise ValueError("Total weight must be > 0")

    return sum(float(i["score"]) * (float(i["weight"]) / total_w) for i in items)


# ---------------------------------------------------------------------------
# Score extraction from Markdown
# Migrated from Lamb-Project/SE-rubric-evaluAItor utils/text_parser.py (GPL-3.0)
# ---------------------------------------------------------------------------

class ScoreExtractor:
    """Extract numeric scores from LLM-generated Markdown evaluation text.

    Tries a cascade of increasingly loose regex patterns to locate
    ``X/10`` style scores in evaluation outputs.
    """

    # Characters from the end of the text to examine in the fallback heuristic.
    # Decimal numbers near the end of an evaluation are more likely to be the
    # final score than inline counts or step numbers.
    FALLBACK_TAIL_SIZE: int = 200

    # Ordered list of patterns – most specific first
    _PATTERNS: List[str] = [
        r"Puntuaci[oó]n Total:\s*(\d+\.?\d*)/10",
        r"Puntuaci[oó]n Total:\s*(\d+\.?\d*)\s*/\s*10",
        r"Puntuaci[oó]n:\s*(\d+\.?\d*)/10",
        r"Puntuaci[oó]n:\s*(\d+\.?\d*)\s*/\s*10",
        r"Nota:\s*(\d+\.?\d*)/10",
        r"Nota:\s*(\d+\.?\d*)\s*/\s*10",
        r"Calificaci[oó]n:\s*(\d+\.?\d*)/10",
        r"Total:\s*(\d+\.?\d*)/10",
        r"(?:Puntuaci[oó]n|Nota|Calificaci[oó]n|Total)(?:\s+(?:Final|Total))?:\s*(\d+\.?\d*)\s*/\s*10",
        r"(\d+\.?\d*)\s*/\s*10\s*puntos?",
        r"(\d+\.?\d*)\s*/\s*10\s*(?:sobre|de)\s*10",
        r"(\d+\.?\d*)\s*/\s*10\s*$",
        r"^\s*\|\s*.*?\|\s*(\d+\.?\d*)/10\s*\|",
        r"^\s*-\s*.*?(\d+\.?\d*)/10",
        r"(\d+\.?\d*)/10",
        r"\*\*Puntuaci[oó]n Total:\*\*\s*(\d+\.?\d*)/10",
    ]

    def extract(self, text: str, criterion: str = "unknown") -> Optional[str]:
        """Try to extract a score string from *text*.

        Parameters
        ----------
        text:
            Raw Markdown evaluation text.
        criterion:
            Human-readable criterion name used only for log messages.

        Returns
        -------
        str | None
            Score string (e.g. ``"7.5"``) or ``None`` if not found.
        """
        for i, pattern in enumerate(self._PATTERNS):
            try:
                match = re.search(pattern, text, re.MULTILINE | re.IGNORECASE)
                if match:
                    value = match.group(1).strip()
                    if value:
                        logger.debug("Score for %s extracted with pattern %d: %s", criterion, i + 1, value)
                        return value
            except Exception as exc:
                logger.debug("Pattern %d error for %s: %s", i + 1, criterion, exc)

        return self._fallback(text, criterion)

    def _fallback(self, text: str, criterion: str) -> Optional[str]:
        """Last-resort: find any number in [0, 10] range.

        Preference order:
        1. Decimal numbers (e.g. ``8.5``) in the last 200 characters of
           *text* – most likely to be a final score rather than a count.
        2. Any number in [0, 10] from the full text (least specific).
        """
        # Prefer decimal numbers near the end of the evaluation text.
        tail = text[-self.FALLBACK_TAIL_SIZE:] if len(text) > self.FALLBACK_TAIL_SIZE else text
        decimal_in_range = [
            n for n in re.findall(r"\b(\d+\.\d+)\b", tail)
            if 0.0 <= float(n) <= 10.0
        ]
        if decimal_in_range:
            result = decimal_in_range[-1]
            logger.warning(
                "Fallback score extraction for %s (decimal near end of text): %s "
                "– verify this is the intended score",
                criterion, result,
            )
            return result

        # Fall back to any number in valid range.
        numbers = re.findall(r"\b(\d+\.?\d*)\b", text)
        candidates = [n for n in numbers if 0.0 <= float(n) <= 10.0]
        if candidates:
            result = candidates[-1]
            logger.warning(
                "Fallback score extraction for %s (any number in [0,10]): %s "
                "– verify this is the intended score and not a count or step number",
                criterion, result,
            )
            return result
        logger.warning("Could not extract score for %s", criterion)
        return None

    def to_float(self, value: Optional[str], criterion: str = "unknown") -> float:
        """Convert a score string to float, clamped to [0, 10].

        Parameters
        ----------
        value:
            String score (may be ``None``).
        criterion:
            Used for log messages.

        Returns
        -------
        float
            Parsed score, clamped to ``[0.0, 10.0]``.  Returns ``0.0``
            if *value* is ``None`` or cannot be parsed.
        """
        if not value:
            logger.warning("No score found for %s – defaulting to 0.0", criterion)
            return 0.0
        try:
            result = float(value)
            if not (0.0 <= result <= 10.0):
                logger.warning("Score out of range for %s: %s – clamping", criterion, result)
                return max(0.0, min(10.0, result))
            return result
        except (ValueError, TypeError) as exc:
            logger.error("Cannot convert score for %s: %r – %s", criterion, value, exc)
            return 0.0

    def extract_all(self, eval_results: Dict[str, str]) -> Dict[str, float]:
        """Extract scores from a mapping of criterion → evaluation Markdown.

        Parameters
        ----------
        eval_results:
            ``{ "criterion_key": "markdown_text", … }``

        Returns
        -------
        dict
            ``{ "criterion_key": float_score, … }``
        """
        scores: Dict[str, float] = {}
        for criterion, text in eval_results.items():
            raw = self.extract(text, criterion)
            scores[criterion] = self.to_float(raw, criterion)
        return scores


# ---------------------------------------------------------------------------
# Rubric grader
# Migrated from Lamb-Project/SE-rubric-evaluAItor utils/report_generator.py (GPL-3.0)
# ---------------------------------------------------------------------------

# Default rubric weights (must sum to 1.0)
DEFAULT_WEIGHTS: Dict[str, float] = {
    "objetivos": 0.20,
    "requisitos_info": 0.15,
    "requisitos_nf": 0.10,
    "casos_uso": 0.35,
    "matrices": 0.20,
}

DEFAULT_CRITERION_LABELS: Dict[str, str] = {
    "objetivos": "Objetivos",
    "requisitos_info": "Requisitos de Información",
    "requisitos_nf": "Requisitos No Funcionales",
    "casos_uso": "Casos de Uso",
    "matrices": "Matrices de Trazabilidad",
}


@dataclass
class GradingResult:
    """Result of :meth:`RubricGrader.grade`.

    Attributes
    ----------
    scores:
        Per-criterion raw scores (0–10).
    weights:
        Per-criterion weights (normalised to 1.0).
    weighted_final:
        Weighted final grade (0–10).
    mean_xbar:
        Simple arithmetic mean of the raw scores.
    performance_level:
        Human-readable performance label.
    """
    scores: Dict[str, float]
    weights: Dict[str, float]
    weighted_final: float
    mean_xbar: float
    performance_level: str = ""
    evaluated_file: str = ""
    evaluated_at: str = field(default_factory=lambda: datetime.now().isoformat())

    def as_dict(self) -> Dict[str, Any]:
        return {
            "evaluated_file": self.evaluated_file,
            "evaluated_at": self.evaluated_at,
            "scores": self.scores,
            "weights": self.weights,
            "mean_xbar": round(self.mean_xbar, 4),
            "weighted_final": round(self.weighted_final, 2),
            "performance_level": self.performance_level,
        }

    def rubric_table_markdown(self) -> str:
        """Render a Markdown rubric table."""
        rows = []
        for key, label in DEFAULT_CRITERION_LABELS.items():
            if key not in self.scores:
                continue
            score = self.scores[key]
            weight = self.weights.get(key, 0.0)
            rows.append(
                f"| **{label}** | {weight * 100:.0f}% | "
                f"{score:.1f}/10 | {score * weight:.2f} |"
            )
        rows.append(
            f"| **TOTAL** | **100%** | | **{self.weighted_final:.2f}/10** |"
        )
        header = (
            "| Criterio | Peso | Puntuación | Nota Ponderada |\n"
            "|----------|------|------------|----------------|\n"
        )
        return header + "\n".join(rows)


class RubricGrader:
    """High-level rubric grader.

    Wraps :class:`ScoreExtractor` and :func:`weighted_score` to provide
    a single :meth:`grade` method that the agent can call after collecting
    all evaluation Markdown texts.

    Parameters
    ----------
    weights:
        Criterion weights (normalised internally).  Defaults to
        :data:`DEFAULT_WEIGHTS`.
    evaluated_file:
        Optional name of the evaluated document (for reports).
    """

    def __init__(
        self,
        weights: Optional[Dict[str, float]] = None,
        evaluated_file: str = "",
    ) -> None:
        self.weights = weights or dict(DEFAULT_WEIGHTS)
        self.evaluated_file = evaluated_file
        self._extractor = ScoreExtractor()

    def grade(
        self,
        eval_results: Dict[str, str],
        scores: Optional[Dict[str, float]] = None,
    ) -> GradingResult:
        """Compute the final grade from evaluation texts or explicit scores.

        Parameters
        ----------
        eval_results:
            Mapping of ``criterion_key → evaluation_markdown``.  Scores
            are extracted automatically.  Pass an empty dict if you
            supply *scores* directly.
        scores:
            Optional explicit per-criterion scores (override extraction).

        Returns
        -------
        GradingResult
        """
        extracted = self._extractor.extract_all(eval_results) if eval_results else {}
        if scores:
            extracted.update(scores)

        # Build weighted items
        items = [
            {"name": k, "score": extracted.get(k, 0.0), "weight": w}
            for k, w in self.weights.items()
        ]
        wfinal = weighted_score(items)
        all_scores = [extracted.get(k, 0.0) for k in self.weights]
        xbar = mean(all_scores) if all_scores else 0.0

        level = self._performance_level(wfinal)

        return GradingResult(
            scores=extracted,
            weights=self.weights,
            weighted_final=round(wfinal, 2),
            mean_xbar=round(xbar, 4),
            performance_level=level,
            evaluated_file=self.evaluated_file,
        )

    @staticmethod
    def _performance_level(grade: float) -> str:
        if grade >= 9.0:
            return "Excelente"
        if grade >= 7.0:
            return "Bueno"
        if grade >= 5.0:
            return "Aceptable"
        return "Insuficiente"


# ---------------------------------------------------------------------------
# CLI
# ---------------------------------------------------------------------------

def main() -> None:
    """Command-line interface for the deterministic grader."""
    parser = argparse.ArgumentParser(
        description="Deterministic grader for SE-Agentic-Evaluator."
    )
    parser.add_argument(
        "--scores", nargs="*", type=float,
        help="Raw scores to average (e.g. --scores 7 8.5 9)",
    )
    parser.add_argument(
        "--criteria-json", type=str,
        help="Path to a JSON file with {criteria: [{name, score, weight}]}",
    )
    parser.add_argument(
        "--eval-md", nargs="*",
        help=(
            "One or more FILEPATH:CRITERION pairs pointing to evaluation "
            "Markdown files (e.g. eval_obj.md:objetivos eval_cu.md:casos_uso)"
        ),
    )
    args = parser.parse_args()

    result: Dict[str, Any] = {}

    if args.scores is not None and len(args.scores) > 0:
        result["mean_xbar"] = round(mean(args.scores), 4)

    if args.criteria_json:
        with open(args.criteria_json, "r", encoding="utf-8") as f:
            payload = json.load(f)
        items = payload.get("criteria", [])
        result["weighted_final"] = round(weighted_score(items), 2)

    if args.eval_md:
        grader = RubricGrader()
        eval_results: Dict[str, str] = {}
        for pair in args.eval_md:
            if ":" not in pair:
                raise SystemExit(f"Expected FILEPATH:CRITERION but got: {pair!r}")
            filepath, criterion = pair.rsplit(":", 1)
            eval_results[criterion] = Path(filepath).read_text(encoding="utf-8")
        grading = grader.grade(eval_results)
        result.update(grading.as_dict())

    if not result:
        raise SystemExit("Provide --scores, --criteria-json, or --eval-md")

    print(json.dumps(result, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
