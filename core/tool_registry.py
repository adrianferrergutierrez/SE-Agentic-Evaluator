#!/usr/bin/env python3
"""
core/tool_registry.py
======================
Central registry for all evaluation tools.

Provides a unified interface for tool discovery and execution.
Tools are registered with their metadata (params, outputs, description)
and an executor function.

Usage:
    from core.tool_registry import registry
    tool = registry.get("docx_extract")
    result = tool.execute(input="...", output_dir="...")
"""

from __future__ import annotations

import json
import logging
import os
from abc import ABC, abstractmethod
from pathlib import Path
from typing import Any, Callable, Dict, List, Optional

logger = logging.getLogger(__name__)


class Tool(ABC):
    """Abstract base class for evaluation tools."""

    @property
    @abstractmethod
    def name(self) -> str:
        """Unique tool identifier."""
        pass

    @property
    @abstractmethod
    def description(self) -> str:
        """Human-readable description."""
        pass

    @property
    @abstractmethod
    def category(self) -> str:
        """Tool category (extract, analyze, evaluate, etc.)."""
        pass

    @property
    @abstractmethod
    def params(self) -> Dict[str, str]:
        """Expected parameters with descriptions."""
        pass

    @property
    @abstractmethod
    def output(self) -> Dict[str, str]:
        """Expected output fields with descriptions."""
        pass

    @abstractmethod
    def execute(self, **kwargs: Any) -> Dict[str, Any]:
        """Execute the tool with given parameters."""
        pass

    def __repr__(self) -> str:
        return f"<Tool {self.name} ({self.category})>"


class ToolRegistry:
    """Registry for evaluation tools."""

    def __init__(self):
        self._tools: Dict[str, Tool] = {}

    def register(self, tool: Tool) -> None:
        """Register a tool."""
        self._tools[tool.name] = tool
        logger.info("Registered tool: %s", tool.name)

    def get(self, name: str) -> Optional[Tool]:
        """Get a tool by name."""
        return self._tools.get(name)

    def list_all(self) -> List[Tool]:
        """List all registered tools."""
        return list(self._tools.values())

    def list_by_category(self, category: str) -> List[Tool]:
        """List tools by category."""
        return [t for t in self._tools.values() if t.category == category]

    def execute(self, name: str, **kwargs: Any) -> Dict[str, Any]:
        """Execute a tool by name."""
        tool = self.get(name)
        if not tool:
            raise ValueError(f"Tool '{name}' not found in registry")
        return tool.execute(**kwargs)


# Global registry instance
registry = ToolRegistry()


# ---------------------------------------------------------------------------
# Concrete Tool Implementations
# ---------------------------------------------------------------------------

class ReadFileTool(Tool):
    @property
    def name(self) -> str: return "read_file"
    @property
    def description(self) -> str: return "Read the contents of a file (text files only)"
    @property
    def category(self) -> str: return "utility"
    @property
    def params(self) -> Dict[str, str]: return {
        "file_path": "Absolute or relative path to the file to read (must be a file, not a directory)"
    }
    @property
    def output(self) -> Dict[str, str]: return {"content": "File contents as text"}

    def execute(self, **kwargs: Any) -> Dict[str, Any]:
        from pathlib import Path
        file_path = Path(kwargs["file_path"])
        if not file_path.exists():
            raise FileNotFoundError(f"File not found: {file_path}")
        if file_path.is_dir():
            raise ValueError(f"Path is a directory, not a file: {file_path}")
        content = file_path.read_text(encoding="utf-8")
        return {"result": {"content": content, "size": len(content)}}


class ListDirectoryTool(Tool):
    @property
    def name(self) -> str: return "list_directory"
    @property
    def description(self) -> str: return "List files and subdirectories in a directory"
    @property
    def category(self) -> str: return "utility"
    @property
    def params(self) -> Dict[str, str]: return {
        "dir_path": "Absolute or relative path to the directory to list"
    }
    @property
    def output(self) -> Dict[str, str]: return {"files": "List of files", "dirs": "List of subdirectories"}

    def execute(self, **kwargs: Any) -> Dict[str, Any]:
        from pathlib import Path
        dir_path = Path(kwargs["dir_path"])
        if not dir_path.exists():
            raise FileNotFoundError(f"Directory not found: {dir_path}")
        if not dir_path.is_dir():
            raise ValueError(f"Path is not a directory: {dir_path}")
        files = [f.name for f in dir_path.iterdir() if f.is_file()]
        dirs = [d.name for d in dir_path.iterdir() if d.is_dir()]
        return {"result": {"files": sorted(files), "dirs": sorted(dirs)}}


class DocxExtractTool(Tool):
    @property
    def name(self) -> str: return "docx_extract"
    @property
    def description(self) -> str: return "Convert DOCX to Markdown with image extraction"
    @property
    def category(self) -> str: return "extract"
    @property
    def params(self) -> Dict[str, str]: return {"input": "DOCX path", "output_dir": "Output dir"}
    @property
    def output(self) -> Dict[str, str]: return {"contents_md": "Markdown path", "images": "Image count"}

    def execute(self, **kwargs: Any) -> Dict[str, Any]:
        from core.extraction.docx_extract import extract_docx
        result = extract_docx(kwargs["input"], kwargs["output_dir"])
        return {"result": result}


class RubricImporterTool(Tool):
    @property
    def name(self) -> str: return "rubric_importer"
    @property
    def description(self) -> str: return "Import Markdown rubric table to YAML config format. Use this when you have a rubric in Markdown format and need to convert it to YAML for evaluation."
    @property
    def category(self) -> str: return "config"
    @property
    def params(self) -> Dict[str, str]: return {
        "input": "REQUIRED: Path to the rubric Markdown file (e.g., 'rubrics/hito1.md'). Must be a file, not a directory.",
        "output": "REQUIRED: Path where the YAML config will be saved (e.g., 'configs/rubric_hito1.yaml'). Must end with .yaml extension."
    }
    @property
    def output(self) -> Dict[str, str]: return {"config_path": "Path to the generated YAML config file"}

    def execute(self, **kwargs: Any) -> Dict[str, Any]:
        from core.config.rubric_importer import import_rubric
        input_path = kwargs.get("input")
        output_path = kwargs.get("output")
        
        if not input_path:
            raise ValueError("Parameter 'input' is required (path to rubric Markdown file)")
        if not output_path:
            raise ValueError("Parameter 'output' is required (path to save YAML config)")
        
        input_path = Path(input_path)
        output_path = Path(output_path)
        
        if not input_path.exists():
            raise FileNotFoundError(f"Rubric file not found: {input_path}")
        if input_path.is_dir():
            raise ValueError(f"'input' must be a file, not a directory: {input_path}")
        
        output_path.parent.mkdir(parents=True, exist_ok=True)
        prompts_dir = str(output_path.parent / "prompts")
        import_rubric(str(input_path), str(output_path), prompts_dir)
        # Fix prompt paths
        import yaml
        with open(output_path) as f:
            cfg = yaml.safe_load(f)
        rubric_id = output_path.stem.replace("rubric_", "").replace("rubrica_", "")
        for criterion in cfg["rubric"]["criteria"]:
            criterion["prompt"] = f"{rubric_id}/" + criterion["prompt"]
        with open(output_path, "w") as f:
            yaml.dump(cfg, f, default_flow_style=False, allow_unicode=True)
        return {"result": {"config_path": str(output_path)}}


class ExtractObjectivesTool(Tool):
    @property
    def name(self) -> str: return "extract_objectives"
    @property
    def description(self) -> str: return "Extract objectives (OBJ-X) via LLM"
    @property
    def category(self) -> str: return "extract"
    @property
    def params(self) -> Dict[str, str]: return {"document": "Markdown path"}
    @property
    def output(self) -> Dict[str, str]: return {"markdown": "Extracted objectives MD"}

    def execute(self, **kwargs: Any) -> Dict[str, Any]:
        from core.extraction.objectives import extract_objectives
        from core.clients import get_client
        doc = Path(kwargs["document"]).read_text(encoding="utf-8")
        result = extract_objectives(doc, client=get_client())
        return {"result": {"markdown": result}}


class ExtractRequirementsTool(Tool):
    @property
    def name(self) -> str: return "extract_requirements"
    @property
    def description(self) -> str: return "Extract IRQ/NFR via LLM"
    @property
    def category(self) -> str: return "extract"
    @property
    def params(self) -> Dict[str, str]: return {"document": "Markdown path"}
    @property
    def output(self) -> Dict[str, str]: return {"markdown": "Extracted requirements MD"}

    def execute(self, **kwargs: Any) -> Dict[str, Any]:
        from core.extraction.requirements import extract_requirements
        from core.clients import get_client
        doc = Path(kwargs["document"]).read_text(encoding="utf-8")
        result = extract_requirements(doc, client=get_client())
        return {"result": {"markdown": result}}


class ExtractUseCasesTool(Tool):
    @property
    def name(self) -> str: return "extract_use_cases"
    @property
    def description(self) -> str: return "Extract use cases (CU-XXX) via LLM"
    @property
    def category(self) -> str: return "extract"
    @property
    def params(self) -> Dict[str, str]: return {"document": "Markdown path"}
    @property
    def output(self) -> Dict[str, str]: return {"markdown": "Extracted use cases MD"}

    def execute(self, **kwargs: Any) -> Dict[str, Any]:
        from core.extraction.use_cases import extract_use_cases
        from core.clients import get_client
        doc = Path(kwargs["document"]).read_text(encoding="utf-8")
        result = extract_use_cases(doc, client=get_client())
        return {"result": {"markdown": result}}


class DetectOrphansTool(Tool):
    @property
    def name(self) -> str: return "detect_orphans"
    @property
    def description(self) -> str: return "Detect orphan requirements/objectives"
    @property
    def category(self) -> str: return "analyze"
    @property
    def params(self) -> Dict[str, str]: return {"objectives_md": "Objectives MD", "requirements_md": "Requirements MD"}
    @property
    def output(self) -> Dict[str, str]: return {"markdown": "Orphan report MD"}

    def execute(self, **kwargs: Any) -> Dict[str, Any]:
        from core.analysis.orphans import detect_orphans
        report = detect_orphans(kwargs["objectives_md"], kwargs["requirements_md"])
        return {"result": {"markdown": report.as_markdown()}}


class EvaluateSmartTool(Tool):
    @property
    def name(self) -> str: return "evaluate_smart"
    @property
    def description(self) -> str: return "Evaluate objectives against SMART criteria"
    @property
    def category(self) -> str: return "analyze"
    @property
    def params(self) -> Dict[str, str]: return {"objectives_md": "Objectives MD"}
    @property
    def output(self) -> Dict[str, str]: return {"markdown": "SMART report MD"}

    def execute(self, **kwargs: Any) -> Dict[str, Any]:
        from core.analysis.smart import evaluate_objectives_smart, smart_summary_markdown
        scores = evaluate_objectives_smart(kwargs["objectives_md"])
        return {"result": {"markdown": smart_summary_markdown(scores)}}


class ClassifyIso25010Tool(Tool):
    @property
    def name(self) -> str: return "classify_iso25010"
    @property
    def description(self) -> str: return "Classify NFRs against ISO 25010"
    @property
    def category(self) -> str: return "analyze"
    @property
    def params(self) -> Dict[str, str]: return {"requirements_md": "Requirements MD"}
    @property
    def output(self) -> Dict[str, str]: return {"markdown": "ISO 25010 report MD"}

    def execute(self, **kwargs: Any) -> Dict[str, Any]:
        from core.analysis.iso25010 import classify_requirements_iso25010
        report = classify_requirements_iso25010(kwargs["requirements_md"])
        return {"result": {"markdown": report.as_markdown()}}


class BuildContextTool(Tool):
    @property
    def name(self) -> str: return "build_context"
    @property
    def description(self) -> str: return "Build consolidated analysis context"
    @property
    def category(self) -> str: return "analyze"
    @property
    def params(self) -> Dict[str, str]: return {
        "objectives_md": "Objectives MD",
        "requirements_md": "Requirements MD",
        "use_cases_md": "Use cases MD",
        "orphans_report": "Orphans report",
        "smart_report": "SMART report",
        "iso_report": "ISO report"
    }
    @property
    def output(self) -> Dict[str, str]: return {"markdown": "Context MD"}

    def execute(self, **kwargs: Any) -> Dict[str, Any]:
        parts = []
        for key, val in kwargs.items():
            if val and Path(val).exists():
                parts.append(f"### {key}\n\n{Path(val).read_text(encoding='utf-8')}")
            elif val:
                parts.append(f"### {key}\n\n{val}")
        return {"result": {"markdown": "\n\n".join(parts)}}


class CriterionEvaluatorTool(Tool):
    @property
    def name(self) -> str: return "criterion_evaluator"
    @property
    def description(self) -> str: return "Evaluate criteria against rubric via LLM"
    @property
    def category(self) -> str: return "evaluate"
    @property
    def params(self) -> Dict[str, str]: return {
        "document": "Markdown path",
        "config": "YAML config path",
        "full": "Boolean: run full analysis",
        "context": "Optional context path",
        "output_dir": "Output dir"
    }
    @property
    def output(self) -> Dict[str, str]: return {"scores": "Scores dict", "output_dir": "Output dir"}

    def execute(self, **kwargs: Any) -> Dict[str, Any]:
        from core.evaluation.criterion_evaluator import run_criterion_evaluation
        eval_params = {
            "document_path": kwargs["document"],
            "config_path": kwargs["config"],
            "output_dir": kwargs["output_dir"],
        }
        if kwargs.get("context"):
            eval_params["context_path"] = kwargs["context"]
        elif kwargs.get("full"):
            eval_params["full"] = True
        result = run_criterion_evaluation(**eval_params)
        return {"result": {"scores": result["scores"], "output_dir": kwargs["output_dir"]}}


class GraderTool(Tool):
    @property
    def name(self) -> str: return "grader"
    @property
    def description(self) -> str: return "Calculate weighted final grade"
    @property
    def category(self) -> str: return "grade"
    @property
    def params(self) -> Dict[str, str]: return {"scores": "Scores dict", "config": "YAML config path"}
    @property
    def output(self) -> Dict[str, str]: return {
        "weighted_final": "Final grade",
        "mean_xbar": "Mean score",
        "performance_level": "Performance label"
    }

    def execute(self, **kwargs: Any) -> Dict[str, Any]:
        from core.grading.grader import RubricGrader
        scores = kwargs["scores"]
        if isinstance(scores, str):
            # Try loading as JSON first
            try:
                scores_data = json.loads(scores)
                scores = scores_data.get("scores", scores_data)
            except json.JSONDecodeError:
                # Try loading as file path
                if Path(scores).exists():
                    with open(scores) as f:
                        scores_data = json.load(f)
                    scores = scores_data.get("scores", scores_data)
                else:
                    # Try parsing as Python dict string
                    import ast
                    try:
                        scores = ast.literal_eval(scores)
                    except (ValueError, SyntaxError):
                        raise ValueError(f"Cannot parse scores: {scores}")
        grader = RubricGrader.from_config(kwargs["config"])
        grading = grader.grade({}, scores=scores)
        return {"result": grading.as_dict()}


class WorkflowGeneratorTool(Tool):
    @property
    def name(self) -> str: return "generate_workflow"
    @property
    def description(self) -> str: return "Generate a reusable workflow JSON from a rubric. Use this when you need to create a new evaluation workflow for a specific rubric. The generated workflow can be reused for multiple documents."
    @property
    def category(self) -> str: return "generate"
    @property
    def params(self) -> Dict[str, str]: return {
        "rubric_path": "REQUIRED: Path to rubric YAML file (e.g., 'configs/rubric_hito1.yaml'). Must be a file, not a directory.",
        "output_path": "REQUIRED: Path where the workflow JSON will be saved (e.g., 'workflows/hito1.json'). Must end with .json extension.",
        "sample_doc": "OPTIONAL: Path to a sample document for context (e.g., 'docs/sample.md'). Helps the generator understand the document structure."
    }
    @property
    def output(self) -> Dict[str, str]: return {"workflow_path": "Path to the generated workflow JSON file"}

    def execute(self, **kwargs: Any) -> Dict[str, Any]:
        from core.meta_agent.workflow_generator import generate_workflow
        
        rubric_path = kwargs.get("rubric_path")
        output_path = kwargs.get("output_path")
        sample_doc = kwargs.get("sample_doc", "")
        
        if not rubric_path:
            raise ValueError("Parameter 'rubric_path' is required (path to rubric YAML file)")
        if not output_path:
            raise ValueError("Parameter 'output_path' is required (path to save workflow JSON)")
        
        rubric_path = Path(rubric_path)
        output_path = Path(output_path)
        
        if not rubric_path.exists():
            raise FileNotFoundError(f"Rubric file not found: {rubric_path}")
        if rubric_path.is_dir():
            raise ValueError(f"'rubric_path' must be a file, not a directory: {rubric_path}")
        
        output_path.parent.mkdir(parents=True, exist_ok=True)
        
        result = generate_workflow(
            rubric_path=str(rubric_path),
            output_path=str(output_path),
            document_path=sample_doc
        )
        return {"result": {"workflow_path": str(output_path)}}


class WorkflowExecutorTool(Tool):
    @property
    def name(self) -> str: return "execute_workflow"
    @property
    def description(self) -> str: return "Execute a pre-defined workflow JSON against a document"
    @property
    def category(self) -> str: return "execute"
    @property
    def params(self) -> Dict[str, str]: return {
        "workflow_path": "Path to workflow JSON",
        "input_doc": "Path to document to evaluate",
        "output_dir": "Directory for results",
        "rubric_path": "Path to rubric YAML file (optional, inferred from workflow metadata if omitted)"
    }
    @property
    def output(self) -> Dict[str, str]: return {"log_path": "Path to execution log"}

    def execute(self, **kwargs: Any) -> Dict[str, Any]:
        from core.workflow_executor import WorkflowExecutor
        import json
        from pathlib import Path

        workflow_path = Path(kwargs["workflow_path"])
        input_doc = Path(kwargs["input_doc"])
        output_dir = Path(kwargs["output_dir"])
        rubric_path = kwargs.get("rubric_path")
        
        output_dir.mkdir(parents=True, exist_ok=True)

        with open(workflow_path) as f:
            workflow = json.load(f)

        # Inject runtime variables
        workflow["variables"]["input_docx"] = str(input_doc)
        workflow["variables"]["output_dir"] = str(output_dir)
        
        # Inject rubric path if provided and exists, otherwise try to infer from metadata
        if rubric_path and Path(rubric_path).exists():
            workflow["variables"]["input_rubric"] = str(rubric_path)
        elif "metadata" in workflow and "rubric_id" in workflow["metadata"]:
            rubric_id = workflow["metadata"]["rubric_id"]
            candidates = [
                Path(f"configs/rubric_{rubric_id}.yaml"),
                Path(f"configs/rubrica_{rubric_id}.yaml"),
                input_doc.parent / f"rubric_{rubric_id}.yaml",
                input_doc.parent / f"rubrica_{rubric_id}.yaml",
                input_doc.parent.parent / f"rubric_{rubric_id}.yaml",
                input_doc.parent.parent / f"rubrica_{rubric_id}.yaml",
                Path.cwd() / f"rubric_{rubric_id}.yaml",
                Path.cwd() / f"rubrica_{rubric_id}.yaml",
                REPO_ROOT / "configs" / f"rubric_{rubric_id}.yaml",
                REPO_ROOT / "configs" / f"rubrica_{rubric_id}.yaml",
            ]
            for path in Path.cwd().rglob(f"rubrica_{rubric_id}.yaml"):
                candidates.append(path)
                break
            for path in Path.cwd().rglob(f"rubric_{rubric_id}.yaml"):
                candidates.append(path)
                break
            found = None
            for c in candidates:
                if c.exists():
                    found = c
                    break
            if found:
                workflow["variables"]["input_rubric"] = str(found)
            else:
                raise ValueError(
                    f"Rubric path not provided and cannot infer from metadata. "
                    f"Tried: {[str(c) for c in candidates]}"
                )
        else:
            raise ValueError(
                "Rubric path not provided and workflow has no metadata.rubric_id"
            )

        executor = WorkflowExecutor(workflow)
        result = executor.execute()
        
        log_path = output_dir / "execution_log.json"
        log_path.write_text(json.dumps(result, indent=2))
        return {"result": {"log_path": str(log_path), "status": result["status"]}}


class ReportGeneratorTool(Tool):
    @property
    def name(self) -> str: return "report_generator"
    @property
    def description(self) -> str: return "Generate final evaluation report"
    @property
    def category(self) -> str: return "report"
    @property
    def params(self) -> Dict[str, str]: return {
        "document": "Markdown path",
        "eval_dir": "Eval dir",
        "config": "YAML config path",
        "scores": "Scores path or dict",
        "output": "Report output path"
    }
    @property
    def output(self) -> Dict[str, str]: return {"report_path": "Report path"}

    def execute(self, **kwargs: Any) -> Dict[str, Any]:
        from core.evaluation.evaluator import run_report_generation
        run_report_generation(
            document_path=kwargs["document"],
            eval_dir=kwargs["eval_dir"],
            config_path=kwargs["config"],
            scores_path=kwargs.get("scores"),
            output_dir=str(Path(kwargs["output"]).parent),
        )
        return {"result": {"report_path": kwargs["output"]}}


class XlsxToMarkdownTool(Tool):
    @property
    def name(self) -> str: return "xlsx_to_markdown"
    @property
    def description(self) -> str: return "Convert Excel (.xlsx) rubric to Markdown"
    @property
    def category(self) -> str: return "extract"
    @property
    def params(self) -> Dict[str, str]: return {"input": "XLSX path", "output": "Markdown output path"}
    @property
    def output(self) -> Dict[str, str]: return {"markdown_path": "Markdown path"}

    def execute(self, **kwargs: Any) -> Dict[str, Any]:
        from core.extraction.xlsx_to_markdown import xlsx_to_markdown
        return {"result": xlsx_to_markdown(kwargs["input"], kwargs["output"])}


class DescribeDiagramsTool(Tool):
    @property
    def name(self) -> str: return "describe_diagrams"
    @property
    def description(self) -> str: return "Analyze diagram images and append textual descriptions"
    @property
    def category(self) -> str: return "extract"
    @property
    def params(self) -> Dict[str, str]: return {
        "document_path": "Path to Markdown file with images",
        "model": "Vision model (default: qwen3-vl-32b)",
        "prompt": "Custom prompt for vision model"
    }
    @property
    def output(self) -> Dict[str, str]: return {
        "updated_md": "Path to updated Markdown",
        "descriptions_count": "Number of images described"
    }

    def execute(self, **kwargs: Any) -> Dict[str, Any]:
        from core.extraction.diagramlens_tool import describe_diagrams
        
        call_kwargs = {}
        if "model" in kwargs and kwargs["model"]:
            call_kwargs["model"] = kwargs["model"]
            
        # Only pass prompt if it's explicitly provided (not None)
        if "prompt" in kwargs and kwargs["prompt"]:
            call_kwargs["prompt"] = kwargs["prompt"]
        
        return {"result": describe_diagrams(
            kwargs.get("document_path"),
            **call_kwargs
        )}


# ---------------------------------------------------------------------------
# Auto-registration
# ---------------------------------------------------------------------------

def register_all_tools() -> None:
    """Register all built-in tools."""
    tools = [
        DocxExtractTool(),
        XlsxToMarkdownTool(),
        DescribeDiagramsTool(),
        RubricImporterTool(),
        ExtractObjectivesTool(),
        ExtractRequirementsTool(),
        ExtractUseCasesTool(),
        DetectOrphansTool(),
        EvaluateSmartTool(),
        ClassifyIso25010Tool(),
        BuildContextTool(),
        CriterionEvaluatorTool(),
        GraderTool(),
        ReportGeneratorTool(),
        # New Agent-focused tools
        WorkflowGeneratorTool(),
        WorkflowExecutorTool(),
        # Utility tools
        ReadFileTool(),
        ListDirectoryTool(),
    ]
    for tool in tools:
        registry.register(tool)


# Register tools on module import
register_all_tools()
