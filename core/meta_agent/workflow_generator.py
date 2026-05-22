#!/usr/bin/env python3
"""
core/meta_agent/workflow_generator.py
=======================================
Generates dynamic evaluation workflows from rubrics and documents.

Uses the LLM to analyze a rubric and document, then generates a JSON
workflow that defines which tools to execute, in what order, and with
what parameters.

Usage:
    python core/meta_agent/workflow_generator.py \
        --document tests/test2/output/phase0_extract/contents.md \
        --rubric configs/rubric_hito1_test2.yaml \
        --output tests/test2/output/workflow.json
"""

from __future__ import annotations

import argparse
import json
import logging
import re
import time
from datetime import datetime
from pathlib import Path
from typing import Any, Dict, List, Optional

from dotenv import load_dotenv
load_dotenv()

import jsonschema

from core.clients.dashscope_client import DashScopeClient
from core.meta_agent.tool_catalog import format_catalog_for_prompt

logger = logging.getLogger(__name__)

REPO_ROOT = Path(__file__).parent.parent.parent
SCHEMA_PATH = REPO_ROOT / "schemas" / "workflow_schema.json"
PROMPT_PATH = REPO_ROOT / "prompts" / "workflow_generator" / "workflow_generation.md"

DEFAULT_MODEL = "qwen3.6-plus"
MAX_RETRIES = 3


def _load_json(path: Path) -> Any:
    with open(path) as f:
        return json.load(f)


def _load_text(path: Path) -> str:
    return path.read_text(encoding="utf-8")


def _extract_json_from_response(text: str) -> Optional[Dict]:
    """Extract JSON from LLM response, handling markdown code blocks."""
    # Try to find JSON in code blocks
    match = re.search(r"```(?:json)?\s*\n(.*?)\n```", text, re.DOTALL)
    if match:
        text = match.group(1)

    # Try to find JSON object
    match = re.search(r"\{.*\}", text, re.DOTALL)
    if match:
        try:
            return json.loads(match.group(0))
        except json.JSONDecodeError:
            pass

    # Try entire text
    try:
        return json.loads(text)
    except json.JSONDecodeError:
        return None


def _validate_workflow(workflow: Dict, schema: Dict) -> List[str]:
    """Validate a workflow against the schema. Returns list of errors."""
    errors = []
    try:
        jsonschema.validate(instance=workflow, schema=schema)
    except jsonschema.ValidationError as e:
        errors.append(str(e.message))
    return errors


def build_prompt(
    rubric_text: str,
    document_text: str,
    catalog_text: str,
) -> str:
    """Build the workflow generation prompt."""
    template = _load_text(PROMPT_PATH)
    return (
        template
        .replace("--{CATALOGO}--", catalog_text)
        .replace("--{RUBRICA}--", rubric_text)
        .replace("--{DOCUMENTO}--", document_text[:5000])  # Limit doc context
    )


def generate_workflow(
    rubric_path: str,
    document_path: str,
    output_path: Optional[str] = None,
    model: str = DEFAULT_MODEL,
    max_retries: int = MAX_RETRIES,
    client: Optional[DashScopeClient] = None,
) -> Dict[str, Any]:
    """Generate a workflow JSON from a rubric and document.

    Parameters
    ----------
    rubric_path:
        Path to the rubric YAML config file.
    document_path:
        Path to the Markdown document to evaluate.
    output_path:
        Optional path to write the generated workflow JSON.
    model:
        LLM model name to use.
    max_retries:
        Maximum number of retries if validation fails.
    client:
        Optional DashScopeClient instance.

    Returns
    -------
    dict
        Generated workflow JSON.

    Raises
    ------
    RuntimeError
        If workflow generation fails after all retries.
    """
    if client is None:
        client = DashScopeClient()

    schema = _load_json(SCHEMA_PATH)
    catalog_text = format_catalog_for_prompt()
    rubric_text = _load_text(Path(rubric_path))
    document_text = _load_text(Path(document_path))

    prompt = build_prompt(rubric_text, document_text, catalog_text)

    last_errors = []
    for attempt in range(1, max_retries + 1):
        logger.info("Workflow generation attempt %d/%d", attempt, max_retries)

        # Add validation errors to prompt for retry
        retry_prompt = prompt
        if last_errors:
            error_context = "\n\n".join(last_errors)
            retry_prompt += f"\n\n## Errors in Previous Attempt\n\n{error_context}\n\nFix these errors and respond with a corrected JSON."

        response = client.generate(
            model=model,
            prompt=retry_prompt,
            temperature=0.1,
            max_tokens=4096,
        )

        workflow = _extract_json_from_response(response)
        if workflow is None:
            last_errors = ["No valid JSON found in response"]
            logger.warning("Attempt %d: No valid JSON found", attempt)
            continue

        errors = _validate_workflow(workflow, schema)
        if not errors:
            logger.info("Workflow generated and validated successfully")
            
            # Inject metadata for traceability
            rubric_id = Path(rubric_path).stem.replace("rubric_", "").replace("rubrica_", "")
            workflow["metadata"] = {
                "rubric_id": rubric_id,
                "created_at": datetime.now().isoformat(),
                "version": "1.0"
            }
            
            if output_path:
                out = Path(output_path)
                out.parent.mkdir(parents=True, exist_ok=True)
                out.write_text(
                    json.dumps(workflow, ensure_ascii=False, indent=2),
                    encoding="utf-8",
                )
                logger.info("Workflow saved to %s", out)
            return workflow

        last_errors = errors
        logger.warning("Attempt %d: Validation errors: %s", attempt, errors)

    raise RuntimeError(
        f"Workflow generation failed after {max_retries} attempts. "
        f"Last errors: {last_errors}"
    )


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Generate a dynamic evaluation workflow from a rubric and document."
    )
    parser.add_argument("--document", type=str, required=True, help="Path to Markdown document")
    parser.add_argument("--rubric", type=str, required=True, help="Path to rubric YAML config")
    parser.add_argument("--output", type=str, required=True, help="Path to write workflow JSON")
    parser.add_argument("--model", type=str, default=DEFAULT_MODEL, help="LLM model name")
    parser.add_argument("--max-retries", type=int, default=MAX_RETRIES, help="Max retries on validation failure")
    args = parser.parse_args()

    logging.basicConfig(level=logging.INFO, format="%(levelname)s: %(message)s")

    workflow = generate_workflow(
        rubric_path=args.rubric,
        document_path=args.document,
        output_path=args.output,
        model=args.model,
        max_retries=args.max_retries,
    )

    print(f"\n✅ Workflow generated: {args.output}")
    print(f"   Steps: {len(workflow['steps'])}")
    print(f"   Name: {workflow['name']}")


if __name__ == "__main__":
    main()
