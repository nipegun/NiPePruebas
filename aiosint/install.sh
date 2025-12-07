#!/bin/bash

# install.sh
# Instala el framework AIOSINT (n8n, Maigret, Sherlock, Holehe) de forma nativa en Debian 13.

# Colores para la salida
cColorRojo='\033[1;31m'
cColorVerde='\033[1;32m'
cFinColor='\033[0m'

echo -e "${cColorVerde}[+] Iniciando instalación nativa para Debian 13...${cFinColor}"

# 1. Actualizar e instalar dependencias del sistema
echo -e "${cColorVerde}[+] Actualizando el sistema e instalando dependencias base...${cFinColor}"
sudo apt-get update
sudo apt-get install -y curl git python3-full python3-pip python3-venv nodejs npm build-essential libffi-dev libssl-dev zlib1g-dev lsof netcat-openbsd procps

# 2. Configurar estructura de directorios
echo -e "${cColorVerde}[+] Configurando estructura de directorios...${cFinColor}"
INSTALL_DIR="$HOME/aiosint"
mkdir -p "$INSTALL_DIR/n8n/demo-data/workflows"
mkdir -p "$INSTALL_DIR/venv"

# Copiar archivos necesarios si existen en el directorio actual
# Nos aseguramos de tener los archivos más recientes
if [ -f "./n8n/social-api.py" ]; then
    cp ./n8n/social-api.py "$INSTALL_DIR/n8n/"
else
    echo -e "${cColorRojo}[!] social-api.py no encontrado localmente. Por favor asegúrate de que esté presente.${cFinColor}"
fi

if [ -f "./n8n/demo-data/workflows/Agente_Smith.json" ]; then
    cp ./n8n/demo-data/workflows/Agente_Smith.json "$INSTALL_DIR/n8n/demo-data/workflows/"
fi

# 3. Instalar n8n globalmente
echo -e "${cColorVerde}[+] Instalando n8n globalmente...${cFinColor}"
sudo npm install -g n8n

# 4. Instalar herramientas Python en entorno virtual
echo -e "${cColorVerde}[+] Instalando herramientas Python en entorno virtual...${cFinColor}"
if [ ! -f "$INSTALL_DIR/venv/bin/activate" ]; then
    python3 -m venv "$INSTALL_DIR/venv"
fi

source "$INSTALL_DIR/venv/bin/activate"

# Actualizar pip
pip install --upgrade pip

# Instalar Holehe
echo -e "${cColorVerde}  - Instalando Holehe...${cFinColor}"
pip install holehe

# Instalar Maigret
echo -e "${cColorVerde}  - Instalando Maigret...${cFinColor}"
pip install maigret

# Instalar Sherlock
echo -e "${cColorVerde}  - Instalando Sherlock...${cFinColor}"
pip install sherlock-project

# Instalar Flask
echo -e "${cColorVerde}  - Instalando Flask...${cFinColor}"
pip install flask

deactivate

# 5. Arreglar permisos
echo -e "${cColorVerde}[+] Estableciendo permisos...${cFinColor}"
sudo chown -R $USER:$USER "$INSTALL_DIR"
chmod +x "$INSTALL_DIR/n8n/social-api.py"

echo -e "${cColorVerde}[+] ¡Instalación completada!${cFinColor}"
echo -e "${cColorVerde}[+] Ejecuta './start.sh' para iniciar los servicios.${cFinColor}"
