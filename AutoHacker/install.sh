sudo apt install -y build-essential libssl-dev zlib1g-dev \
  libbz2-dev libreadline-dev libsqlite3-dev curl \
  libncursesw5-dev xz-utils tk-dev libxml2-dev \
  libxmlsec1-dev libffi-dev liblzma-dev

curl https://pyenv.run | bash

echo 'export PATH="$HOME/.pyenv/bin:$PATH"' | tee -a ~/.bashrc
echo 'eval "$(pyenv init -)"'               | tee -a ~/.bashrc
echo 'eval "$(pyenv virtualenv-init -)"'    | tee -a ~/.bashrc

source ~/.bashrc

vVersPython='3.8.19'

pyenv install "$vVersPython"

# Crear entorno virtual
  mkdir ~/HackingTools/AutoHacker/ 2> /dev/null
  cd ~/HackingTools/AutoHacker/
  $HOME/.pyenv/versions/"$vVersPython"/bin/python3.8 -m venv ~/HackingTools/AutoHacker/venv38

source $HOME/HackingTools/AutoHacker/venv38/bin/activate
  pip install --upgrade pip
  cd $HOME/HackingTools/AutoHacker/
  pip install -r requirements.txt

sed -i 's|from cai.|from CAI.|g' ~/HackingTools/AutoHacker/cli.py

  source deactivate
