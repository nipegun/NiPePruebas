#!/usr/bin/env python3
"""Test mínimo con una herramienta"""
import asyncio
import os

os.environ['CAI_TRACING'] = 'false'
os.environ['OPENAI_API_KEY'] = 'sk-placeholder'
os.environ['CAI_MODEL'] = 'llama3.2'
os.environ['LITELLM_LOG'] = 'ERROR'

from cai.sdk.agents import Agent, Runner, RunConfig
from cai.sdk.agents.models.ollama_provider import OllamaProvider
from cai.tools.reconnaissance.generic_linux_command import generic_linux_command

async def main():
    print("🧪 Test con herramienta")
    print("=" * 50)

    ollama = OllamaProvider(
        base_url="http://localhost:11434/v1",
        model_name="llama3.2"
    )

    agent = Agent(
        name="TestAgent",
        instructions="Eres un asistente. Usa comandos cuando sea necesario.",
        tools=[generic_linux_command],
        model=ollama.get_model()
    )

    print("\n📝 Pregunta: Ejecuta 'uname -a'")
    print("-" * 50)

    result = await Runner.run(
        starting_agent=agent,
        input="Ejecuta el comando 'uname -a'",
        run_config=RunConfig(tracing_disabled=True)
    )

    print(f"\n💬 Respuesta: {result.final_output}")
    print(f"\n✅ Test completado")

if __name__ == "__main__":
    asyncio.run(main())
