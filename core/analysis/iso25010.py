"""
core/analysis/iso25010.py
===========================
Helper: classify and evaluate Non-Functional Requirements (NFR) against
the ISO/IEC 25010:2011 quality characteristics.

ISO/IEC 25010 defines eight top-level quality characteristics:
  1. Functional Suitability
  2. Performance Efficiency
  3. Compatibility
  4. Usability
  5. Reliability
  6. Security
  7. Maintainability
  8. Portability

This module maps NFR text to these categories heuristically (keyword-based,
no LLM required) and produces coverage reports.
"""

from __future__ import annotations

import re
from dataclasses import dataclass, field
from typing import Dict, List, Optional, Set


# ---------------------------------------------------------------------------
# ISO/IEC 25010 characteristic definitions and keyword signals
# ---------------------------------------------------------------------------

ISO_CHARACTERISTICS: Dict[str, Dict] = {
    "functional_suitability": {
        "label": "Functional Suitability",
        "sub": ["functional_completeness", "functional_correctness", "functional_appropriateness"],
        "keywords": [
            r"\b(funcional|completitud|funcionalidad|correctitud|exactitud|apropiado)\b",
            r"\b(functional|completeness|correctness|appropriateness|capability)\b",
        ],
    },
    "performance_efficiency": {
        "label": "Performance Efficiency",
        "sub": ["time_behaviour", "resource_utilisation", "capacity"],
        "keywords": [
            r"\b(rendimiento|tiempo\s+de\s+respuesta|throughput|latencia|capacidad|recursos)\b",
            r"\b(performance|response\s+time|throughput|latency|capacity|resource|speed)\b",
            r"\b\d+\s*(ms|segundos?|seconds?|milisegundos?)\b",
        ],
    },
    "compatibility": {
        "label": "Compatibility",
        "sub": ["co_existence", "interoperability"],
        "keywords": [
            r"\b(compatible|interoperabilidad|integraci[oó]n|coexistencia)\b",
            r"\b(compatibility|interoperability|integration|co-existence)\b",
        ],
    },
    "usability": {
        "label": "Usability",
        "sub": ["appropriateness_recognisability", "learnability", "operability",
                "user_error_protection", "user_interface_aesthetics", "accessibility"],
        "keywords": [
            r"\b(usabilidad|facilidad\s+de\s+uso|accesibilidad|aprendizaje|interfaz)\b",
            r"\b(usability|ease\s+of\s+use|accessibility|learnability|user\s+interface|ui)\b",
        ],
    },
    "reliability": {
        "label": "Reliability",
        "sub": ["maturity", "availability", "fault_tolerance", "recoverability"],
        "keywords": [
            r"\b(disponibilidad|fiabilidad|tolerancia\s+a\s+fallos|recuperaci[oó]n|uptime)\b",
            r"\b(availability|reliability|fault\s+tolerance|recovery|uptime|mtbf)\b",
            r"\b\d+\s*%\s*(uptime|disponibilidad|availability)\b",
        ],
    },
    "security": {
        "label": "Security",
        "sub": ["confidentiality", "integrity", "non_repudiation", "accountability", "authenticity"],
        "keywords": [
            r"\b(seguridad|autenticaci[oó]n|autorizaci[oó]n|cifrado|encriptaci[oó]n|RGPD|GDPR|privacidad)\b",
            r"\b(security|authentication|authorization|encryption|privacy|confidentiality|audit)\b",
        ],
    },
    "maintainability": {
        "label": "Maintainability",
        "sub": ["modularity", "reusability", "analysability", "modifiability", "testability"],
        "keywords": [
            r"\b(mantenibilidad|modularidad|reutilizaci[oó]n|testabilidad|modificabilidad)\b",
            r"\b(maintainability|modularity|reusability|testability|modifiability)\b",
        ],
    },
    "portability": {
        "label": "Portability",
        "sub": ["adaptability", "installability", "replaceability"],
        "keywords": [
            r"\b(portabilidad|instalabilidad|adaptabilidad|multiplataforma|cross-platform)\b",
            r"\b(portability|installability|adaptability|multi-platform|cross-platform)\b",
        ],
    },
}


def classify_nfr(nfr_text: str) -> List[str]:
    """Classify an NFR description against ISO/IEC 25010 characteristics.

    Parameters
    ----------
    nfr_text:
        Full description of the NFR.

    Returns
    -------
    list of str
        Matched characteristic keys (may be empty if none match).
    """
    matched: List[str] = []
    for key, info in ISO_CHARACTERISTICS.items():
        for pattern in info["keywords"]:
            if re.search(pattern, nfr_text, re.IGNORECASE):
                matched.append(key)
                break
    return matched


# ---------------------------------------------------------------------------
# Public data classes
# ---------------------------------------------------------------------------

@dataclass
class NfrClassification:
    """ISO/IEC 25010 classification for a single NFR."""
    nfr_id: str
    nfr_text: str
    characteristics: List[str] = field(default_factory=list)
    unclassified: bool = False

    @property
    def labels(self) -> List[str]:
        return [ISO_CHARACTERISTICS[c]["label"] for c in self.characteristics]

    def as_markdown(self) -> str:
        if self.unclassified:
            return (
                f"- ⚠️ **{self.nfr_id}**: *Unclassified* – "
                "no ISO/IEC 25010 characteristic matched. "
                "Consider adding measurable quality attributes.\n"
            )
        labels_str = ", ".join(self.labels)
        return f"- ✅ **{self.nfr_id}**: {labels_str}\n"


@dataclass
class Iso25010Report:
    """Coverage report across all analysed NFRs."""
    classifications: List[NfrClassification] = field(default_factory=list)

    @property
    def coverage(self) -> Dict[str, int]:
        """Return count of NFRs per ISO characteristic."""
        counts: Dict[str, int] = {k: 0 for k in ISO_CHARACTERISTICS}
        for clf in self.classifications:
            for char in clf.characteristics:
                counts[char] += 1
        return counts

    @property
    def uncovered_characteristics(self) -> List[str]:
        """ISO characteristics with zero NFR coverage."""
        return [k for k, count in self.coverage.items() if count == 0]

    def as_markdown(self) -> str:
        lines = ["# ISO/IEC 25010 NFR Classification Report\n\n"]
        lines.append(f"**Total NFRs analysed:** {len(self.classifications)}\n")
        unclassified = sum(1 for c in self.classifications if c.unclassified)
        lines.append(f"**Unclassified NFRs:** {unclassified}\n\n")

        lines.append("## Per-NFR Classification\n\n")
        for clf in self.classifications:
            lines.append(clf.as_markdown())

        lines.append("\n## Coverage by ISO/IEC 25010 Characteristic\n\n")
        lines.append("| Characteristic | NFRs Covering It |\n")
        lines.append("|---|---|\n")
        for key, count in self.coverage.items():
            label = ISO_CHARACTERISTICS[key]["label"]
            status = "✅" if count > 0 else "❌"
            lines.append(f"| {status} {label} | {count} |\n")

        if self.uncovered_characteristics:
            lines.append("\n## ⚠️ Uncovered Characteristics\n\n")
            lines.append(
                "The following ISO/IEC 25010 characteristics have **no** associated NFR "
                "and should be considered:\n\n"
            )
            for key in self.uncovered_characteristics:
                info = ISO_CHARACTERISTICS[key]
                lines.append(f"- **{info['label']}** (sub-characteristics: "
                              f"{', '.join(info['sub'])})\n")
        else:
            lines.append("\n✅ All ISO/IEC 25010 characteristics are covered.\n")

        return "".join(lines)


# ---------------------------------------------------------------------------
# Main public function
# ---------------------------------------------------------------------------

def classify_requirements_iso25010(
    requirements_md: str,
) -> Iso25010Report:
    """Classify NFRs from structured Markdown against ISO/IEC 25010.

    Parameters
    ----------
    requirements_md:
        Markdown produced by ``core/extraction/requirements.py``.

    Returns
    -------
    Iso25010Report
        Full classification and coverage report.
    """
    _NFR_HEADER = re.compile(r"^###\s+(NFR-\d+)[^\n]*\n(.*?)(?=^###|\Z)", re.DOTALL | re.MULTILINE | re.IGNORECASE)
    _DESC_LINE = re.compile(r"\*\*Descripci[oó]n:\*\*\s*(.+)", re.IGNORECASE)

    classifications: List[NfrClassification] = []

    for m in _NFR_HEADER.finditer(requirements_md):
        nfr_id = m.group(1).upper()
        block = m.group(2)

        desc_match = _DESC_LINE.search(block)
        nfr_text = desc_match.group(1).strip() if desc_match else block[:300].strip()

        chars = classify_nfr(nfr_text + " " + block)
        clf = NfrClassification(
            nfr_id=nfr_id,
            nfr_text=nfr_text,
            characteristics=chars,
            unclassified=len(chars) == 0,
        )
        classifications.append(clf)

    return Iso25010Report(classifications=classifications)
