#!/usr/bin/env python3
"""
Bug Bounty Hunter - Automated Vulnerability Scanner

Este script analiza endpoints web en busca de vulnerabilidades de seguridad
utilizando un agente de IA especializado en bug bounty hunting.

Uso:
    python bug_bounty_hunter.py <URL>
    python bug_bounty_hunter.py https://example.com/api/users
    python bug_bounty_hunter.py https://api.example.com --method POST

Características:
    - Análisis de headers de seguridad
    - Detección de información sensible
    - Identificación de configuraciones inseguras
    - Búsqueda de vulnerabilidades OWASP Top 10
    - Reporte detallado con recomendaciones
"""

import asyncio
import argparse
import os
import sys
from pathlib import Path

# IMPORTANTE: Configurar ANTES de importar el framework
os.environ['CAI_TRACING'] = 'false'
os.environ['OPENAI_API_KEY'] = 'sk-placeholder'
os.environ['CAI_MODEL'] = os.getenv('CAI_MODEL', 'llama3.2')
os.environ['LITELLM_LOG'] = 'ERROR'

# Asegurar que el directorio raíz está en el path
PROJECT_ROOT = Path(__file__).resolve().parent.parent
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from dotenv import load_dotenv
from cai.sdk.agents import Agent, Runner, RunConfig
from cai.sdk.agents.models.ollama_provider import OllamaProvider
from cai.util import load_prompt_template, create_system_prompt_renderer
from cai.tools.reconnaissance.generic_linux_command import generic_linux_command
from cai.tools.reconnaissance.exec_code import execute_code
from cai.tools.web.http_analyzer import analyze_http_endpoint

load_dotenv()


def parse_arguments():
    """Parsear argumentos de línea de comandos."""
    parser = argparse.ArgumentParser(
        description='Bug Bounty Hunter - Automated Vulnerability Scanner',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Ejemplos:
  %(prog)s https://example.com
  %(prog)s https://api.example.com/users --method GET
  %(prog)s https://example.com/login --method POST

Nota:
  - El análisis se realiza de forma ética y responsable
  - Solo analiza endpoints con autorización
  - No realiza ataques destructivos
        """
    )

    parser.add_argument(
        'url',
        type=str,
        help='URL del endpoint a analizar (ej: https://example.com/api/users)'
    )

    parser.add_argument(
        '--method',
        type=str,
        default='GET',
        choices=['GET', 'POST', 'PUT', 'DELETE', 'PATCH', 'HEAD', 'OPTIONS'],
        help='Método HTTP a utilizar (default: GET)'
    )

    parser.add_argument(
        '--model',
        type=str,
        default='llama3.2',
        help='Modelo de Ollama a usar (default: llama3.2)'
    )

    parser.add_argument(
        '--ollama-url',
        type=str,
        default='http://localhost:11434/v1',
        help='URL base de Ollama (default: http://localhost:11434/v1)'
    )

    parser.add_argument(
        '--no-guardrails',
        action='store_true',
        help='Desactivar guardrails de seguridad (más rápido pero menos seguro)'
    )

    parser.add_argument(
        '--verbose',
        '-v',
        action='store_true',
        help='Mostrar información detallada del proceso'
    )

    return parser.parse_args()


async def main():
    """Función principal del bug bounty hunter."""
    args = parse_arguments()

    # Banner
    print("╔" + "═" * 78 + "╗")
    print("║" + " " * 20 + "🔍 BUG BOUNTY HUNTER 🔍" + " " * 35 + "║")
    print("║" + " " * 15 + "Automated Vulnerability Scanner with AI" + " " * 24 + "║")
    print("╚" + "═" * 78 + "╝")
    print()

    # Mostrar configuración
    print("📋 CONFIGURACIÓN:")
    print(f"  • Target URL: {args.url}")
    print(f"  • HTTP Method: {args.method}")
    print(f"  • Ollama URL: {args.ollama_url}")
    print(f"  • Model: {args.model}")
    print(f"  • Guardrails: {'Disabled' if args.no_guardrails else 'Enabled'}")
    print()

    # Validar URL
    if not args.url.startswith(('http://', 'https://')):
        print("❌ Error: La URL debe comenzar con http:// o https://")
        sys.exit(1)

    # Crear provider de Ollama
    if args.verbose:
        print(f"🔧 Inicializando Ollama provider con modelo {args.model}...")

    ollama_provider = OllamaProvider(
        base_url=args.ollama_url,
        model_name=args.model
    )

    # Cargar prompt del sistema
    try:
        bug_bounty_prompt = load_prompt_template("prompts/system_bug_bounter.md")
    except Exception as e:
        if args.verbose:
            print(f"⚠️  No se pudo cargar el prompt personalizado: {e}")
        # Usar un prompt básico si no se encuentra el archivo
        bug_bounty_prompt = """You are an expert bug bounty hunter specializing in web security.
        Analyze endpoints for vulnerabilities following OWASP Top 10 guidelines.
        Always provide detailed, actionable findings with remediation recommendations."""

    # Definir herramientas
    tools = [
        analyze_http_endpoint,  # Herramienta principal para análisis HTTP
        generic_linux_command,   # Para comandos adicionales si es necesario
        execute_code,           # Para scripts de análisis personalizados
    ]

    # Obtener guardrails si están habilitados
    agent_kwargs = {
        "name": "Bug Bounty Hunter",
        "description": "Expert in web security, vulnerability discovery, and ethical hacking.",
        "instructions": None,  # Se asignará después
        "tools": None,  # Se asignará después
        "model": None  # Se asignará después
    }

    if not args.no_guardrails:
        try:
            from cai.agents.guardrails import get_security_guardrails
            input_guardrails, output_guardrails = get_security_guardrails()
            agent_kwargs["input_guardrails"] = input_guardrails
            agent_kwargs["output_guardrails"] = output_guardrails
            if args.verbose:
                print("🛡️  Guardrails de seguridad activados")
        except Exception as e:
            if args.verbose:
                print(f"⚠️  No se pudieron cargar guardrails: {e}")

    # Crear el agente Bug Bounty Hunter
    if args.verbose:
        print("🤖 Creando agente Bug Bounty Hunter...")

    agent_kwargs["instructions"] = create_system_prompt_renderer(bug_bounty_prompt)
    agent_kwargs["tools"] = tools
    agent_kwargs["model"] = ollama_provider.get_model()

    agent = Agent(**agent_kwargs)

    # Preparar la tarea
    task = f"""Analiza el siguiente endpoint web en busca de vulnerabilidades de seguridad:

URL: {args.url}
Método HTTP: {args.method}

Por favor:
1. Analiza el endpoint usando la herramienta analyze_http_endpoint
2. Identifica vulnerabilidades de seguridad (OWASP Top 10)
3. Evalúa headers de seguridad
4. Busca exposición de información sensible
5. Proporciona un reporte detallado con:
   - Vulnerabilidades encontradas (clasificadas por severidad)
   - Impacto potencial de cada vulnerabilidad
   - Recomendaciones específicas para remediar cada issue

Enfócate en hallazgos accionables y realistas. No hagas suposiciones sin evidencia."""

    print("─" * 80)
    print("🔍 INICIANDO ANÁLISIS DE SEGURIDAD...")
    print("─" * 80)
    print()

    try:
        # Ejecutar el análisis
        result = await Runner.run(
            starting_agent=agent,
            input=task,
            run_config=RunConfig(tracing_disabled=True)
        )

        # Mostrar resultados
        print("─" * 80)
        print("📊 REPORTE DE VULNERABILIDADES")
        print("─" * 80)
        print()
        print(result.final_output)
        print()
        print("─" * 80)
        print("✅ Análisis completado")
        print("─" * 80)

        # Disclaimer ético
        print()
        print("⚠️  AVISO LEGAL:")
        print("  Este análisis es solo para fines educativos y de seguridad autorizada.")
        print("  No uses esta herramienta contra sistemas sin autorización explícita.")
        print("  El uso no autorizado puede ser ilegal y está sujeto a consecuencias legales.")
        print()

    except KeyboardInterrupt:
        print("\n\n⚠️  Análisis interrumpido por el usuario")
        sys.exit(1)
    except Exception as e:
        print(f"\n❌ Error durante el análisis: {str(e)}")
        if args.verbose:
            import traceback
            traceback.print_exc()
        sys.exit(1)


if __name__ == "__main__":
    print()
    asyncio.run(main())
