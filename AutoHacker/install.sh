sudo apt install -y build-essential libssl-dev zlib1g-dev \
  libbz2-dev libreadline-dev libsqlite3-dev curl \
  libncursesw5-dev xz-utils tk-dev libxml2-dev \
  libxmlsec1-dev libffi-dev liblzma-dev

curl https://pyenv.run | bash

echo 'export PATH="$HOME/.pyenv/bin:$PATH"' | tee -a ~/.bashrc
echo 'eval "$(pyenv init -)"'               | tee -a ~/.bashrc
echo 'eval "$(pyenv virtualenv-init -)"'    | tee -a ~/.bashrc

source ~/.bashrc


pyenv install 3.8.19

# Crear entorno virtual
  mkdir ~/HackingTools/AutoHacker/
  cd ~/HackingTools/AutoHacker/
  pyenv virtualenv 3.8.19 venv38
  pyenv activate venv38

  source deactivate
