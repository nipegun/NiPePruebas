#!/usr/bin/env python3
"""
DFIR Service - Digital Forensics & Incident Response

Servicio para análisis forense digital y respuesta a incidentes.
Especializado en investigación de compromisos y análisis post-mortem.

Uso:
    python services/dfir.py --investigate
    python services/dfir.py --analyze-disk /dev/sda1
    python services/dfir.py --timeline /var/log
    python services/dfir.py --interactive
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
    parser = argparse.ArgumentParser(description='DFIR Service')
    parser.add_argument('--investigate', action='store_true', help='Start incident investigation')
    parser.add_argument('--analyze-disk', type=str, help='Disk/partition to analyze')
    parser.add_argument('--timeline', type=str, help='Directory for timeline analysis')
    parser.add_argument('--model', default='llama3.2')
    parser.add_argument('--interactive', action='store_true')
    parser.add_argument('--no-guardrails', action='store_true')
    return parser.parse_args()


async def main():
    args = parse_args()

    print("\n" + "═" * 80)
    print("🔍 DFIR SERVICE - DIGITAL FORENSICS & INCIDENT RESPONSE")
    print("═" * 80)
    print(f"\n📋 Configuration:")
    print(f"  • Model: {args.model}")
    if args.analyze_disk:
        print(f"  • Disk: {args.analyze_disk}")
    if args.timeline:
        print(f"  • Timeline Directory: {args.timeline}")
    print()

    ollama = OllamaProvider(model_name=args.model)

    try:
        prompt = load_prompt_template("prompts/system_dfir.md")
    except:
        prompt = """You are a digital forensics and incident response expert.
        Investigate security incidents, analyze artifacts, create timelines,
        and determine the scope and impact of security breaches."""

    tools = [generic_linux_command, execute_code]

    agent_kwargs = {
        "name": "DFIR Analyst",
        "description": "Digital forensics and incident response specialist",
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
        print("🔍 Entering interactive DFIR mode...\n")
        while True:
            try:
                task = input("dfir> ")
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
        if args.analyze_disk:
            task = f"Perform forensic analysis on {args.analyze_disk}. Look for deleted files, hidden data, and evidence of tampering."
        elif args.timeline:
            task = f"Create a forensic timeline from {args.timeline}. Analyze file access patterns and identify suspicious activity."
        elif args.investigate:
            task = "Investigate the current system for security incidents. Collect artifacts, identify IOCs, and determine the scope of compromise."
        else:
            task = "Perform initial triage of the system. Check for common indicators of compromise and suspicious artifacts."

        print(f"🎯 Starting forensic investigation...\n")
        print("─" * 80)

        result = await Runner.run(
            starting_agent=agent,
            input=task,
            run_config=RunConfig(tracing_disabled=True)
        )

        print("\n📊 FORENSIC ANALYSIS RESULTS")
        print("─" * 80)
        print(result.final_output)
        print("\n" + "═" * 80)

    print("\n⚠️  FORENSIC NOTICE: Maintain chain of custody. Document all findings.\n")


if __name__ == "__main__":
    asyncio.run(main())
