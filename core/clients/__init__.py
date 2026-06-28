from core.clients.base import BaseLLMClient
from core.clients.dashscope_client import DashScopeClient
from core.clients.ollama_client import OllamaClient

__all__ = ["BaseLLMClient", "DashScopeClient", "OllamaClient", "get_client"]

import os

def get_client() -> BaseLLMClient:
    """Factory function to get the appropriate LLM client based on the environment."""
    provider = os.environ.get("LLM_PROVIDER", "dashscope").lower()
    if provider == "ollama":
        return OllamaClient()
    return DashScopeClient()
