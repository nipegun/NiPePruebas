#!/usr/bin/env python3
"""
Blue Team Service - Defensive Security Operations

Servicio de blue team para operaciones de seguridad defensiva.
Especializado en detección, análisis de amenazas y respuesta a incidentes.

Uso:
    python services/blue_teamer.py
    python services/blue_teamer.py --analyze-logs /var/log/auth.log
    python services/blue_teamer.py --mode threat-hunting --interactive
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
    parser = argparse.ArgumentParser(description='Blue Team Service - Defensive Security')
    parser.add_argument('--analyze-logs', type=str, help='Log file to analyze')
    parser.add_argument('--mode', choices=['detection', 'threat-hunting', 'incident-response'],
                       default='detection', help='Operation mode')
    parser.add_argument('--model', default='llama3.2', help='Ollama model')
    parser.add_argument('--interactive', action='store_true', help='Interactive mode')
    parser.add_argument('--no-guardrails', action='store_true')
    return parser.parse_args()


async def main():
    args = parse_args()

    print("\n" + "═" * 80)
    print("🔵 BLUE TEAM SERVICE - DEFENSIVE SECURITY OPERATIONS")
    print("═" * 80)
    print(f"\n📋 Configuration:")
    print(f"  • Model: {args.model}")
    print(f"  • Mode: {args.mode}")
    if args.analyze_logs:
        print(f"  • Log File: {args.analyze_logs}")
    print()

    ollama = OllamaProvider(model_name=args.model)

    try:
        prompt = load_prompt_template("prompts/system_blue_team_agent.md")
    except:
        prompt = """You are a blue team security expert specializing in defensive security.
        Your role is threat detection, log analysis, and incident response.
        Focus on identifying malicious activity and protecting systems."""

    tools = [generic_linux_command, execute_code]

    agent_kwargs = {
        "name": "Blue Teamer",
        "description": "Defensive security specialist",
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
        print("🔵 Entering interactive blue team mode...\n")
        while True:
            try:
                task = input("blue-team> ")
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
        if args.analyze_logs:
            task = f"Analyze the log file {args.analyze_logs} for security threats, suspicious activities, and IOCs."
        else:
            tasks = {
                'detection': "Analyze the current system for signs of compromise. Check for suspicious processes, network connections, and file modifications.",
                'threat-hunting': "Perform proactive threat hunting. Look for indicators of compromise and advanced persistent threats.",
                'incident-response': "Analyze the system for active security incidents. Provide recommendations for containment and remediation."
            }
            task = tasks[args.mode]

        print(f"🎯 Executing {args.mode} operation...\n")

        result = await Runner.run(
            starting_agent=agent,
            input=task,
            run_config=RunConfig(tracing_disabled=True)
        )

        print("\n📊 ANALYSIS RESULTS")
        print("─" * 80)
        print(result.final_output)
        print("\n" + "═" * 80)


if __name__ == "__main__":
    asyncio.run(main())
