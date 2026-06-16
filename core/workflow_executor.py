#!/usr/bin/env python3
"""
core/workflow_executor.py
==========================
Executes dynamically generated evaluation workflows.

Loads a workflow JSON, executes each step in order, passes variables
between steps, handles conditions and errors, and logs execution details.

Usage:
    python core/workflow_executor.py \
        --workflow tests/test2/output/generated_workflow.json \
        --output tests/test2/output/execution_log.json
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

logger = logging.getLogger(__name__)

REPO_ROOT = Path(__file__).parent.parent

# Variable pattern: ${step_id.output.key} or ${variable_name}
VAR_PATTERN = re.compile(r"\$\{([^}]+)\}")


class WorkflowExecutor:
    """Executes a workflow JSON definition."""

    def __init__(self, workflow: Dict[str, Any], dry_run: bool = False):
        self.workflow = workflow
        self.variables: Dict[str, Any] = dict(workflow.get("variables", {}))
        self.step_results: Dict[str, Dict[str, Any]] = {}
        self.execution_log: List[Dict[str, Any]] = []
        self.dry_run = dry_run

    def validate_inputs(self) -> List[str]:
        """Validate that all variables referenced in steps are available."""
        missing = set()
        for step in self.workflow.get("steps", []):
            params = step.get("params", {})
            # Check params for variable references
            def find_vars(value):
                if isinstance(value, str):
                    for match in VAR_PATTERN.finditer(value):
                        var_path = match.group(1)
                        if var_path.startswith("variables."):
                            var_path = var_path[len("variables."):]
                        # Only check top-level variables (not step outputs)
                        if "." not in var_path and var_path not in self.variables:
                            missing.add(var_path)
                elif isinstance(value, dict):
                    for v in value.values():
                        find_vars(v)
                elif isinstance(value, list):
                    for v in value:
                        find_vars(v)
            find_vars(params)
        return list(missing)

    ENV_PATTERN = re.compile(r"\$\{env\.([^}]+)\}")

    def _resolve_variables(self, value: Any) -> Any:
        """Resolve variable references in a value.
        
        If the value is a complete reference (e.g., ${step_id.result.key}),
        return the object as-is (preserving dicts, lists, etc.).
        If it's a partial reference (interpolated in a string), convert to string.
        Also resolves ${env.VAR_NAME} from environment variables.
        """
        if isinstance(value, str):
            # First resolve environment variables: ${env.VAR_NAME}
            value = self.ENV_PATTERN.sub(lambda m: os.environ.get(m.group(1), m.group(0)), value)

            # Check if the entire value is a single variable reference
            if VAR_PATTERN.fullmatch(value):
                var_path = VAR_PATTERN.search(value).group(1)
                # Handle ${variables.key} syntax by stripping prefix
                if var_path.startswith("variables."):
                    var_path = var_path[len("variables."):]
                
                parts = var_path.split(".")
                if len(parts) >= 3 and parts[1] in ("output", "result"):
                    step_id = parts[0]
                    key = ".".join(parts[2:])
                    if step_id in self.step_results:
                        # First try result, then output (return as-is, preserving type)
                        val = self.step_results[step_id].get("result", {})
                        for k in key.split("."):
                            if isinstance(val, dict):
                                val = val.get(k)
                            else:
                                val = None
                                break
                        if val is not None:
                            return val  # Return object as-is
                        # Fallback to output mapping
                        val = self.step_results[step_id].get("output", {})
                        for k in key.split("."):
                            if isinstance(val, dict):
                                val = val.get(k)
                            else:
                                return None
                        return val  # Return object as-is
                elif var_path in self.variables:
                    return self.variables[var_path]  # Return object as-is
                return None
            
            # Partial reference (interpolated in a string): convert to string
            def replacer(match):
                var_path = match.group(1)
                # Handle ${variables.key} syntax by stripping prefix
                if var_path.startswith("variables."):
                    var_path = var_path[len("variables."):]
                
                parts = var_path.split(".")
                if len(parts) >= 3 and parts[1] in ("output", "result"):
                    step_id = parts[0]
                    key = ".".join(parts[2:])
                    if step_id in self.step_results:
                        # First try result, then output
                        val = self.step_results[step_id].get("result", {})
                        for k in key.split("."):
                            if isinstance(val, dict):
                                val = val.get(k)
                            else:
                                val = None
                                break
                        if val is not None:
                            return str(val)
                        # Fallback to output mapping
                        val = self.step_results[step_id].get("output", {})
                        for k in key.split("."):
                            if isinstance(val, dict):
                                val = val.get(k)
                            else:
                                return match.group(0)
                        return str(val) if val is not None else match.group(0)
                elif var_path in self.variables:
                    return str(self.variables[var_path])
                return match.group(0)
            return VAR_PATTERN.sub(replacer, value)
        elif isinstance(value, dict):
            return {k: self._resolve_variables(v) for k, v in value.items()}
        elif isinstance(value, list):
            return [self._resolve_variables(v) for v in value]
        return value

    def _evaluate_condition(self, condition: Optional[Dict]) -> bool:
        """Evaluate a step condition."""
        if not condition:
            return True
        expr = condition.get("if", "true")
        resolved = self._resolve_variables(expr)
        # Simple boolean evaluation
        return resolved.lower() in ("true", "1", "yes") if isinstance(resolved, str) else bool(resolved)

    def _execute_tool(self, tool_name: str, params: Dict[str, Any]) -> Dict[str, Any]:
        """Execute a tool by name with resolved parameters."""
        if self.dry_run:
            logger.info("[DRY RUN] Would execute tool: %s with params: %s", tool_name, params)
            return {"result": {"dry_run": True}}

        from core.tool_registry import registry
        return registry.execute(tool_name, **params)

    def execute(self) -> Dict[str, Any]:
        """Execute the workflow and return the execution log."""
        workflow_name = self.workflow.get("name", "unknown")
        workflow_version = self.workflow.get("version", "unknown")
        
        logger.info("Starting workflow: %s (v%s)", workflow_name, workflow_version)
        
        # Validate inputs before execution
        missing_vars = self.validate_inputs()
        if missing_vars:
            logger.error("Missing required variables: %s", ", ".join(missing_vars))
            return {"status": "failed", "error": f"Missing variables: {missing_vars}", "log": []}
        
        logger.info("Runtime variables: %s", json.dumps({k: v for k, v in self.variables.items() if k in ["input_docx", "output_dir", "input_rubric"]}, indent=2))
        
        start_time = time.time()

        for step in self.workflow.get("steps", []):
            step_id = step["id"]
            tool_name = step["tool"]
            on_error = step.get("on_error", "abort")
            max_retries = step.get("max_retries", 0)

            # Check condition
            if not self._evaluate_condition(step.get("condition")):
                logger.info("Step %s skipped (condition not met)", step_id)
                self.execution_log.append({"step": step_id, "status": "skipped", "reason": "condition_false"})
                continue

            # Resolve parameters
            params = self._resolve_variables(step.get("params", {}))

            # Execute with retries
            success = False
            for attempt in range(max_retries + 1):
                try:
                    logger.info("Executing step %s: %s (attempt %d)", step_id, tool_name, attempt + 1)
                    result = self._execute_tool(tool_name, params)
                    self.step_results[step_id] = {
                        "output": self._resolve_variables(step.get("output", {})),
                        "result": result.get("result", {})
                    }
                    self.execution_log.append({
                        "step": step_id,
                        "tool": tool_name,
                        "status": "success",
                        "attempt": attempt + 1,
                        "duration": time.time() - start_time
                    })
                    success = True
                    break
                except Exception as e:
                    logger.warning("Step %s failed (attempt %d): %s", step_id, attempt + 1, e)
                    if attempt == max_retries:
                        if on_error == "skip":
                            logger.info("Step %s skipped after failure", step_id)
                            self.execution_log.append({"step": step_id, "status": "skipped", "reason": str(e)})
                            success = True  # Consider skipped as success for flow
                        elif on_error == "abort":
                            logger.error("Workflow aborted at step %s", step_id)
                            self.execution_log.append({"step": step_id, "status": "aborted", "reason": str(e)})
                            return {"status": "aborted", "log": self.execution_log}
                        else:
                            self.execution_log.append({"step": step_id, "status": "failed", "reason": str(e)})
                            return {"status": "failed", "log": self.execution_log}
                    time.sleep(1)  # Wait before retry

            if not success and on_error == "skip":
                self.execution_log.append({"step": step_id, "status": "skipped", "reason": "max_retries_exceeded"})

        total_duration = time.time() - start_time
        logger.info("Workflow completed in %.1fs", total_duration)
        return {"status": "completed", "log": self.execution_log, "duration": total_duration}


def main() -> None:
    parser = argparse.ArgumentParser(description="Execute a workflow JSON.")
    parser.add_argument("--workflow", type=str, required=True, help="Path to workflow JSON")
    parser.add_argument("--output", type=str, default=None, help="Path to write execution log")
    parser.add_argument("--dry-run", action="store_true", help="Simulate execution without running tools")
    args = parser.parse_args()

    logging.basicConfig(level=logging.INFO, format="%(levelname)s: %(message)s")

    with open(args.workflow) as f:
        workflow = json.load(f)

    executor = WorkflowExecutor(workflow, dry_run=args.dry_run)
    result = executor.execute()

    if args.output:
        out_path = Path(args.output)
        out_path.parent.mkdir(parents=True, exist_ok=True)
        out_path.write_text(json.dumps(result, ensure_ascii=False, indent=2), encoding="utf-8")
        logger.info("Execution log saved to %s", out_path)

    print(f"\n✅ Workflow execution: {result['status']}")
    print(f"   Steps executed: {len(result['log'])}")


if __name__ == "__main__":
    main()
