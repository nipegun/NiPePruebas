#!/usr/bin/env python3
"""
Test simple de CaiFramework con Ollama
"""
import asyncio
from cai.sdk.agents import Agent, Runner
from cai.sdk.agents.models.ollama_provider import OllamaProvider

async def main():
    print("🚀 Probando CaiFramework con Ollama")
    print("=" * 50)

    # Crear provider de Ollama
    ollama = OllamaProvider(model_name="llama3.2")

    # Crear un agente simple
    agent = Agent(
        name="Asistente Local",
        instructions="Eres un asistente útil que responde de manera concisa.",
        model=ollama.get_model()
    )

    # Ejecutar una pregunta simple
    print("\n📝 Pregunta: ¿Qué es Python?")
    print("-" * 50)

    result = await Runner.run(
        starting_agent=agent,
        input="Explica en 2 líneas qué es Python."
    )

    print(f"\n💬 Respuesta: {result.final_output}")
    print("-" * 50)
    print(f"\n📊 Tokens usados: {result.usage.total_tokens}")
    print(f"🔄 Turnos: {len(result.run_items)}")
    print("\n✅ ¡Funcionó correctamente!")

if __name__ == "__main__":
    asyncio.run(main())
