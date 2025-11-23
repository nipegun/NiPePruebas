#!/bin/bash

# Definir constantes
  vNombreRepoGithub='pruebas'
  vUbicArchEnRepo='PHAH'

# Clonar el repo de pruebas
  cd /tmp
  rm -rf /tmp/"$vNombreRepoGithub"/
  git clone https://github.com/nipegun/"$vNombreRepoGithub".git

# Crear carpeta de hacking en la home del usuario
  mkdir -p $HOME/HackingTools/PHAH/ 2> /dev/null
  rm -rf $HOME/HackingTools/PHAH/* 2> /dev/null

# Desactivar posible entorno virtual de python ejecutándose
  deactivate

# Mover archivos a la carpeta
  cp -Rv /tmp/"$vNombreRepoGithub"/"$vUbicArchEnRepo"/* $HOME/HackingTools/PHAH/

# Crear el entorno virtual de python
  cd $HOME/HackingTools/PHAH/
  python3 -m venv venv

# Entrar en el entorno virtual e instalar requirements
  source $HOME/HackingTools/PHAH/venv/bin/activate
  pip install -r install/requirements.txt

# Salir del entorno virtual
  deactivate

# Notificar fin de la instalación
  echo ""
  echo "  Instalación finalizada."
  echo ""
  echo "  Para ejecutar y posicionarse en la carpeta:"
  echo ""
  echo "    source $HOME/HackingTools/PHAH/venv/bin/activate  && cd $HOME/HackingTools/PHAH/"
  echo ""
  echo ""
  echo "  Para listar servicios:"
  echo ""
  echo "    python phah.py --list-services"
  echo ""

