#!/usr/bin/env python3
"""
core/extraction/diagramlens/annotate.py
========================================
Importable module for vision-based diagram description.

Adapted from Lamb-Project/DiagramLens ``annotate_images_enhanced.py`` (GPL-3.0).
Original repository: https://github.com/Lamb-Project/DiagramLens
Copyright (C) Lamb-Project contributors.

Modifications for SE-Agentic-Evaluator:
  - Converted from a CLI script to an importable module.
  - Exposed pure functions: ``find_image_refs_with_context``,
    ``call_ollama``, ``pre_categorize_with_context``,
    ``load_categories_config``, ``describe_diagram``,
    ``process_markdown_document``.
  - Added ``DEFAULT_CATEGORIES_PATH`` pointing to the bundled
    ``image_categories_enhanced.json`` inside this package.
  - The original ``main()`` entry-point is preserved for CLI use.

This file is distributed under the GNU General Public License v3.0.
See the LICENSE file at the root of this repository for the full text.
"""

from __future__ import annotations

import argparse
import base64
import json
import os
import re
import sys
import unicodedata
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple

# ---------------------------------------------------------------------------
# Optional heavy dependencies – gracefully degrade when not available so that
# unit-tests and imports succeed even without a full vision stack installed.
# ---------------------------------------------------------------------------
try:
    import requests as _requests
except ImportError:  # pragma: no cover
    _requests = None  # type: ignore[assignment]

try:
    from PIL import Image as _Image
except ImportError:  # pragma: no cover
    _Image = None  # type: ignore[assignment]

try:
    from rich.console import Console as _Console
    from rich.progress import track as _track
except ImportError:  # pragma: no cover
    _Console = None  # type: ignore[assignment]
    _track = None  # type: ignore[assignment]

# ---------------------------------------------------------------------------
# Package-level constants
# ---------------------------------------------------------------------------
_HERE = Path(__file__).parent
DEFAULT_CATEGORIES_PATH: Path = _HERE / "image_categories_enhanced.json"
"""Path to the bundled enhanced image-categories configuration."""

DEFAULT_MODEL: str = "qwen3-vl"
"""Default Ollama vision model used for diagram description."""

OLLAMA_URL: str = "http://localhost:11434/api/chat"
MAX_IMAGE_SIZE: int = 5 * 1024 * 1024  # 5 MiB
CONTEXT_CHARS: int = 500  # Characters of context to extract around an image


# ---------------------------------------------------------------------------
# Ollama helper
# ---------------------------------------------------------------------------

def _load_image_as_base64(image_path: Path) -> str:
    """Read an image file and return a base64-encoded string."""
    with image_path.open("rb") as f:
        return base64.b64encode(f.read()).decode("utf-8")


def call_ollama(
    model: str,
    prompt: str,
    image_path: Optional[Path] = None,
    temperature: float = 0.0,
    ollama_url: str = OLLAMA_URL,
) -> str:
    """Send a request to a local Ollama server.

    Parameters
    ----------
    model:
        Ollama model tag (e.g. ``"qwen3-vl"``).
    prompt:
        Text prompt sent to the model.
    image_path:
        Optional path to an image file.  When provided the image is
        base64-encoded and attached to the message.
    temperature:
        Sampling temperature (0.0 = deterministic).
    ollama_url:
        Endpoint URL for the Ollama ``/api/chat`` route.

    Returns
    -------
    str
        Model response text, or an empty string on failure.
    """
    if _requests is None:
        raise ImportError("The 'requests' package is required to call Ollama.")

    message: Dict[str, Any] = {"role": "user", "content": prompt}

    if image_path is not None:
        if _Image is None:
            raise ImportError("The 'Pillow' package is required for image handling.")
        # Read the file once; validate from an in-memory buffer to avoid a
        # second disk access, then reuse the same bytes for encoding.
        import io as _io
        raw = Path(image_path).read_bytes()
        try:
            _Image.open(_io.BytesIO(raw)).verify()
        except Exception as exc:
            raise ValueError(f"Invalid or corrupt image file '{image_path}': {exc}") from exc
        message["images"] = [base64.b64encode(raw).decode("utf-8")]

    payload: Dict[str, Any] = {
        "model": model,
        "messages": [message],
        "options": {"temperature": temperature},
        "stream": False,
    }

    try:
        resp = _requests.post(ollama_url, json=payload, timeout=180)
        resp.raise_for_status()
        data = resp.json()
        return data.get("message", {}).get("content", "").strip()
    except Exception as exc:
        sys.stderr.write(f"[ERROR] Ollama request failed: {exc}\n")
        return ""


# ---------------------------------------------------------------------------
# Markdown processing
# ---------------------------------------------------------------------------

_IMG_REGEX = re.compile(r"!\[(?P<alt>.*?)\]\((?P<path>[^)]+)\)")


def find_image_refs_with_context(
    md_text: str, context_size: int = CONTEXT_CHARS
) -> List[Dict[str, Any]]:
    """Find all Markdown image references with surrounding context.

    Parameters
    ----------
    md_text:
        Full content of the Markdown document.
    context_size:
        Number of characters to extract before and after each image
        reference as contextual text.

    Returns
    -------
    list of dict
        Each dict contains:
        ``path``, ``alt_text``, ``start``, ``end``,
        ``text_before``, ``text_after``, ``current_heading``,
        ``full_match``.
    """
    matches: List[Dict[str, Any]] = []
    for m in _IMG_REGEX.finditer(md_text):
        start_idx = m.start()
        end_idx = m.end()

        # Context before
        context_start = max(0, start_idx - context_size)
        text_before = md_text[context_start:start_idx]
        para_breaks = [text_before.rfind("\n\n"), text_before.rfind("\n#")]
        para_start = max(para_breaks)
        if para_start > 0:
            text_before = text_before[para_start:].strip()

        # Context after
        context_end = min(len(md_text), end_idx + context_size)
        text_after = md_text[end_idx:context_end]
        para_breaks_after = [text_after.find("\n\n"), text_after.find("\n#")]
        para_end = min((p for p in para_breaks_after if p > 0), default=len(text_after))
        text_after = text_after[:para_end].strip()

        # Nearest heading
        heading_search = md_text[max(0, start_idx - 1000):start_idx]
        heading_match = re.findall(r"^#+\s+(.+)$", heading_search, re.MULTILINE)
        current_heading = heading_match[-1] if heading_match else ""

        matches.append(
            {
                "path": m.group("path"),
                "alt_text": m.group("alt"),
                "start": start_idx,
                "end": end_idx,
                "text_before": text_before,
                "text_after": text_after,
                "current_heading": current_heading,
                "full_match": m.group(0),
            }
        )
    return matches


def load_categories_config(
    json_path: Optional[Path] = None,
) -> Dict[str, Any]:
    """Load the categories-and-prompts configuration from a JSON file.

    Parameters
    ----------
    json_path:
        Path to the JSON configuration file.  When ``None`` the bundled
        ``image_categories_enhanced.json`` is used.

    Returns
    -------
    dict
        Parsed configuration with keys ``"categories"`` and
        ``"category_prompts"``.
    """
    path = json_path if json_path is not None else DEFAULT_CATEGORIES_PATH
    with Path(path).open(encoding="utf-8") as f:
        return json.load(f)


def pre_categorize_with_context(
    context_info: Dict[str, Any],
    categories: List[str],
    model: str = DEFAULT_MODEL,
    temperature: float = 0.1,
) -> Optional[str]:
    """Predict the diagram type from surrounding Markdown text.

    Uses the section heading, alt text, and paragraphs around the image
    to ask the LLM for a quick category hint *before* looking at the
    actual pixel data.

    Parameters
    ----------
    context_info:
        Dictionary produced by :func:`find_image_refs_with_context`.
    categories:
        List of valid category names (from the JSON config).
    model:
        Ollama model tag.
    temperature:
        Sampling temperature.

    Returns
    -------
    str | None
        Predicted category name (lower-cased) or ``None`` when uncertain.
    """
    prompt = (
        "Based on the surrounding text context, predict what type of diagram is being referenced.\n\n"
        f"Current section heading: {context_info.get('current_heading') or 'None'}\n"
        f"Image alt text: {context_info.get('alt_text') or 'None'}\n\n"
        f"Text BEFORE the image:\n{(context_info.get('text_before') or '')[:300] or 'None'}\n\n"
        f"Text AFTER the image:\n{(context_info.get('text_after') or '')[:300] or 'None'}\n\n"
        f"Available categories: {', '.join(categories)}\n\n"
        "Reply with ONLY the most likely category name. "
        "If you cannot determine with reasonable confidence, reply with \"unknown\"."
    )

    response = call_ollama(model=model, prompt=prompt, temperature=temperature)
    if response:
        response_lower = response.lower().strip()
        if response_lower in [c.lower() for c in categories]:
            return response_lower
    return None


def describe_diagram(
    image_path: Path,
    context_info: Optional[Dict[str, Any]] = None,
    model: str = DEFAULT_MODEL,
    categories_path: Optional[Path] = None,
) -> Dict[str, Any]:
    """Describe a single diagram image using a local Ollama vision model.

    High-level helper that:

    1. Optionally pre-categorizes the diagram using surrounding Markdown
       context (if *context_info* is provided).
    2. Asks the model to confirm the category by looking at the image.
    3. Generates a detailed technical description using the per-category
       prompt from the JSON config.

    Parameters
    ----------
    image_path:
        Path to the image file.
    context_info:
        Optional dict from :func:`find_image_refs_with_context`.
    model:
        Ollama vision model tag.
    categories_path:
        Optional path to the categories JSON.  Falls back to the
        bundled ``image_categories_enhanced.json``.

    Returns
    -------
    dict
        ``{"category": str, "description": str}``
    """
    config = load_categories_config(categories_path)
    categories: List[str] = config.get("categories", [])
    category_prompts: Dict[str, Any] = config.get("category_prompts", {})

    predicted_category: Optional[str] = None
    if context_info is not None:
        try:
            predicted_category = pre_categorize_with_context(
                context_info, categories, model, temperature=0.1
            )
        except Exception:
            predicted_category = None

    # Build categorisation prompt
    hint = (
        f"Context suggests this might be a {predicted_category} diagram.\n"
        if predicted_category and predicted_category != "unknown"
        else ""
    )
    heading_hint = (
        f"Section heading: {context_info['current_heading']}\n"
        if context_info and context_info.get("current_heading")
        else ""
    )
    cat_prompt = (
        f"Identify the type of this software engineering diagram.\n\n"
        f"{hint}"
        f"{heading_hint}"
        f"Examine the visual elements carefully and choose ONE category from: "
        f"{', '.join(categories)}\n\n"
        "Reply with only the category name, nothing else."
    )

    category_response = call_ollama(
        model=model, prompt=cat_prompt, image_path=image_path, temperature=0.0
    )
    category = category_response.lower().strip()
    if category not in [c.lower() for c in categories]:
        category = "other"

    # Build description prompt
    desc_prompt_cfg = category_prompts.get(category, category_prompts.get("other", {}))
    desc_prompt = desc_prompt_cfg.get("prompt", "Describe this diagram in detail.")

    if context_info:
        extra: List[str] = []
        if context_info.get("text_before"):
            extra.append(f"Before image: {context_info['text_before'][:200]}")
        if context_info.get("text_after"):
            extra.append(f"After image: {context_info['text_after'][:200]}")
        if extra:
            desc_prompt += "\n\nAdditional context from the document:\n" + "\n".join(extra)

    description = call_ollama(
        model=model, prompt=desc_prompt, image_path=image_path, temperature=0.1
    )

    return {
        "category": category,
        "description": description or "No description generated.",
    }


def process_markdown_document(
    input_md: Path,
    output_annotated: Path,
    output_summary: Path,
    model: str = DEFAULT_MODEL,
    categories_path: Optional[Path] = None,
    context_size: int = CONTEXT_CHARS,
    verbose: bool = False,
) -> List[Dict[str, Any]]:
    """Process all images in a Markdown document and insert descriptions.

    For each ``![alt](path)`` reference found in *input_md*:

    * Categorises the diagram type.
    * Generates a technical description via a local Ollama vision model.
    * Inserts the description block immediately after the image in the
      annotated output file.
    * Writes a structured summary file listing all diagrams.

    Parameters
    ----------
    input_md:
        Path to the source Markdown file.
    output_annotated:
        Path for the annotated Markdown output.
    output_summary:
        Path for the summary Markdown output.
    model:
        Ollama vision model tag.
    categories_path:
        Path to the categories JSON (uses bundled file when ``None``).
    context_size:
        Characters of context to extract around each image.
    verbose:
        If ``True`` and Rich is available, print per-image progress.

    Returns
    -------
    list of dict
        One dict per processed image with keys
        ``"path"``, ``"category"``, ``"description"``.
    """
    input_md = Path(input_md).resolve()
    output_annotated = Path(output_annotated).resolve()
    output_summary = Path(output_summary).resolve()

    if not input_md.is_file():
        raise FileNotFoundError(f"Input markdown not found: {input_md}")

    md_text = input_md.read_text(encoding="utf-8")
    image_refs = find_image_refs_with_context(md_text, context_size)

    if not image_refs:
        output_annotated.write_text(md_text, encoding="utf-8")
        output_summary.write_text("# Diagram Analysis Summary\n\nNo images found.\n", encoding="utf-8")
        return []

    config = load_categories_config(categories_path)
    categories: List[str] = config.get("categories", [])
    category_prompts: Dict[str, Any] = config.get("category_prompts", {})

    console = _Console() if _Console is not None else None
    iterator = (
        _track(image_refs, description="Processing diagrams…")
        if (not verbose and _track is not None)
        else image_refs
    )

    new_md_parts: List[str] = []
    summary_lines: List[str] = [
        "# Diagram Analysis Summary\n\n",
        f"**Source Document:** {input_md.name}\n\n",
        f"**Total Diagrams:** {len(image_refs)}\n\n",
        "---\n\n",
    ]
    results: List[Dict[str, Any]] = []
    last_idx = 0

    for idx, img_info in enumerate(iterator, 1):
        new_md_parts.append(md_text[last_idx: img_info["start"]])
        new_md_parts.append(img_info["full_match"])

        img_path_str = unicodedata.normalize("NFC", img_info["path"]).strip()
        img_path = (input_md.parent / img_path_str).resolve()

        category = "unknown"
        description = ""

        if not img_path.is_file():
            description = f"⚠️ Image file not found: `{img_info['path']}`"
        else:
            try:
                result = describe_diagram(img_path, img_info, model, categories_path)
                category = result["category"]
                description = result["description"]
            except Exception as exc:
                description = f"⚠️ Error processing image: {exc}"

        desc_block = (
            f"\n\n**Diagram Type:** {category.replace('_', ' ').title()}\n\n"
            f"**Technical Description:**\n{description}\n\n"
        )
        new_md_parts.append(desc_block)

        summary_lines.append(f"## Diagram {idx}: {os.path.basename(img_info['path'])}\n\n")
        summary_lines.append(f"- **Type:** {category.replace('_', ' ').title()}\n")
        summary_lines.append(f"- **File:** `{img_info['path']}`\n")
        if img_info.get("current_heading"):
            summary_lines.append(f"- **Section:** {img_info['current_heading']}\n")
        summary_lines.append(f"- **Description:**\n\n{description}\n\n---\n\n")

        results.append(
            {"path": str(img_info["path"]), "category": category, "description": description}
        )
        last_idx = img_info["end"]

    new_md_parts.append(md_text[last_idx:])

    output_annotated.parent.mkdir(parents=True, exist_ok=True)
    output_annotated.write_text("".join(new_md_parts), encoding="utf-8")

    output_summary.parent.mkdir(parents=True, exist_ok=True)
    output_summary.write_text("".join(summary_lines), encoding="utf-8")

    return results


# ---------------------------------------------------------------------------
# CLI entry-point (preserved from original script for backwards compatibility)
# ---------------------------------------------------------------------------

def main() -> None:  # pragma: no cover
    """Command-line interface for processing a Markdown document."""
    parser = argparse.ArgumentParser(
        description="Generate technical descriptions of diagrams in Markdown files."
    )
    parser.add_argument("--input", required=True, help="Path to source .md file")
    parser.add_argument("--output", required=True, help="Path for annotated .md file")
    parser.add_argument("--summary", required=True, help="Path for summary .md file")
    parser.add_argument(
        "--categories",
        default=str(DEFAULT_CATEGORIES_PATH),
        help="JSON file with categories and description prompts",
    )
    parser.add_argument(
        "--model",
        default=DEFAULT_MODEL,
        help=f"Ollama vision model (default: {DEFAULT_MODEL})",
    )
    parser.add_argument(
        "--context-size",
        type=int,
        default=CONTEXT_CHARS,
        help=f"Characters of context around images (default: {CONTEXT_CHARS})",
    )
    parser.add_argument("--verbose", action="store_true", help="Show detailed progress")
    args = parser.parse_args()

    results = process_markdown_document(
        input_md=Path(args.input),
        output_annotated=Path(args.output),
        output_summary=Path(args.summary),
        model=args.model,
        categories_path=Path(args.categories),
        context_size=args.context_size,
        verbose=args.verbose,
    )

    print(f"✅ Processed {len(results)} diagram(s).")
    print(f"   Annotated: {args.output}")
    print(f"   Summary:   {args.summary}")


if __name__ == "__main__":
    main()
