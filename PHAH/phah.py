#!/usr/bin/env python3
"""
PHAH - Plataforma de Hacking de Penetración Automatizada
Punto de entrada principal para pruebas de penetración automatizadas

Uso:
  phah.py -service web -target https://ejemplo.com [-port 8080] [-report]
  phah.py -service ssh -target 192.168.1.10 [-port 2222] [-report]
  phah.py -service samba -target 192.168.1.10 [-report]
"""

import sys
import asyncio
import argparse
from pathlib import Path

# Añadir raíz del proyecto al path
PROJECT_ROOT = Path(__file__).parent
sys.path.insert(0, str(PROJECT_ROOT))

from core import AutoPentester
from services import get_default_ports


def parse_arguments():
  """Analizar argumentos de línea de comandos"""
  parser = argparse.ArgumentParser(
    description='PHAH - Plataforma de Hacking de Penetración Automatizada',
    epilog='''
Ejemplos:
  phah.py -service web -target https://ejemplo.com -report
  phah.py -service ssh -target 192.168.1.10 -port 2222
  phah.py -service samba -target 192.168.1.10 -report
  phah.py -service ftp -target ftp.ejemplo.com
    ''',
    formatter_class=argparse.RawDescriptionHelpFormatter
  )

  parser.add_argument(
    '-service',
    type=str,
    required=False,
    help='Servicio a probar (web, ssh, samba, ftp, mysql, postgresql, rdp, dns, etc.)'
  )

  parser.add_argument(
    '-target',
    type=str,
    required=False,
    help='Host o URL objetivo'
  )

  parser.add_argument(
    '-port',
    type=int,
    default=None,
    help='Puerto objetivo (usa valores por defecto del servicio si no se especifica)'
  )

  parser.add_argument(
    '-report',
    action='store_true',
    help='Generar reporte detallado (HTML, Markdown, JSON)'
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
    help='Suprimir salida detallada (solo mostrar resultados finales)'
  )

  parser.add_argument(
    '--list-services',
    action='store_true',
    help='Listar servicios disponibles y salir'
  )

  args = parser.parse_args()

  # Validar argumentos requeridos cuando no se solicita solo el listado
  if not args.list_services:
    missing_args = []
    if not args.service:
      missing_args.append('-service')
    if not args.target:
      missing_args.append('-target')

    if missing_args:
      parser.error(f"los siguientes argumentos son requeridos: {', '.join(missing_args)}")

  return args


def list_services():
  """Listar servicios disponibles"""
  services = {
    'web': 'Pruebas de aplicaciones web (HTTP/HTTPS)',
    'ssh': 'Evaluación de seguridad del servicio SSH',
    'samba': 'Pruebas de seguridad Samba/SMB',
    'smb': 'Pruebas del servicio SMB (alias de samba)',
    'ftp': 'Evaluación de seguridad del servicio FTP',
    'mysql': 'Pruebas de seguridad de base de datos MySQL',
    'postgresql': 'Pruebas de base de datos PostgreSQL',
    'rdp': 'Evaluación de seguridad del servicio RDP',
    'dns': 'Pruebas de seguridad del servicio DNS',
    'smtp': 'Pruebas del servicio de correo SMTP',
    'pop3': 'Pruebas del servicio de correo POP3',
    'imap': 'Pruebas del servicio de correo IMAP',
    'telnet': 'Evaluación de seguridad del servicio Telnet',
    'vnc': 'Pruebas de seguridad del servicio VNC',
    'mongodb': 'Pruebas de seguridad de base de datos MongoDB',
    'redis': 'Pruebas de seguridad de base de datos Redis',
    'elasticsearch': 'Pruebas de seguridad de Elasticsearch',
  }

  print("\n╔════════════════════════════════════════════════════════════════╗")
  print("║              PHAH - Servicios Disponibles                      ║")
  print("╚════════════════════════════════════════════════════════════════╝\n")

  for service, description in sorted(services.items()):
    default_ports = get_default_ports(service)
    ports_str = ', '.join(map(str, default_ports)) if default_ports else 'N/A'
    print(f"  {service:15} - {description:45} [Puertos: {ports_str}]")

  print()


def print_banner():
  """Mostrar banner de PHAH"""
  banner = """
╔═════════════════════════════════════╗
║                                     ║
║   ██████╗ ██╗  ██╗ █████╗ ██╗  ██╗  ║
║   ██╔══██╗██║  ██║██╔══██╗██║  ██║  ║
║   ██████╔╝███████║███████║███████║  ║
║   ██╔═══╝ ██╔══██║██╔══██║██╔══██║  ║
║   ██║     ██║  ██║██║  ██║██║  ██║  ║
║   ╚═╝     ╚═╝  ╚═╝╚═╝  ╚═╝╚═╝  ╚═╝  ║
║         PYMEHackers AutoHack        ║
║                 v0.1                ║
║                                     ║
╚═════════════════════════════════════╝
"""
  print(banner)


async def main():
  """Punto de entrada principal"""
  # Analizar argumentos
  args = parse_arguments()

  # Listar servicios si se solicita
  if args.list_services:
    list_services()
    return 0

  # Mostrar banner
  if not args.quiet:
    print_banner()

  # Validar servicio
  service = args.service.lower()
  available_services = ['web', 'ssh', 'samba', 'smb', 'ftp', 'mysql', 'postgresql',
                        'rdp', 'dns', 'smtp', 'pop3', 'imap', 'telnet', 'vnc',
                        'mongodb', 'redis', 'elasticsearch']

  if service not in available_services:
    print(f"\n❌ Error: Servicio desconocido '{args.service}'")
    print(f"\nServicios disponibles: {', '.join(available_services)}")
    print(f"\nUsa --list-services para ver información detallada")
    return 1

  # Obtener puerto (usar valor por defecto si no se especifica)
  port = args.port
  if port is None:
    default_ports = get_default_ports(service)
    if default_ports:
      port = default_ports[0]  # Usar primer puerto por defecto

  # Mostrar configuración
  if not args.quiet:
    print(f"\n📋 Configuración:")
    print(f"   Servicio:      {service.upper()}")
    print(f"   Objetivo:      {args.target}")
    print(f"   Puerto:        {port if port else 'Por defecto'}")
    print(f"   Modelo:        {args.model}")
    print(f"   Reporte:       {'Sí' if args.report else 'No'}")
    print()

  # Crear pentester
  pentester = AutoPentester(
    service=service,
    target=args.target,
    port=port,
    model=args.model,
    verbose=not args.quiet,
    generate_report=args.report
  )

  # Ejecutar prueba
  try:
    result = await pentester.run()

    if result.get('success'):
      print("\n✅ Prueba de penetración completada con éxito!")
      if args.report:
        print("\n📊 Los reportes se han generado en el directorio 'reports/'")
      return 0
    else:
      print(f"\n❌ Prueba de penetración fallida: {result.get('error', 'Error desconocido')}")
      return 1

  except KeyboardInterrupt:
    print("\n\n⚠️  Prueba interrumpida por el usuario")
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
