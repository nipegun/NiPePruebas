#!/bin/bash

    # Crear carpeta de Git
      mkdir -p $HOME/Git/ 2> /dev/null

    # Clonar Git
      cd $HOME/Git/
      # Borrar versión ya instalada
        rm -rf $HOME/Git/llama.cpp/
      git clone --depth 1 https://github.com/ggerganov/llama.cpp.git

# Instalar la versión 11 del compilador cpp
  sudo apt-get -y update
  sudo apt-get -y install gcc-11
  sudo apt-get -y install 'g++-11'

# Descargar el instalador de CUDA toolkit 11.4
  cd /tmp
  sudo wget https://developer.download.nvidia.com/compute/cuda/11.4.4/local_installers/cuda_11.4.4_470.82.01_linux.run
  sudo mkdir -p /root/Software/CUDAToolkit/v11.4.4/
  sudo mv /tmp/cuda_11.4.4_470.82.01_linux.run /root/Software/CUDAToolkit/v11.4.4/installer.run

# Instalar sólo CUDA toolkit usando el compilador version 11
  export CC=/usr/bin/gcc-11
  export CXX=/usr/bin/g++-11
  sudo sh /root/Software/CUDAToolkit/v11.4.4/installer.run --toolkit --silent

# Exportar variables
  export CUDA_HOME=/usr/local/cuda-11.4
  export PATH=$CUDA_HOME/bin:$PATH
  export LD_LIBRARY_PATH=$CUDA_HOME/lib64:$LD_LIBRARY_PATH


    # Instalar dependencias para compilar
      sudo apt-get -y update
      sudo apt-get -y install cmake
      sudo apt-get -y install build-essential
      sudo apt-get -y install libcurl4-openssl-dev
      sudo apt-get -y install ccache
      sudo apt-get -y install libncurses-dev

mkdir -p $HOME/Git/llama.cpp/build
cd $HOME/Git/llama.cpp/build
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

