"""
Ejemplo de uso de CaiFramework con llama.cpp

Este ejemplo demuestra cómo configurar un agente usando llama.cpp
para ejecutar modelos GGUF locales.

Prerequisitos:
    1. Compilar llama.cpp:
       git clone https://github.com/ggerganov/llama.cpp
       cd llama.cpp
       make -j

    2. Descargar un modelo GGUF (ejemplo con Llama 3.2):
       # Desde Hugging Face
       huggingface-cli download bartowski/Meta-Llama-3.2-3B-Instruct-GGUF

    3. Iniciar el servidor llama.cpp:
       ./llama-server -m models/llama-3.2-3b-instruct-q4_k_m.gguf \
                      --host 0.0.0.0 --port 8080 \
                      --ctx-size 4096 --n-gpu-layers 35

Variables de entorno opcionales:
    LLAMACPP_API_BASE: URL del servidor (default: http://localhost:8080/v1)
    LLAMACPP_MODEL: Nombre del modelo (default: local-model)
    LLAMACPP_CONTEXT_SIZE: Tamaño del contexto (default: 4096)
"""

import asyncio
import os
import sys
from pathlib import Path

from dotenv import load_dotenv

from cai.agents.guardrails import get_security_guardrails
from cai.sdk.agents import Agent, Runner
from cai.sdk.agents.models.llamacpp_provider import (
    LlamaCppProvider,
    get_llamacpp_server_command,
)
from cai.tools.reconnaissance.exec_code import execute_code
from cai.tools.reconnaissance.generic_linux_command import generic_linux_command
from cai.tools.web.search_web import make_web_search_with_explanation
from cai.util import create_system_prompt_renderer, load_prompt_template

# Ensure repository root is on the import path
PROJECT_ROOT = Path(__file__).resolve().parent.parent
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

load_dotenv()

# Configuración de llama.cpp
LLAMACPP_BASE_URL = os.getenv("LLAMACPP_API_BASE", "http://localhost:8080/v1")
LLAMACPP_MODEL = os.getenv("LLAMACPP_MODEL", "local-model")
LLAMACPP_CONTEXT_SIZE = int(os.getenv("LLAMACPP_CONTEXT_SIZE", "4096"))

print(f"=== CaiFramework con llama.cpp ===")
print(f"Base URL: {LLAMACPP_BASE_URL}")
print(f"Modelo: {LLAMACPP_MODEL}")
print(f"Context Size: {LLAMACPP_CONTEXT_SIZE}")
print()


async def main():
    """Función principal del ejemplo."""
    # Crear el proveedor de llama.cpp
    llamacpp_provider = LlamaCppProvider(
        base_url=LLAMACPP_BASE_URL,
        model_name=LLAMACPP_MODEL,
        context_size=LLAMACPP_CONTEXT_SIZE,
    )

    # Opcional: Verificar que el servidor está disponible
    try:
        server_info = await llamacpp_provider.get_server_info()
        print(f"Estado del servidor: {server_info}")
        print()
    except Exception as e:
        print(f"⚠️  Advertencia: No se pudo conectar al servidor llama.cpp: {e}")
        print(
            "Asegúrate de que el servidor está corriendo en",
            LLAMACPP_BASE_URL.replace("/v1", ""),
        )
        print()

    # Cargar el prompt del sistema
    redteam_prompt = load_prompt_template("prompts/system_red_team_agent.md")

    # Definir las herramientas disponibles
    tools = [
        generic_linux_command,
        execute_code,
    ]

    # Añadir búsqueda web si está configurada
    if os.getenv("PERPLEXITY_API_KEY"):
        tools.append(make_web_search_with_explanation)

    # Obtener guardrails de seguridad
    input_guardrails, output_guardrails = get_security_guardrails()

    # Crear el agente usando llama.cpp
    agent = Agent(
        name="llama.cpp Security Agent",
        description="""Agente de seguridad ejecutándose con llama.cpp.
                       Utiliza modelos GGUF locales para análisis de seguridad.
                       Experto en ciberseguridad, reconocimiento y análisis.""",
        instructions=create_system_prompt_renderer(redteam_prompt),
        tools=tools,
        input_guardrails=input_guardrails,
        output_guardrails=output_guardrails,
        model=llamacpp_provider.get_model(),
    )

    # Ejecutar el agente con una tarea de ejemplo
    print("Ejecutando agente con llama.cpp...")
    print("Tarea: Analizar el sistema y proporcionar información básica")
    print()

    result = await Runner.run(
        starting_agent=agent,
        input="Ejecuta el comando 'uname -a' y explica qué sistema operativo estoy usando.",
    )

    print("\n=== Resultado ===")
    print(result.final_output)
    print()
    print(f"Tokens usados: {result.usage.total_tokens}")
    print(f"Turnos realizados: {len(result.run_items)}")


if __name__ == "__main__":
    print("Iniciando ejemplo con llama.cpp...")
    print()
    print("Configuración:")
    print(f"  - llama.cpp API: {LLAMACPP_BASE_URL}")
    print(f"  - Modelo: {LLAMACPP_MODEL}")
    print(f"  - Context Size: {LLAMACPP_CONTEXT_SIZE}")
    print()
    print("Para cambiar la configuración, usa:")
    print("  export LLAMACPP_API_BASE='http://localhost:8080/v1'")
    print("  export LLAMACPP_MODEL='local-model'")
    print("  export LLAMACPP_CONTEXT_SIZE='4096'")
    print()
    print("Comando de ejemplo para iniciar el servidor:")
    example_cmd = get_llamacpp_server_command(
        model_path="models/llama-3.2-3b-instruct-q4_k_m.gguf",
        ctx_size=4096,
        n_gpu_layers=35,
    )
    print(f"  {example_cmd}")
    print()
    print("Modelos GGUF recomendados:")
    print("  - Llama 3.2 (3B, 8B): Bueno para tareas generales")
    print("  - CodeLlama (7B, 13B, 34B): Especializado en código")
    print("  - Mistral (7B): Muy eficiente y rápido")
    print("  - DeepSeek Coder (6.7B, 33B): Excelente para programación")
    print("  - Qwen2.5 (7B, 14B, 32B): Potente y multilingüe")
    print()
    print("Cuantizaciones recomendadas:")
    print("  - Q4_K_M: Buen balance velocidad/calidad (recomendado)")
    print("  - Q5_K_M: Mejor calidad, un poco más lento")
    print("  - Q6_K: Máxima calidad, más pesado")
    print("  - Q8_0: Casi sin pérdida de calidad")
    print()
    print("-" * 60)
    print()

    asyncio.run(main())
