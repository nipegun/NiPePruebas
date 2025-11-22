# AutoHacker

## Instalación

```
mkdir ~/Git/ 2> /dev/null
cd ~/Git/
rm -rf pruebas/
git clone https://github.com/nipegun/pruebas.git
mkdir ~/HackingTools/AutoHacker/
cp -R ~/Git/pruebas/AutoHacker/* ~/HackingTools/AutoHacker/
cd ~/HackingTools/AutoHacker/
python3 -m venv venv
source ~/HackingTools/AutoHacker/venv/bin/activate
pip install requirements.txt
deactivate
```

## Descripción General

**AutoHacker** es un framework especializado en Python para construir **Inteligencias Artificiales de Ciberseguridad (IAC)** de nivel profesional, específicamente orientadas a Bug Bounty, Red Teaming, Blue Teaming y análisis de seguridad ofensiva/defensiva.

Se trata de un sistema multi-agente basado en IA que utiliza modelos de lenguaje grandes (LLMs) para ejecutar tareas complejas de ciberseguridad de forma autónoma o semi-autónoma.

## Arquitectura Principal

### 1. Sistema de Agentes

El framework implementa una arquitectura basada en **agentes especializados**, donde cada agente tiene un rol específico en el ciclo de ataque/defensa:

#### Agentes Ofensivos:
- **Red Team Agent**: Simula un atacante especializado en penetración de sistemas y escalado de privilegios
- **Bug Bounty Agent**: Enfocado en encontrar vulnerabilidades web y reportarlas según estándares de Bug Bounty
- **Exploit Expert**: Especialista en desarrollo y ejecución de exploits
- **Network Traffic Analyzer**: Análisis de tráfico de red para identificar vectores de ataque

#### Agentes de Análisis:
- **Android SAST Agent**: Análisis estático de aplicaciones Android
- **Reverse Engineering Agent**: Análisis inverso de binarios y malware
- **Memory Analysis Agent**: Análisis forense de memoria
- **Replay Attack Agent**: Especialista en ataques de repetición

#### Agentes Defensivos:
- **Blue Team Agent**: Defensa y detección de amenazas
- **DFIR Agent**: Digital Forensics and Incident Response

#### Agentes de Soporte:
- **Reporter Agent**: Generación de informes profesionales
- **Flag Discriminator**: Identificación y validación de flags en CTFs
- **Thought Router**: Coordinador de estrategias entre agentes

#### Agentes Especializados en Hardware:
- **WiFi Security Tester**: Evaluación de seguridad WiFi
- **SubGHz SDR Agent**: Análisis de señales de radio de frecuencias sub-GHz

### 2. Patrones Agénticos (Agentic Patterns)

El framework implementa diferentes patrones de coordinación entre agentes:

**Formalmente definido como:** AP = (A, H, D, C, E)
- **A (Agents)**: Conjunto de entidades autónomas
- **H (Handoffs)**: Función de transferencia de tareas entre agentes
- **D (Decision Mechanism)**: Mecanismo de decisión sobre qué agente actúa
- **C (Communication Protocol)**: Protocolo de comunicación entre agentes
- **E (Execution Model)**: Modelo de ejecución de tareas

#### Patrones Implementados:
1. **Swarm (Enjambre)**: Agentes auto-organizados sin coordinador central
2. **Hierarchical (Jerárquico)**: Agente planificador asigna tareas a sub-agentes
3. **Chain-of-Thought (Secuencial)**: Pipeline estructurado con handoffs lineales
4. **Auction-Based (Basado en Subastas)**: Agentes compiten por tareas según capacidad
5. **Recursive (Recursivo)**: Agente refinando su propia salida iterativamente

#### Patrones Específicos Implementados:
- **CTF Agentic Pattern**: Equipo de agentes trabajando colaborativamente en CTFs
- **Red-Blue Team Pattern**: Coordinación entre equipos ofensivos y defensivos
- **Bug Bounty Triage Pattern**: Triaje automatizado de vulnerabilidades

## Herramientas y Capacidades

### Categorías de Herramientas:

1. **Reconocimiento** (`tools/reconnaissance/`):
   - Nmap, Netcat, Netstat
   - Shodan API integration
   - Ejecución genérica de comandos Linux
   - Herramientas criptográficas
   - Manipulación de sistema de archivos

2. **Explotación** (`tools/exploitation/`):
   - Framework para desarrollo de exploits

3. **Comando y Control** (`tools/command_and_control/`):
   - Ejecución remota vía SSH (sshpass)
   - Gestión de sesiones interactivas

4. **Web** (`tools/web/`):
   - Análisis de cabeceras HTTP
   - Búsqueda web integrada (Google, Perplexity)
   - Web shell suite

5. **Red** (`tools/network/`):
   - Captura de tráfico de red

6. **Movimiento Lateral** (`tools/lateral_movement/`)

7. **Escalado de Privilegios** (`tools/privilege_scalation/`)

8. **Exfiltración de Datos** (`tools/data_exfiltration/`)

9. **Miscelánea** (`tools/misc/`):
   - Intérprete de código
   - RAG (Retrieval-Augmented Generation)
   - Razonamiento avanzado

## Características Clave

### 1. Gestión de Sesiones Shell
Los agentes pueden crear y gestionar sesiones interactivas:
- Iniciar sesiones (netcat, SSH, etc.)
- Listar sesiones activas
- Enviar comandos a sesiones
- Obtener output de sesiones
- Terminar sesiones

### 2. Sistema de Guardrails de Seguridad
Implementa medidas de seguridad para prevenir:
- Ejecución de comandos peligrosos
- Outputs potencialmente dañinos
- Interacciones no autorizadas

### 3. Memoria y Contexto
- **Memoria Episódica**: Registro de eventos y acciones
- **Memoria Semántica**: Conocimiento acumulado
- **Modo Online**: Actualización en tiempo real
- **Modo Offline**: Procesamiento diferido

### 4. Soporte Multi-Modelo
Compatible con múltiples proveedores de LLM:
- OpenAI
- Anthropic (Claude)
- Modelos locales
- Configuración mediante alias

### 5. Integración con CTFs
Soporte nativo para plataformas CTF:
- Configuración de entornos containerizados
- Gestión de redes aisladas
- Detección y validación automática de flags
- Generación de write-ups

## Variables de Entorno Principales

```bash
# Modelo y Configuración
CAI_MODEL="alias0"                    # Modelo LLM a utilizar
CAI_AGENT_TYPE="one_tool_agent"       # Tipo de agente a ejecutar
CAI_DEBUG="1"                         # Nivel de debug (0-2)
CAI_MAX_TURNS="inf"                   # Máximo de turnos

# CTF Configuration
CTF_NAME="hackableii"                 # Nombre del CTF
CTF_CHALLENGE="linux ii"              # Reto específico
CTF_SUBNET="192.168.3.0/24"          # Subred del contenedor
CTF_IP="192.168.3.100"               # IP del contenedor
CTF_INSIDE="true"                     # Ejecutar desde dentro del contenedor

# Memoria
CAI_MEMORY="episodic"                 # Tipo de memoria (episodic/semantic/all)
CAI_MEMORY_ONLINE="true"              # Memoria online activa
CAI_MEMORY_ONLINE_INTERVAL="5"        # Intervalo de actualización

# Límites
CAI_PRICE_LIMIT="1"                   # Límite de coste en dólares
CAI_PARALLEL="1"                      # Instancias paralelas

# Reportes
CAI_REPORT="pentesting"               # Tipo de reporte (ctf/nis2/pentesting)

# Seguridad
CAI_GUARDRAILS="true"                 # Activar guardrails de seguridad

# Telemetría
CAI_TRACING="true"                    # OpenTelemetry tracing
CAI_TELEMETRY="true"                  # Telemetría general
```

## Casos de Uso Principales

### 1. Resolución Automatizada de CTFs
```bash
CTF_NAME="kiddoctf" CTF_CHALLENGE="02 linux ii" \
  CAI_AGENT_TYPE="one_tool_agent" CAI_MODEL="alias0" \
  CAI_TRACING="false" cai
```

### 2. Red Teaming con Memoria
```bash
CTF_NAME="hackableII" CAI_MEMORY="episodic" \
  CAI_MODEL="alias0" CAI_MEMORY_ONLINE="True" \
  CTF_INSIDE="False" CAI_PRICE_LIMIT="5" cai
```

### 3. Generación de Informes de Pentesting
```bash
CAI_TRACING=False CAI_REPORT=pentesting CAI_MODEL="alias0" cai
```

### 4. Bug Bounty con Ejecución Paralela
```bash
CAI_AGENT_TYPE="bug_bounter" CAI_PARALLEL="3" \
  CAI_MODEL="alias0" cai
```

## SDK y Estructura Interna

### Componentes del SDK (`sdk/agents/`):
- **Agent Core**: Clase base para todos los agentes
- **Function Schema**: Definición de herramientas y funciones
- **Handoffs**: Sistema de transferencia entre agentes
- **Run Context**: Gestión del contexto de ejecución
- **Tracing**: Sistema de trazabilidad OpenTelemetry
- **MCP (Model Context Protocol)**: Protocolo de contexto
- **Voice**: Soporte para interacciones por voz (STT/TTS)
- **Parallel Isolation**: Ejecución paralela aislada

### REPL Interactivo (`repl/`):
CLI interactiva con comandos:
- `/agent`: Listar y cambiar agentes
- `/model`: Cambiar modelo LLM
- `/cost`: Ver costes acumulados
- `/history`: Historial de conversación
- `/memory`: Gestión de memoria
- `/parallel`: Ejecutar en paralelo
- `/workspace`: Gestionar espacio de trabajo
- `/graph`: Visualizar flujo de agentes
- `/mcp`: Model Context Protocol
- `/env`: Variables de entorno
- `/run`: Ejecutar patrón específico

## Prompts Especializados

El framework incluye prompts altamente especializados para cada agente:

- **system_red_team_agent.md**: Instrucciones para penetración y escalado de privilegios
- **system_blue_team_agent.md**: Instrucciones para defensa y detección
- **system_bug_bounter.md**: Guías para Bug Bounty hunting
- **system_android_sast.md**: Análisis estático de Android
- **system_dfir_agent.md**: Forense digital y respuesta a incidentes
- **system_network_analyzer.md**: Análisis de tráfico de red
- **wifi_security_agent.md**: Seguridad WiFi
- **subghz_agent.md**: Radio frecuencia sub-GHz
- **memory_analysis_agent.md**: Análisis de memoria
- **reverse_engineering_agent.md**: Ingeniería inversa

## Extensiones

El framework soporta extensiones mediante:
- **pentestperf**: Métricas y rendimiento
- **caiextensions-report**: Generación avanzada de informes
- **caiextensions-memory**: Sistema de memoria extendido
- **caiextensions-platform**: Integración con plataformas

## Arquitectura Técnica

### Flujo de Ejecución:
1. **Inicialización**: Carga de configuración y agentes
2. **Análisis**: Los agentes analizan el entorno objetivo
3. **Planificación**: Estrategia de ataque/análisis
4. **Ejecución**: Uso de herramientas y comandos
5. **Iteración**: Refinamiento basado en resultados
6. **Handoff**: Transferencia a otros agentes si es necesario
7. **Reporte**: Documentación de hallazgos

### Características Avanzadas:
- **State Management**: Gestión de estado entre agentes
- **Tool Execution**: Ejecución segura de herramientas
- **Output Parsing**: Análisis automático de resultados
- **Error Handling**: Recuperación ante fallos
- **Rate Limiting**: Control de uso de API
- **Guardrails**: Prevención de acciones peligrosas

## Conclusión

AutoHacker es una plataforma completa y profesional para automatizar tareas de ciberseguridad mediante IA. Su arquitectura multi-agente, combinada con herramientas especializadas y patrones de coordinación sofisticados, lo convierte en una solución avanzada para:

- Competiciones CTF automatizadas
- Bug Bounty hunting
- Red Teaming
- Blue Teaming
- Análisis forense digital
- Pentesting automatizado
- Investigación en ciberseguridad

El framework destaca por su flexibilidad, extensibilidad y capacidad de trabajar con múltiples modelos LLM, permitiendo adaptar la inteligencia y coste a las necesidades específicas de cada tarea.
