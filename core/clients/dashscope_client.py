#!/usr/bin/env python3
"""
core/clients/dashscope_client.py
=================================
DashScope API client for Qwen models (Alibaba Cloud).

Supports text generation, vision, and function calling for Agents.
"""

from __future__ import annotations

import json
import logging
import os
import time
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any, Dict, List, Optional

import requests

logger = logging.getLogger(__name__)

DASHSCOPE_ENDPOINTS = {
    "singapore": "https://dashscope-intl.aliyuncs.com/compatible-mode/v1",
    "us": "https://dashscope-us.aliyuncs.com/compatible-mode/v1",
    "china": "https://dashscope.aliyuncs.com/compatible-mode/v1",
}

DEFAULT_MODEL = os.environ.get("DASHSCOPE_MODEL", "qwen3.6-plus")
DEFAULT_ENDPOINT = os.environ.get("DASHSCOPE_ENDPOINT", "singapore")

# Retry configuration
RETRY_CONFIG = {
    "max_retries": 5,
    "base_delay": 1.0,
    "max_delay": 120.0,
    "backoff_factor": 2.0,
}
MAX_VISION_PAYLOAD_SIZE = 10 * 1024 * 1024  # 10 MB


@dataclass
class ToolCall:
    """Represents a tool call requested by the LLM."""
    id: str
    name: str
    arguments: Dict[str, Any]


@dataclass
class ChatResponse:
    """Structured response from the LLM."""
    content: str
    tool_calls: List[ToolCall] = field(default_factory=list)

    def assistant_turn(self) -> Dict[str, Any]:
        """Format the response as an assistant message for the history."""
        msg = {"role": "assistant", "content": self.content}
        if self.tool_calls:
            msg["tool_calls"] = [
                {
                    "id": tc.id,
                    "type": "function",
                    "function": {"name": tc.name, "arguments": json.dumps(tc.arguments)},
                }
                for tc in self.tool_calls
            ]
        return msg


class DashScopeClient:
    """Client for DashScope API (Qwen models via Alibaba Cloud)."""

    def __init__(
        self,
        api_key: Optional[str] = None,
        base_url: Optional[str] = None,
        region: Optional[str] = None,
    ):
        self.api_key = api_key or os.environ.get("DASHSCOPE_API_KEY", "")
        self.region = (region or os.environ.get("DASHSCOPE_REGION", "singapore")).lower()
        self.base_url = (
            base_url
            or os.environ.get("DASHSCOPE_BASE_URL", "")
            or DASHSCOPE_ENDPOINTS.get(self.region, DASHSCOPE_ENDPOINTS["singapore"])
        ).rstrip("/")
        self.session = requests.Session()
        self.session.headers.update({
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json",
        })

    def _check_api_key(self) -> None:
        if not self.api_key:
            raise ValueError("DashScope API key not set.")

    def _post_with_retry(
        self,
        url: str,
        payload: Dict[str, Any],
        timeout: int = 120,
        max_retries: int = RETRY_CONFIG["max_retries"],
        base_delay: float = RETRY_CONFIG["base_delay"],
        max_delay: float = RETRY_CONFIG["max_delay"],
        backoff_factor: float = RETRY_CONFIG["backoff_factor"],
    ) -> requests.Response:
        """Send POST request with exponential backoff retry logic."""
        payload_size = len(json.dumps(payload).encode("utf-8"))
        logger.debug(f"Payload size: {payload_size / 1024:.2f} KB")
        
        if payload_size > MAX_VISION_PAYLOAD_SIZE:
            raise ValueError(f"Payload size {payload_size / 1024 / 1024:.2f} MB exceeds limit.")
        
        delay = base_delay
        last_exception = None
        
        for attempt in range(max_retries + 1):
            try:
                response = self.session.post(url, json=payload, timeout=timeout)
                response.raise_for_status()
                if attempt > 0:
                    logger.info(f"Request succeeded after {attempt} retries")
                return response
                
            except requests.exceptions.HTTPError as e:
                last_exception = e
                error_code = e.response.status_code
                error_text = e.response.text[:500]
                
                retryable = error_code in (408, 429, 500, 502, 503, 504)
                if error_code == 400:
                    logger.warning(f"[Attempt {attempt + 1}] 400 Bad Request. Payload: {payload_size / 1024:.2f} KB. Response: {error_text}")
                    retryable = True
                else:
                    logger.warning(f"[Attempt {attempt + 1}] HTTP {error_code}: {error_text}")
                
                if attempt >= max_retries:
                    logger.error(f"Max retries exhausted. Raising error.")
                    raise
                
                if not retryable:
                    logger.error(f"Non-retryable error {error_code}. Not retrying.")
                    raise
                
                # Parse suggested retry delay from 429 responses (e.g. Gemini "Please retry in 30.4s")
                suggested_delay = None
                if error_code == 429:
                    import re as _re
                    match = _re.search(r"retry in ([\d.]+)\s*s", error_text, _re.IGNORECASE)
                    if match:
                        suggested_delay = float(match.group(1))
                
                if suggested_delay:
                    wait_time = suggested_delay + 2.0
                    logger.info(f"Rate limited. Retrying in {wait_time:.1f}s (server suggested {suggested_delay:.1f}s)")
                else:
                    delay = min(max_delay, delay * backoff_factor)
                    wait_time = delay + (0.1 * (attempt + 1))
                    logger.info(f"Retrying in {wait_time:.2f}s")
                time.sleep(wait_time)
                
            except requests.exceptions.Timeout as e:
                last_exception = e
                if attempt >= max_retries:
                    raise
                delay = min(max_delay, delay * backoff_factor)
                wait_time = delay + (0.1 * (attempt + 1))
                logger.warning(f"Timeout. Retrying in {wait_time:.2f}s")
                time.sleep(wait_time)
                
            except requests.exceptions.RequestException as e:
                raise
        
        if last_exception:
            raise last_exception
        raise RuntimeError("Unknown error in _post_with_retry")

    def chat(
        self,
        messages: List[Dict[str, Any]],
        tools: Optional[List[Dict[str, Any]]] = None,
        system: Optional[str] = None,
        model: str = DEFAULT_MODEL,
        temperature: float = 0.1,
        max_tokens: int = 4096,
    ) -> ChatResponse:
        """Chat with the LLM supporting function calling."""
        self._check_api_key()

        final_messages = []
        if system:
            final_messages.append({"role": "system", "content": system})
        final_messages.extend(messages)

        payload: Dict[str, Any] = {
            "model": model,
            "messages": final_messages,
            "temperature": temperature,
            "max_tokens": max_tokens,
        }

        if tools:
            payload["tools"] = tools
            payload["tool_choice"] = "auto"

        url = f"{self.base_url}/chat/completions"
        response = self._post_with_retry(url, payload, timeout=300, max_retries=2)
        data = response.json()

        choice = data.get("choices", [{}])[0]
        message = choice.get("message", {})
        
        content = message.get("content", "")
        tool_calls = []
        
        if "tool_calls" in message:
            for tc in message["tool_calls"]:
                func = tc.get("function", {})
                try:
                    args = json.loads(func.get("arguments", "{}"))
                except json.JSONDecodeError:
                    args = {}
                
                tool_calls.append(ToolCall(
                    id=tc.get("id", ""),
                    name=func.get("name", ""),
                    arguments=args
                ))

        logger.info(
            "DashScope '%s': %d prompt tokens, %d completion tokens, %d tool_calls",
            model,
            data.get("usage", {}).get("prompt_tokens", 0),
            data.get("usage", {}).get("completion_tokens", 0),
            len(tool_calls),
        )

        return ChatResponse(content=content, tool_calls=tool_calls)

    def generate(
        self,
        model: str = DEFAULT_MODEL,
        prompt: str = "",
        system_prompt: Optional[str] = None,
        temperature: float = 0.1,
        max_tokens: int = 4096,
        **kwargs: Any,
    ) -> str:
        """Generate text using a Qwen model (Legacy wrapper around chat)."""
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
        model: str = os.environ.get("DASHSCOPE_VISION_MODEL", "qwen-vl-max"),
        prompt: str = "",
        image_path: Optional[str | Path] = None,
        system_prompt: Optional[str] = None,
        **kwargs: Any,
    ) -> str:
        """Analyze an image using a Qwen vision model."""
        self._check_api_key()

        if image_path:
            image_path = Path(image_path)
            if not image_path.exists():
                raise FileNotFoundError(f"Image not found: {image_path}")

            import base64
            file_size = image_path.stat().st_size
            suffix = image_path.suffix.lower()
            mime = "image/png" if suffix == ".png" else "image/jpeg"
            
            logger.debug(f"Processing image: {image_path.name} ({file_size / 1024:.1f} KB)")
            
            with open(image_path, "rb") as f:
                b64 = base64.b64encode(f.read()).decode("utf-8")
            data_url = f"data:{mime};base64,{b64}"

            messages: List[Dict[str, Any]] = []
            if system_prompt:
                messages.append({"role": "system", "content": system_prompt})
            messages.append({
                "role": "user",
                "content": [
                    {"type": "image_url", "image_url": {"url": data_url}},
                    {"type": "text", "text": prompt},
                ],
            })
        else:
            messages = [{"role": "user", "content": prompt}]

        payload: Dict[str, Any] = {
            "model": model,
            "messages": messages,
            "max_tokens": 2048,
            **kwargs,
        }

        url = f"{self.base_url}/chat/completions"
        response = self._post_with_retry(url, payload, timeout=120, max_retries=3)
        data = response.json()

        content = data.get("choices", [{}])[0].get("message", {}).get("content", "")
        if not content:
            raise ValueError(f"Empty response from DashScope vision model '{model}'")

        logger.info(
            "DashScope vision '%s': %d prompt tokens, %d completion tokens",
            model,
            data.get("usage", {}).get("prompt_tokens", 0),
            data.get("usage", {}).get("completion_tokens", 0),
        )
        return content

    def check_connection(self) -> bool:
        """Verify API key and connectivity."""
        try:
            self._check_api_key()
            self.generate(model=DEFAULT_MODEL, prompt="OK", max_tokens=10)
            return True
        except Exception as exc:
            logger.error("Connection check failed: %s", exc)
            return False

    def list_models(self) -> List[str]:
        """List available models."""
        self._check_api_key()
        url = f"{self.base_url}/models"
        response = self.session.get(url, timeout=30)
        response.raise_for_status()
        data = response.json()
        return [m.get("id", "") for m in data.get("data", [])]
