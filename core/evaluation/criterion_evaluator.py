#!/usr/bin/env python3
"""
core/evaluation/criterion_evaluator.py
========================================
Evaluate document criteria using LLM prompts from YAML rubric config.

This module handles the **evaluation phase** — it loads criteria from a
YAML rubric config, runs each criterion prompt against the document,
extracts scores, and saves individual eval_*.md files.

It accepts optional structured context (from extraction/analysis phases)
to inject into the evaluation prompts via --{CONTEXTO}--.

Usage:
    # Criteria-only mode (document + YAML → eval_*.md + scores.json)
    python core/evaluation/criterion_evaluator.py \
        --document tests/test_arquitectura.md \
        --config configs/rubric_architecture.yaml \
        --output output/evaluacion_arquitectura/

    # With pre-built analysis context
    python core/evaluation/criterion_evaluator.py \
        --document tests/test_arquitectura.md \
        --config configs/rubric_architecture.yaml \
        --output output/evaluacion_arquitectura/ \
        --context output/analysis_context.md
"""

from __future__ import annotations

import argparse
import json
import logging
import os
import re
import time
from pathlib import Path
from typing import Any, Dict, List, Optional

from dotenv import load_dotenv

load_dotenv()

from core.clients.dashscope_client import DashScopeClient
from core.config.config_manager import ConfigManager, CriterionConfig
from core.extraction.objectives import extract_objectives, parse_objective_ids
from core.extraction.requirements import extract_requirements, parse_requirement_ids
from core.extraction.use_cases import extract_use_cases, parse_use_case_ids
from core.analysis.orphans import detect_orphans
from core.analysis.smart import evaluate_objectives_smart, smart_summary_markdown
from core.analysis.iso25010 import classify_requirements_iso25010

logger = logging.getLogger(__name__)

PROMPTS_DIR = Path(__file__).parents[2] / "prompts"


def load_prompt(prompt_filename: str) -> str:
    """Load a prompt template from the prompts directory."""
    prompt_path = PROMPTS_DIR / prompt_filename
    if not prompt_path.exists():
        raise FileNotFoundError(f"Prompt not found: {prompt_path}")
    return prompt_path.read_text(encoding="utf-8")


def extract_score(text: str) -> Optional[float]:
    """Extract a score (X/10) from evaluation text."""
    patterns = [
        r"\*\*Puntuaci[oó]n:\*\*\s*(\d+\.?\d*)/10",
        r"Puntuaci[oó]n:\s*(\d+\.?\d*)/10",
        r"Nota:\s*(\d+\.?\d*)/10",
        r"(\d+\.?\d*)\s*/\s*10",
    ]
    for pattern in patterns:
        match = re.search(pattern, text)
        if match:
            value = float(match.group(1))
            if 0 <= value <= 10:
                return value
    return None


def extract_detailed_scores(text: str) -> Dict[str, float]:
    """Extract per-sub-criterion scores from a markdown table."""
    scores: Dict[str, float] = {}
    table_pattern = re.compile(
        r"\|\s*(.+?)\s*\|.*?\|\s*(\d+\.?\d*)\s*/\s*10\s*\|"
    )
    for match in table_pattern.finditer(text):
        name = match.group(1).strip()
        value = float(match.group(2))
        if 0 <= value <= 10:
            scores[name] = value
    return scores


def find_images_in_document(document: str, doc_path: Path) -> List[Path]:
    """Extract image paths referenced in the markdown document."""
    img_refs = re.findall(r"!\[.*?\]\((.*?)\)", document)
    images: List[Path] = []
    for ref in img_refs:
        img_path = Path(ref)
        if not img_path.is_absolute():
            img_path = doc_path.parent / img_path
        if img_path.exists():
            images.append(img_path)
    return images


# ---------------------------------------------------------------------------
# Criterion evaluation
# ---------------------------------------------------------------------------

BATCH_SIZE = int(os.environ.get("EVAL_BATCH_SIZE", "5"))


def _evaluate_single(
    client: DashScopeClient,
    model: str,
    vision_model: str,
    prompt_template: str,
    document: str,
    doc_path: Path,
    criterion: CriterionConfig,
    options: Any,
    context_str: Optional[str] = None,
) -> str:
    """Evaluate a single criterion using the LLM, with optional vision and context."""
    prompt = prompt_template.replace("--{DOCUMENTO}--", document)

    if context_str:
        prompt = prompt.replace("--{CONTEXTO}--", context_str)
    else:
        prompt = prompt.replace("--{CONTEXTO}--", "No hay análisis previo disponible. Evalúa basándote únicamente en el documento.")

    if options.multimodal and criterion.requires_vision:
        images = find_images_in_document(document, doc_path)
        if images:
            img_descriptions = []
            for img in images:
                logger.info("Analyzing image with vision model: %s", img.name)
                desc = client.vision(
                    model=vision_model,
                    prompt="Describe this diagram in detail for software architecture evaluation.",
                    image_path=str(img),
                )
                img_descriptions.append(f"### {img.name}\n\n{desc}")
            images_text = "\n\n".join(img_descriptions)
            prompt = prompt.replace("--{IMAGENES}--", images_text)
        else:
            prompt = prompt.replace("--{IMAGENES}--", "No hay imágenes disponibles para este criterio.")
    else:
        prompt = prompt.replace("--{IMAGENES}--", "")

    logger.info("Evaluating criterion: %s", criterion.name)
    start = time.time()
    result = client.generate(
        model=model,
        prompt=prompt,
        temperature=0.1,
        max_tokens=4096,
    )
    elapsed = time.time() - start
    logger.info("Criterion %s evaluated in %.1fs", criterion.name, elapsed)

    return result


def _build_batch_prompt(
    criteria_batch: List[CriterionConfig],
    document: str,
    context_str: Optional[str] = None,
) -> str:
    """Build a single prompt that evaluates multiple criteria at once."""
    context_section = context_str or "No hay análisis previo disponible. Evalúa basándote únicamente en el documento."

    criteria_descriptions = []
    for i, c in enumerate(criteria_batch, 1):
        prompt_template = load_prompt(c.prompt)
        levels_text = ""
        for line in prompt_template.split("\n"):
            if line.strip().startswith("- **"):
                levels_text += line + "\n"
        if not levels_text:
            levels_text = "Evalúa de 0 a 10 según tu juicio experto.\n"
        criteria_descriptions.append(
            f"### Criterio {i}: {c.name} (ID: {c.id})\n\nNiveles:\n{levels_text}"
        )

    criteria_block = "\n".join(criteria_descriptions)

    prompt = f"""Analiza el siguiente documento y evalúa CADA UNO de los criterios listados.

Documento:
{document}

## Contexto de Análisis Previo

{context_section}

## Criterios a evaluar

{criteria_block}

## Instrucciones
- Evalúa CADA criterio de forma independiente asignando una puntuación de 0 a 10.
- Para cada criterio, proporciona un análisis detallado con evidencias del documento.
- Utiliza el contexto de análisis previo como evidencia complementaria.

## Formato de respuesta
Para CADA criterio, usa EXACTAMENTE este formato:

---CRITERIO_START---
# Evaluación: [NOMBRE DEL CRITERIO]

## Análisis
[Comentarios detallados con evidencias del documento y contexto]

## Puntuación
**Puntuación:** X/10

## Observaciones
[Recomendaciones de mejora]
---CRITERIO_END---
"""
    return prompt


def _parse_batch_response(text: str, criteria_ids: List[str]) -> Dict[str, str]:
    """Parse a batch response into individual criterion evaluations."""
    results: Dict[str, str] = {}

    blocks = re.split(r"---CRITERIO_START---", text)
    for block in blocks[1:]:
        block = block.strip()
        end_idx = block.find("---CRITERIO_END---")
        if end_idx != -1:
            block = block[:end_idx].strip()

        criterion_id = None
        for cid in criteria_ids:
            normalized_cid = cid.replace("_", " ").replace("  ", " ")
            if normalized_cid in block.lower() or cid in block:
                criterion_id = cid
                break
        if criterion_id is None and criteria_ids:
            idx = len([k for k in results if k in criteria_ids])
            if idx < len(criteria_ids):
                criterion_id = criteria_ids[idx]

        if criterion_id:
            results[criterion_id] = block

    for cid in criteria_ids:
        if cid not in results:
            results[cid] = f"# Evaluación: {cid}\n\n## Puntuación\n**Puntuación:** 0/10\n\n## Observaciones\nNo se pudo extraer la evaluación del lote."

    return results


def evaluate_criteria_batch(
    client: DashScopeClient,
    model: str,
    vision_model: str,
    criteria_batch: List[CriterionConfig],
    document: str,
    doc_path: Path,
    options: Any,
    context_str: Optional[str] = None,
) -> Dict[str, str]:
    """Evaluate a batch of criteria in a single LLM call."""
    prompt = _build_batch_prompt(criteria_batch, document, context_str)

    logger.info("Evaluating batch of %d criteria: %s",
                len(criteria_batch), ", ".join(c.name for c in criteria_batch))
    start = time.time()
    result = client.generate(
        model=model,
        prompt=prompt,
        temperature=0.1,
        max_tokens=8192,
    )
    elapsed = time.time() - start
    logger.info("Batch of %d criteria evaluated in %.1fs", len(criteria_batch), elapsed)

    criteria_ids = [c.id for c in criteria_batch]
    return _parse_batch_response(result, criteria_ids)


def build_context(
    document: str,
    client: DashScopeClient,
    model: str = os.environ.get("DASHSCOPE_MODEL", "qwen3.6-plus"),
) -> str:
    """Run full extraction + analysis pipeline and return context Markdown.

    Executes: objectives extraction, requirements extraction, use-case
    extraction, orphan detection, SMART evaluation, and ISO 25010
    classification.

    Parameters
    ----------
    document:
        Full Markdown document content.
    client:
        DashScopeClient instance for LLM calls.
    model:
        Model name to use for extractions.

    Returns
    -------
    str
        Markdown-formatted analysis context.
    """
    logger.info("Running full extraction pipeline...")

    objectives_md = extract_objectives(document, client=client, model=model)
    logger.info("Objectives extracted: %d chars", len(objectives_md))

    requirements_md = extract_requirements(document, client=client, model=model)
    logger.info("Requirements extracted: %d chars", len(requirements_md))

    use_cases_md = extract_use_cases(document, client=client, model=model)
    logger.info("Use cases extracted: %d chars", len(use_cases_md))

    orphans = detect_orphans(objectives_md, requirements_md)
    orphans_md = orphans.as_markdown()

    smart_scores = evaluate_objectives_smart(objectives_md)
    smart_md = smart_summary_markdown(smart_scores)

    iso_report = classify_requirements_iso25010(requirements_md)
    iso_md = iso_report.as_markdown()

    context_parts = [
        "### Objetivos Extraídos",
        objectives_md,
        "### Requisitos Extraídos",
        requirements_md,
        "### Casos de Uso Extraídos",
        use_cases_md,
        "### Detección de Huérfanos",
        orphans_md,
        "### Evaluación SMART",
        smart_md,
        "### Clasificación ISO/IEC 25010",
        iso_md,
    ]
    return "\n\n".join(context_parts)


def run_criterion_evaluation(
    document_path: str,
    config_path: str,
    output_dir: str,
    context_path: Optional[str] = None,
    full: bool = False,
) -> Dict[str, Any]:
    """Evaluate all criteria from a rubric config.

    Parameters
    ----------
    document_path:
        Path to the document to evaluate.
    config_path:
        Path to YAML rubric configuration.
    output_dir:
        Directory to write eval_*.md and scores.json.
    context_path:
        Optional path to a Markdown file containing analysis context
        (objectives, requirements, orphans, SMART, ISO 25010).
    full:
        If True, run the full extraction + analysis pipeline to build
        context automatically before evaluating criteria.

    Returns
    -------
    dict with scores, detailed_scores, and evaluation file paths.
    """
    manager = ConfigManager(config_path)
    cfg = manager.load()

    doc_path = Path(document_path)
    if not doc_path.exists():
        raise FileNotFoundError(f"Document not found: {doc_path}")
    document = doc_path.read_text(encoding="utf-8")

    client = DashScopeClient(region=cfg.provider.region if cfg.provider else "singapore")
    env_text_model = os.environ.get("DASHSCOPE_MODEL")
    env_vision_model = os.environ.get("DASHSCOPE_VISION_MODEL")
    model = env_text_model or (cfg.provider.text_model if cfg.provider else "qwen3.6-plus")
    vision_model = env_vision_model or (cfg.provider.vision_model if cfg.provider else "qwen-vl-max")

    output_path = Path(output_dir)
    output_path.mkdir(parents=True, exist_ok=True)

    context_str = None
    if full:
        context_str = build_context(document, client, model)
        ctx_file = output_path / "analysis_context.md"
        ctx_file.write_text(context_str, encoding="utf-8")
        logger.info("Analysis context built and saved to %s", ctx_file)
    elif context_path:
        ctx_path = Path(context_path)
        if ctx_path.exists():
            context_str = ctx_path.read_text(encoding="utf-8")
            logger.info("Loaded analysis context from %s", context_path)
        else:
            logger.warning("Context file not found: %s", context_path)

    evaluations: Dict[str, str] = {}
    scores: Dict[str, float] = {}
    detailed_scores: Dict[str, Dict[str, float]] = {}

    print(f"\n{'='*60}")
    print(f"Evaluaitor-Lamb v2.0 — Criterion Evaluation")
    print(f"Documento: {doc_path.name}")
    print(f"Rúbrica: {cfg.id} - {cfg.description}")
    print(f"Modelo: {model}")
    print(f"Criterios: {len(cfg.criteria)}")
    print(f"Batch size: {BATCH_SIZE}")
    if full:
        print(f"Contexto: ✅ Generado automáticamente (--full)")
    elif context_str:
        print(f"Contexto: ✅ Inyectado desde {context_path}")
    else:
        print(f"Contexto: ❌ Sin análisis previo")
    print(f"{'='*60}\n")

    # Split criteria into batches
    criteria_list = cfg.criteria
    batches = [criteria_list[i:i + BATCH_SIZE] for i in range(0, len(criteria_list), BATCH_SIZE)]

    for batch_idx, batch in enumerate(batches):
        batch_names = ", ".join(c.name for c in batch)
        print(f"[Lote {batch_idx + 1}/{len(batches)}] Evaluando: {batch_names}...")

        if len(batch) == 1:
            criterion = batch[0]
            prompt_template = load_prompt(criterion.prompt)
            eval_text = _evaluate_single(
                client, model, vision_model, prompt_template, document, doc_path,
                criterion, cfg.options, context_str
            )
            evaluations[criterion.id] = eval_text
        else:
            batch_results = evaluate_criteria_batch(
                client, model, vision_model, batch, document, doc_path,
                cfg.options, context_str
            )
            evaluations.update(batch_results)

        for criterion in batch:
            eval_text = evaluations.get(criterion.id, "")
            score = extract_score(eval_text)
            if score is not None:
                scores[criterion.id] = score
                print(f"  → {criterion.name}: {score}/10")
            else:
                print(f"  → {criterion.name}: ⚠️ No se pudo extraer puntuación (se asigna 0)")
                scores[criterion.id] = 0.0

            if cfg.options.detailed_scoring:
                sub_scores = extract_detailed_scores(eval_text)
                if sub_scores:
                    detailed_scores[criterion.id] = sub_scores

            eval_file = output_path / f"eval_{criterion.id}.md"
            eval_file.write_text(eval_text, encoding="utf-8")

    scores_data = {"scores": scores}
    if detailed_scores:
        scores_data["detailed"] = detailed_scores

    scores_file = output_path / "scores.json"
    scores_file.write_text(
        json.dumps(scores_data, ensure_ascii=False, indent=2),
        encoding="utf-8",
    )

    print(f"\n✅ Evaluaciones guardadas en: {output_path}/")
    print(f"✅ Puntuaciones guardadas en: {scores_file}")

    return scores_data


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Evaluate document criteria using YAML rubric config."
    )
    parser.add_argument("--document", type=str, required=True, help="Path to document to evaluate")
    parser.add_argument("--config", type=str, required=True, help="Path to YAML rubric config")
    parser.add_argument("--output", type=str, required=True, help="Output directory for eval_*.md files")
    parser.add_argument(
        "--context", type=str, default=None,
        help="Path to a Markdown file with pre-built analysis context (objectives, orphans, SMART, etc.)"
    )
    parser.add_argument(
        "--full", action="store_true",
        help="Run full extraction + analysis pipeline before evaluating criteria"
    )
    args = parser.parse_args()

    logging.basicConfig(level=logging.INFO, format="%(levelname)s: %(message)s")
    run_criterion_evaluation(args.document, args.config, args.output, args.context, args.full)


if __name__ == "__main__":
    main()
