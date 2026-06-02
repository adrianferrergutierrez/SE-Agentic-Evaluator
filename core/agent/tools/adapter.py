"""
core/agent/tools/adapter.py
============================
Adapter for exposing existing tools to the Agent Loop.

Bridges the existing `core/tool_registry.py` with the Agent's requirements:
- JSON Schemas for function calling.
- Safe dispatching with security checks.
"""

from __future__ import annotations

import json
import logging
from typing import Any, Dict, List

from core.tool_registry import registry as global_registry
from core.agent.security import SecurityPolicy

logger = logging.getLogger(__name__)


class ToolAdapter:
    """Adapts the global tool registry for use by the Agent."""

    def __init__(self, security: SecurityPolicy):
        self.security = security
        self._tools = global_registry.list_all()
        
        # Auto-allow all registered tools (for development)
        for tool in self._tools:
            self.security.allow(tool.name)

    def get_schemas(self) -> List[Dict[str, Any]]:
        """Return JSON schemas for all allowed tools."""
        schemas = []
        for tool in self._tools:
            if tool.name in self.security.allowed_tools:
                # Extract required fields from parameter descriptions
                required = []
                properties = {}
                for param_name, param_desc in tool.params.items():
                    properties[param_name] = {
                        "type": "string",
                        "description": param_desc
                    }
                    if param_desc.upper().startswith("REQUIRED"):
                        required.append(param_name)
                
                # DashScope expects OpenAI-compatible format
                schema = {
                    "type": "function",
                    "function": {
                        "name": tool.name,
                        "description": tool.description,
                        "parameters": {
                            "type": "object",
                            "properties": properties,
                        },
                    }
                }
                if required:
                    schema["function"]["parameters"]["required"] = required
                schemas.append(schema)
        return schemas

    def dispatch(self, tool_name: str, arguments: Dict[str, Any]) -> Any:
        """
        Dispatch a tool call after security check.
        
        Parameters
        ----------
        tool_name : str
            Name of the tool to execute.
        arguments : dict
            Arguments to pass to the tool.
            
        Returns
        -------
        Any
            Result of the tool execution.
            
        Raises
        ------
        PermissionError
            If the tool is not allowed.
        ValueError
            If the tool is not found.
        """
        # 1. Security Check (Scaffolding responsibility)
        self.security.check(tool_name, arguments)
        
        # 2. Execution
        logger.info(f"Dispatching tool: {tool_name} with args: {arguments}")
        try:
            result = global_registry.execute(tool_name, **arguments)
            logger.info(f"Tool {tool_name} executed successfully.")
            return result
        except Exception as e:
            logger.error(f"Tool {tool_name} failed: {e}")
            raise
