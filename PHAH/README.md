# 🔒 PHAH - Plataforma de hacking automatizada

**Pruebas de penetración automatizadas potenciadas por IA con Ollama**

PHAH es una plataforma inteligente de pruebas de penetración que combina el poder de los modelos de lenguaje grandes (Ollama) con herramientas tradicionales de seguridad para realizar evaluaciones de seguridad automatizadas y exhaustivas.

---

## 🌟 Características

- **Pruebas Potenciadas por IA**: Usa LLMs de Ollama para toma de decisiones inteligente.
- **Soporte Multi-Servicio**: Prueba aplicaciones Web, SSH, Samba, FTP, bases de datos y más.
- **Reportes Automatizados**: Genera reportes profesionales en HTML, Markdown y JSON.
- **Consciente del Contexto**: Mantiene historial de conversación para progresión inteligente de pruebas.
- **Extensible**: Fácil de añadir nuevos servicios y metodologías de prueba.
- **Local y Privado**: Todo el procesamiento ocurre en tu máquina con Ollama local.

---

## 📋 Servicios Soportados

| Servicio | Puertos por Defecto | Descripción |
|---------|---------------------|-------------|
| `web` | 80, 443, 8080, 8443 | Pruebas de seguridad de aplicaciones web |
| `ssh` | 22 | Evaluación de seguridad del servicio SSH |
| `samba` | 139, 445 | Pruebas de seguridad Samba/SMB |
| `ftp` | 21 | Evaluación de seguridad del servicio FTP |
| `mysql` | 3306 | Pruebas de seguridad de base de datos MySQL |
| `postgresql` | 5432 | Pruebas de base de datos PostgreSQL |
| `rdp` | 3389 | Evaluación de seguridad del servicio RDP |
| `dns` | 53 | Pruebas de seguridad del servicio DNS |
| `smtp` | 25, 465, 587 | Pruebas del servicio de correo SMTP |

Ver todos los servicios: `python phah.py --list-services`

---

## 🚀 Inicio Rápido

### Prerequisitos

1. **Ollama instalado y ejecutándose**:
   ```bash
   # Instalar Ollama
   curl -fsSL https://ollama.ai/install.sh | sh

   # Iniciar servidor Ollama
   ollama serve

   # Descargar modelo requerido
   ollama pull llama3.2
   ```

2. **Python 3.8+**:
   ```bash
   python3 --version
   ```

3. **Herramientas de pentesting** (instalar según necesidad):
   ```bash
   # Debian/Ubuntu
   sudo apt install nmap nikto dirb smbclient enum4linux curl

   # Herramientas opcionales
   sudo apt install sqlmap wpscan hydra ssh-audit
   ```

### Instalación

```bash
# Clonar o navegar al directorio PHAH
cd /home/nipegun/Git/pruebas/PHAH

# Instalar dependencias de Python
pip install -r requirements.txt

# Hacer ejecutable
chmod +x phah.py
```

---

## 💻 Uso

### Sintaxis Básica

```bash
python phah.py -service <SERVICIO> -target <OBJETIVO> [-port <PUERTO>] [-report] [-model <MODELO>]
```

### Ejemplos

#### Pruebas de Aplicaciones Web

```bash
# Prueba web básica (puertos 80, 443)
python phah.py -service web -target https://ejemplo.com

# Puerto personalizado con generación de reporte
python phah.py -service web -target https://ejemplo.com -port 8080 -report

# Usando modelo diferente
python phah.py -service web -target https://ejemplo.com -model qwen2.5 -report
```

#### Evaluación de Seguridad SSH

```bash
# Prueba SSH básica (puerto 22)
python phah.py -service ssh -target 192.168.1.10

# Puerto personalizado con reporte
python phah.py -service ssh -target 192.168.1.10 -port 2222 -report
```

#### Pruebas Samba/SMB

```bash
# Probar servicio Samba (puertos 139, 445)
python phah.py -service samba -target 192.168.1.10 -report

# Alias para samba
python phah.py -service smb -target 192.168.1.10
```

#### Pruebas FTP

```bash
# Prueba FTP básica
python phah.py -service ftp -target ftp.ejemplo.com

# Puerto personalizado
python phah.py -service ftp -target 192.168.1.10 -port 2121 -report
```

#### Pruebas de Bases de Datos

```bash
# Evaluación de seguridad MySQL
python phah.py -service mysql -target 192.168.1.10 -report

# Pruebas PostgreSQL
python phah.py -service postgresql -target 192.168.1.10 -port 5433
```

---

## 📊 Generación de Reportes

Cuando se usa la opción `-report`, PHAH genera tres formatos de reporte:

### 1. Reporte HTML
- HTML profesional y estilizado
- Niveles de gravedad codificados por color
- Hallazgos interactivos
- Ubicado en: `reports/phah_<servicio>_<objetivo>_<marca_temporal>.html`

### 2. Reporte Markdown
- Formato markdown estructurado
- Fácil de compartir y controlar versiones
- Ubicado en: `reports/phah_<servicio>_<objetivo>_<marca_temporal>.md`

### 3. Reporte JSON
- Formato legible por máquina
- Fácil de analizar e integrar
- Ubicado en: `reports/phah_<servicio>_<objetivo>_<marca_temporal>.json`

### Ejemplo de Estructura de Reporte

```
reports/
├── phah_web_ejemplo.com_20231122_143052.html
├── phah_web_ejemplo.com_20231122_143052.md
└── phah_web_ejemplo.com_20231122_143052.json
```

---

## 🏗️ Arquitectura

PHAH sigue la arquitectura de CaiFramework para la integración con Ollama:

```
┌─────────────────┐
│   phah.py       │  Punto de entrada principal
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│  AutoPentester  │  Orquesta las pruebas
└────────┬────────┘
         │
    ┌────┴────┬──────────────┬──────────────┐
    ▼         ▼              ▼              ▼
┌─────────┐ ┌──────────┐ ┌──────────┐ ┌──────────┐
│ Ollama  │ │ Command  │ │  Report  │ │ Service  │
│ Client  │ │ Executor │ │Generator │ │ Prompts  │
└─────────┘ └──────────┘ └──────────┘ └──────────┘
     │           │              │            │
     └───────────┴──────────────┴────────────┘
                       │
                       ▼
              ┌────────────────┐
              │ Servidor Ollama│
              │ (localhost)    │
              └────────────────┘
```

### Componentes Clave

1. **OllamaClient** (`core/ollama_client.py`):
   - Gestiona la comunicación con el LLM de Ollama
   - Mantiene el historial de conversación
   - Maneja la gestión de contexto

2. **CommandExecutor** (`tools/command_executor.py`):
   - Ejecuta comandos del sistema de forma segura
   - Captura salida y errores
   - Mantiene historial de comandos

3. **AutoPentester** (`core/pentester.py`):
   - Orquesta el flujo de trabajo de pruebas
   - Bucle iterativo de pruebas con IA
   - Coordina entre el LLM y las herramientas

4. **ReportGenerator** (`core/report_generator.py`):
   - Genera reportes en múltiples formatos
   - Estilizado y formateo profesional
   - Documentación exhaustiva de hallazgos

5. **Service Prompts** (`prompts/*.md`):
   - Prompts especializados por servicio
   - Metodologías de prueba
   - Formatos de salida esperados

---

## 🎯 Cómo Funciona

### Flujo de Trabajo de Pruebas

```
1. INICIALIZACIÓN
   ├─ Cargar prompt específico del servicio
   ├─ Inicializar cliente Ollama
   └─ Crear ejecutor de comandos

2. FASE DE RECONOCIMIENTO
   ├─ IA sugiere comandos iniciales
   ├─ Ejecutar herramientas de reconocimiento
   ├─ Realimentar resultados a la IA
   └─ IA analiza la salida

3. BUCLE ITERATIVO DE PRUEBAS
   ├─ IA determina siguiente acción
   ├─ Ejecutar comando sugerido
   ├─ Capturar y analizar salida
   ├─ IA identifica hallazgos
   ├─ Actualizar contexto
   └─ Repetir hasta completar

4. ANÁLISIS E INFORMES
   ├─ IA proporciona análisis final
   ├─ Extraer todos los hallazgos
   ├─ Generar reportes (si se solicita)
   └─ Mostrar resumen
```

### Gestión de Contexto

PHAH mantiene el contexto de conversación similar a CaiFramework:

- **Historial de Mensajes**: Todas las interacciones almacenadas en memoria
- **Integración de Salida de Herramientas**: Resultados de comandos añadidos al contexto
- **Refinamiento Iterativo**: IA aprende de salidas anteriores
- **Preservación de Estado**: Contexto completo disponible para toma de decisiones

---

## 🔧 Opciones de Línea de Comandos

```
Opciones:
  -service SERVICIO    Servicio a probar (requerido)
  -target OBJETIVO     Host o URL objetivo (requerido)
  -port PUERTO         Puerto objetivo (opcional, usa valores por defecto)
  -report              Generar reportes detallados
  -model MODELO        Modelo de Ollama (por defecto: llama3.2)
  -quiet               Suprimir salida detallada
  --list-services      Listar todos los servicios disponibles
  -h, --help           Mostrar mensaje de ayuda
```

---

## 🎨 Personalización

### Añadir Nuevos Servicios

1. **Crear prompt del servicio** (`prompts/<servicio>_pentester.md`):
   ```markdown
   # <Servicio> Penetration Tester

   ## Tus Objetivos
   ...

   ## Herramientas Disponibles
   ...

   ## Metodología de Prueba
   ...
   ```

2. **Añadir puertos por defecto** (`services/__init__.py`):
   ```python
   SERVICE_PORTS = {
       'miservicio': [1234, 5678],
   }
   ```

3. **Probar el nuevo servicio**:
   ```bash
   python phah.py -service miservicio -target ejemplo.com
   ```

### Usar Diferentes Modelos

```bash
# Usar codellama para análisis de código
python phah.py -service web -target ejemplo.com -model codellama

# Usar mistral para pruebas más rápidas
python phah.py -service ssh -target 192.168.1.10 -model mistral

# Usar qwen2.5 para reportes detallados
python phah.py -service samba -target 192.168.1.10 -model qwen2.5 -report
```

---

## ⚠️ Descargo de Responsabilidad Legal y de Seguridad

### Notas Importantes

- **Autorización Requerida**: Solo prueba sistemas que poseas o para los que tengas permiso explícito por escrito
- **Las Pruebas No Autorizadas Son Ilegales**: Acceder a sistemas informáticos sin autorización es un delito
- **Divulgación Responsable**: Reporta vulnerabilidades de forma responsable
- **Sin Garantías**: Esta herramienta se proporciona tal cual sin garantías
- **Propósito Educativo**: Destinada solo para pruebas de seguridad autorizadas

### Mejores Prácticas

1. **Obtén Autorización por Escrito** antes de probar
2. **Define el Alcance** claramente con el propietario del sistema
3. **Prueba en Entorno Controlado** cuando sea posible
4. **Documenta Todo** incluyendo permisos
5. **Reporta Responsablemente** a través de canales apropiados
6. **Evita Interrupciones** - no realices pruebas DoS o destructivas

---

## 🐛 Solución de Problemas

### Problemas de Conexión con Ollama

```bash
# Comprobar si Ollama está ejecutándose
curl http://localhost:11434/api/tags

# Iniciar Ollama si no está ejecutándose
ollama serve

# Comprobar disponibilidad de modelo
ollama list
```

### Herramientas Faltantes

```bash
# Comprobar si las herramientas requeridas están instaladas
which nmap nikto curl

# Instalar herramientas faltantes (Debian/Ubuntu)
sudo apt install nmap nikto curl smbclient
```

### Problemas de Permisos

```bash
# Algunas herramientas requieren privilegios de root
sudo python phah.py -service <servicio> -target <objetivo>

# O ejecutar comandos específicos con sudo cuando se solicite
```

---

## 📚 Ejemplos

### Ejemplo 1: Evaluación Web Completa

```bash
python phah.py -service web -target https://sitioprueba.com -report -model llama3.2
```

Salida:
```
╔═══════════════════════════════════════════════════════════════════╗
║                       PHAH                                        ║
║        Plataforma de Hacking de Penetración Automatizada         ║
╚═══════════════════════════════════════════════════════════════════╝

📋 Configuración:
   Servicio:      WEB
   Objetivo:      https://sitioprueba.com
   Puerto:        443
   Modelo:        llama3.2
   Reporte:       Sí

[20:15:30] [PHAH] Iniciando prueba de penetración automatizada
[20:15:31] [IA] Inicializando pentester de IA...
[20:15:35] [CMD] Ejecutando: nmap -sV -p 80,443 sitioprueba.com
...
[20:18:45] [REPORTE] Reportes generados:
  - Markdown: reports/phah_web_sitioprueba.com_20231122_201530.md
  - HTML: reports/phah_web_sitioprueba.com_20231122_201530.html
  - JSON: reports/phah_web_sitioprueba.com_20231122_201530.json

✅ Prueba de penetración completada con éxito!
```

### Ejemplo 2: Auditoría de Seguridad SSH

```bash
python phah.py -service ssh -target 192.168.1.100 -port 2222
```

### Ejemplo 3: Escaneo de Vulnerabilidades Samba

```bash
python phah.py -service samba -target 192.168.1.50 -report
```

---

## 🤝 Integración con CaiFramework

PHAH está construido usando los mismos principios de arquitectura que CaiFramework:

- **Integración con Ollama**: Mismo patrón OllamaProvider
- **Gestión de Contexto**: Manejo similar del historial de mensajes
- **Ejecución de Comandos**: Inspirado en `generic_linux_command`
- **Operaciones Asíncronas**: Mismos patrones async/await

Puedes adaptar componentes de PHAH para usar en CaiFramework o viceversa.

---

## 📈 Hoja de Ruta

- [ ] Añadir más servicios (LDAP, Kerberos, NFS, etc.)
- [ ] Implementar módulo de pruebas de credenciales
- [ ] Añadir capacidades de sugerencia de exploits
- [ ] Crear interfaz web
- [ ] Integración con bases de datos de vulnerabilidades
- [ ] Exportar a herramientas externas (Metasploit, etc.)
- [ ] Soporte multi-objetivo
- [ ] Escaneos automatizados programados

---

## 👨‍💻 Desarrollo

### Estructura del Proyecto

```
PHAH/
├── phah.py                 # Punto de entrada principal
├── core/
│   ├── __init__.py
│   ├── ollama_client.py    # Cliente LLM de Ollama
│   ├── pentester.py        # Clase principal de pentester
│   └── report_generator.py # Generación de reportes
├── tools/
│   ├── __init__.py
│   └── command_executor.py # Ejecución de comandos
├── services/
│   └── __init__.py         # Definiciones de servicios
├── prompts/
│   ├── web_pentester.md    # Prompt de pruebas web
│   ├── ssh_pentester.md    # Prompt de pruebas SSH
│   ├── samba_pentester.md  # Prompt de pruebas Samba
│   └── ftp_pentester.md    # Prompt de pruebas FTP
├── reports/                # Reportes generados
├── requirements.txt        # Dependencias de Python
└── README.md              # Este archivo
```

---

## 📝 Licencia

Esta herramienta se proporciona solo para propósitos educativos y de pruebas de seguridad autorizadas.

---

## 🙏 Agradecimientos

- Basado en la arquitectura de CaiFramework
- Potenciado por Ollama LLM
- Usa herramientas estándar de la industria de pentesting

---

**Versión**: 1.0.0
**Última Actualización**: 2025-11-22
**Estado**: ✅ Totalmente Funcional

---

Para preguntas, problemas o contribuciones, por favor consulta la documentación de CaiFramework para patrones de arquitectura y mejores prácticas.
