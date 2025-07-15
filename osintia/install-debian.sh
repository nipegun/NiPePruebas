#!/bin/bash

# curl -sL https://raw.githubusercontent.com/nipegun/pruebas/refs/heads/main/osintia/install-debian.sh | bash

# curl -sL https://raw.githubusercontent.com/nipegun/pruebas/refs/heads/main/osintia/install-debian.sh | sed 's-sudo--g' | bash

# Comprobar si el paquete curl está instalado. Si no lo está, instalarlo.
  if [[ $(dpkg-query -s curl 2>/dev/null | grep installed) == "" ]]; then
    echo ""
    echo -e "${cColorRojo}  El paquete curl no está instalado. Iniciando su instalación...${cFinColor}"
    echo ""
    sudo apt-get -y update
    sudo apt-get -y install curl
    echo ""
  fi

# CLonar el repositorio
  echo ""
  echo "  Creando carpetas y archivos..."
  echo ""
  sudo rm -rf $HOME/osintia/
  sudo mkdir -p $HOME/osintia/n8n/demo-data/workflows/
  cd $HOME/osintia/
  sudo curl -sL -O https://raw.githubusercontent.com/nipegun/pruebas/refs/heads/main/osintia/.env_euskal
  sudo curl -sL -O https://raw.githubusercontent.com/nipegun/pruebas/refs/heads/main/osintia/Dockerfile.n8n
  sudo curl -sL -O https://raw.githubusercontent.com/nipegun/pruebas/refs/heads/main/osintia/docker-compose.yaml
  sudo curl -sL -O https://raw.githubusercontent.com/nipegun/pruebas/refs/heads/main/osintia/scraper.py
  sudo curl -sL -O https://raw.githubusercontent.com/nipegun/pruebas/refs/heads/main/osintia/start.sh
  sudo curl -sL -O https://raw.githubusercontent.com/nipegun/pruebas/refs/heads/main/osintia/test.sh
  cd $HOME/osintia/n8n/
  sudo curl -sL -O https://raw.githubusercontent.com/nipegun/pruebas/refs/heads/main/osintia/n8n/n8n.dockerfile
  sudo curl -sL -O https://raw.githubusercontent.com/nipegun/pruebas/refs/heads/main/osintia/n8n/social-api.py
  cd $HOME/osintia/n8n/demo-data/workflows/
  sudo curl -sL -O https://raw.githubusercontent.com/nipegun/pruebas/refs/heads/main/osintia/n8n/demo-data/workflows/Agente_Smith.json
  sudo chown $USER:$USER $HOME/osintia/ -Rv
  # Permisos
    find $HOME/osintia/ -print -type f -name "*.py" -exec chmod +x {} \;
    find $HOME/osintia/ -print -type f -name "*.sh" -exec chmod +x {} \;
  #ls -lha --group-directories-first
