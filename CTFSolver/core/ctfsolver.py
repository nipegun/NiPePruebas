#!/usr/bin/env python3
"""
Módulo CTF Solver
Resuelve desafíos CTF (Capture The Flag) usando IA
"""

import asyncio
from datetime import datetime
from typing import Optional, List, Dict, Any
from pathlib import Path

from .ollama_client import OllamaClient
from .report_generator import ReportGenerator
from tools.command_executor import CommandExecutor


class CTFSolver:
  """Clase principal para resolver desafíos CTF automatizados"""

  def __init__(
    self,
    category: str,
    challenge_name: str,
    target: Optional[str] = None,
    port: Optional[int] = None,
    description: Optional[str] = None,
    files: Optional[List[str]] = None,
    model: str = "llama3.2",
    verbose: bool = True,
    generate_report: bool = False
  ):
    """
    Inicializa CTF Solver

    Args:
      category: Categoría del CTF (web, crypto, forensics, pwn, reversing, misc, etc.)
      challenge_name: Nombre del desafío
      target: Host o URL objetivo (opcional para algunos CTFs)
      port: Puerto objetivo (opcional)
      description: Descripción del desafío proporcionada
      files: Lista de archivos proporcionados para el desafío
      model: Modelo de Ollama a usar
      verbose: Mostrar salida detallada
      generate_report: Generar reporte después de resolver
    """
    self.category = category.lower()
    self.challenge_name = challenge_name
    self.target = target
    self.port = port
    self.description = description or "No se proporcionó descripción"
    self.files = files or []
    self.model = model
    self.verbose = verbose
    self.generate_report_flag = generate_report

    # Componentes
    self.ollama_client = OllamaClient(model=model)
    self.command_executor = CommandExecutor(verbose=verbose)
    self.report_generator = ReportGenerator()

    # Datos del CTF
    self.attempts: List[Dict[str, Any]] = []
    self.flags_found: List[str] = []
    self.start_time: Optional[datetime] = None
    self.end_time: Optional[datetime] = None

  def _print(self, message: str, prefix: str = ""):
    """Mostrar mensaje si verbose está activo"""
    if self.verbose:
      timestamp = datetime.now().strftime("%H:%M:%S")
      if prefix:
        print(f"[{timestamp}] [{prefix}] {message}")
      else:
        print(f"[{timestamp}] {message}")

  async def load_category_prompt(self) -> str:
    """
    Cargar prompt del sistema para la categoría específica de CTF

    Returns:
      Contenido del prompt del sistema
    """
    prompt_file = Path(__file__).parent.parent / "prompts" / f"ctf_{self.category}.md"

    if prompt_file.exists():
      with open(prompt_file, 'r', encoding='utf-8') as f:
        return f.read()
    else:
      # Prompt genérico por defecto
      return f"""Eres un experto en resolver desafíos CTF (Capture The Flag) especializado en {self.category.upper()}.

Tu función es:
1. Analizar el desafío proporcionado
2. Identificar el tipo de vulnerabilidad o técnica necesaria
3. Proponer un enfoque sistemático para resolver el desafío
4. Ejecutar comandos y analizar resultados
5. Encontrar la flag (formato típico: flag{{...}} o CTF{{...}} o similar)

Información del Desafío:
- Categoría: {self.category.upper()}
- Nombre: {self.challenge_name}
- Descripción: {self.description}
- Objetivo: {self.target if self.target else 'N/A'}
- Puerto: {self.port if self.port else 'N/A'}
- Archivos proporcionados: {', '.join(self.files) if self.files else 'Ninguno'}

CATEGORÍAS COMUNES DE CTF:
- **web**: Vulnerabilidades web (SQLi, XSS, LFI, RCE, etc.)
- **crypto**: Criptografía (cifrados débiles, hashes, codificación)
- **forensics**: Análisis forense (archivos ocultos, metadatos, esteganografía)
- **pwn**: Explotación binaria (buffer overflow, ROP, shellcode)
- **reversing**: Ingeniería inversa (análisis de binarios, decompilación)
- **misc**: Miscelánea (programación, lógica, OSINT)
- **steganography**: Datos ocultos en imágenes/audio
- **networking**: Análisis de tráfico de red (pcap, protocolos)

HERRAMIENTAS COMUNES POR CATEGORÍA:
- **web**: curl, wget, burpsuite, sqlmap, dirb, nikto
- **crypto**: python, openssl, hashcat, john, cyberchef
- **forensics**: binwalk, exiftool, strings, foremost, volatility
- **pwn**: gdb, pwntools, checksec, objdump, radare2
- **reversing**: ghidra, radare2, strings, ltrace, strace
- **steganography**: steghide, zsteg, binwalk, exiftool
- **networking**: wireshark, tcpdump, tshark, scapy

METODOLOGÍA:
1. **Reconocimiento**: Analizar toda la información proporcionada
2. **Investigación**: Identificar posibles vectores de ataque
3. **Experimentación**: Probar diferentes técnicas
4. **Análisis**: Examinar resultados de cada intento
5. **Iteración**: Ajustar enfoque basándose en hallazgos
6. **Solución**: Encontrar y extraer la flag

IMPORTANTE:
- La flag suele tener formatos como: flag{{...}}, CTF{{...}}, HTB{{...}}, etc.
- Busca patrones sospechosos en salidas de comandos
- Considera múltiples enfoques si uno no funciona
- Documenta cada intento y resultado
- Piensa creativamente - los CTFs suelen tener trucos ingeniosos

Presenta tu análisis paso a paso, explica tu razonamiento y sugiere comandos concretos a ejecutar.

Comencemos el análisis del desafío."""

  async def run(self) -> Dict[str, Any]:
    """
    Ejecutar la resolución del CTF

    Returns:
      Diccionario con resultados de la resolución
    """
    self.start_time = datetime.now()
    self._print("=" * 80, "CTF SOLVER")
    self._print(f"Iniciando resolución de CTF", "CTF SOLVER")
    self._print(f"Categoría: {self.category.upper()}", "CTF SOLVER")
    self._print(f"Desafío: {self.challenge_name}", "CTF SOLVER")
    if self.target:
      self._print(f"Objetivo: {self.target}", "CTF SOLVER")
    if self.files:
      self._print(f"Archivos: {', '.join(self.files)}", "CTF SOLVER")
    self._print("=" * 80, "CTF SOLVER")

    try:
      # Cargar prompt específico de la categoría
      system_prompt = await self.load_category_prompt()

      # Inicializar conversación con el LLM
      self._print("Inicializando solver de IA...", "IA")
      initial_message = f"""Analiza este desafío CTF:

**Categoría**: {self.category.upper()}
**Nombre**: {self.challenge_name}
**Descripción**: {self.description}
"""
      
      if self.target:
        initial_message += f"**Objetivo**: {self.target}\n"
      if self.port:
        initial_message += f"**Puerto**: {self.port}\n"
      if self.files:
        initial_message += f"**Archivos proporcionados**: {', '.join(self.files)}\n"

      initial_message += "\n¿Cuál es tu análisis inicial y qué enfoque sugieres?"

      response = await self.ollama_client.chat(
        message=initial_message,
        system_prompt=system_prompt,
        temperature=0.7
      )

      self._print("Solver de IA inicializado", "IA")
      if self.verbose:
        print(f"\n{response}\n")

      # Bucle iterativo de resolución
      max_iterations = 15  # Más iteraciones para CTFs complejos
      iteration = 0
      flag_found = False

      while iteration < max_iterations and not flag_found:
        iteration += 1
        self._print(f"Iteración {iteration}/{max_iterations}", "BUCLE")

        # Pedir al LLM el siguiente paso
        next_action_prompt = """Basándote en el análisis actual, ¿cuál es el siguiente paso?

Responde con SOLO UNA de las siguientes opciones:
1. Un único comando a ejecutar (ej: "strings archivo.bin | grep flag")
2. "ANALIZAR [archivo]" si quieres examinar un archivo específico
3. "FLAG: [contenido]" si crees haber encontrado la flag
4. "REFLEXION" si necesitas reconsiderar el enfoque
5. "RESUELTO" si has encontrado la flag y verificado la solución

Tu respuesta:"""

        action_response = await self.ollama_client.chat(
          message=next_action_prompt,
          temperature=0.5
        )

        action = action_response.strip()

        # Comprobar si encontró la flag
        if "FLAG:" in action.upper() or "RESUELTO" in action.upper():
          self._print("¡Posible flag encontrada!", "IA")
          # Extraer la flag
          flag = self._extract_flag(action)
          if flag:
            self.flags_found.append(flag)
            self._print(f"Flag: {flag}", "FLAG")
            flag_found = True
            
            # Verificar que es una flag válida
            verification_prompt = f"¿Es '{flag}' una flag válida para este desafío? ¿Tiene el formato correcto?"
            verification = await self.ollama_client.chat(
              message=verification_prompt,
              temperature=0.3
            )
            if self.verbose:
              print(f"\n{verification}\n")
          break

        # Comprobar si quiere reflexionar
        if "REFLEXION" in action.upper():
          self._print("Replanteando enfoque...", "IA")
          reflection_prompt = "Basándote en lo que hemos intentado, ¿qué otros enfoques podríamos probar? ¿Hay algo que hayamos pasado por alto?"
          reflection = await self.ollama_client.chat(
            message=reflection_prompt,
            temperature=0.7
          )
          if self.verbose:
            print(f"\n{reflection}\n")
          continue

        # Comprobar si quiere analizar un archivo
        if "ANALIZAR" in action.upper():
          # Extraer nombre del archivo
          parts = action.split()
          if len(parts) > 1:
            file_to_analyze = parts[1]
            self._print(f"Analizando archivo: {file_to_analyze}", "ANÁLISIS")
            # Ejecutar comandos de análisis común
            commands = [
              f"file {file_to_analyze}",
              f"strings {file_to_analyze}",
              f"exiftool {file_to_analyze}"
            ]
            for cmd in commands:
              output = await self.command_executor.execute_and_get_output(cmd)
              if output and self.verbose:
                print(f"\n--- {cmd} ---\n{output}\n")
              
              # Analizar salida
              analysis_prompt = f"Analiza esta salida del comando '{cmd}' en busca de pistas o la flag."
              analysis = await self.ollama_client.chat_with_tools(
                message=analysis_prompt,
                tools_output=output,
                temperature=0.7
              )
              if self.verbose:
                print(f"\n{analysis}\n")
              
              # Buscar flags en la salida
              flag = self._extract_flag(output)
              if flag:
                self.flags_found.append(flag)
                self._print(f"¡Flag encontrada en salida: {flag}!", "FLAG")
                flag_found = True
                break
          continue

        # Extraer comando
        command = self._extract_command(action)

        if command:
          # Ejecutar comando
          self._print(f"Ejecutando: {command}", "CMD")
          output = await self.command_executor.execute_and_get_output(command)

          # Registrar intento
          self.attempts.append({
            "iteration": iteration,
            "command": command,
            "output": output[:500] if output else ""  # Limitar para el reporte
          })

          # Mostrar salida si verbose está activo
          if self.verbose and output:
            print(f"\n--- Salida ---\n{output}\n--- Fin Salida ---\n")

          # Buscar flag en la salida
          flag = self._extract_flag(output)
          if flag:
            self.flags_found.append(flag)
            self._print(f"¡Flag encontrada: {flag}!", "FLAG")
            flag_found = True
            break

          # Enviar resultados de vuelta al LLM
          analysis_prompt = f"Analiza la salida del comando '{command}'. ¿Qué información útil revela? ¿Estamos más cerca de la flag?"
          analysis = await self.ollama_client.chat_with_tools(
            message=analysis_prompt,
            tools_output=output,
            temperature=0.7
          )

          if self.verbose:
            print(f"\n{analysis}\n")
        else:
          self._print("No se pudo extraer un comando válido, continuando...", "AVISO")

      # Resumen final
      self.end_time = datetime.now()
      self._print("=" * 80, "CTF SOLVER")
      if flag_found:
        self._print("¡CTF resuelto con éxito!", "CTF SOLVER")
        self._print(f"Flags encontradas: {', '.join(self.flags_found)}", "CTF SOLVER")
      else:
        self._print("No se pudo resolver el CTF en el tiempo asignado", "CTF SOLVER")
      self._print(f"Duración: {self.end_time - self.start_time}", "CTF SOLVER")
      self._print(f"Intentos realizados: {len(self.attempts)}", "CTF SOLVER")
      self._print("=" * 80, "CTF SOLVER")

      # Generar reporte si se solicita
      if self.generate_report_flag:
        await self.generate_report()

      return {
        "success": flag_found,
        "category": self.category,
        "challenge_name": self.challenge_name,
        "flags_found": self.flags_found,
        "attempts": self.attempts,
        "start_time": self.start_time,
        "end_time": self.end_time
      }

    except KeyboardInterrupt:
      self._print("Resolución interrumpida por el usuario", "AVISO")
      return {"success": False, "error": "Interrumpido"}
    except Exception as e:
      self._print(f"Error durante la resolución: {str(e)}", "ERROR")
      import traceback
      if self.verbose:
        traceback.print_exc()
      return {"success": False, "error": str(e)}
    finally:
      await self.ollama_client.close()

  def _extract_command(self, text: str) -> Optional[str]:
    """
    Extraer comando de la respuesta del LLM

    Args:
      text: Texto de respuesta del LLM

    Returns:
      Comando extraído o None
    """
    # Eliminar bloques de código markdown comunes
    text = text.strip()

    # Eliminar marcadores ``` o ```bash
    if "```" in text:
      lines = text.split('\n')
      command_lines = []
      in_code_block = False

      for line in lines:
        if line.strip().startswith("```"):
          in_code_block = not in_code_block
          continue
        if in_code_block and line.strip():
          command_lines.append(line.strip())

      if command_lines:
        return command_lines[0]

    # Intentar encontrar patrones que parezcan comandos
    lines = text.split('\n')
    for line in lines:
      line = line.strip()
      # Saltar líneas vacías y líneas que parezcan explicaciones
      if not line or line.endswith(':') or line.endswith('?'):
        continue
      
      # Comandos comunes en CTFs
      common_commands = [
        'cat', 'strings', 'file', 'binwalk', 'exiftool', 'steghide', 'zsteg',
        'curl', 'wget', 'python', 'python3', 'nc', 'netcat', 'nmap',
        'john', 'hashcat', 'base64', 'openssl', 'gpg',
        'gdb', 'objdump', 'readelf', 'ltrace', 'strace',
        'wireshark', 'tshark', 'tcpdump', 'foremost', 'volatility',
        'sqlmap', 'dirb', 'gobuster', 'ffuf', 'wfuzz',
        'grep', 'find', 'ls', 'xxd', 'hexdump', 'dd'
      ]
      
      if any(line.startswith(cmd) for cmd in common_commands):
        return line

    return None

  def _extract_flag(self, text: str) -> Optional[str]:
    """
    Extraer flag de un texto

    Args:
      text: Texto donde buscar la flag

    Returns:
      Flag encontrada o None
    """
    if not text:
      return None

    import re
    
    # Patrones comunes de flags
    flag_patterns = [
      r'flag\{[^}]+\}',
      r'FLAG\{[^}]+\}',
      r'CTF\{[^}]+\}',
      r'HTB\{[^}]+\}',
      r'picoCTF\{[^}]+\}',
      r'THM\{[^}]+\}',
      r'\w+\{[^}]{8,}\}',  # Formato genérico {contenido}
    ]

    for pattern in flag_patterns:
      matches = re.findall(pattern, text, re.IGNORECASE)
      if matches:
        return matches[0]

    return None

  async def generate_report(self):
    """Generar reporte de resolución de CTF"""
    self._print("Generando reporte...", "REPORTE")

    # Obtener historial de conversación para análisis
    llm_history = self.ollama_client.get_history()

    # Extraer análisis final del LLM
    llm_analysis = ""
    for msg in reversed(llm_history):
      if msg.get("role") == "assistant":
        content = msg.get("content", "")
        if len(content) > 100:
          llm_analysis = content
          break

    # Obtener historial de comandos
    commands = [cmd["command"] for cmd in self.command_executor.get_history()]

    # Crear contenido del reporte personalizado para CTF
    report_data = {
      "challenge_name": self.challenge_name,
      "category": self.category,
      "target": self.target,
      "port": self.port,
      "description": self.description,
      "files": self.files,
      "flags_found": self.flags_found,
      "attempts": self.attempts,
      "commands_executed": commands,
      "llm_analysis": llm_analysis,
      "start_time": self.start_time,
      "end_time": self.end_time,
      "duration": str(self.end_time - self.start_time) if self.end_time and self.start_time else "N/A"
    }

    # Generar reportes (reutilizando el generador existente adaptado)
    from datetime import datetime
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    reports_dir = Path("reports")
    reports_dir.mkdir(exist_ok=True)

    # Reporte Markdown
    md_file = reports_dir / f"ctf_{self.category}_{timestamp}.md"
    with open(md_file, 'w', encoding='utf-8') as f:
      f.write(f"# CTF Resolution Report\n\n")
      f.write(f"**Challenge**: {self.challenge_name}\n")
      f.write(f"**Category**: {self.category.upper()}\n")
      f.write(f"**Status**: {'✅ SOLVED' if self.flags_found else '❌ UNSOLVED'}\n\n")
      
      if self.flags_found:
        f.write(f"## 🚩 Flags Found\n\n")
        for flag in self.flags_found:
          f.write(f"- `{flag}`\n")
        f.write("\n")
      
      f.write(f"## 📋 Challenge Information\n\n")
      f.write(f"**Description**: {self.description}\n\n")
      if self.target:
        f.write(f"**Target**: {self.target}\n\n")
      if self.files:
        f.write(f"**Files**: {', '.join(self.files)}\n\n")
      
      f.write(f"## 🔍 Solution Process\n\n")
      f.write(f"**Attempts**: {len(self.attempts)}\n")
      f.write(f"**Duration**: {report_data['duration']}\n\n")
      
      f.write(f"### Commands Executed\n\n")
      for i, cmd in enumerate(commands, 1):
        f.write(f"{i}. `{cmd}`\n")
      
      f.write(f"\n### AI Analysis\n\n")
      f.write(f"{llm_analysis}\n")

    self._print(f"Reportes generados:", "REPORTE")
    self._print(f"  - Markdown: {md_file}", "REPORTE")
