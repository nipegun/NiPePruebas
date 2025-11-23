# CTFSolver - Resolución Automatizada de CTFs con IA

Sistema automatizado para resolver desafíos CTF (Capture The Flag) usando modelos de lenguaje local mediante Ollama.

## 🎯 Características

- ✅ **Múltiples categorías**: Web, Crypto, Forensics, Pwn, Reversing, Misc, etc.
- 🤖 **IA local**: Usa Ollama sin enviar datos a APIs externas
- 🔍 **Análisis inteligente**: El LLM analiza y propone comandos específicos
- 🚩 **Detección automática de flags**: Reconoce formatos comunes de flags
- 📊 **Reportes detallados**: Genera informes Markdown de la solución
- 🔄 **Iterativo**: Aprende de cada intento y ajusta estrategia

## 📋 Requisitos

- Python 3.8+
- Ollama instalado y ejecutándose
- Herramientas de seguridad comunes instaladas (opcional pero recomendado)

### Herramientas Recomendadas por Categoría

**Web:**
```bash
apt install curl wget nikto dirb gobuster sqlmap whatweb
```

**Crypto:**
```bash
apt install python3-pycryptodome hashcat john openssl
```

**Forensics:**
```bash
apt install binwalk exiftool foremost strings file
```

**Steganography:**
```bash
apt install steghide stegseek zsteg
```

**Pwn/Reversing:**
```bash
apt install gdb radare2 pwntools
```

**Networking:**
```bash
apt install wireshark tshark tcpdump nmap
```

## 🚀 Instalación

```bash
# 1. Clonar el repositorio
git clone https://github.com/nipegun/pruebas.git
cd pruebas/PHAH

# 2. Instalar dependencias
pip install -r install/requirements.txt

# 3. Verificar que Ollama esté corriendo
ollama list

# 4. Descargar modelo (si no lo tienes)
ollama pull llama3.2
```

## 💡 Uso

### Sintaxis Básica

```bash
./ctf.py -category <CATEGORIA> -name "<NOMBRE>" [OPCIONES]
```

### Ejemplos por Categoría

#### CTF Web
```bash
# Desafío web con objetivo remoto
./ctf.py -category web \
         -name "SQL Injection Login" \
         -target http://ctf.example.com/login \
         -description "Bypasea el login para obtener la flag" \
         -report

# Desafío web con puerto personalizado
./ctf.py -category web \
         -name "Command Injection" \
         -target 192.168.1.100 \
         -port 8080 \
         -report
```

#### CTF Crypto
```bash
# Archivo cifrado
./ctf.py -category crypto \
         -name "Caesar Cipher" \
         -files mensaje_cifrado.txt \
         -description "Descifra este mensaje usando cifrado César"

# Múltiples archivos
./ctf.py -category crypto \
         -name "RSA Challenge" \
         -files public.pem encrypted.txt \
         -description "Factoriza la clave pública y descifra el mensaje"
```

#### CTF Forensics
```bash
# Análisis de imagen
./ctf.py -category forensics \
         -name "Hidden Data" \
         -files imagen_sospechosa.png \
         -description "Encuentra datos ocultos en esta imagen"

# Análisis de memoria
./ctf.py -category forensics \
         -name "Memory Dump" \
         -files memory.dmp \
         -description "Analiza el volcado de memoria y encuentra credenciales"
```

#### CTF Steganography
```bash
# Esteganografía en imagen
./ctf.py -category steganography \
         -name "Secret Message" \
         -files secret.jpg \
         -description "La contraseña es: password123"
```

#### CTF Pwn/Reversing
```bash
# Binario a explotar
./ctf.py -category pwn \
         -name "Buffer Overflow" \
         -target 192.168.1.100 \
         -port 9001 \
         -files vuln_binary \
         -description "Explota el buffer overflow para obtener shell"

# Ingeniería inversa
./ctf.py -category reversing \
         -name "Crack Me" \
         -files crackme \
         -description "Encuentra la contraseña correcta"
```

#### CTF Networking
```bash
# Análisis de captura de red
./ctf.py -category networking \
         -name "Packet Analysis" \
         -files capture.pcap \
         -description "Analiza el tráfico y encuentra credenciales"
```

### Opciones Disponibles

```
-category CATEGORIA    Categoría del CTF (web, crypto, forensics, etc.)
-name NOMBRE          Nombre del desafío
-target URL/IP        Objetivo remoto (opcional)
-port PUERTO          Puerto del servicio (opcional)
-description TEXTO    Descripción/enunciado del desafío
-files ARCHIVO(S)     Archivos proporcionados (separados por espacio)
-model MODELO         Modelo de Ollama a usar (default: llama3.2)
-report              Generar reporte detallado
-quiet               Modo silencioso
--list-categories    Listar categorías disponibles
```

## 📁 Estructura de Prompts

El sistema utiliza prompts especializados por categoría ubicados en `prompts/`:

```
prompts/
├── ctf_web.md           # Vulnerabilidades web
├── ctf_crypto.md        # Criptografía
├── ctf_forensics.md     # Análisis forense
├── ctf_pwn.md          # Explotación binaria
├── ctf_reversing.md    # Ingeniería inversa
├── ctf_steganography.md # Esteganografía
├── ctf_networking.md   # Análisis de red
└── ctf_misc.md         # Miscelánea
```

Puedes crear o modificar estos prompts para personalizar el comportamiento del solver.

## 🔍 Cómo Funciona

1. **Carga del Prompt**: Se carga el prompt especializado para la categoría
2. **Análisis Inicial**: El LLM analiza la descripción y archivos
3. **Planificación**: Propone una estrategia de resolución
4. **Ejecución Iterativa**: 
   - Sugiere comandos a ejecutar
   - Ejecuta comandos de forma segura
   - Analiza resultados
   - Ajusta estrategia según hallazgos
5. **Detección de Flag**: Busca patrones de flags en salidas
6. **Reporte**: Documenta el proceso de resolución

## 🚩 Formatos de Flags Soportados

El sistema detecta automáticamente estos formatos comunes:

- `flag{...}`
- `FLAG{...}`
- `CTF{...}`
- `HTB{...}` (HackTheBox)
- `picoCTF{...}`
- `THM{...}` (TryHackMe)
- Formatos personalizados tipo `XXX{contenido}`

## 📊 Reportes

Los reportes se generan en formato Markdown en el directorio `reports/`:

```
reports/
└── ctf_web_20250523_143022.md
```

Contenido del reporte:
- ✅ Estado de resolución (SOLVED/UNSOLVED)
- 🚩 Flags encontradas
- 📋 Información del desafío
- 🔍 Comandos ejecutados
- 💡 Análisis de la IA
- ⏱️ Tiempo de resolución

## ⚙️ Configuración Avanzada

### Usar Diferentes Modelos

```bash
# Usar llama3.1
./ctf.py -category web -name "Challenge" -target http://ctf.local -model llama3.1

# Usar qwen2.5
./ctf.py -category crypto -name "Cipher" -files data.enc -model qwen2.5
```

### Configurar Servidor Ollama Remoto

```bash
export OLLAMA_API_BASE="http://192.168.1.100:11434/api"
./ctf.py -category forensics -name "Analysis" -files image.png
```

## 🎓 Tips para Mejores Resultados

1. **Proporciona contexto**: Usa `-description` con detalles del enunciado
2. **Archivos locales**: Asegúrate de que los archivos estén en el directorio actual
3. **Modelo adecuado**: Usa modelos más grandes para CTFs complejos
4. **Revisa reportes**: Los reportes contienen el razonamiento completo
5. **Iteración manual**: Si falla, usa el reporte para continuar manualmente

## 🔧 Troubleshooting

### "No se pudo conectar a Ollama"
```bash
# Verificar que Ollama esté corriendo
systemctl status ollama
# o
ollama serve
```

### "Comando no encontrado"
```bash
# Instalar herramienta faltante
apt install <herramienta>
```

### "No se encontró la flag"
- Verifica el formato esperado en la descripción del CTF
- Revisa el reporte generado para ver el análisis
- Prueba manualmente siguiendo los pasos del reporte

## 📝 Crear Prompts Personalizados

Puedes crear prompts para nuevas categorías:

```bash
# Crear nuevo prompt
cat > prompts/ctf_blockchain.md << 'EOF'
# CTF Solver - Blockchain

Eres experto en resolver CTFs de blockchain...
EOF

# Usar nueva categoría
./ctf.py -category blockchain -name "Smart Contract" -files contract.sol
```

## 🤝 Contribuir

Para añadir soporte a nuevas categorías o mejorar prompts existentes:

1. Crea un nuevo archivo en `prompts/ctf_CATEGORIA.md`
2. Define las herramientas, técnicas y metodología
3. Prueba con desafíos reales
4. Envía un pull request

## ⚠️ Aviso Legal

Esta herramienta está diseñada para:
- ✅ Competiciones CTF legítimas
- ✅ Entornos de práctica autorizados
- ✅ Aprendizaje educativo

NO usar para:
- ❌ Acceso no autorizado a sistemas
- ❌ Pruebas sin permiso explícito
- ❌ Actividades ilegales

El uso indebido es responsabilidad exclusiva del usuario.

## 📜 Licencia

Este proyecto está bajo la misma licencia que PHAH.

## 🙏 Agradecimientos

- Basado en PHAH (PYMEHackers AutoHack)
- Integración con Ollama para IA local
- Inspirado en la comunidad CTF

---

**¡Happy Hacking! 🚩**
