#!/usr/bin/env python3
"""
Reverse Engineering Service

Servicio para análisis de binarios, malware y ingeniería inversa.
Especializado en descompilación, análisis estático y dinámico.

Uso:
    python services/reverse_engineer.py --binary /path/to/binary
    python services/reverse_engineer.py --analyze malware.exe
    python services/reverse_engineer.py --decompile program --interactive
"""

import asyncio
import argparse
import os
import sys
from pathlib import Path

os.environ['CAI_TRACING'] = 'false'
os.environ['OPENAI_API_KEY'] = 'sk-placeholder'
os.environ['CAI_MODEL'] = os.getenv('CAI_MODEL', 'llama3.2')

PROJECT_ROOT = Path(__file__).resolve().parent.parent
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from cai.sdk.agents import Agent, Runner, RunConfig
from cai.sdk.agents.models.ollama_provider import OllamaProvider
from cai.util import load_prompt_template, create_system_prompt_renderer
from cai.tools.reconnaissance.generic_linux_command import generic_linux_command
from cai.tools.reconnaissance.exec_code import execute_code


def parse_args():
    parser = argparse.ArgumentParser(description='Reverse Engineering Service')
    parser.add_argument('--binary', type=str, help='Binary file to analyze')
    parser.add_argument('--analyze', type=str, help='File to analyze (alias for --binary)')
    parser.add_argument('--decompile', type=str, help='Binary to decompile')
    parser.add_argument('--model', default='codellama', help='Ollama model (default: codellama)')
    parser.add_argument('--interactive', action='store_true')
    parser.add_argument('--no-guardrails', action='store_true')
    return parser.parse_args()


async def main():
    args = parse_args()

    print("\n" + "═" * 80)
    print("🔧 REVERSE ENGINEERING SERVICE")
    print("═" * 80)
    print(f"\n📋 Configuration:")
    print(f"  • Model: {args.model}")

    target = args.binary or args.analyze or args.decompile
    if target:
        print(f"  • Target: {target}")
    print()

    ollama = OllamaProvider(model_name=args.model)

    try:
        prompt = load_prompt_template("prompts/system_reverse_engineering_agent.md")
    except:
        prompt = """You are a reverse engineering expert specializing in binary analysis,
        malware analysis, and code decompilation. You can analyze executables,
        identify obfuscation techniques, and understand malicious behavior."""

    tools = [generic_linux_command, execute_code]

    agent_kwargs = {
        "name": "Reverse Engineer",
        "description": "Binary analysis and reverse engineering specialist",
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

    if args.interactive:
        print("🔧 Entering interactive reverse engineering mode...\n")
        while True:
            try:
                task = input("re> ")
                if task.lower() in ['exit', 'quit']:
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
                break
    else:
        if not target:
            print("❌ Error: Please specify a binary with --binary, --analyze, or --decompile")
            sys.exit(1)

        if args.decompile:
            task = f"Decompile and analyze the binary {target}. Provide pseudocode and explain functionality."
        else:
            task = f"Perform reverse engineering analysis on {target}. Identify file type, architecture, strings, functions, and potential malicious behavior."

        print(f"🎯 Analyzing binary: {target}\n")
        print("─" * 80)

        result = await Runner.run(
            starting_agent=agent,
            input=task,
            run_config=RunConfig(tracing_disabled=True)
        )

        print("\n📊 REVERSE ENGINEERING ANALYSIS")
        print("─" * 80)
        print(result.final_output)
        print("\n" + "═" * 80)


if __name__ == "__main__":
    asyncio.run(main())
