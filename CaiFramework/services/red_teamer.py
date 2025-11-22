#!/usr/bin/env python3
"""
Red Team Service - Offensive Security Operations

Servicio de red team para operaciones de seguridad ofensiva.
Especializado en penetration testing, explotación y post-explotación.

Uso:
    python services/red_teamer.py
    python services/red_teamer.py --target 192.168.1.0/24
    python services/red_teamer.py --target example.com --mode recon
"""

import asyncio
import argparse
import os
import sys
from pathlib import Path

# Configuración ANTES de importar
os.environ['CAI_TRACING'] = 'false'
os.environ['OPENAI_API_KEY'] = 'sk-placeholder'
os.environ['CAI_MODEL'] = os.getenv('CAI_MODEL', 'llama3.2')
os.environ['LITELLM_LOG'] = 'ERROR'

PROJECT_ROOT = Path(__file__).resolve().parent.parent
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from dotenv import load_dotenv
from cai.sdk.agents import Agent, Runner, RunConfig
from cai.sdk.agents.models.ollama_provider import OllamaProvider
from cai.util import load_prompt_template, create_system_prompt_renderer
from cai.tools.reconnaissance.generic_linux_command import generic_linux_command
from cai.tools.reconnaissance.exec_code import execute_code

load_dotenv()


def parse_args():
    parser = argparse.ArgumentParser(
        description='Red Team Service - Offensive Security Operations',
        formatter_class=argparse.RawDescriptionHelpFormatter
    )
    parser.add_argument('--target', type=str, help='Target IP, domain, or network')
    parser.add_argument('--mode', choices=['recon', 'exploit', 'post-exploit', 'full'],
                       default='recon', help='Operation mode (default: recon)')
    parser.add_argument('--model', default='llama3.2', help='Ollama model (default: llama3.2)')
    parser.add_argument('--no-guardrails', action='store_true', help='Disable security guardrails')
    parser.add_argument('--interactive', action='store_true', help='Interactive mode')
    return parser.parse_args()


async def main():
    args = parse_args()

    # Banner
    print("\n" + "═" * 80)
    print("🔴 RED TEAM SERVICE - OFFENSIVE SECURITY OPERATIONS")
    print("═" * 80)
    print(f"\n📋 Configuration:")
    print(f"  • Model: {args.model}")
    print(f"  • Mode: {args.mode}")
    print(f"  • Guardrails: {'Disabled' if args.no_guardrails else 'Enabled'}")
    if args.target:
        print(f"  • Target: {args.target}")
    print()

    # Crear provider
    ollama = OllamaProvider(model_name=args.model)

    # Cargar prompt
    try:
        prompt = load_prompt_template("prompts/system_red_team_agent.md")
    except:
        prompt = """You are a red team security expert specializing in offensive security.
        Your role is reconnaissance, vulnerability discovery, and exploitation testing.
        Always follow ethical guidelines and only test authorized systems."""

    # Herramientas
    tools = [generic_linux_command, execute_code]

    # Guardrails opcionales
    agent_kwargs = {
        "name": "Red Teamer",
        "description": "Offensive security specialist for penetration testing",
        "instructions": create_system_prompt_renderer(prompt),
        "tools": tools,
        "model": ollama.get_model()
    }

    if not args.no_guardrails:
        try:
            from cai.agents.guardrails import get_security_guardrails
            input_gr, output_gr = get_security_guardrails()
            agent_kwargs["input_guardrails"] = input_gr
            agent_kwargs["output_guardrails"] = output_gr
        except:
            pass

    agent = Agent(**agent_kwargs)

    # Modo interactivo
    if args.interactive:
        print("🔴 Entering interactive red team mode...")
        print("Type your commands or 'exit' to quit.\n")

        while True:
            try:
                task = input("red-team> ")
                if task.lower() in ['exit', 'quit', 'q']:
                    break

                if not task.strip():
                    continue

                result = await Runner.run(
                    starting_agent=agent,
                    input=task,
                    run_config=RunConfig(tracing_disabled=True)
                )
                print(f"\n{result.final_output}\n")

            except KeyboardInterrupt:
                print("\n\n⚠️  Exiting...")
                break
            except Exception as e:
                print(f"\n❌ Error: {e}\n")

    # Modo por tarea
    else:
        tasks = {
            'recon': f"Perform reconnaissance on {args.target if args.target else 'the local system'}. "
                    "Gather information about open ports, services, OS, and potential vulnerabilities.",
            'exploit': f"Analyze {args.target if args.target else 'the target'} for exploitable vulnerabilities. "
                      "Suggest potential attack vectors and exploitation methods.",
            'post-exploit': "Perform post-exploitation analysis. Suggest privilege escalation, "
                          "persistence mechanisms, and lateral movement strategies.",
            'full': f"Perform a complete red team assessment of {args.target if args.target else 'the target'}. "
                   "Include reconnaissance, vulnerability analysis, and exploitation recommendations."
        }

        task = tasks.get(args.mode, tasks['recon'])

        print(f"🎯 Executing {args.mode} operation...\n")
        print("─" * 80)

        result = await Runner.run(
            starting_agent=agent,
            input=task,
            run_config=RunConfig(tracing_disabled=True)
        )

        print("\n📊 RESULTS")
        print("─" * 80)
        print(result.final_output)
        print("\n" + "═" * 80)

    print("\n⚠️  LEGAL NOTICE: Only use on authorized systems. Unauthorized access is illegal.\n")


if __name__ == "__main__":
    asyncio.run(main())
