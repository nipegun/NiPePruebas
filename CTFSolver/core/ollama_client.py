#!/usr/bin/env python3
"""
Cliente Ollama para PHAH
Gestiona la comunicación con el servidor LLM local de Ollama
Basado en la arquitectura de integración de Ollama de CaiFramework
"""

import os
import json
import httpx
from typing import Optional, List, Dict, Any


class OllamaClient:
  """Cliente para interactuar con el LLM de Ollama"""

  DEFAULT_BASE_URL = "http://localhost:11434/api"
  DEFAULT_MODEL = "llama3.2"
  DEFAULT_TIMEOUT = 300.0

  def __init__(
    self,
    base_url: Optional[str] = None,
    model: Optional[str] = None,
    timeout: float = DEFAULT_TIMEOUT,
  ):
    """
    Inicializa el cliente Ollama

    Args:
      base_url: URL base de la API de Ollama (por defecto: http://localhost:11434/api)
      model: Nombre del modelo a usar (por defecto: llama3.2)
      timeout: Tiempo de espera de la petición en segundos (por defecto: 300.0)
    """
    self.base_url = base_url or os.getenv("OLLAMA_API_BASE", self.DEFAULT_BASE_URL)
    self.model = model or os.getenv("OLLAMA_MODEL", self.DEFAULT_MODEL)
    self.timeout = timeout
    self.message_history: List[Dict[str, str]] = []

    # Cliente HTTP con pool de conexiones
    self.client = httpx.AsyncClient(timeout=httpx.Timeout(self.timeout))

  def add_system_message(self, content: str):
    """Añade mensaje de sistema al historial"""
    self.message_history.append({
      "role": "system",
      "content": content
    })

  def add_user_message(self, content: str):
    """Añade mensaje de usuario al historial"""
    self.message_history.append({
      "role": "user",
      "content": content
    })

  def add_assistant_message(self, content: str):
    """Añade mensaje del asistente al historial"""
    self.message_history.append({
      "role": "assistant",
      "content": content
    })

  async def chat(
    self,
    message: str,
    system_prompt: Optional[str] = None,
    temperature: float = 0.7,
    stream: bool = False
  ) -> str:
    """
    Envía un mensaje de chat a Ollama y obtiene respuesta

    Args:
      message: Mensaje del usuario
      system_prompt: Prompt del sistema opcional (solo se usa si no hay historial)
      temperature: Temperatura de muestreo (0.0-1.0)
      stream: Si se debe transmitir la respuesta en streaming

    Returns:
      Texto de respuesta del asistente
    """
    # Añadir prompt del sistema si es el primer mensaje
    if not self.message_history and system_prompt:
      self.add_system_message(system_prompt)

    # Añadir mensaje del usuario al historial
    self.add_user_message(message)

    # Preparar petición
    url = f"{self.base_url}/chat"
    payload = {
      "model": self.model,
      "messages": self.message_history,
      "stream": stream,
      "options": {
        "temperature": temperature
      }
    }

    # Enviar petición
    response = await self.client.post(url, json=payload)
    response.raise_for_status()

    # Analizar respuesta
    result = response.json()
    assistant_message = result.get("message", {}).get("content", "")

    # Añadir respuesta del asistente al historial
    self.add_assistant_message(assistant_message)

    return assistant_message

  async def chat_with_tools(
    self,
    message: str,
    tools_output: Optional[str] = None,
    system_prompt: Optional[str] = None,
    temperature: float = 0.7
  ) -> str:
    """
    Chat con contexto de ejecución de herramientas

    Args:
      message: Mensaje del usuario
      tools_output: Salida de la ejecución de herramientas
      system_prompt: Prompt del sistema opcional
      temperature: Temperatura de muestreo

    Returns:
      Respuesta del asistente
    """
    # Si tenemos salida de herramientas, añadirla al mensaje
    if tools_output:
      enhanced_message = f"{message}\n\nSalida de herramienta:\n```\n{tools_output}\n```"
    else:
      enhanced_message = message

    return await self.chat(
      message=enhanced_message,
      system_prompt=system_prompt,
      temperature=temperature
    )

  def clear_history(self):
    """Limpiar historial de conversación"""
    self.message_history = []

  def get_history(self) -> List[Dict[str, str]]:
    """Obtener historial de conversación actual"""
    return self.message_history.copy()

  async def close(self):
    """Cerrar cliente HTTP"""
    await self.client.aclose()

  async def __aenter__(self):
    return self

  async def __aexit__(self, exc_type, exc_val, exc_tb):
    await self.close()
