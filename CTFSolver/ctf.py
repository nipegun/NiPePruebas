#!/usr/bin/env python3
"""
CTF Solver - Resolución de desafíos CTF usando IA
Punto de entrada principal para resolver CTFs automatizados

Uso:
  ctf.py -category web -name "SQL Login" -target https://ctf.ejemplo.com [-port 8080] [-report]
  ctf.py -category crypto -name "Caesar Cipher" -files mensaje.enc [-description "Cifrado César con ROT13"]
  ctf.py -category forensics -name "Hidden Data" -files imagen.png [-report]
"""

import sys
import asyncio
import argparse
from pathlib import Path

# Añadir raíz del proyecto al path
PROJECT_ROOT = Path(__file__).parent
sys.path.insert(0, str(PROJECT_ROOT))

from core.ctfsolver import CTFSolver


def parse_arguments():
  """Analizar argumentos de línea de comandos"""
  parser = argparse.ArgumentParser(
    description='CTF Solver - Resolución automatizada de desafíos CTF usando IA',
    epilog='''
Ejemplos:
  ctf.py -category web -name "SQL Injection" -target http://ctf.local/login -report
  ctf.py -category crypto -name "Weak Cipher" -files cipher.txt -description "Descifra el mensaje"
  ctf.py -category forensics -name "Hidden Flag" -files image.png
  ctf.py -category pwn -name "Buffer Overflow" -target 192.168.1.100 -port 9001
    ''',
    formatter_class=argparse.RawDescriptionHelpFormatter
  )

  parser.add_argument(
    '-category',
    type=str,
    required=False,
    help='Categoría del CTF (web, crypto, forensics, pwn, reversing, misc, steganography, networking)'
  )

  parser.add_argument(
    '-name',
    type=str,
    required=False,
    help='Nombre del desafío CTF'
  )

  parser.add_argument(
    '-target',
    type=str,
    default=None,
    help='Host o URL objetivo (para desafíos remotos)'
  )

  parser.add_argument(
    '-port',
    type=int,
    default=None,
    help='Puerto objetivo (opcional)'
  )

  parser.add_argument(
    '-description',
    type=str,
    default=None,
    help='Descripción del desafío proporcionada por los organizadores'
  )

  parser.add_argument(
    '-files',
    type=str,
    nargs='+',
    default=None,
    help='Archivos proporcionados para el desafío (separados por espacios)'
  )

  parser.add_argument(
    '-report',
    action='store_true',
    help='Generar reporte detallado de la solución'
  )

  parser.add_argument(
    '-model',
    type=str,
    default='llama3.2',
    help='Modelo de Ollama a usar (por defecto: llama3.2)'
  )

  parser.add_argument(
    '-quiet',
    action='store_true',
    help='Suprimir salida detallada (solo mostrar resultado final)'
  )

  parser.add_argument(
    '--list-categories',
    action='store_true',
    help='Listar categorías de CTF disponibles y salir'
  )

  args = parser.parse_args()

  # Validar argumentos requeridos cuando no se solicita solo el listado
  if not args.list_categories:
    missing_args = []
    if not args.category:
      missing_args.append('-category')
    if not args.name:
      missing_args.append('-name')

    if missing_args:
      parser.error(f"los siguientes argumentos son requeridos: {', '.join(missing_args)}")

  return args


def list_categories():
  """Listar categorías de CTF disponibles"""
  categories = {
    'web': 'Vulnerabilidades en aplicaciones web (SQLi, XSS, LFI, RCE, etc.)',
    'crypto': 'Criptografía y criptoanálisis (cifrados, hashes, codificación)',
    'forensics': 'Análisis forense digital (archivos ocultos, metadatos, memoria)',
    'pwn': 'Explotación binaria (buffer overflow, ROP, shellcode)',
    'reversing': 'Ingeniería inversa (decompilación, análisis de binarios)',
    'misc': 'Miscelánea (programación, lógica, OSINT, trivia)',
    'steganography': 'Esteganografía (datos ocultos en imágenes/audio/video)',
    'networking': 'Análisis de red (pcap, protocolos, tráfico)',
    'osint': 'Open Source Intelligence (investigación en fuentes públicas)',
    'mobile': 'Seguridad móvil (Android, iOS)',
    'hardware': 'Seguridad de hardware (IoT, firmware, radio)',
    'cloud': 'Seguridad en la nube (AWS, Azure, GCP misconfigurations)',
  }

  print("\n╔════════════════════════════════════════════════════════════════╗")
  print("║            CTF Solver - Categorías Disponibles                ║")
  print("╚════════════════════════════════════════════════════════════════╝\n")

  for category, description in sorted(categories.items()):
    print(f"  {category:15} - {description}")

  print("\n💡 Consejo: Usa -description para proporcionar el enunciado del desafío")
  print("💡 Usa -files para especificar archivos descargados del CTF\n")


def print_banner():
  """Mostrar banner de CTF Solver"""
  banner = """
╔═════════════════════════════════════════════╗
║                                             ║
║    ██████╗████████╗███████╗                 ║
║   ██╔════╝╚══██╔══╝██╔════╝                 ║
║   ██║        ██║   █████╗                   ║
║   ██║        ██║   ██╔══╝                   ║
║   ╚██████╗   ██║   ██║                      ║
║    ╚═════╝   ╚═╝   ╚═╝                      ║
║              SOLVER                         ║
║          AI-Powered CTF Solution            ║
║                  v1.0                       ║
║                                             ║
╚═════════════════════════════════════════════╝
"""
  print(banner)


async def main():
  """Punto de entrada principal"""
  # Analizar argumentos
  args = parse_arguments()

  # Listar categorías si se solicita
  if args.list_categories:
    list_categories()
    return 0

  # Mostrar banner
  if not args.quiet:
    print_banner()

  # Validar categoría
  category = args.category.lower()
  available_categories = [
    'web', 'crypto', 'forensics', 'pwn', 'reversing', 'misc',
    'steganography', 'networking', 'osint', 'mobile', 'hardware', 'cloud'
  ]

  if category not in available_categories:
    print(f"\n❌ Error: Categoría desconocida '{args.category}'")
    print(f"\nCategorías disponibles: {', '.join(available_categories)}")
    print(f"\nUsa --list-categories para ver información detallada")
    return 1

  # Validar que al menos haya target o files
  if not args.target and not args.files:
    print("\n⚠️  Advertencia: No se especificó ni -target ni -files")
    print("   Algunos desafíos CTF requieren al menos uno de estos parámetros")
    response = input("\n¿Deseas continuar de todos modos? [s/N]: ")
    if response.lower() not in ['s', 'si', 'sí', 'y', 'yes']:
      print("Operación cancelada")
      return 1

  # Mostrar configuración
  if not args.quiet:
    print(f"\n📋 Configuración del CTF:")
    print(f"   Categoría:     {category.upper()}")
    print(f"   Desafío:       {args.name}")
    if args.target:
      print(f"   Objetivo:      {args.target}")
    if args.port:
      print(f"   Puerto:        {args.port}")
    if args.files:
      print(f"   Archivos:      {', '.join(args.files)}")
    if args.description:
      print(f"   Descripción:   {args.description[:60]}{'...' if len(args.description) > 60 else ''}")
    print(f"   Modelo:        {args.model}")
    print(f"   Reporte:       {'Sí' if args.report else 'No'}")
    print()

  # Crear solver
  solver = CTFSolver(
    category=category,
    challenge_name=args.name,
    target=args.target,
    port=args.port,
    description=args.description,
    files=args.files,
    model=args.model,
    verbose=not args.quiet,
    generate_report=args.report
  )

  # Ejecutar resolución
  try:
    result = await solver.run()

    if result.get('success'):
      print("\n" + "="*60)
      print("✅ ¡CTF RESUELTO CON ÉXITO!")
      print("="*60)
      
      if result.get('flags_found'):
        print("\n🚩 FLAGS ENCONTRADAS:")
        for flag in result['flags_found']:
          print(f"   {flag}")
      
      if args.report:
        print("\n📊 Reporte generado en el directorio 'reports/'")
      
      print()
      return 0
    else:
      print("\n" + "="*60)
      print("❌ No se pudo resolver el CTF")
      print("="*60)
      
      error = result.get('error', 'Error desconocido')
      print(f"\nMotivo: {error}")
      
      if result.get('attempts'):
        print(f"\nIntentos realizados: {len(result['attempts'])}")
        print("\n💡 Consejos:")
        print("   - Revisa la descripción del desafío")
        print("   - Verifica que los archivos estén en el directorio correcto")
        print("   - Prueba con un modelo más potente (-model)")
        print("   - Genera un reporte (-report) para ver el análisis completo")
      
      print()
      return 1

  except KeyboardInterrupt:
    print("\n\n⚠️  Resolución interrumpida por el usuario")
    return 130
  except Exception as e:
    print(f"\n❌ Error fatal: {str(e)}")
    if not args.quiet:
      import traceback
      traceback.print_exc()
    return 1


if __name__ == '__main__':
  exit_code = asyncio.run(main())
  sys.exit(exit_code)
