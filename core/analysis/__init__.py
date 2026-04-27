# core.analysis – tools for traceability, completeness, and orphan detection
from .traceability import analyze_traceability
from .completeness import analyze_completeness
from .orphans import detect_orphans

__all__ = ["analyze_traceability", "analyze_completeness", "detect_orphans"]
