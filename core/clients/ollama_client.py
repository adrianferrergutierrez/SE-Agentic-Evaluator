import json
import logging
import os
import uuid
from pathlib import Path
from typing import Any, Dict, List, Optional
import requests

from core.clients.base import BaseLLMClient, ChatResponse, ToolCall

logger = logging.getLogger(__name__)

class OllamaClient(BaseLLMClient):
    """Client for local Ollama API."""

    def __init__(self, base_url: Optional[str] = None):
        self.base_url = (base_url or os.environ.get("OLLAMA_BASE_URL", "http://localhost:11434")).rstrip("/")

    def chat(
        self,
        messages: List[Dict[str, Any]],
        tools: Optional[List[Dict[str, Any]]] = None,
        system: Optional[str] = None,
        model: str = "",
        temperature: float = 0.1,
        max_tokens: int = 4096,
    ) -> ChatResponse:
        model = model or os.environ.get("OLLAMA_MODEL", "llama3")
        
        final_messages = []
        if system:
            final_messages.append({"role": "system", "content": system})
        import copy
        for msg in messages:
            msg_copy = copy.deepcopy(msg)
            # Ollama requires tool call arguments to be dicts, not strings like OpenAI
            if msg_copy.get("role") == "assistant" and "tool_calls" in msg_copy:
                for tc in msg_copy["tool_calls"]:
                    func = tc.get("function", {})
                    args = func.get("arguments", {})
                    if isinstance(args, str):
                        try:
                            func["arguments"] = json.loads(args)
                        except json.JSONDecodeError:
                            pass
            final_messages.append(msg_copy)

        payload: Dict[str, Any] = {
            "model": model,
            "messages": final_messages,
            "options": {
                "temperature": temperature,
                "num_predict": max_tokens
            },
            "stream": False
        }

        if tools:
            # Ollama expects tools in the OpenAI format
            payload["tools"] = tools

        url = f"{self.base_url}/api/chat"
        response = requests.post(url, json=payload, timeout=1800)
        response.raise_for_status()
        data = response.json()

        message = data.get("message", {})
        content = message.get("content", "")
        tool_calls = []

        if "tool_calls" in message:
            for tc in message["tool_calls"]:
                func = tc.get("function", {})
                args = func.get("arguments", {})
                
                # Ollama can sometimes return arguments as a string, or a dict
                if isinstance(args, str):
                    try:
                        args = json.loads(args)
                    except json.JSONDecodeError:
                        args = {}
                
                # We generate a pseudo-ID because Ollama doesn't provide them natively
                tc_id = str(uuid.uuid4())
                
                tool_calls.append(ToolCall(
                    id=tc_id,
                    name=func.get("name", ""),
                    arguments=args
                ))

        # --- FALLBACK FOR LOCAL MODELS ---
        # If no native tool_calls were returned, check if the model hallucinated a JSON block in the text
        if not tool_calls and "```json" in content:
            import re
            match = re.search(r"```json\s*(\{.*?\})\s*```", content, re.DOTALL)
            if match:
                try:
                    parsed = json.loads(match.group(1))
                    if "name" in parsed and "arguments" in parsed:
                        logger.warning("Applying fallback JSON parser for hallucinated tool call.")
                        tool_calls.append(ToolCall(
                            id=str(uuid.uuid4()),
                            name=parsed["name"],
                            arguments=parsed["arguments"]
                        ))
                        # Optional: Remove the JSON block from content so the user doesn't see raw JSON
                        content = content.replace(match.group(0), "").strip()
                except json.JSONDecodeError:
                    pass
        # ---------------------------------

        logger.info(
            "Ollama '%s': %d eval tokens, %d tool_calls",
            model,
            data.get("eval_count", 0),
            len(tool_calls),
        )

        return ChatResponse(content=content, tool_calls=tool_calls)

    def generate(
        self,
        model: str = "",
        prompt: str = "",
        system_prompt: Optional[str] = None,
        temperature: float = 0.1,
        max_tokens: int = 4096,
        **kwargs: Any,
    ) -> str:
        messages = [{"role": "user", "content": prompt}]
        response = self.chat(
            messages=messages,
            system=system_prompt,
            model=model,
            temperature=temperature,
            max_tokens=max_tokens,
        )
        return response.content

    def vision(
        self,
        model: str = "",
        prompt: str = "",
        image_path: Optional[str | Path] = None,
        system_prompt: Optional[str] = None,
        **kwargs: Any,
    ) -> str:
        """Analyze an image using a local Ollama vision model."""
        model = model or os.environ.get("OLLAMA_VISION_MODEL", "llava")
        
        messages = []
        if system_prompt:
            messages.append({"role": "system", "content": system_prompt})
            
        user_message: Dict[str, Any] = {"role": "user", "content": prompt}
        
        if image_path:
            import base64
            img_path = Path(image_path)
            if not img_path.exists():
                raise FileNotFoundError(f"Image not found: {img_path}")
                
            with open(img_path, "rb") as f:
                b64_data = base64.b64encode(f.read()).decode("utf-8")
                
            user_message["images"] = [b64_data]
            
        messages.append(user_message)
        
        payload: Dict[str, Any] = {
            "model": model,
            "messages": messages,
            "stream": False,
        }
        if kwargs:
            payload["options"] = kwargs
            
        url = f"{self.base_url}/api/chat"
        response = requests.post(url, json=payload, timeout=1800)
        response.raise_for_status()
        data = response.json()
        
        return data.get("message", {}).get("content", "")

    def check_connection(self) -> bool:
        try:
            url = f"{self.base_url}/api/tags"
            response = requests.get(url, timeout=5)
            return response.status_code == 200
        except Exception as exc:
            logger.error("Ollama connection check failed: %s", exc)
            return False
