"""
Models module for CaiFramework.

This module provides model providers for local LLM integration
with Ollama and llama.cpp.
"""

from .chatcompletions import ChatCompletionsModel
from .interface import Model, ModelProvider, ModelTracing
from .llamacpp_provider import LlamaCppProvider, create_llamacpp_model
from .ollama_provider import OllamaProvider, create_ollama_model

__all__ = [
    "Model",
    "ModelProvider",
    "ModelTracing",
    "ChatCompletionsModel",
    "OllamaProvider",
    "create_ollama_model",
    "LlamaCppProvider",
    "create_llamacpp_model",
]
