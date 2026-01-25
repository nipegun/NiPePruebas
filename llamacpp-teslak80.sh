#!/bin/bash

# Instalar gcc version 10

  # Desisntalar la vesión actual del compilador gcc
    sudo apt-get -y autoremove --purge gcc g++ gcc-11 g++-11 

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

  # Seleccionar gcc-10 como predeterminado
    sudo update-alternatives --config gcc
    sudo update-alternatives --config g++
    sudo update-alternatives --set gcc /usr/bin/gcc-10
    sudo update-alternatives --set g++ /usr/bin/g++-10




echo 'export PATH=/usr/local/cuda-11.4/bin:$PATH' >> ~/.bashrc
echo 'export LD_LIBRARY_PATH=/usr/local/cuda-11.4/lib64:$LD_LIBRARY_PATH' >> ~/.bashrc
source ~/.bashrc





    # Crear carpeta de Git
      mkdir -p $HOME/Git/ 2> /dev/null

    # Clonar Git
      cd $HOME/Git/
      # Borrar versión ya instalada
        rm -rf $HOME/Git/llama.cpp/
      git clone --depth 1 https://github.com/ggerganov/llama.cpp.git



# Instalar la versión 11 del compilador cpp
  sudo apt-get -y update
  sudo apt-get -y install gcc-10
  sudo apt-get -y install 'g++-10'

# Enlazar el compilador 11 a los binarios por defecto de gcc
  sudo ln -sf /usr/bin/gcc-11 /usr/bin/gcc
  sudo ln -sf /usr/bin/g++-11 /usr/bin/g++

# Descargar el instalador de CUDA toolkit 11.4
  cd /tmp
  sudo wget https://developer.download.nvidia.com/compute/cuda/11.4.4/local_installers/cuda_11.4.4_470.82.01_linux.run
  sudo mkdir -p /root/Software/CUDAToolkit/v11.4.4/
  sudo mv /tmp/cuda_11.4.4_470.82.01_linux.run /root/Software/CUDAToolkit/v11.4.4/installer.run

# Instalar sólo CUDA toolkit usando el compilador version 11
  export CC=/usr/bin/gcc-11
  export CXX=/usr/bin/g++-11
  sudo sh /root/Software/CUDAToolkit/v11.4.4/installer.run --toolkit --silent




    # Instalar dependencias para compilar
      sudo apt-get -y update
      sudo apt-get -y install cmake
      sudo apt-get -y install build-essential
      sudo apt-get -y install libcurl4-openssl-dev
      sudo apt-get -y install ccache
      sudo apt-get -y install libncurses-dev

mkdir -p $HOME/Git/llama.cpp/build
cd $HOME/Git/llama.cpp/build
# Exportar variables
  export CUDA_HOME=/usr/local/cuda-11.4
  export PATH=$CUDA_HOME/bin:$PATH
  export LD_LIBRARY_PATH=$CUDA_HOME/lib64:$LD_LIBRARY_PATH

  export CUDACXX=/usr/local/cuda-11.4/bin/nvcc
  export CC=/usr/bin/gcc-11
  export CXX=/usr/bin/g++-11
  export CUDAHOSTCXX=/usr/bin/g++-11
  
cmake ..                      \
  -DGGML_CUDA=ON              \
  -DGGML_CUDA_FORCE=ON        \
  -DGGML_CUDA_ARCHS=37        \
  -DGGML_CUDA_F16=OFF         \
  -DGGML_CUDA_NO_PEER_COPY=ON \
  -DGGML_NATIVE=OFF           \
  -DCMAKE_CXX_FLAGS="-march=ivybridge -mtune=ivybridge -O3"

cmake --build . --config Release -- -j$(nproc)






CUDA_VISIBLE_DEVICES=0 \
$HOME/IA/LlamaCPP/llama-cli \
  -m modelo.gguf \
  -ngl 20 \
  --stats

