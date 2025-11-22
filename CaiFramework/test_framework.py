#!/usr/bin/env python3
"""
Test del framework completo con configuración correcta
"""
import asyncio
import os

# Configurar ANTES de importar cualquier cosa del framework
os.environ['CAI_TRACING'] = 'false'
os.environ['OPENAI_API_KEY'] = 'sk-placeholder'
os.environ['OLLAMA_API_BASE'] = 'http://localhost:11434/v1'
os.environ['CAI_MODEL'] = 'llama3.2'
os.environ['LITELLM_LOG'] = 'ERROR'

from cai.sdk.agents import Agent, Runner, RunConfig
from cai.sdk.agents.models.ollama_provider import OllamaProvider

async def main():
    print("🚀 Test de CaiFramework con Ollama")
    print("=" * 50)

    # Crear provider
    ollama = OllamaProvider(
        base_url="http://localhost:11434/v1",
        model_name="llama3.2"
    )

    # Crear agente
    agent = Agent(
        name="Asistente",
        instructions="Responde de manera muy concisa en 1-2 líneas.",
        model=ollama.get_model()
    )

    print("\n📝 Pregunta: ¿Qué es Python?")
    print("-" * 50)

    # Ejecutar
    result = await Runner.run(
        starting_agent=agent,
        input="¿Qué es Python? Responde en UNA línea.",
        run_config=RunConfig(tracing_disabled=True)
    )

    print(f"\n💬 Respuesta: {result.final_output}")
    print(f"\n✅ ¡CaiFramework funciona correctamente con Ollama!")

if __name__ == "__main__":
    asyncio.run(main())
