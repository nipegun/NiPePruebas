"""
llama.cpp Model Provider for CaiFramework

This module provides integration with llama.cpp server, allowing CAI agents
to use LLMs through llama.cpp's OpenAI-compatible API server.
"""

from __future__ import annotations

import os
from typing import Optional

import httpx
from openai import AsyncOpenAI, DefaultAsyncHttpxClient

from .interface import Model, ModelProvider
from .chatcompletions import ChatCompletionsModel

# Default llama.cpp configuration
DEFAULT_LLAMACPP_MODEL: str = "local-model"
DEFAULT_LLAMACPP_BASE_URL: str = "http://localhost:8080/v1"


_llamacpp_http_client: httpx.AsyncClient | None = None


def get_llamacpp_http_client() -> httpx.AsyncClient:
    """
    Get or create a shared HTTP client for llama.cpp requests.
    
    This ensures connection pooling for better performance.
    """
    global _llamacpp_http_client
    if _llamacpp_http_client is None:
        _llamacpp_http_client = DefaultAsyncHttpxClient(
            timeout=httpx.Timeout(600.0, connect=120.0)  # Very long timeout for local inference
        )
    return _llamacpp_http_client


class LlamaCppProvider(ModelProvider):
    """
    llama.cpp Model Provider.
    
    Provides access to LLMs running through llama.cpp's server with OpenAI-compatible API.
    
    Prerequisites:
        1. Build llama.cpp with server support:
           ```bash
           git clone https://github.com/ggerganov/llama.cpp
           cd llama.cpp
           make -j
           ```
        
        2. Download a GGUF model (e.g., from Hugging Face)
        
        3. Start the llama.cpp server:
           ```bash
           ./llama-server -m models/llama-3.2-8b-q4_k_m.gguf \
                          --host 0.0.0.0 --port 8080 \
                          --ctx-size 4096 --n-gpu-layers 35
           ```
    
    Usage:
        # Set environment variables
        export LLAMACPP_API_BASE="http://localhost:8080/v1"
        export LLAMACPP_MODEL="local-model"
        export LLAMACPP="true"
        
        # Or use programmatically
        from cai.sdk.agents.models.llamacpp_provider import LlamaCppProvider
        
        provider = LlamaCppProvider(
            base_url="http://localhost:8080/v1",
            model_name="local-model"
        )
        model = provider.get_model()
        
    Environment Variables:
        LLAMACPP_API_BASE: Base URL for llama.cpp server (default: http://localhost:8080/v1)
        LLAMACPP_MODEL: Model name to use (default: local-model)
        LLAMACPP: Set to "true" to enable llama.cpp mode
        
    Server Arguments:
        Common llama.cpp server arguments:
        -m, --model: Path to the model file (GGUF format)
        --host: IP address to bind (default: 127.0.0.1)
        --port: Port to listen on (default: 8080)
        --ctx-size: Context size (default: 512)
        --n-gpu-layers: Number of layers to offload to GPU
        --n-threads: Number of threads to use for generation
        --batch-size: Batch size for prompt processing
        
    Performance Tips:
        - Use quantized GGUF models (Q4_K_M, Q5_K_M, Q6_K) for better performance
        - Offload layers to GPU with --n-gpu-layers for faster inference
        - Increase --ctx-size for longer context windows
        - Adjust --n-threads based on your CPU cores
    """

    def __init__(
        self,
        *,
        base_url: Optional[str] = None,
        model_name: Optional[str] = None,
        api_key: str = "llamacpp",  # llama.cpp doesn't require a real API key
        timeout: float = 600.0,
        context_size: Optional[int] = None,
    ) -> None:
        """
        Initialize llama.cpp provider.
        
        Args:
            base_url: llama.cpp server base URL. If not provided, uses LLAMACPP_API_BASE
                     env var or defaults to http://localhost:8080/v1
            model_name: Model name (usually "local-model" for llama.cpp). If not provided,
                       uses LLAMACPP_MODEL env var or defaults to local-model
            api_key: API key (not used by llama.cpp, but required by OpenAI client)
            timeout: Request timeout in seconds (default: 600.0)
            context_size: Context window size (optional, for tracking purposes)
        """
        self._base_url = base_url or os.environ.get(
            "LLAMACPP_API_BASE", DEFAULT_LLAMACPP_BASE_URL
        )
        self._default_model = model_name or os.environ.get(
            "LLAMACPP_MODEL", DEFAULT_LLAMACPP_MODEL
        )
        self._api_key = api_key
        self._timeout = timeout
        self._context_size = context_size
        self._client: AsyncOpenAI | None = None
        
        # Set the LLAMACPP environment variable to enable llama.cpp-specific handling
        os.environ["LLAMACPP"] = "true"

    def _get_client(self) -> AsyncOpenAI:
        """
        Get or create the llama.cpp client.
        
        Returns:
            AsyncOpenAI client configured for llama.cpp
        """
        if self._client is None:
            self._client = AsyncOpenAI(
                api_key=self._api_key,
                base_url=self._base_url,
                http_client=get_llamacpp_http_client(),
            )
        return self._client

    def get_model(self, model_name: str | None = None) -> Model:
        """
        Get a llama.cpp model instance.
        
        Args:
            model_name: Name of the model to use. If not provided,
                       uses the default model specified in __init__
                       (usually "local-model" for llama.cpp)
                       
        Returns:
            ChatCompletionsModel configured for llama.cpp
            
        Examples:
            >>> provider = LlamaCppProvider()
            >>> model = provider.get_model()
            >>> model = provider.get_model("local-model")
        """
        if model_name is None:
            model_name = self._default_model

        client = self._get_client()

        return ChatCompletionsModel(
            model=model_name,
            openai_client=client,
        )

    async def get_server_info(self) -> dict:
        """
        Get information about the running llama.cpp server.
        
        This queries the /health endpoint to check server status.
        
        Returns:
            Dictionary with server information
            
        Example:
            >>> provider = LlamaCppProvider()
            >>> info = await provider.get_server_info()
            >>> print(info)
        """
        import httpx
        
        health_url = self._base_url.replace("/v1", "/health")
        async with httpx.AsyncClient() as client:
            try:
                response = await client.get(health_url)
                return response.json()
            except Exception as e:
                return {"error": str(e), "status": "unavailable"}


# Convenience function for quick llama.cpp setup
def create_llamacpp_model(
    model_name: Optional[str] = None,
    base_url: Optional[str] = None,
    context_size: Optional[int] = None,
) -> Model:
    """
    Create a llama.cpp model with minimal configuration.
    
    Args:
        model_name: Model name (default: from LLAMACPP_MODEL env or local-model)
        base_url: llama.cpp server base URL (default: from LLAMACPP_API_BASE env or http://localhost:8080/v1)
        context_size: Context window size (optional)
        
    Returns:
        ChatCompletionsModel configured for llama.cpp
        
    Example:
        >>> from cai.sdk.agents.models.llamacpp_provider import create_llamacpp_model
        >>> model = create_llamacpp_model()
    """
    provider = LlamaCppProvider(
        base_url=base_url,
        model_name=model_name,
        context_size=context_size,
    )
    return provider.get_model()


# Helper function to start llama.cpp server programmatically (advanced usage)
def get_llamacpp_server_command(
    model_path: str,
    host: str = "0.0.0.0",
    port: int = 8080,
    ctx_size: int = 4096,
    n_gpu_layers: int = 35,
    threads: Optional[int] = None,
    batch_size: int = 512,
) -> str:
    """
    Generate a llama.cpp server command with the given parameters.
    
    Args:
        model_path: Path to the GGUF model file
        host: Host to bind to (default: 0.0.0.0)
        port: Port to listen on (default: 8080)
        ctx_size: Context size (default: 4096)
        n_gpu_layers: Number of GPU layers to offload (default: 35)
        threads: Number of CPU threads (default: auto)
        batch_size: Batch size (default: 512)
        
    Returns:
        Command string to start llama.cpp server
        
    Example:
        >>> cmd = get_llamacpp_server_command("models/llama-3.2-8b-q4_k_m.gguf")
        >>> print(cmd)
        ./llama-server -m models/llama-3.2-8b-q4_k_m.gguf --host 0.0.0.0 --port 8080 ...
    """
    cmd_parts = [
        "./llama-server",
        f"-m {model_path}",
        f"--host {host}",
        f"--port {port}",
        f"--ctx-size {ctx_size}",
        f"--n-gpu-layers {n_gpu_layers}",
        f"--batch-size {batch_size}",
    ]
    
    if threads is not None:
        cmd_parts.append(f"--n-threads {threads}")
    
    return " ".join(cmd_parts)
