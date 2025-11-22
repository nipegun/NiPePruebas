"""
Ejemplo de uso de CaiFramework con Ollama

Este ejemplo demuestra cómo configurar un agente usando Ollama
para ejecutar modelos locales en lugar de APIs de pago.

Prerequisitos:
    1. Instalar Ollama: https://ollama.ai
    2. Iniciar el servidor: ollama serve
    3. Descargar un modelo: ollama pull llama3.2

Variables de entorno opcionales:
    OLLAMA_API_BASE: URL del servidor Ollama (default: http://localhost:11434/v1)
    OLLAMA_MODEL: Modelo a usar (default: llama3.2)
"""

import asyncio
import os
import sys
from pathlib import Path

# IMPORTANTE: Configurar ANTES de importar el framework
os.environ['CAI_TRACING'] = 'false'
os.environ.setdefault('OPENAI_API_KEY', 'sk-placeholder')

from dotenv import load_dotenv

from cai.agents.guardrails import get_security_guardrails
from cai.sdk.agents import Agent, Runner, RunConfig
from cai.sdk.agents.models.ollama_provider import OllamaProvider
from cai.tools.reconnaissance.exec_code import execute_code
from cai.tools.reconnaissance.generic_linux_command import generic_linux_command
from cai.tools.web.search_web import make_web_search_with_explanation
from cai.util import create_system_prompt_renderer, load_prompt_template

# Ensure repository root is on the import path
PROJECT_ROOT = Path(__file__).resolve().parent.parent
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

load_dotenv()

# Configuración de Ollama
OLLAMA_BASE_URL = os.getenv("OLLAMA_API_BASE", "http://localhost:11434/v1")
OLLAMA_MODEL = os.getenv("OLLAMA_MODEL", "llama3.2")

print(f"=== CaiFramework con Ollama ===")
print(f"Base URL: {OLLAMA_BASE_URL}")
print(f"Modelo: {OLLAMA_MODEL}")
print()


async def main():
    """Función principal del ejemplo."""
    # Crear el proveedor de Ollama
    ollama_provider = OllamaProvider(
        base_url=OLLAMA_BASE_URL,
        model_name=OLLAMA_MODEL,
    )

    # Cargar el prompt del sistema (usando el prompt de red team como ejemplo)
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

    # Crear el agente usando Ollama
    agent = Agent(
        name="Ollama Security Agent",
        description="""Agente de seguridad ejecutándose con Ollama.
                       Utiliza modelos locales para análisis de seguridad.
                       Experto en ciberseguridad, reconocimiento y análisis.""",
        instructions=create_system_prompt_renderer(redteam_prompt),
        tools=tools,
        input_guardrails=input_guardrails,
        output_guardrails=output_guardrails,
        model=ollama_provider.get_model(),
    )

    # Ejecutar el agente con una tarea de ejemplo
    print("Ejecutando agente con Ollama...")
    print("Tarea: Analizar el sistema y proporcionar información básica")
    print()

    result = await Runner.run(
        starting_agent=agent,
        input="Ejecuta el comando 'uname -a' y explica qué sistema operativo estoy usando.",
        run_config=RunConfig(tracing_disabled=True)
    )

    print("\n=== Resultado ===")
    print(result.final_output)
    print()
    if hasattr(result, 'usage') and result.usage:
        print(f"Tokens usados: {result.usage.total_tokens}")
    if hasattr(result, 'run_items'):
        print(f"Turnos realizados: {len(result.run_items)}")


if __name__ == "__main__":
    print("Iniciando ejemplo con Ollama...")
    print()
    print("Configuración:")
    print(f"  - Ollama API: {OLLAMA_BASE_URL}")
    print(f"  - Modelo: {OLLAMA_MODEL}")
    print()
    print("Para cambiar la configuración, usa:")
    print("  export OLLAMA_API_BASE='http://localhost:11434/v1'")
    print("  export OLLAMA_MODEL='llama3.2'")
    print()
    print("Modelos Ollama recomendados:")
    print("  - llama3.2 (recomendado): Modelo general balanceado")
    print("  - llama3.1:70b: Más potente pero requiere más recursos")
    print("  - codellama: Especializado en código y programación")
    print("  - mistral: Rápido y eficiente para tareas generales")
    print("  - qwen2.5: Excelente para tareas multilingües")
    print()
    print("-" * 60)
    print()

    asyncio.run(main())
