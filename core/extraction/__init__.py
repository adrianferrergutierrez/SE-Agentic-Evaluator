# core.extraction – tools for extracting structured data from documents
from .objectives import extract_objectives
from .requirements import extract_requirements
from .use_cases import extract_use_cases

__all__ = ["extract_objectives", "extract_requirements", "extract_use_cases"]
