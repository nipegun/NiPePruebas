# Ejemplo Práctico de Uso - CTF Solver

## 🎯 Caso de Uso: CTF Web - SQL Injection Login Bypass

### Escenario del Desafío

**Plataforma**: HackTheBox / picoCTF  
**Categoría**: Web  
**Nombre**: "Easy Login"  
**Descripción**: "Bypasea el formulario de login para obtener acceso administrativo"  
**URL**: http://ctf.example.com:8080/login  
**Pista**: "El desarrollador dejó un comentario interesante en el código fuente"

### Paso 1: Preparación

```bash
# Asegúrate de que Ollama esté corriendo
ollama list

# Si no tienes el modelo, descárgalo
ollama pull llama3.2

# Verifica que tienes las herramientas necesarias
which curl wget sqlmap
```

### Paso 2: Ejecutar CTF Solver

```bash
# Modo básico (sin reporte)
./ctf.py \
  -category web \
  -name "Easy Login" \
  -target http://ctf.example.com:8080/login \
  -description "Bypasea el formulario de login para obtener acceso administrativo. El desarrollador dejó un comentario interesante en el código fuente."

# Modo con reporte completo
./ctf.py \
  -category web \
  -name "Easy Login" \
  -target http://ctf.example.com:8080/login \
  -port 8080 \
  -description "Bypasea el formulario de login para obtener acceso administrativo" \
  -model llama3.2 \
  -report
```

### Paso 3: Proceso Automático (Salida Esperada)

```
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

📋 Configuración del CTF:
   Categoría:     WEB
   Desafío:       Easy Login
   Objetivo:      http://ctf.example.com:8080/login
   Puerto:        8080
   Descripción:   Bypasea el formulario de login...
   Modelo:        llama3.2
   Reporte:       Sí

================================================================================
[CTF SOLVER] Iniciando resolución de CTF
[CTF SOLVER] Categoría: WEB
[CTF SOLVER] Desafío: Easy Login
[CTF SOLVER] Objetivo: http://ctf.example.com:8080/login
================================================================================
[IA] Inicializando solver de IA...
[IA] Solver de IA inicializado

Este desafío parece ser un bypass de autenticación SQL. Basándome en la 
descripción, hay pistas en el código fuente. Mi estrategia será:

1. Primero, inspeccionar el código fuente del formulario
2. Buscar comentarios o información útil
3. Probar payloads SQL injection básicos
4. Intentar bypass de autenticación con ' OR '1'='1

Empecemos con el reconocimiento básico.

[BUCLE] Iteración 1/15
[CMD] Ejecutando: curl -s http://ctf.example.com:8080/login

--- Salida ---
<!DOCTYPE html>
<html>
<head><title>Login Portal</title></head>
<body>
<!-- TODO: Remove debug comment - Admin password is admin123 -->
<form method="POST" action="/login">
    <input type="text" name="username">
    <input type="password" name="password">
    <button type="submit">Login</button>
</form>
</body>
</html>
--- Fin Salida ---

¡Excelente! Encontré un comentario HTML con credenciales de debug:
- Username: (cualquiera, probablemente admin)
- Password: admin123

Probaré estas credenciales.

[BUCLE] Iteración 2/15
[CMD] Ejecutando: curl -X POST http://ctf.example.com:8080/login -d "username=admin&password=admin123"

--- Salida ---
Welcome Admin! Your flag is: flag{sql_comments_are_bad_mkay}
--- Fin Salida ---

[FLAG] ¡Flag encontrada: flag{sql_comments_are_bad_mkay}!

================================================================================
[CTF SOLVER] ¡CTF resuelto con éxito!
[CTF SOLVER] Flags encontradas: flag{sql_comments_are_bad_mkay}
[CTF SOLVER] Duración: 0:00:23
[CTF SOLVER] Intentos realizados: 2
================================================================================
[REPORTE] Generando reporte...
[REPORTE] Reportes generados:
[REPORTE]   - Markdown: reports/ctf_web_20250523_143022.md

============================================================
✅ ¡CTF RESUELTO CON ÉXITO!
============================================================

🚩 FLAGS ENCONTRADAS:
   flag{sql_comments_are_bad_mkay}

📊 Reporte generado en el directorio 'reports/'
```

### Paso 4: Revisar Reporte Generado

```bash
cat reports/ctf_web_20250523_143022.md
```

**Contenido del reporte**:

```markdown
# CTF Resolution Report

**Challenge**: Easy Login
**Category**: WEB
**Status**: ✅ SOLVED

## 🚩 Flags Found

- `flag{sql_comments_are_bad_mkay}`

## 📋 Challenge Information

**Description**: Bypasea el formulario de login para obtener acceso administrativo. El desarrollador dejó un comentario interesante en el código fuente.

**Target**: http://ctf.example.com:8080/login

## 🔍 Solution Process

**Attempts**: 2
**Duration**: 0:00:23

### Commands Executed

1. `curl -s http://ctf.example.com:8080/login`
2. `curl -X POST http://ctf.example.com:8080/login -d "username=admin&password=admin123"`

### AI Analysis

El desafío fue resuelto mediante reconocimiento básico. Al inspeccionar
el código fuente de la página de login, se encontró un comentario HTML
de debug que revelaba las credenciales de administrador. 

La solución no requirió SQL injection ya que las credenciales estaban
expuestas directamente en el código fuente, demostrando la importancia
de no dejar información sensible en comentarios de producción.
```

---

## 🎯 Caso de Uso 2: CTF Crypto - Base64 Encoding

### Escenario

**Categoría**: Crypto  
**Nombre**: "Easy Decode"  
**Descripción**: "Descifra este mensaje para obtener la flag"  
**Archivo**: `mensaje.txt` conteniendo `ZmxhZ3tCYXNlNjRfaXNfbm90X2VuY3J5cHRpb259Cg==`

### Ejecución

```bash
# Crear el archivo
echo "ZmxhZ3tCYXNlNjRfaXNfbm90X2VuY3J5cHRpb259Cg==" > mensaje.txt

# Ejecutar solver
./ctf.py \
  -category crypto \
  -name "Easy Decode" \
  -files mensaje.txt \
  -description "Descifra este mensaje para obtener la flag" \
  -report
```

### Proceso (simplificado)

```
[IA] Analizando archivo mensaje.txt...
[IA] El contenido termina en '==', característico de Base64

[CMD] Ejecutando: file mensaje.txt
[Salida] mensaje.txt: ASCII text

[CMD] Ejecutando: base64 -d mensaje.txt
[Salida] flag{Base64_is_not_encryption}

[FLAG] ¡Flag encontrada: flag{Base64_is_not_encryption}!
```

---

## 🎯 Caso de Uso 3: CTF Forensics - Datos Ocultos en Imagen

### Escenario

**Categoría**: Forensics  
**Nombre**: "Hidden Secrets"  
**Archivos**: `challenge.png`  
**Descripción**: "Hay algo más en esta imagen de lo que se ve a simple vista"

### Ejecución

```bash
./ctf.py \
  -category forensics \
  -name "Hidden Secrets" \
  -files challenge.png \
  -description "Hay algo más en esta imagen de lo que se ve a simple vista"
```

### Proceso Esperado

```
[CMD] Ejecutando: file challenge.png
[Salida] challenge.png: PNG image data, 800 x 600, 8-bit/color RGB

[CMD] Ejecutando: strings challenge.png
[Salida] 
IHDR
...(contenido)...
flag{st3g4n0gr4phy_1s_fun}
IEND

[FLAG] ¡Flag encontrada en strings: flag{st3g4n0gr4phy_1s_fun}!

[IA] Voy a confirmar con otras herramientas...

[CMD] Ejecutando: exiftool challenge.png
[CMD] Ejecutando: binwalk challenge.png
```

---

## 🔧 Tips de Resolución Manual

Si el solver no encuentra la flag automáticamente, puedes:

### 1. Revisar el reporte
```bash
cat reports/ctf_*_latest.md
```

### 2. Continuar manualmente con los comandos sugeridos
```bash
# El reporte muestra los comandos ejecutados
# Continúa desde donde se quedó
```

### 3. Dar más contexto
```bash
# Re-ejecutar con más información
./ctf.py \
  -category web \
  -name "Challenge" \
  -target http://target \
  -description "Pista adicional: usa SQLmap con --batch --dump"
```

---

## 📊 Estadísticas de Éxito Esperadas

| Categoría | Dificultad | Tasa de Éxito Estimada |
|-----------|------------|------------------------|
| Web (básico) | Fácil | 80-90% |
| Crypto (encoding) | Fácil | 90-95% |
| Forensics (strings) | Fácil | 70-80% |
| Web (SQLi avanzado) | Media | 50-60% |
| Crypto (RSA débil) | Media | 40-50% |
| Pwn | Difícil | 20-30% |
| Reversing | Difícil | 15-25% |

---

## ⚡ Comandos Rápidos

```bash
# CTF web rápido
./ctf.py -category web -name "Test" -target http://ctf.local

# CTF crypto con archivo
./ctf.py -category crypto -name "Cipher" -files data.enc

# Con reporte completo
./ctf.py -category forensics -name "Analysis" -files image.jpg -report

# Modelo más potente
./ctf.py -category pwn -name "Exploit" -target 10.0.0.1 -port 9001 -model llama3.1

# Ver todas las categorías
./ctf.py --list-categories
```

---

## 🎓 Lecciones Aprendidas

1. **Siempre lee la descripción**: Las pistas están ahí
2. **Empieza simple**: curl, strings, file
3. **Busca lo obvio**: admin/admin, comentarios HTML
4. **Usa el reporte**: Documenta el razonamiento
5. **Itera**: Si falla una vez, ajusta y reintenta

---

¡Buena suerte con tus CTFs! 🚩
