#!/usr/bin/env python3
"""
Memory Forensics Service

Servicio para análisis forense de memoria RAM.
Especializado en análisis de volcados de memoria y detección de malware en memoria.

Uso:
    python services/memory_forensics.py --dump memory.raw
    python services/memory_forensics.py --analyze-process 1234
    python services/memory_forensics.py --live-analysis
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
    parser = argparse.ArgumentParser(description='Memory Forensics Service')
    parser.add_argument('--dump', type=str, help='Memory dump file to analyze')
    parser.add_argument('--analyze-process', type=str, help='Process ID to analyze')
    parser.add_argument('--live-analysis', action='store_true', help='Analyze live system memory')
    parser.add_argument('--model', default='llama3.2')
    parser.add_argument('--no-guardrails', action='store_true')
    return parser.parse_args()


async def main():
    args = parse_args()

    print("\n" + "═" * 80)
    print("🧠 MEMORY FORENSICS SERVICE")
    print("═" * 80)
    print(f"\n📋 Configuration:")
    print(f"  • Model: {args.model}")
    if args.dump:
        print(f"  • Memory Dump: {args.dump}")
    if args.analyze_process:
        print(f"  • Process ID: {args.analyze_process}")
    print()

    ollama = OllamaProvider(model_name=args.model)

    try:
        prompt = load_prompt_template("prompts/system_memory_analysis_agent.md")
    except:
        prompt = """You are a memory forensics expert specializing in RAM analysis.
        You can analyze memory dumps, detect process injection, find malware artifacts,
        and identify rootkits hiding in memory."""

    tools = [generic_linux_command, execute_code]

    agent_kwargs = {
        "name": "Memory Forensics Analyst",
        "description": "Memory forensics and malware detection specialist",
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

    if args.dump:
        task = f"Analyze the memory dump file {args.dump}. Look for suspicious processes, injected code, and malware artifacts."
    elif args.analyze_process:
        task = f"Analyze the memory of process ID {args.analyze_process}. Check for code injection, suspicious modules, and malicious activity."
    elif args.live_analysis:
        task = "Perform live memory analysis of the current system. Identify suspicious processes, rootkits, and memory anomalies."
    else:
        task = "Analyze current system memory for security threats. Check running processes, loaded modules, and memory patterns."

    print(f"🎯 Starting memory forensics analysis...\n")
    print("─" * 80)

    result = await Runner.run(
        starting_agent=agent,
        input=task,
        run_config=RunConfig(tracing_disabled=True)
    )

    print("\n📊 MEMORY FORENSICS RESULTS")
    print("─" * 80)
    print(result.final_output)
    print("\n" + "═" * 80)


if __name__ == "__main__":
    asyncio.run(main())
