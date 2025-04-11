# case_elo
Resolução do desafio técnico para o processo seletivo de análise de dados do Elo Group 2025

## Estrutura de Pastas
Este projeto conta com a seguinte estrutura de pastas:

```
case_elo/
├── notebooks/           # Notebooks Jupyter para análise e exploração
│   ├── raw_data/        # Dados brutos
│   ├── curated_data/    # Dados processados e organizados
│   ├── analytics_data/  # Dados para análise final
│   ├── get_data.ipynb   # Notebook para buscar os dados
│   ├── clean_data.ipynb # Notebook para limpeza e transformação dos dados
│   └── analysis.ipynb   # Notebook para análise de hipóteses e proposta de solução
├── pipeline/            # Scripts de ETL e pipeline de dados
│   ├── raw_data/        # Dados brutos
│   ├── curated_data/    # Dados processados e organizados
│   ├── analytics_data/  # Dados para análise final
│   ├── src/                 # Scripts principais para o pipeline
│   │   ├── get_data.py      # Script para buscar os dados
│   │   ├── process_data.py  # Script para limpeza e transformação dos dados
│   │   ├── analytics.py     # Script para análise de dados
|   ├── pipeline.py          # Script principal que executa as funções do pipeline
├── reports/                    # Apresentação de resultados
│   ├── presentation.md         # montagem da apresentação em markdown
│   ├── presentation.pdf        # apresentação em pdf
├── requirements.txt     # Bibliotecas para execução do projeto
└── README.md            # Documentação do projeto
```

A recomendação final estará em formato .txt na pasta analytics_data, tanto em notebooks quanto no pipeline de dados.



## Como executar

### Requisitos
- Foi utilizada versão python 3.12
- Máquina deve ter ferramenta de gerenciamento de ambientes virtuais (como virtualenv) e git instaladas


### Executando localmente
1. Clone o repositório:
```bash
git clone https://github.com/adonaiarruda/case_elo.git
cd case_elo
```
2. Crie um ambiente virtual:
```bash
python3 -m virtualenv .venv
```
3. Ative o ambiente virtual:
    - No Linux/MacOS:
    ```bash
    source .venv/bin/activate
    ```
    - No Windows:
    ```bash
    .venv\Scripts\activate
    ```
4. Instale as dependências:
```bash
pip install -r requirements.txt
```

### Executando no Google Colab
1. Faça upload dos notebooks para o Google Colab.
2. Certifique-se de carregar os dados necessários no ambiente do Colab.
3. Instale as dependências diretamente no Colab, se necessário:
```python
!pip install -r requirements.txt
```
4. Execute as células do notebook conforme indicado.


### Executando notebooks interativos de análise
Execute nesta ordem:
- get_data.ipynb
- clean_data.ipynb
- analysis.ipynb

### Executando pipeline de dados

Execute usando o comando: 
```bash
python3 pipeline/pipeline.py
```
As recomendações de ZCTAs estão no arquivo: 
```bash
pipeline/analytics_data/proposed_zctas.txt
```

obs: É possível que ocorra erro no download dos dados. Aguarde alguns segundos e execute novamente.


## Arquivos de dados

Os arquivos de dados brutos estão armazenados em .zip no endereço: 
https://drive.usercontent.google.com/download?id=1GINDasXHcESqGYMX6KuhEGzCZEx71wHg

Os dados tratados pelo pipeline de dados ou pelos notebooks iterativos são armazenados localmente após execução.


observação: Este repositório terá visibilidade pública durante o período de avaliação e depois retornará a ser privado para proteção de dados.