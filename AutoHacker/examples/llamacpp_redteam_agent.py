"""
Ejemplo de Red Team Agent usando llama.cpp

Este agente demuestra cómo configurar un agente de red teaming
que utiliza llama.cpp con modelos GGUF locales.
"""

import os
import sys
from pathlib import Path

from dotenv import load_dotenv
from cai.sdk.agents import Agent
from cai.sdk.agents.models.llamacpp_provider import LlamaCppProvider

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

# Configuración de llama.cpp
# Puedes cambiar estos valores según tu configuración
LLAMACPP_BASE_URL = os.getenv("LLAMACPP_API_BASE", "http://localhost:8080/v1")
LLAMACPP_MODEL = os.getenv("LLAMACPP_MODEL", "local-model")
LLAMACPP_CONTEXT_SIZE = int(os.getenv("LLAMACPP_CONTEXT_SIZE", "4096"))

# Crear el proveedor de llama.cpp
llamacpp_provider = LlamaCppProvider(
    base_url=LLAMACPP_BASE_URL,
    model_name=LLAMACPP_MODEL,
    context_size=LLAMACPP_CONTEXT_SIZE,
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

# Crear el agente usando llama.cpp
llamacpp_redteam_agent = Agent(
    name="llama.cpp Red Team Agent",
    description="""Red Team Agent ejecutándose con llama.cpp.
                   Utiliza modelos GGUF locales para pentesting y resolución de CTFs.
                   Experto en ciberseguridad, reconocimiento y explotación.""",
    instructions=create_system_prompt_renderer(redteam_agent_system_prompt),
    tools=tools,
    input_guardrails=input_guardrails,
    output_guardrails=output_guardrails,
    model=llamacpp_provider.get_model(),
)


# Función de transferencia
def transfer_to_llamacpp_redteam_agent(**kwargs):
    """Transferir al agente de red team con llama.cpp."""
    return llamacpp_redteam_agent


# Ejemplo de uso
if __name__ == "__main__":
    from cai.sdk.agents.models.llamacpp_provider import get_llamacpp_server_command
    
    print(f"=== llama.cpp Red Team Agent ===")
    print(f"Modelo: {LLAMACPP_MODEL}")
    print(f"Base URL: {LLAMACPP_BASE_URL}")
    print(f"Context Size: {LLAMACPP_CONTEXT_SIZE}")
    print(f"Herramientas disponibles: {len(tools)}")
    print()
    print("Para usar este agente:")
    print()
    print("1. Compila llama.cpp:")
    print("   git clone https://github.com/ggerganov/llama.cpp")
    print("   cd llama.cpp")
    print("   make -j")
    print()
    print("2. Descarga un modelo GGUF (ejemplo con Llama 3.2):")
    print("   # Desde Hugging Face")
    print("   huggingface-cli download bartowski/Meta-Llama-3.2-3B-Instruct-GGUF")
    print()
    print("3. Inicia el servidor llama.cpp:")
    example_cmd = get_llamacpp_server_command(
        model_path="models/llama-3.2-3b-instruct-q4_k_m.gguf",
        ctx_size=4096,
        n_gpu_layers=35,
    )
    print(f"   {example_cmd}")
    print()
    print("4. Configura las variables de entorno:")
    print("   export LLAMACPP_API_BASE='http://localhost:8080/v1'")
    print("   export LLAMACPP_MODEL='local-model'")
    print("   export LLAMACPP_CONTEXT_SIZE='4096'")
    print("   export CAI_AGENT_TYPE='llamacpp_redteam_agent'")
    print()
    print("5. Ejecuta: cai")
    print()
    print("Modelos recomendados (GGUF):")
    print("  - Llama 3.2 (3B, 8B): Bueno para tareas generales")
    print("  - CodeLlama (7B, 13B, 34B): Especializado en código")
    print("  - Mistral (7B): Muy eficiente")
    print("  - DeepSeek Coder (6.7B, 33B): Excelente para coding")
    print("  - Qwen2.5 (7B, 14B, 32B): Potente y multilingüe")
    print()
    print("Cuantizaciones recomendadas:")
    print("  - Q4_K_M: Buen balance velocidad/calidad (recomendado)")
    print("  - Q5_K_M: Mejor calidad, más lento")
    print("  - Q6_K: Máxima calidad, más pesado")
    print("  - Q8_0: Casi sin pérdida de calidad")
