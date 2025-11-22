"""
Ollama Model Provider for CaiFramework

This module provides integration with Ollama, allowing CAI agents to use
locally hosted LLMs through Ollama's API (compatible with OpenAI).
"""

from __future__ import annotations

import os
from typing import Optional

import httpx
from openai import AsyncOpenAI, DefaultAsyncHttpxClient

from .interface import Model, ModelProvider
from .chatcompletions import ChatCompletionsModel

# Default Ollama configuration
DEFAULT_OLLAMA_MODEL: str = "llama3.2"
DEFAULT_OLLAMA_BASE_URL: str = "http://localhost:11434/v1"


_ollama_http_client: httpx.AsyncClient | None = None


def get_ollama_http_client() -> httpx.AsyncClient:
    """
    Get or create a shared HTTP client for Ollama requests.
    
    This ensures connection pooling for better performance.
    """
    global _ollama_http_client
    if _ollama_http_client is None:
        _ollama_http_client = DefaultAsyncHttpxClient(
            timeout=httpx.Timeout(300.0, connect=60.0)  # Longer timeout for local models
        )
    return _ollama_http_client


class OllamaProvider(ModelProvider):
    """
    Ollama Model Provider.
    
    Provides access to locally hosted LLMs through Ollama's OpenAI-compatible API.
    
    Usage:
        # Set environment variables
        export OLLAMA_API_BASE="http://localhost:11434/v1"
        export OLLAMA_MODEL="llama3.2"
        export OLLAMA="true"
        
        # Or use programmatically
        from cai.sdk.agents.models.ollama_provider import OllamaProvider
        
        provider = OllamaProvider(
            base_url="http://localhost:11434/v1",
            model_name="llama3.2"
        )
        model = provider.get_model()
        
    Environment Variables:
        OLLAMA_API_BASE: Base URL for Ollama API (default: http://localhost:11434/v1)
        OLLAMA_MODEL: Default model name (default: llama3.2)
        OLLAMA: Set to "true" to enable Ollama mode
        
    Supported Models:
        - llama3.2, llama3.2:latest
        - llama3.1, llama3.1:70b
        - codellama, codellama:13b, codellama:34b
        - mistral, mistral:7b
        - mixtral, mixtral:8x7b
        - qwen2.5, qwen2.5:14b, qwen2.5:32b
        - deepseek-coder:6.7b, deepseek-coder:33b
        - And any other model available in Ollama
    """

    def __init__(
        self,
        *,
        base_url: Optional[str] = None,
        model_name: Optional[str] = None,
        api_key: str = "ollama",  # Ollama doesn't require a real API key
        timeout: float = 300.0,
    ) -> None:
        """
        Initialize Ollama provider.
        
        Args:
            base_url: Ollama API base URL. If not provided, uses OLLAMA_API_BASE env var
                     or defaults to http://localhost:11434/v1
            model_name: Default model name. If not provided, uses OLLAMA_MODEL env var
                       or defaults to llama3.2
            api_key: API key (not used by Ollama, but required by OpenAI client)
            timeout: Request timeout in seconds (default: 300.0)
        """
        self._base_url = base_url or os.environ.get(
            "OLLAMA_API_BASE", DEFAULT_OLLAMA_BASE_URL
        )
        self._default_model = model_name or os.environ.get(
            "OLLAMA_MODEL", DEFAULT_OLLAMA_MODEL
        )
        self._api_key = api_key
        self._timeout = timeout
        self._client: AsyncOpenAI | None = None
        
        # Set the OLLAMA environment variable to enable Ollama-specific handling
        os.environ["OLLAMA"] = "true"

    def _get_client(self) -> AsyncOpenAI:
        """
        Get or create the Ollama client.
        
        Returns:
            AsyncOpenAI client configured for Ollama
        """
        if self._client is None:
            self._client = AsyncOpenAI(
                api_key=self._api_key,
                base_url=self._base_url,
                http_client=get_ollama_http_client(),
            )
        return self._client

    def get_model(self, model_name: str | None = None) -> Model:
        """
        Get an Ollama model instance.
        
        Args:
            model_name: Name of the Ollama model to use. If not provided,
                       uses the default model specified in __init__
                       
        Returns:
            ChatCompletionsModel configured for Ollama
            
        Examples:
            >>> provider = OllamaProvider()
            >>> model = provider.get_model("llama3.2")
            >>> model = provider.get_model("codellama:13b")
            >>> model = provider.get_model("mistral:7b")
        """
        if model_name is None:
            model_name = self._default_model

        client = self._get_client()

        return ChatCompletionsModel(
            model=model_name,  # Use model name directly with Ollama client
            openai_client=client,
        )

    def list_models(self) -> list[str]:
        """
        List available Ollama models.
        
        This is a helper method that could be implemented to query Ollama's
        /api/tags endpoint, but requires additional HTTP calls.
        
        Returns:
            List of available model names
        """
        # This would require making a request to http://localhost:11434/api/tags
        # For now, return common models
        return [
            "llama3.2",
            "llama3.1",
            "codellama",
            "mistral",
            "mixtral",
            "qwen2.5",
            "deepseek-coder",
        ]


# Convenience function for quick Ollama setup
def create_ollama_model(
    model_name: Optional[str] = None,
    base_url: Optional[str] = None,
) -> Model:
    """
    Create an Ollama model with minimal configuration.
    
    Args:
        model_name: Ollama model name (default: from OLLAMA_MODEL env or llama3.2)
        base_url: Ollama API base URL (default: from OLLAMA_API_BASE env or http://localhost:11434/v1)
        
    Returns:
        ChatCompletionsModel configured for Ollama
        
    Example:
        >>> from cai.sdk.agents.models.ollama_provider import create_ollama_model
        >>> model = create_ollama_model("llama3.2")
    """
    provider = OllamaProvider(base_url=base_url, model_name=model_name)
    return provider.get_model()
