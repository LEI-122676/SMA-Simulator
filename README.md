# SMA-Simulator

## Grupo AA1
- Catarina Figueiredo, 122706
- Pedro Torrado, 106584
- Tiago Candeias, 122676

Simulador de agentes (SMA) em Python com suporte a ambientes de forrageamento e cooperação, redes neurais simples e visualizações.

## Visão geral

Este repositório contém um simulador acadêmico/experimental para estudar comportamentos emergentes de agentes em ambientes discretos (nests, walls, eggs, pedras, galinheiros, etc.). Possui:

- Implementação do mundo e itens (`Worlds/`, `Items/`).
- Agentes e ações (`Agents/`, `Actions/`).
- Motor de simulação e utilitários (`Simulators/`).
- Redes neurais simples para controlar agentes (`NeuralNetworks/`).
- Ferramentas de visualização (`visualization/`).

O objetivo deste README é explicar como instalar dependências, executar o demo e gerar visualizações dos resultados.

## Requisitos

- Python 3.8+ (testado em 3.8/3.9/3.10)
- Bibliotecas Python (instale via pip):
  - numpy
  - matplotlib
  - seaborn

Observação: `tkinter` faz parte da biblioteca padrão do Python em muitas distribuições; no Windows normalmente já está disponível. Se o seu ambiente Python foi construído sem `tkinter`, instale a versão do Python que inclua suporte a Tk.

---

## Instalação

1. Crie um ambiente virtual e ative-o:

```terminal
python -m venv .venv
.\.venv\Scripts\Activate.ps1
```

2. Instale as dependências:

```terminal
pip install --upgrade pip
pip install -r requirements.txt
```

O ficheiro `requirements.txt` já está incluído na raiz do repositório com as dependências básicas do projeto (`numpy`, `matplotlib`, `seaborn`).

## Estrutura principal do projeto

- `Simulators/` — motor de simulação, demo e utilitários.
- `Worlds/`, `Items/`, `Agents/`, `Actions/` — modelagem do ambiente e agentes.
- `NeuralNetworks/` — implementação simples de redes neurais usadas para controlar agentes.
- `visualization/` — scripts para gerar gráficos e replay GUI.
- `Levels/` — exemplos de mapas (text files) usados pelo simulador.

## Executar o projeto

O arquivo de entrada principal é `Simulators/demo.py`. Ele possui 3 modos de execução:

- `DUMB` — política heurística fixa (execução única).
- `TRAIN` — treina com um algoritmo evolucionário (várias gerações) e salva resultados em `results/`.
- `TEST` — testa a rede treinada num mapa (execução única).

Exemplo para executar o demo num Terminal:

```terminal
# A partir da raíz do projeto, abra um terminal e execute:
python -m Simulators.demo
```

Deve mudar a variável "MODE" no início de `demo.py` para um dos 3 modos de execução referidos acima.

### Executar com parâmetros (visualizar o runner)

Você também pode usar o script `visualization/visualize.py` para rodar o simulador com argumentos CLI e salvar gráficos:

```terminal
# Exemplo (executar no mapa 3 de foraging com 40 gerações de 80 indivíduos):
python -m visualization.visualize --map Levels/foraging_level3.txt --pop 80 --gens 40 --outdir results
```

Parâmetros úteis:
- `--map` / `-m`: ficheiro de mapa (em `Levels/`).
- `--pop` / `-p`: tamanho da população para o algoritmo evolucionário.
- `--gens` / `-g`: número de gerações.
- `--outdir` / `-o`: diretório de saída para imagens (se omitido, mostra as janelas interativas).
- `--headless`: executa sem abrir as janelas gráficas (útil em servidores sem display).

## Visualização gráfica e replay GUI

```terminal
# Para abrir a GUI (apenas após treinos, .pkl é necessário):
$ python -m visualization.replay_gui
```
---
