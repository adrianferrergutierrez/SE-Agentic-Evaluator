"""
core/agent/agent.py
====================
The core Agent implementation (Fold Phase).

Implements the ~30-line agent loop described in the methodology.
Orchestrates LLM, Tools, Security, and Session Management.
"""

from __future__ import annotations

import logging
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple

import os
from core.clients.base import BaseLLMClient
from core.clients import get_client
from core.agent.security import SecurityPolicy
from core.agent.tools.adapter import ToolAdapter
from core.agent.session_store import SessionStore

logger = logging.getLogger(__name__)


class Agent:
    """
    The central Agent class.
    
    Attributes
    ----------
    llm : BaseLLMClient
        The LLM backend.
    tools : ToolAdapter
        Adapter exposing tools with schemas and security checks.
    system : str
        The static system prompt (skills + character + directives).
    security : SecurityPolicy
        Security policy for tool dispatching.
    session : SessionStore
        Storage for conversation history.
    """

    def __init__(
        self,
        llm: Optional[BaseLLMClient] = None,
        skills_dir: Optional[str] = None,
        security: Optional[SecurityPolicy] = None,
    ):
        # 1. LLM Client
        if llm is None:
            self.llm = get_client()
        else:
            self.llm = llm

        # 2. Security & Tools
        self.security = security or SecurityPolicy()
        self.tools = ToolAdapter(self.security)

        # 3. System Prompt Construction (Skills Injection)
        self.system = self._build_system_prompt(skills_dir)

        # 4. Session Store
        self.session = SessionStore()

        logger.info("Agent initialized with %d tools", len(self.tools.get_schemas()))

    def _build_system_prompt(self, skills_dir: Optional[str] = None) -> str:
        """Construct the system prompt by loading all skills from the directory."""
        skills_path = Path(skills_dir) if skills_dir else Path(__file__).parent / "skills"
        
        if not skills_path.exists():
            logger.warning(f"Skills directory not found: {skills_path}")
            return "You are a helpful assistant."

        parts = ["# System Instructions\n"]
        
        # Load all markdown files as skills
        for skill_file in sorted(skills_path.glob("*.md")):
            content = skill_file.read_text(encoding="utf-8")
            parts.append(f"## Skill: {skill_file.stem}\n\n{content}\n")
            logger.debug(f"Loaded skill: {skill_file.name}")

        return "\n".join(parts)

    def run(
        self, 
        user_message: str, 
        session_id: Optional[str] = None
    ) -> Tuple[str, str]:
        """
        Run the agent loop.
        
        Parameters
        ----------
        user_message : str
            The user's input.
        session_id : str, optional
            Existing session ID to continue, or None to start new.
            
        Returns
        -------
        Tuple[str, str]
            (final_response, session_id)
        """
        # 1. Initialize Session
        if not session_id:
            import uuid
            session_id = str(uuid.uuid4())
            
        messages = self.session.load(session_id)
        messages.append({"role": "user", "content": user_message})

        logger.info(f"Starting agent loop for session {session_id}")

        # 2. The Agent Loop (~30 lines)
        while True:
            # A. Call LLM (Static tools/system, growing messages)
            response = self.llm.chat(
                tools=self.tools.get_schemas(),
                system=self.system,
                messages=messages,
            )

            # B. Append Assistant Turn
            messages.append(response.assistant_turn())

            # C. Check for Tool Calls
            if not response.tool_calls:
                # No tools -> End of turn
                self.session.save(session_id, messages)
                return response.content, session_id

            # D. Process Tool Calls
            for tc in response.tool_calls:
                try:
                    # Security Check (Scaffolding responsibility)
                    self.security.check(tc.name, tc.arguments)
                    
                    # Dispatch Tool
                    result = self.tools.dispatch(tc.name, tc.arguments)
                    
                    # Append Tool Result
                    messages.append({
                        "role": "tool",
                        "tool_call_id": tc.id,
                        "content": str(result),
                    })
                except Exception as e:
                    logger.error(f"Tool execution failed: {e}")
                    messages.append({
                        "role": "tool",
                        "tool_call_id": tc.id,
                        "content": f"Error: {e}",
                    })
