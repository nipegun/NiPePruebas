#!/bin/bash

# Pongo a disposición pública este script bajo el término de "software de dominio público".
# Puedes hacer lo que quieras con él porque es libre de verdad; no libre con condiciones como las licencias GNU y otras patrañas similares.
# Si se te llena la boca hablando de libertad entonces hazlo realmente libre.
# No tienes que aceptar ningún tipo de términos de uso o licencia para utilizarlo o modificarlo porque va sin CopyLeft.

# ----------
# Script de NiPeGun para compilar e instalar llama.cpp para nVidia Tesla K80 en Debian
#
# Ejecución remota (puede requerir permisos sudo):
#   curl -sL x | bash
#
# Ejecución remota como root (para sistemas sin sudo):
#   curl -sL x | sed 's-sudo--g' | bash
#
# Ejecución remota sin caché:
#   curl -sL -H 'Cache-Control: no-cache, no-store' x | bash
#
# Ejecución remota con parámetros:
#   curl -sL x | bash -s Parámetro1 Parámetro2
#
# Bajar y editar directamente el archivo en nano
#   curl -sL x | nano -
# ----------

# Definir constantes de color
  cColorAzul='\033[0;34m'
  cColorAzulClaro='\033[1;34m'
  cColorVerde='\033[1;32m'
  cColorRojo='\033[1;31m'
  # Para el color rojo también:
    #echo "$(tput setaf 1)Mensaje en color rojo. $(tput sgr 0)"
  cFinColor='\033[0m'

# Determinar la versión de Debian
  if [ -f /etc/os-release ]; then             # Para systemd y freedesktop.org.
    . /etc/os-release
    cNomSO=$NAME
    cVerSO=$VERSION_ID
  elif type lsb_release >/dev/null 2>&1; then # Para linuxbase.org.
    cNomSO=$(lsb_release -si)
    cVerSO=$(lsb_release -sr)
  elif [ -f /etc/lsb-release ]; then          # Para algunas versiones de Debian sin el comando lsb_release.
    . /etc/lsb-release
    cNomSO=$DISTRIB_ID
    cVerSO=$DISTRIB_RELEASE
  elif [ -f /etc/debian_version ]; then       # Para versiones viejas de Debian.
    cNomSO=Debian
    cVerSO=$(cat /etc/debian_version)
  else                                        # Para el viejo uname (También funciona para BSD).
    cNomSO=$(uname -s)
    cVerSO=$(uname -r)
  fi

# Ejecutar comandos dependiendo de la versión de Debian detectada

  if [ $cVerSO == "13" ]; then

    echo ""
    echo -e "${cColorAzulClaro}  Iniciando el script de compilación e instalación de llama.cpp para nVidia Tesla K80 en Debian 13 (x)...${cFinColor}"
    echo ""

    echo ""
    echo -e "${cColorRojo}    Comandos para Debian 13 todavía no preparados. Prueba ejecutarlo en otra versión de Debian.${cFinColor}"
    echo ""

  elif [ $cVerSO == "12" ]; then

    echo ""
    echo -e "${cColorAzulClaro}  Iniciando el script de compilación e instalación de llama.cpp para nVidia Tesla K80 en Debian 12 (Bookworm)...${cFinColor}"
    echo ""

    # Instalar dependencias para compilar
      sudo apt-get -y update
      sudo apt-get -y install cmake
      sudo apt-get -y install build-essential
      sudo apt-get -y install libcurl4-openssl-dev
      sudo apt-get -y install ccache
      sudo apt-get -y install libncurses-dev
      sudo apt-get -y install libssl-dev
      sudo apt-get -y install git

    # Instalar gcc version 10
      # Desisntalar la vesión actual del compilador gcc
        #sudo apt-get -y autoremove --purge gcc g++ gcc-11 g++-11 
      # Añadir repositorio de Debian 11
        echo "deb http://deb.debian.org/debian bullseye main" | sudo tee /etc/apt/sources.list.d/bullseye.list
      # Crear archivo de preferencias para evitar conflictos
        echo 'Package: *'                                                   | sudo tee    /etc/apt/preferences.d/bullseye
        echo 'Pin: release n=bullseye'                                      | sudo tee -a /etc/apt/preferences.d/bullseye
        echo 'Pin-Priority: 100'                                            | sudo tee -a /etc/apt/preferences.d/bullseye
        echo ''                                                             | sudo tee -a /etc/apt/preferences.d/bullseye
        echo 'Package: gcc-10 g++-10 cpp-10 libgcc-10-dev libstdc++-10-dev' | sudo tee -a /etc/apt/preferences.d/bullseye
        echo 'Pin: release n=bullseye'                                      | sudo tee -a /etc/apt/preferences.d/bullseye
        echo 'Pin-Priority: 500'                                            | sudo tee -a /etc/apt/preferences.d/bullseye
      # Instalar gcc 10
        sudo apt-get -y update
        sudo apt-get -y install gcc-10
        sudo apt-get -y install g++-10
      # Configurar alternativas para compilación cuda
        sudo update-alternatives --install /usr/bin/gcc gcc /usr/bin/gcc-10 10
        sudo update-alternatives --install /usr/bin/g++ g++ /usr/bin/g++-10 10
        sudo update-alternatives --install /usr/bin/gcc gcc /usr/bin/gcc-12 12
        sudo update-alternatives --install /usr/bin/g++ g++ /usr/bin/g++-12 12

    # Instalar cuda toolkit 11.4
      # Descargar el instalador
        cd /tmp
        sudo wget https://developer.download.nvidia.com/compute/cuda/11.4.4/local_installers/cuda_11.4.4_470.82.01_linux.run
        sudo mkdir -p /root/Software/CUDAToolkit/v11.4.4/
        sudo mv /tmp/cuda_11.4.4_470.82.01_linux.run /root/Software/CUDAToolkit/v11.4.4/installer.run
      # Instalar
        # Seleccionar gcc-10 como predeterminado
          sudo update-alternatives --set gcc /usr/bin/gcc-10
          sudo update-alternatives --set g++ /usr/bin/g++-10
        sudo sh /root/Software/CUDAToolkit/v11.4.4/installer.run --toolkit
        # Para instalar con el driver:
        #   sudo sh /root/Software/CUDAToolkit/v11.4.4/installer.run --toolkit --driver --silent
        # Para desinstalar:
        #   /usr/local/cuda-11.4/bin/cuda-uninstaller
        # Preparar path
          # Para el usuario actual
            echo 'export PATH=/usr/local/cuda-11.4/bin:$PATH' >> ~/.bashrc
            echo 'export LD_LIBRARY_PATH=/usr/local/cuda-11.4/lib64:$LD_LIBRARY_PATH' >> ~/.bashrc
            source ~/.bashrc
          # Para el root
            echo '/usr/local/cuda-11.4/lib64' | sudo tee -a /etc/ld.so.conf.d/cuda.conf

    # Descargar el repo de llama.cpp
      mkdir -p $HOME/Git/ 2> /dev/null
      cd $HOME/Git/
      # Borrar versión ya descargada
        rm -rf $HOME/Git/llama.cpp/
      git clone --depth 1 https://github.com/ggerganov/llama.cpp.git

    # Compilar
      mkdir -p $HOME/Git/llama.cpp/build
      cd $HOME/Git/llama.cpp/build
      cmake ..                                              \
        -DGGML_CUDA=ON                                      \
        -DGGML_CUDA_FORCE=ON                                \
        -DGGML_CUDA_ARCHS=37                                \
        -DGGML_CUDA_F16=OFF                                 \
        -DGGML_CUDA_NO_PEER_COPY=ON                         \
        -DGGML_NATIVE=ON                                    \
        -DCMAKE_CUDA_COMPILER=/usr/local/cuda-11.4/bin/nvcc \
        -DCMAKE_C_COMPILER=gcc-10                           \
        -DCMAKE_CXX_COMPILER=g++-10                         \
        -DCMAKE_CUDA_FLAGS="-Wno-deprecated-gpu-targets"
        #-DCMAKE_CXX_FLAGS="-march=ivybridge -mtune=ivybridge -O3"
      #export CUDA_NVCC_FLAGS="-Wno-deprecated-gpu-targets"
      cmake --build . --config Release -- -j$(nproc)
      #make NVCCFLAGS="-Wno-deprecated-gpu-targets" -j$(nproc)

    # Crear carpeta
      mkdir -p $HOME/IA/LlamaCPP/ 2> /dev/null
      rm -rf $HOME/IA/LlamaCPP/* 2> /dev/null
      cp -fv $HOME/Git/llama.cpp/build/bin/* $HOME/IA/LlamaCPP/

    # Notificar fin de ejecución del script
      echo ""
      echo "  Ejecución del script, finalizada."
      echo ""
      echo "    Para ejecutar llama.cpp y realizar una consulta, cerrando la conversación:"
      echo ""
      echo "      $HOME/IA/LlamaCPP/llama-cli -m $HOME/IA/Modelos/GGUF/Llama-3.2-3B-Instruct-Q8_0.gguf -p 'Hazme un script de python que diga hola?' -no-cnv"
      echo ""
      echo "      Podemos hacer que cierre la conversación, aunque no responda por completo, limitando el nro de tokens de respuesta:"
      echo ""
      echo "        $HOME/IA/LlamaCPP/llama-cli -m $HOME/IA/Modelos/GGUF/Llama-3.2-3B-Instruct-Q8_0.gguf -p 'Hazme un script de python que diga hola?' -n 128 -no-cnv"
      echo ""
      echo "    Para indicarle cuanta VRAM usar (en el caso de haber compilado con soporte CUDA):"
      echo ""
      echo "      $HOME/IA/LlamaCPP/llama-cli -m $HOME/IA/Modelos/GGUF/Llama-3.2-3B-Instruct-Q8_0.gguf -ngl 100 --n-gpu-layers 32"
      echo ""
      echo "        -ngl 100: Usa la GPU completamente."
      echo "        --n-gpu-layers 32: Define cuántas capas del modelo se ejecutarán en la GPU (ajústalo según la VRAM disponible)."
      echo ""
      echo "    Para ejecutar en modo conversación:"
      echo ""
      echo "      $HOME/IA/LlamaCPP/llama-cli -m $HOME/IA/Modelos/GGUF/Llama-3.2-3B-Instruct-Q8_0.gguf"
      echo ""
      echo "    Para ejecutar como API/servidor:"
      echo ""
      echo "      $HOME/IA/LlamaCPP/llama-server --port 9000 -m $HOME/IA/Modelos/GGUF/Llama-3.2-3B-Instruct-Q8_0.gguf"
      echo ""
      echo "      Crear un servidor para 4 usuarios simultáneos y contexto de 4096 para cada uno:"
      echo ""
      echo "        $HOME/IA/LlamaCPP/llama-server --port 9000 -m $HOME/IA/Modelos/GGUF/Llama-3.2-3B-Instruct-Q8_0.gguf -c 16384 -np 4"
      echo ""
      echo "      Luego podemos tirarle consultas con:"
      echo ""
      echo "        curl -X POST http://localhost:9000/completion -d '{"prompt": "Hola, ¿cómo estás?", "n_predict": 50}'"
      echo ""

    # Ejecutar
      #$HOME/IA/LlamaCPP/llama-cli -m modelo.gguf -ngl 20  --stats

    # Exportar variables
      #export CUDA_HOME=/usr/local/cuda-11.4
      #export PATH=$CUDA_HOME/bin:$PATH
      #export LD_LIBRARY_PATH=$CUDA_HOME/lib64:$LD_LIBRARY_PATH
      #export CUDACXX=/usr/local/cuda-11.4/bin/nvcc
      #export CC=/usr/bin/gcc-11
      #export CXX=/usr/bin/g++-11
      #export CUDAHOSTCXX=/usr/bin/g++-11

  elif [ $cVerSO == "11" ]; then

    echo ""
    echo -e "${cColorAzulClaro}  Iniciando el script de compilación e instalación de llama.cpp para nVidia Tesla K80 en Debian 11 (Bullseye)...${cFinColor}"
    echo ""

    echo ""
    echo -e "${cColorRojo}    Comandos para Debian 11 todavía no preparados. Prueba ejecutarlo en otra versión de Debian.${cFinColor}"
    echo ""

  elif [ $cVerSO == "10" ]; then

    echo ""
    echo -e "${cColorAzulClaro}  Iniciando el script de compilación e instalación de llama.cpp para nVidia Tesla K80 en Debian 10 (Buster)...${cFinColor}"
    echo ""

    echo ""
    echo -e "${cColorRojo}    Comandos para Debian 10 todavía no preparados. Prueba ejecutarlo en otra versión de Debian.${cFinColor}"
    echo ""

  elif [ $cVerSO == "9" ]; then

    echo ""
    echo -e "${cColorAzulClaro}  Iniciando el script de compilación e instalación de llama.cpp para nVidia Tesla K80 en Debian 9 (Stretch)...${cFinColor}"
    echo ""

    echo ""
    echo -e "${cColorRojo}    Comandos para Debian 9 todavía no preparados. Prueba ejecutarlo en otra versión de Debian.${cFinColor}"
    echo ""

  elif [ $cVerSO == "8" ]; then

    echo ""
    echo -e "${cColorAzulClaro}  Iniciando el script de compilación e instalación de llama.cpp para nVidia Tesla K80 en Debian 8 (Jessie)...${cFinColor}"
    echo ""

    echo ""
    echo -e "${cColorRojo}    Comandos para Debian 8 todavía no preparados. Prueba ejecutarlo en otra versión de Debian.${cFinColor}"
    echo ""

  elif [ $cVerSO == "7" ]; then

    echo ""
    echo -e "${cColorAzulClaro}  Iniciando el script de compilación e instalación de llama.cpp para nVidia Tesla K80 en Debian 7 (Wheezy)...${cFinColor}"
    echo ""

    echo ""
    echo -e "${cColorRojo}    Comandos para Debian 7 todavía no preparados. Prueba ejecutarlo en otra versión de Debian.${cFinColor}"
    echo ""

  fi

# Remove the ollama service:
  sudo systemctl stop ollama
  sudo systemctl disable ollama
  sudo rm /etc/systemd/system/ollama.service

# Remove ollama libraries from your lib directory (either /usr/local/lib, /usr/lib, or /lib):
  sudo rm -r $(which ollama | tr 'bin' 'lib')
  sudo rm -rf /usr/lib/ollama

# Remove the ollama binary from your bin directory (either /usr/local/bin, /usr/bin, or /bin):
  sudo rm $(which ollama)

# Remove the downloaded models and Ollama service user and group:
  sudo userdel ollama
  sudo groupdel ollama
  sudo rm -r /usr/share/ollama

https://huggingface.co/ggml-org/GLM-4.7-Flash-GGUF/resolve/main/GLM-4.7-Flash-Q4_K.gguf
https://huggingface.co/ggml-org/GLM-4.7-Flash-GGUF/resolve/main/GLM-4.7-Flash-Q8_0.gguf
