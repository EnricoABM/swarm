# swarm
Projeto de automação residencial utilizando de sensores e atuadores controlados por uma placa ESP32. A aplicação integra Internet da Coisas (IoT) ao cená cotidiano para auxiliar em tarefas cotidianas. 

# Como executar

### Dependências necessárias:
* Visual Studio Code.
* Socat

### Baixe as extensões necessárias no Visual Studio Code.
* Python
* Wokwi
* ESP-IDF
* MicroPico

### Faça clone do repositório.
```bash
git clone https://github.com/EnricoABM/swarm.git

cd swarm
```

### Crie um ambiente virtual e instale as bibliotecas.
```bash
python -m venv .venv

source ./.venv/bin/activate

pip install -f requirements.txt
```

### Crie o canal de comunicação.
```bash
socat PTY,link=$HOME/wokwi-serial,raw,echo=0 TCP:localhost:4000
```

### Inicie o simulador e envie os arquivos para o ESP32.
```bash
python -m mpremote connect $HOME/wokwi-serial fs cp *.py : + run main.py
```

