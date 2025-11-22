"""
Ejemplo de Red Team Agent usando Ollama

Este agente demuestra cómo configurar un agente de red teaming
que utiliza Ollama con modelos locales en lugar de APIs de pago.
"""

import os
import sys
from pathlib import Path

from dotenv import load_dotenv
from cai.sdk.agents import Agent
from cai.sdk.agents.models.ollama_provider import OllamaProvider

from cai.tools.reconnaissance.generic_linux_command import generic_linux_command
from cai.tools.web.search_web import make_web_search_with_explanation
from cai.tools.reconnaissance.exec_code import execute_code
from cai.util import load_prompt_template, create_system_prompt_renderer
from cai.agents.guardrails import get_security_guardrails

# Ensure repository root is on the import path when running the example directly
PROJECT_ROOT = Path(__file__).resolve().parent.parent
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

load_dotenv()

# Configuración de Ollama
# Puedes cambiar estos valores según tu configuración
OLLAMA_BASE_URL = os.getenv("OLLAMA_API_BASE", "http://localhost:11434/v1")
OLLAMA_MODEL = os.getenv("OLLAMA_MODEL", "llama3.2")

# Crear el proveedor de Ollama
ollama_provider = OllamaProvider(
    base_url=OLLAMA_BASE_URL,
    model_name=OLLAMA_MODEL,
)

# Cargar el prompt del sistema
redteam_agent_system_prompt = load_prompt_template("prompts/system_red_team_agent.md")

# Definir las herramientas disponibles
tools = [
    generic_linux_command,
    execute_code,
]

# Añadir búsqueda web si está configurada
if os.getenv('PERPLEXITY_API_KEY'):
    tools.append(make_web_search_with_explanation)

# Obtener guardrails de seguridad
input_guardrails, output_guardrails = get_security_guardrails()

# Crear el agente usando Ollama
ollama_redteam_agent = Agent(
    name="Ollama Red Team Agent",
    description="""Red Team Agent ejecutándose con Ollama.
                   Utiliza modelos locales para pentesting y resolución de CTFs.
                   Experto en ciberseguridad, reconocimiento y explotación.""",
    instructions=create_system_prompt_renderer(redteam_agent_system_prompt),
    tools=tools,
    input_guardrails=input_guardrails,
    output_guardrails=output_guardrails,
    model=ollama_provider.get_model(),
)


# Función de transferencia
def transfer_to_ollama_redteam_agent(**kwargs):
    """Transferir al agente de red team con Ollama."""
    return ollama_redteam_agent


# Ejemplo de uso
if __name__ == "__main__":
    print(f"=== Ollama Red Team Agent ===")
    print(f"Modelo: {OLLAMA_MODEL}")
    print(f"Base URL: {OLLAMA_BASE_URL}")
    print(f"Herramientas disponibles: {len(tools)}")
    print()
    print("Para usar este agente:")
    print("1. Asegúrate de que Ollama está corriendo: ollama serve")
    print("2. Descarga el modelo: ollama pull llama3.2")
    print("3. Configura las variables de entorno:")
    print("   export OLLAMA_API_BASE='http://localhost:11434/v1'")
    print("   export OLLAMA_MODEL='llama3.2'")
    print("   export CAI_AGENT_TYPE='ollama_redteam_agent'")
    print("4. Ejecuta: cai")
