#!/usr/bin/env python3
"""
run_evaluation.py
==================
Orchestrator for SE-Agentic-Evaluator.

Supports two distinct modes:
  1. generate: Creates a workflow JSON from a rubric and optional sample document.
  2. evaluate: Executes a workflow JSON against a specific document.

Usage:
    # Generate a workflow for a rubric
    python run_evaluation.py generate \\
        --rubric configs/rubric_hito2.yaml \\
        --sample-doc tests/test-1-hito-2/output/phase0_extract/contents.md \\
        --output workflows/workflow_hito2.json

    # Evaluate a document using an existing workflow
    python run_evaluation.py evaluate \\
        --workflow workflows/workflow_hito2.json \\
        --input "tests/test-1-hito-2/A1.1 Memoria trabajo final (2).docx" \\
        --output results/alumno_01/
"""

from __future__ import annotations

import argparse
import json
import logging
import sys
from pathlib import Path

# Ensure repo root is in path
REPO_ROOT = Path(__file__).parent
sys.path.insert(0, str(REPO_ROOT))

from core.meta_agent.workflow_generator import generate_workflow
from core.workflow_executor import WorkflowExecutor

logger = logging.getLogger(__name__)


def cmd_generate(args: argparse.Namespace) -> None:
    """Generate a workflow JSON from a rubric."""
    logging.basicConfig(level=logging.INFO, format="%(levelname)s: %(message)s")

    rubric_path = Path(args.rubric)
    output_path = Path(args.output)
    sample_doc_path = Path(args.sample_doc) if args.sample_doc else None

    if not rubric_path.exists():
        logger.error("Rubric file not found: %s", rubric_path)
        sys.exit(1)

    # If sample doc is provided, use it for context.
    # If not, we pass an empty string or a placeholder to the generator.
    doc_path_str = str(sample_doc_path) if sample_doc_path and sample_doc_path.exists() else ""
    if not doc_path_str:
        logger.warning("No sample document provided. Workflow generation may be less precise.")

    logger.info("Generating workflow for rubric: %s", rubric_path)
    
    try:
        # The generator needs a document path to read content. 
        # If none provided, we might need to handle this in the generator or pass a dummy.
        # For now, we assume the generator can handle an empty string or we require a doc.
        # Let's enforce a sample doc for now as the current generator relies on it.
        if not doc_path_str:
            logger.error("A sample document is currently required for workflow generation.")
            sys.exit(1)

        workflow = generate_workflow(
            rubric_path=str(rubric_path),
            document_path=doc_path_str,
            output_path=str(output_path),
            model=args.model,
            max_retries=args.max_retries,
        )
        logger.info("✅ Workflow generated successfully: %s", output_path)
    except Exception as e:
        logger.error("Failed to generate workflow: %s", e)
        sys.exit(1)


def cmd_evaluate(args: argparse.Namespace) -> None:
    """Execute a workflow JSON against a document."""
    logging.basicConfig(level=logging.INFO, format="%(levelname)s: %(message)s")

    workflow_path = Path(args.workflow)
    input_doc = Path(args.input)
    output_dir = Path(args.output)

    if not workflow_path.exists():
        logger.error("Workflow file not found: %s", workflow_path)
        sys.exit(1)
    if not input_doc.exists():
        logger.error("Input document not found: %s", input_doc)
        sys.exit(1)

    output_dir.mkdir(parents=True, exist_ok=True)

    logger.info("Loading workflow: %s", workflow_path)
    with open(workflow_path) as f:
        workflow = json.load(f)

    # Inject runtime variables into the workflow
    # This allows the same workflow to be reused for different documents/outputs
    if "variables" not in workflow:
        workflow["variables"] = {}
    
    # Map standard CLI args to workflow variables
    workflow["variables"]["input_docx"] = str(input_doc)
    workflow["variables"]["output_dir"] = str(output_dir)
    
    # If the workflow expects input_rubric but it's not in variables, try to infer or warn
    if "input_rubric" not in workflow["variables"]:
        logger.warning("Workflow does not define 'input_rubric'. Evaluation may fail if steps require it.")

    logger.info("Executing workflow for document: %s", input_doc)
    logger.info("Output directory: %s", output_dir)

    try:
        executor = WorkflowExecutor(workflow, dry_run=args.dry_run)
        
        # Pre-execution validation
        missing = executor.validate_inputs()
        if missing:
            logger.error("Workflow validation failed. Missing variables: %s", missing)
            sys.exit(1)
            
        result = executor.execute()

        log_path = output_dir / "execution_log.json"
        log_path.write_text(json.dumps(result, ensure_ascii=False, indent=2), encoding="utf-8")
        logger.info("✅ Execution log saved to: %s", log_path)
        
        if result["status"] == "completed":
            logger.info("✅ Workflow completed in %.1fs", result.get("duration", 0))
        else:
            logger.warning("⚠️ Workflow finished with status: %s", result["status"])
            sys.exit(1)
    except Exception as e:
        logger.error("Workflow execution failed: %s", e)
        sys.exit(1)


def main() -> None:
    parser = argparse.ArgumentParser(
        description="SE-Agentic-Evaluator Orchestrator"
    )
    subparsers = parser.add_subparsers(dest="command", required=True, help="Command to execute")

    # --- Generate Command ---
    parser_gen = subparsers.add_parser("generate", help="Generate a workflow JSON from a rubric")
    parser_gen.add_argument("--rubric", type=str, required=True, help="Path to rubric YAML/Markdown")
    parser_gen.add_argument("--sample-doc", type=str, required=False, help="Path to sample document (Markdown)")
    parser_gen.add_argument("--output", type=str, required=True, help="Path to save generated workflow JSON")
    parser_gen.add_argument("--model", type=str, default="qwen3.6-plus", help="LLM model to use")
    parser_gen.add_argument("--max-retries", type=int, default=3, help="Max retries on validation failure")
    parser_gen.set_defaults(func=cmd_generate)

    # --- Evaluate Command ---
    parser_eval = subparsers.add_parser("evaluate", help="Execute a workflow JSON against a document")
    parser_eval.add_argument("--workflow", type=str, required=True, help="Path to workflow JSON")
    parser_eval.add_argument("--input", type=str, required=True, help="Path to document to evaluate (DOCX/MD)")
    parser_eval.add_argument("--output", type=str, required=True, help="Directory for results")
    parser_eval.add_argument("--dry-run", action="store_true", help="Simulate execution without running tools")
    parser_eval.set_defaults(func=cmd_evaluate)

    args = parser.parse_args()
    args.func(args)


if __name__ == "__main__":
    main()
