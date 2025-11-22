#!/usr/bin/env python3
"""
Network Traffic Analyzer Service

Servicio para análisis de tráfico de red y detección de anomalías.
Especializado en análisis de pcap, detección de intrusiones y malware.

Uso:
    python services/network_analyzer.py --pcap capture.pcap
    python services/network_analyzer.py --interface eth0 --live
    python services/network_analyzer.py --analyze-traffic
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
    parser = argparse.ArgumentParser(description='Network Traffic Analyzer Service')
    parser.add_argument('--pcap', type=str, help='PCAP file to analyze')
    parser.add_argument('--interface', type=str, help='Network interface to monitor')
    parser.add_argument('--live', action='store_true', help='Live capture mode')
    parser.add_argument('--analyze-traffic', action='store_true', help='Analyze current network traffic')
    parser.add_argument('--model', default='llama3.2')
    parser.add_argument('--no-guardrails', action='store_true')
    return parser.parse_args()


async def main():
    args = parse_args()

    print("\n" + "═" * 80)
    print("📡 NETWORK TRAFFIC ANALYZER SERVICE")
    print("═" * 80)
    print(f"\n📋 Configuration:")
    print(f"  • Model: {args.model}")
    if args.pcap:
        print(f"  • PCAP File: {args.pcap}")
    if args.interface:
        print(f"  • Interface: {args.interface}")
    print()

    ollama = OllamaProvider(model_name=args.model)

    try:
        prompt = load_prompt_template("prompts/system_network_traffic_analyzer.md")
    except:
        prompt = """You are a network traffic analysis expert.
        Analyze network packets, detect anomalies, identify malware C2 traffic,
        and find indicators of compromise in network communications."""

    tools = [generic_linux_command, execute_code]

    agent_kwargs = {
        "name": "Network Analyzer",
        "description": "Network traffic analysis specialist",
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

    # Construir tarea
    if args.pcap:
        task = f"Analyze the PCAP file {args.pcap}. Identify suspicious connections, potential malware C2 traffic, and security threats."
    elif args.interface and args.live:
        task = f"Monitor network traffic on interface {args.interface}. Detect anomalies and potential security threats in real-time."
    elif args.analyze_traffic:
        task = "Analyze current network connections and traffic. Identify suspicious activity, unusual ports, and potential threats."
    else:
        task = "Analyze the current network configuration and active connections. Look for security issues and misconfigurations."

    print(f"🎯 Starting network analysis...\n")
    print("─" * 80)

    result = await Runner.run(
        starting_agent=agent,
        input=task,
        run_config=RunConfig(tracing_disabled=True)
    )

    print("\n📊 NETWORK ANALYSIS RESULTS")
    print("─" * 80)
    print(result.final_output)
    print("\n" + "═" * 80)


if __name__ == "__main__":
    asyncio.run(main())
