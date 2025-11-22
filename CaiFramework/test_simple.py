#!/usr/bin/env python3
"""
Test MUY simple - llamada directa sin Runner
"""
import asyncio
import os

# Deshabilitar tracing
os.environ['CAI_TRACING'] = 'false'
os.environ['OPENAI_API_KEY'] = 'sk-not-needed'

from openai import AsyncOpenAI

async def main():
    print("🧪 Test directo a Ollama")
    print("=" * 50)

    # Cliente directo a Ollama
    client = AsyncOpenAI(
        base_url="http://localhost:11434/v1",
        api_key="ollama"  # No se usa, pero es requerido
    )

    print("\n📝 Haciendo llamada a Ollama...")

    response = await client.chat.completions.create(
        model="llama3.2",
        messages=[
            {"role": "user", "content": "¿Qué es Python? Responde en 1 línea."}
        ]
    )

    print(f"\n💬 Respuesta: {response.choices[0].message.content}")
    print(f"\n✅ ¡Funciona! Ollama está respondiendo correctamente.")

if __name__ == "__main__":
    asyncio.run(main())
