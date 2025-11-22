# 🛠️ CaiFramework Services

Servicios especializados de seguridad para el framework CaiFramework.

Cada servicio es un script independiente que proporciona funcionalidad especializada de seguridad usando agentes de IA con Ollama.

## 📋 Servicios Disponibles

### 🔴 Red Team Service (`red_teamer.py`)

**Operaciones ofensivas de seguridad**

```bash
# Reconocimiento básico
python services/red_teamer.py --mode recon

# Con objetivo específico
python services/red_teamer.py --target 192.168.1.0/24 --mode recon

# Análisis de explotación
python services/red_teamer.py --target example.com --mode exploit --no-guardrails

# Modo interactivo
python services/red_teamer.py --interactive --no-guardrails
```

**Modos disponibles:**
- `recon` - Reconocimiento y enumeración
- `exploit` - Análisis de vulnerabilidades
- `post-exploit` - Post-explotación y persistencia
- `full` - Evaluación completa de red team

---

### 🔵 Blue Team Service (`blue_teamer.py`)

**Operaciones defensivas de seguridad**

```bash
# Detección de amenazas
python services/blue_teamer.py --mode detection

# Análisis de logs
python services/blue_teamer.py --analyze-logs /var/log/auth.log

# Threat hunting
python services/blue_teamer.py --mode threat-hunting --no-guardrails

# Modo interactivo
python services/blue_teamer.py --interactive
```

**Modos disponibles:**
- `detection` - Detección de amenazas
- `threat-hunting` - Caza proactiva de amenazas
- `incident-response` - Respuesta a incidentes

---

### 📡 Network Traffic Analyzer (`network_analyzer.py`)

**Análisis de tráfico de red**

```bash
# Analizar archivo PCAP
python services/network_analyzer.py --pcap capture.pcap --no-guardrails

# Monitorear interfaz
python services/network_analyzer.py --interface eth0 --live

# Análisis general
python services/network_analyzer.py --analyze-traffic
```

**Características:**
- Análisis de archivos PCAP
- Detección de tráfico C2
- Identificación de anomalías
- Análisis de protocolos

---

### 🔧 Reverse Engineering Service (`reverse_engineer.py`)

**Análisis de binarios e ingeniería inversa**

```bash
# Analizar binario
python services/reverse_engineer.py --binary /path/to/binary --no-guardrails

# Descompilar
python services/reverse_engineer.py --decompile malware.exe --no-guardrails

# Modo interactivo
python services/reverse_engineer.py --interactive --no-guardrails

# Con modelo especializado en código
python services/reverse_engineer.py --binary program --model codellama
```

**Características:**
- Análisis estático de binarios
- Identificación de ofuscación
- Detección de malware
- Análisis de strings y funciones

---

### 🧠 Memory Forensics Service (`memory_forensics.py`)

**Análisis forense de memoria**

```bash
# Analizar volcado de memoria
python services/memory_forensics.py --dump memory.raw --no-guardrails

# Analizar proceso específico
python services/memory_forensics.py --analyze-process 1234

# Análisis en vivo
python services/memory_forensics.py --live-analysis
```

**Características:**
- Análisis de volcados de RAM
- Detección de inyección de código
- Búsqueda de rootkits
- Análisis de procesos

---

### 🔍 DFIR Service (`dfir.py`)

**Análisis forense digital y respuesta a incidentes**

```bash
# Investigación de incidente
python services/dfir.py --investigate --no-guardrails

# Análisis de disco
python services/dfir.py --analyze-disk /dev/sda1

# Crear timeline
python services/dfir.py --timeline /var/log

# Modo interactivo
python services/dfir.py --interactive --no-guardrails
```

**Características:**
- Investigación de compromisos
- Creación de timelines
- Análisis de artefactos
- Cadena de custodia

---

## 🚀 Instalación y Requisitos

### Requisitos Previos

1. **Ollama instalado y corriendo:**
   ```bash
   curl -fsSL https://ollama.ai/install.sh | sh
   ollama serve
   ollama pull llama3.2
   ```

2. **Activar entorno virtual:**
   ```bash
   source /home/nipegun/PythonVirtualEnvironments/CaiFramework/bin/activate
   ```

3. **Variables de entorno:**
   ```bash
   export CAI_TRACING=false
   export OPENAI_API_KEY=sk-placeholder
   export CAI_MODEL=llama3.2
   ```

### Modelos Recomendados

- `llama3.2` - General, balanceado (default)
- `codellama` - Para reverse engineering y análisis de código
- `mistral` - Rápido y eficiente
- `qwen2.5` - Excelente para reportes detallados

---

## 📊 Ejemplos de Uso

### Ejemplo 1: Análisis de Seguridad Completo

```bash
# 1. Reconocimiento (Red Team)
python services/red_teamer.py --target myserver.com --mode recon --no-guardrails

# 2. Detección (Blue Team)
python services/blue_teamer.py --mode detection

# 3. Análisis de Tráfico
python services/network_analyzer.py --analyze-traffic
```

### Ejemplo 2: Respuesta a Incidente

```bash
# 1. Investigación inicial
python services/dfir.py --investigate --no-guardrails

# 2. Análisis de memoria
python services/memory_forensics.py --live-analysis

# 3. Análisis de logs
python services/blue_teamer.py --analyze-logs /var/log/syslog
```

### Ejemplo 3: Análisis de Malware

```bash
# 1. Reverse engineering
python services/reverse_engineer.py --binary malware.exe --no-guardrails

# 2. Análisis de memoria
python services/memory_forensics.py --dump infected_memory.raw --no-guardrails

# 3. Análisis forense
python services/dfir.py --analyze-disk /mnt/infected_system
```

---

## 🎯 Opciones Comunes

Todos los servicios soportan estas opciones:

```bash
--model MODEL          Modelo de Ollama a usar (default: llama3.2)
--no-guardrails        Desactivar guardrails de seguridad
--interactive          Modo interactivo (algunos servicios)
--help                 Mostrar ayuda completa
```

---

## 🔒 Consideraciones de Seguridad

### Uso Ético

**IMPORTANTE:** Estos servicios son herramientas de seguridad profesional. Solo usar en:

- ✅ Sistemas que posees
- ✅ Entornos autorizados
- ✅ Pentesting con permiso escrito
- ✅ Investigaciones legales

**NO usar para:**
- ❌ Sistemas no autorizados
- ❌ Actividades ilegales
- ❌ Violación de privacidad

### Guardrails

Los guardrails están activados por defecto y bloquean:
- Comandos potencialmente destructivos
- Operaciones no autorizadas
- Patrones de ataque maliciosos

**Desactivar guardrails solo cuando:**
- Estés en un entorno controlado
- Tengas autorización explícita
- Sepas lo que estás haciendo

---

## 💡 Tips y Trucos

### 1. Modo Interactivo

Todos los servicios con modo interactivo permiten comandos continuos:

```bash
python services/red_teamer.py --interactive --no-guardrails

red-team> scan port 80 on target.com
red-team> enumerate services
red-team> exit
```

### 2. Pipelines de Servicios

Combina servicios para análisis completo:

```bash
# Script bash para pipeline completo
#!/bin/bash
TARGET="target.com"

echo "[*] Red Team Recon..."
python services/red_teamer.py --target $TARGET --mode recon --no-guardrails > recon.txt

echo "[*] Network Analysis..."
python services/network_analyzer.py --analyze-traffic > network.txt

echo "[*] Blue Team Detection..."
python services/blue_teamer.py --mode detection > detection.txt

echo "[+] Analysis complete. Check *.txt files"
```

### 3. Modelos Especializados

Usa modelos específicos para mejor rendimiento:

```bash
# CodeLlama para reverse engineering
python services/reverse_engineer.py --binary app --model codellama

# Qwen2.5 para reportes detallados
python services/dfir.py --investigate --model qwen2.5

# Mistral para análisis rápido
python services/network_analyzer.py --pcap capture.pcap --model mistral
```

---

## 📈 Roadmap

Servicios futuros planeados:

- [ ] `wifi_tester.py` - Testing de seguridad WiFi
- [ ] `web_scanner.py` - Scanning web automatizado
- [ ] `crypto_analyzer.py` - Análisis criptográfico
- [ ] `social_engineer.py` - Ingeniería social (educativo)
- [ ] `iot_scanner.py` - Testing de dispositivos IoT
- [ ] `cloud_auditor.py` - Auditoría de seguridad cloud

---

## 🐛 Troubleshooting

### Error: "Guardrail triggered tripwire"

**Solución:** Usar `--no-guardrails`

```bash
python services/red_teamer.py --mode exploit --no-guardrails
```

### Error: "Connection refused" (Ollama)

**Solución:** Verificar que Ollama está corriendo

```bash
ollama serve  # Terminal 1
python services/red_teamer.py ...  # Terminal 2
```

### Error: "Model not found"

**Solución:** Descargar el modelo

```bash
ollama pull llama3.2
ollama pull codellama
```

---

## 📚 Documentación Adicional

- `../GUIA_RAPIDA.md` - Guía rápida del framework
- `../examples/BUG_BOUNTY_README.md` - Guía de bug bounty hunting
- `../MIGRATION_TO_LOCAL_MODELS.md` - Información sobre Ollama

---

## 📞 Soporte

Para problemas o sugerencias:
1. Verifica que Ollama esté corriendo
2. Usa `--help` en cualquier servicio
3. Revisa los logs con modo verbose (si disponible)
4. Consulta la documentación del framework

---

**Última actualización:** 2025-11-22
**Versión:** 1.0.0
**Estado:** ✅ Funcional y probado
