#!/usr/bin/env python3
"""
core/evaluation/evaluator.py
==============================
Report generation from pre-computed evaluation files.

This module is the **Report phase** of the pipeline. It does NOT:
- Evaluate criteria (that's core/analysis/ and core/extraction/)
- Calculate grades (that's core/grading/grader.py)

It ONLY assembles existing evaluation markdown files and scores
into a final synthesis report using the LLM.

Usage:
    # From pre-generated evaluation files + scores
    python core/evaluation/evaluator.py \
        --document tests/test_arquitectura.md \
        --eval-dir output/evaluacion_arquitectura/ \
        --scores output/evaluacion_arquitectura/scores.json \
        --output output/evaluacion_arquitectura/

    # From evaluation files only (grader calculates scores)
    python core/evaluation/evaluator.py \
        --document tests/test_arquitectura.md \
        --eval-dir output/evaluacion_arquitectura/ \
        --config configs/rubric_architecture.yaml \
        --output output/evaluacion_arquitectura/
"""

from __future__ import annotations

import argparse
import json
import logging
import os
import re
import time
from datetime import datetime
from pathlib import Path
from typing import Any, Dict, List, Optional

from dotenv import load_dotenv

load_dotenv()

from core.clients.base import BaseLLMClient
from core.clients import get_client
from core.config.config_manager import ConfigManager
from core.grading.grader import GradingResult, RubricGrader

logger = logging.getLogger(__name__)

PROMPTS_DIR = Path(__file__).parents[2] / "prompts"


def load_prompt(prompt_filename: str) -> str:
    """Load a prompt template from the prompts directory."""
    prompt_path = PROMPTS_DIR / prompt_filename
    if not prompt_path.exists():
        raise FileNotFoundError(f"Prompt not found: {prompt_path}")
    return prompt_path.read_text(encoding="utf-8")


def load_evaluations_from_dir(eval_dir: Path) -> Dict[str, str]:
    """Load all eval_*.md files from a directory.

    Returns {criterion_id: markdown_content}.
    Filenames must follow the pattern: eval_<criterion_id>.md
    """
    evaluations: Dict[str, str] = {}
    pattern = re.compile(r"^eval_(.+)\.md$")

    for f in sorted(eval_dir.glob("eval_*.md")):
        match = pattern.match(f.name)
        if match:
            criterion_id = match.group(1)
            evaluations[criterion_id] = f.read_text(encoding="utf-8")
            logger.info("Loaded evaluation: %s (%s)", criterion_id, f.name)

    if not evaluations:
        raise FileNotFoundError(f"No eval_*.md files found in {eval_dir}")

    return evaluations


def load_scores_from_file(scores_path: Path) -> Dict[str, float]:
    """Load scores from a scores.json file."""
    with open(scores_path, "r", encoding="utf-8") as f:
        data = json.load(f)
    return data.get("scores", {})


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


def generate_final_report(
    client: BaseLLMClient,
    model: str,
    document: str,
    evaluations: Dict[str, str],
    grading_result: GradingResult,
) -> str:
    """Generate the final evaluation report using the LLM."""
    prompt_template = load_prompt("4_1_generacion_informe.md")

    evals_summary = "\n\n".join(
        f"### {criterion}\n\n{text}" for criterion, text in evaluations.items()
    )

    prompt = prompt_template.replace("--{DOCUMENTO}--", document)
    prompt = prompt.replace("--{EVALUACIONES}--", evals_summary)
    prompt = prompt.replace(
        "--{NOTA_FINAL}--",
        f"Ponderada: {grading_result.weighted_final}/10, Media: {grading_result.mean_xbar}/10, Nivel: {grading_result.performance_level}",
    )

    logger.info("Generating final report with %d evaluations", len(evaluations))
    start = time.time()
    result = client.generate(
        model=model,
        prompt=prompt,
        temperature=0.1,
        max_tokens=4096,
    )
    elapsed = time.time() - start
    logger.info("Final report generated in %.1fs", elapsed)

    return result


def run_report_generation(
    document_path: str,
    eval_dir: str,
    output_dir: str,
    config_path: Optional[str] = None,
    scores_path: Optional[str] = None,
) -> Dict[str, Any]:
    """Generate the final report from pre-computed evaluations.

    Parameters
    ----------
    document_path:
        Path to the original document being evaluated.
    eval_dir:
        Directory containing eval_*.md files (one per criterion).
    output_dir:
        Directory to write the final report and scores.
    config_path:
        Optional YAML rubric config (used if scores_path is not provided).
    scores_path:
        Optional path to pre-computed scores.json.
    """
    doc_path = Path(document_path)
    if not doc_path.exists():
        raise FileNotFoundError(f"Document not found: {doc_path}")
    document = doc_path.read_text(encoding="utf-8")

    eval_path = Path(eval_dir)
    if not eval_path.exists():
        raise FileNotFoundError(f"Evaluation directory not found: {eval_path}")

    evaluations = load_evaluations_from_dir(eval_path)

    grading_result: GradingResult

    if scores_path and Path(scores_path).exists():
        scores = load_scores_from_file(Path(scores_path))
        logger.info("Loaded scores from %s: %s", scores_path, scores)

        if config_path:
            grader = RubricGrader.from_config(config_path, evaluated_file=doc_path.name)
        else:
            grader = RubricGrader(evaluated_file=doc_path.name)

        grading_result = grader.grade({}, scores=scores)
    elif config_path:
        grader = RubricGrader.from_config(config_path, evaluated_file=doc_path.name)
        grading_result = grader.grade(evaluations)
    else:
        raise ValueError("Either --config or --scores is required for grading")

    provider_cfg = None
    if config_path:
        manager = ConfigManager(config_path)
        cfg = manager.load()
        provider_cfg = cfg.provider

    client = get_client()
    
    if os.environ.get("LLM_PROVIDER", "dashscope").lower() == "ollama":
        model = os.environ.get("OLLAMA_MODEL", "llama3.1")
    else:
        model = os.environ.get("DASHSCOPE_MODEL") or (provider_cfg.text_model if provider_cfg else "qwen3.6-plus")

    output_path = Path(output_dir)
    output_path.mkdir(parents=True, exist_ok=True)

    print(f"\n{'='*60}")
    print(f"Evaluaitor-Lamb v2.0 — Report Generation")
    print(f"Documento: {doc_path.name}")
    print(f"Evaluaciones cargadas: {len(evaluations)}")
    print(f"Nota ponderada: {grading_result.weighted_final}/10")
    print(f"Media (x̄): {grading_result.mean_xbar}")
    print(f"Nivel: {grading_result.performance_level}")
    print(f"{'='*60}\n")

    print(grading_result.rubric_table_markdown())

    print("\nGenerando informe final...")
    final_report = generate_final_report(client, model, document, evaluations, grading_result)

    report_file = output_path / "evaluacion_final.md"
    report_file.write_text(final_report, encoding="utf-8")

    scores_data = grading_result.as_dict()
    scores_file = output_path / "scores.json"
    scores_file.write_text(
        json.dumps(scores_data, ensure_ascii=False, indent=2),
        encoding="utf-8",
    )

    print(f"\n✅ Informe guardado en: {report_file}")
    print(f"✅ Puntuaciones guardadas en: {scores_file}")

    return grading_result.as_dict()


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Generate final evaluation report from pre-computed evaluations."
    )
    parser.add_argument("--document", type=str, required=True, help="Path to document evaluated")
    parser.add_argument("--eval-dir", type=str, required=True, help="Directory with eval_*.md files")
    parser.add_argument("--output", type=str, required=True, help="Output directory")
    parser.add_argument("--config", type=str, default=None, help="Path to YAML rubric config")
    parser.add_argument("--scores", type=str, default=None, help="Path to pre-computed scores.json")
    args = parser.parse_args()

    logging.basicConfig(level=logging.INFO, format="%(levelname)s: %(message)s")
    run_report_generation(args.document, args.eval_dir, args.output, args.config, args.scores)


if __name__ == "__main__":
    main()
