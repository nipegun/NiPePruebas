#!/usr/bin/env python3
"""
Generador de Reportes para PHAH
Genera reportes profesionales de pruebas de penetración
"""

import os
import json
from datetime import datetime
from typing import List, Dict, Any, Optional
from pathlib import Path


class ReportGenerator:
  """Genera reportes de pruebas de penetración en varios formatos"""

  def __init__(self, output_dir: str = "reports"):
    """
    Inicializa el generador de reportes

    Args:
      output_dir: Directorio donde guardar los reportes
    """
    self.output_dir = Path(output_dir)
    self.output_dir.mkdir(parents=True, exist_ok=True)

  def generate_markdown_report(
    self,
    service: str,
    target: str,
    port: Optional[int],
    findings: List[Dict[str, Any]],
    commands_executed: List[str],
    llm_analysis: str,
    start_time: datetime,
    end_time: datetime
  ) -> str:
    """
    Genera un reporte en formato Markdown

    Args:
      service: Tipo de servicio (web, ssh, etc.)
      target: Host/URL objetivo
      port: Puerto objetivo
      findings: Lista de hallazgos
      commands_executed: Lista de comandos ejecutados
      llm_analysis: Análisis del LLM
      start_time: Hora de inicio de la prueba
      end_time: Hora de finalización de la prueba

    Returns:
      Ruta al archivo de reporte generado
    """
    timestamp = start_time.strftime("%Y%m%d_%H%M%S")
    filename = f"phah_{service}_{target.replace('://', '_').replace('/', '_')}_{timestamp}.md"
    filepath = self.output_dir / filename

    # Calcular duración
    duration = end_time - start_time
    duration_str = str(duration).split('.')[0]  # Eliminar microsegundos

    # Construir contenido del reporte
    report = f"""# Reporte de Prueba de Penetración PHAH

## Resumen Ejecutivo

**Servicio**: {service.upper()}
**Objetivo**: {target}
**Puerto**: {port if port else 'Por defecto'}
**Hora de Inicio**: {start_time.strftime('%Y-%m-%d %H:%M:%S')}
**Hora de Finalización**: {end_time.strftime('%Y-%m-%d %H:%M:%S')}
**Duración**: {duration_str}
**Generado Por**: PHAH (Plataforma de Hacking de Penetración Automatizada)

---

## Tabla de Contenidos

1. [Alcance](#alcance)
2. [Metodología](#metodología)
3. [Hallazgos](#hallazgos)
4. [Comandos Ejecutados](#comandos-ejecutados)
5. [Análisis de IA](#análisis-de-ia)
6. [Recomendaciones](#recomendaciones)

---

## Alcance

Esta prueba de penetración se realizó contra:
- **Objetivo**: {target}
- **Servicio**: {service.upper()}
- **Puerto(s)**: {port if port else 'Puertos por defecto del servicio'}

---

## Metodología

Esta prueba de penetración automatizada utilizó:
- Reconocimiento y explotación potenciados por IA
- Herramientas estándar de la industria para pruebas de penetración
- LLM Ollama para toma de decisiones inteligente y análisis

---

## Hallazgos

"""

    # Añadir hallazgos
    if findings:
      for i, finding in enumerate(findings, 1):
        severity = finding.get('severity', 'Info')
        title = finding.get('title', 'Hallazgo')
        description = finding.get('description', '')

        report += f"""### {i}. {title}

**Gravedad**: {severity}

{description}

"""
    else:
      report += "No se descubrieron hallazgos significativos durante esta prueba.\n\n"

    # Añadir comandos ejecutados
    report += """---

## Comandos Ejecutados

Los siguientes comandos se ejecutaron durante la prueba de penetración:

```bash
"""
    for cmd in commands_executed:
      report += f"{cmd}\n"

    report += """```

---

## Análisis de IA

"""
    report += llm_analysis + "\n\n"

    # Añadir recomendaciones
    report += """---

## Recomendaciones

### Acciones Inmediatas

"""
    # Extraer recomendaciones del análisis del LLM o añadir genéricas
    report += """
1. Revisar todos los hallazgos marcados con gravedad ALTA o CRÍTICA
2. Aplicar parches y actualizaciones de seguridad a servicios vulnerables
3. Implementar controles de acceso y autenticación apropiados
4. Activar monitorización y registro de seguridad

### Mejoras de Seguridad a Largo Plazo

1. Realizar evaluaciones de seguridad regulares
2. Implementar un programa de gestión de vulnerabilidades
3. Proporcionar formación en concienciación de seguridad
4. Mantener un plan de respuesta a incidentes

---

## Descargo de Responsabilidad

Este reporte fue generado por una herramienta automatizada de pruebas de penetración potenciada por IA.
Los hallazgos deben ser revisados por profesionales de seguridad cualificados.
Esta prueba se realizó de manera autorizada en sistemas que posees o para los que tienes permiso de prueba.

**IMPORTANTE**: El acceso no autorizado a sistemas informáticos es ilegal.

---

*Reporte generado el {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}*
*PHAH Versión 1.0*
"""

    # Escribir reporte al archivo
    with open(filepath, 'w', encoding='utf-8') as f:
      f.write(report)

    return str(filepath)

  def generate_json_report(
    self,
    service: str,
    target: str,
    port: Optional[int],
    findings: List[Dict[str, Any]],
    commands_executed: List[str],
    llm_analysis: str,
    start_time: datetime,
    end_time: datetime
  ) -> str:
    """
    Genera un reporte en formato JSON

    Args:
      service: Tipo de servicio
      target: Host/URL objetivo
      port: Puerto objetivo
      findings: Lista de hallazgos
      commands_executed: Comandos ejecutados
      llm_analysis: Análisis del LLM
      start_time: Hora de inicio de la prueba
      end_time: Hora de finalización de la prueba

    Returns:
      Ruta al archivo de reporte generado
    """
    timestamp = start_time.strftime("%Y%m%d_%H%M%S")
    filename = f"phah_{service}_{target.replace('://', '_').replace('/', '_')}_{timestamp}.json"
    filepath = self.output_dir / filename

    report_data = {
      "metadatos": {
        "herramienta": "PHAH",
        "version": "1.0",
        "servicio": service,
        "objetivo": target,
        "puerto": port,
        "hora_inicio": start_time.isoformat(),
        "hora_fin": end_time.isoformat(),
        "duracion_segundos": (end_time - start_time).total_seconds()
      },
      "hallazgos": findings,
      "comandos_ejecutados": commands_executed,
      "analisis_llm": llm_analysis
    }

    with open(filepath, 'w', encoding='utf-8') as f:
      json.dump(report_data, f, indent=2, ensure_ascii=False)

    return str(filepath)

  def generate_html_report(
    self,
    service: str,
    target: str,
    port: Optional[int],
    findings: List[Dict[str, Any]],
    commands_executed: List[str],
    llm_analysis: str,
    start_time: datetime,
    end_time: datetime
  ) -> str:
    """
    Genera un reporte en formato HTML

    Args:
      service: Tipo de servicio
      target: Host/URL objetivo
      port: Puerto objetivo
      findings: Lista de hallazgos
      commands_executed: Comandos ejecutados
      llm_analysis: Análisis del LLM
      start_time: Hora de inicio de la prueba
      end_time: Hora de finalización de la prueba

    Returns:
      Ruta al archivo de reporte generado
    """
    timestamp = start_time.strftime("%Y%m%d_%H%M%S")
    filename = f"phah_{service}_{target.replace('://', '_').replace('/', '_')}_{timestamp}.html"
    filepath = self.output_dir / filename

    duration = str(end_time - start_time).split('.')[0]

    # Mapeo de colores de gravedad
    severity_colors = {
      'CRÍTICO': '#dc3545',
      'CRITICO': '#dc3545',
      'CRITICAL': '#dc3545',
      'ALTO': '#fd7e14',
      'HIGH': '#fd7e14',
      'MEDIO': '#ffc107',
      'MEDIUM': '#ffc107',
      'BAJO': '#17a2b8',
      'LOW': '#17a2b8',
      'INFO': '#6c757d'
    }

    # Construir HTML de hallazgos
    findings_html = ""
    if findings:
      for i, finding in enumerate(findings, 1):
        severity = finding.get('severity', 'INFO').upper()
        title = finding.get('title', 'Hallazgo')
        description = finding.get('description', '')
        color = severity_colors.get(severity, '#6c757d')

        findings_html += f"""
        <div class="finding">
          <h3>{i}. {title}</h3>
          <span class="severity" style="background-color: {color};">{severity}</span>
          <p>{description}</p>
        </div>
        """
    else:
      findings_html = '<p class="no-findings">No se descubrieron hallazgos significativos.</p>'

    # Construir HTML de comandos
    commands_html = "<br>".join(commands_executed)

    html_content = f"""<!DOCTYPE html>
<html lang="es">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>Reporte PHAH - {service.upper()} - {target}</title>
  <style>
    body {{
      font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
      line-height: 1.6;
      max-width: 1200px;
      margin: 0 auto;
      padding: 20px;
      background-color: #f5f5f5;
    }}
    .header {{
      background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
      color: white;
      padding: 30px;
      border-radius: 10px;
      margin-bottom: 30px;
    }}
    .header h1 {{
      margin: 0;
      font-size: 2.5em;
    }}
    .info-grid {{
      display: grid;
      grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
      gap: 15px;
      margin-top: 20px;
    }}
    .info-item {{
      background: rgba(255,255,255,0.2);
      padding: 10px;
      border-radius: 5px;
    }}
    .info-label {{
      font-size: 0.9em;
      opacity: 0.9;
    }}
    .info-value {{
      font-size: 1.2em;
      font-weight: bold;
    }}
    .section {{
      background: white;
      padding: 25px;
      margin-bottom: 20px;
      border-radius: 10px;
      box-shadow: 0 2px 4px rgba(0,0,0,0.1);
    }}
    .section h2 {{
      color: #667eea;
      border-bottom: 2px solid #667eea;
      padding-bottom: 10px;
    }}
    .finding {{
      background: #f8f9fa;
      padding: 15px;
      margin: 15px 0;
      border-left: 4px solid #667eea;
      border-radius: 5px;
    }}
    .severity {{
      display: inline-block;
      color: white;
      padding: 5px 15px;
      border-radius: 20px;
      font-size: 0.9em;
      font-weight: bold;
      margin: 10px 0;
    }}
    .commands {{
      background: #2d2d2d;
      color: #f8f8f2;
      padding: 20px;
      border-radius: 5px;
      font-family: 'Courier New', monospace;
      overflow-x: auto;
    }}
    .analysis {{
      background: #e8f4f8;
      padding: 20px;
      border-left: 4px solid #17a2b8;
      border-radius: 5px;
      white-space: pre-wrap;
    }}
    .footer {{
      text-align: center;
      color: #666;
      margin-top: 40px;
      padding: 20px;
      border-top: 1px solid #ddd;
    }}
  </style>
</head>
<body>
  <div class="header">
    <h1>🔒 Reporte de Prueba de Penetración PHAH</h1>
    <div class="info-grid">
      <div class="info-item">
        <div class="info-label">Servicio</div>
        <div class="info-value">{service.upper()}</div>
      </div>
      <div class="info-item">
        <div class="info-label">Objetivo</div>
        <div class="info-value">{target}</div>
      </div>
      <div class="info-item">
        <div class="info-label">Puerto</div>
        <div class="info-value">{port if port else 'Por defecto'}</div>
      </div>
      <div class="info-item">
        <div class="info-label">Duración</div>
        <div class="info-value">{duration}</div>
      </div>
    </div>
  </div>

  <div class="section">
    <h2>📋 Resumen Ejecutivo</h2>
    <p><strong>Hora de Inicio:</strong> {start_time.strftime('%Y-%m-%d %H:%M:%S')}</p>
    <p><strong>Hora de Finalización:</strong> {end_time.strftime('%Y-%m-%d %H:%M:%S')}</p>
    <p><strong>Generado Por:</strong> PHAH (Plataforma de Hacking de Penetración Automatizada)</p>
  </div>

  <div class="section">
    <h2>🔍 Hallazgos</h2>
    {findings_html}
  </div>

  <div class="section">
    <h2>⚙️ Comandos Ejecutados</h2>
    <div class="commands">
      {commands_html}
    </div>
  </div>

  <div class="section">
    <h2>🤖 Análisis de IA</h2>
    <div class="analysis">{llm_analysis}</div>
  </div>

  <div class="footer">
    <p><strong>PHAH Versión 1.0</strong></p>
    <p>Reporte generado el {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}</p>
    <p><em>⚠️ Este reporte fue generado por una herramienta automatizada. Por favor, revisa los hallazgos con profesionales de seguridad cualificados.</em></p>
  </div>
</body>
</html>
"""

    with open(filepath, 'w', encoding='utf-8') as f:
      f.write(html_content)

    return str(filepath)
