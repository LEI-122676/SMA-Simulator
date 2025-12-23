# SMA-Simulator

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

## Instalação (Windows PowerShell)

1. Crie um ambiente virtual e ative-o:

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
```

2. Instale as dependências:

```powershell
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

## Executar o demo

O arquivo de entrada principal é `Simulators/demo.py`. Ele possui 3 modos de execução:

- `DUMB` — política heurística fixa (execução única).
- `TRAIN` — treina com um algoritmo evolucionário (várias gerações) e salva resultados em `results/`.
- `TEST` — testa a rede treinada num mapa (execução única).

Exemplo para executar o demo em PowerShell:

```powershell
# ativar o ambiente como acima, então:
python -m Simulators.demo

# Ou editar a variável MODE dentro de Simulators/demo.py e executar:
python Simulators\demo.py
```

Por padrão o `demo.py` usa `headless=False` (mostra visualização durante a execução) e grava gráficos de análise em `results/` quando no modo `TRAIN`.

### Executar com parâmetros (visualize runner)

Você também pode usar o script `visualization/visualize.py` para rodar o simulador com argumentos CLI e salvar gráficos:

```powershell
python visualization\visualize.py --map Levels/simple_foraging.txt --pop 40 --gens 20 --outdir results
```

Parâmetros úteis:
- `--map` / `-m`: ficheiro de mapa (em `Levels/`).
- `--pop` / `-p`: tamanho da população para o algoritmo evolucionário.
- `--gens` / `-g`: número de gerações.
- `--outdir` / `-o`: diretório de saída para imagens (se omitido, mostra as janelas interativas).
- `--headless`: executa sem abrir as janelas gráficas (útil em servidores sem display).

## Visualização gráfica e replay GUI

- `visualization/visualize.py` gera gráficos (heatmap de visitas, caminhos representativos, fitness por geração) e salva PNGs.
- `visualization/replay_gui.py` é uma pequena GUI baseada em `tkinter` + `matplotlib` para abrir replays/arquivos; execute-a diretamente para carregar resultados.

## Testes

Não há uma suíte de testes automatizada incluída no repositório (ex.: pytest). Para testar manualmente:

1. Execute o demo em modo `DUMB` para validar que o simulador roda e que não há erros óbvios.
2. Execute com `MODE = "TRAIN"` por poucas gerações (ex.: `NUM_GENERATIONS` menor) e verifique a criação de imagens em `results/`.

Se desejar, posso adicionar uma pequena suíte de testes (pytest) com um teste rápido de importação e execução mínima do motor.

## Sugestões e notas de desenvolvimento

- Para reproduzir resultados mais previsíveis, fixe a seed de `random` e `numpy.random` antes dos treinos.
- Parâmetros importantes do motor (população, número de gerações, tamanho da rede) estão em `Simulators/SimulatorMotor.py` e podem ser ajustados antes da execução.
- Para execução em servidores sem GUI, passe `--headless` a `visualize.py` ou utilize `SimulatorMotor.create(..., headless=True)`.


---

*README gerado com auxílio de ferramentas automatizadas.*