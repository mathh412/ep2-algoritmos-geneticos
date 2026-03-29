# Otimização de Reabastecimento de Estoque com Algoritmo Genético

Este repositório contém a implementação de um Algoritmo Genético (AG) desenvolvido para resolver o problema de reabastecimento semanal de uma rede de supermercados com 4 filiais e 20 produtos.

O objetivo do algoritmo é gerar um plano de entregas que minimize os custos operacionais (frete e produtos) e evite penalidades rigorosas relacionadas a rupturas de estoque, excesso de armazenamento, validades e dias de entrega não permitidos.

## Estrutura do Repositório

```text
/
├── README.md               <- Este arquivo com as instruções de execução
├── src/
│   ├── main.py             <- Código-fonte principal do Algoritmo Genético
│   └── experimentos.py     <- Script de automação para o estudo de hiperparâmetros
└── docs/
    ├── modelagem.md        <- Documentação técnica detalhando a modelagem do AG
    └── hiperparametros.md  <- Relatório de testes e gráficos de convergência
```

## Requisitos

O projeto foi desenvolvido utilizando **Python puro** e não possui dependências externas.
* **Python 3.11 ou superior**

## Como Executar

Abra o terminal, navegue até o diretório raiz do projeto e execute o arquivo `main.py` localizado na pasta `src`. Você pode rodar o algoritmo com os parâmetros padrão ou customizar os hiperparâmetros via linha de comando.

### Execução com Parâmetros Padrão

```bash
python src/main.py
```
*(Parâmetros padrão: População = 100, Gerações = 200, Mutação = 5%, Crossover = 85%, Elitismo = 4)*

### Execução Customizada

Você pode alterar o comportamento do algoritmo passando argumentos diretamente no terminal:

```bash
python src/main.py --populacao 150 --geracoes 300 --mutacao 0.10 --crossover 0.90
```

**Argumentos disponíveis:**
* `--populacao`: Tamanho da população (Inteiro. Ex: 100)
* `--geracoes`: Número máximo de gerações (Inteiro. Ex: 200)
* `--mutacao`: Taxa de probabilidade de mutação (Float de 0.0 a 1.0. Ex: 0.05)
* `--crossover`: Taxa de probabilidade de cruzamento (Float de 0.0 a 1.0. Ex: 0.85)

### Automação de Testes (Hiperparâmetros)

Para reproduzir os testes exigidos para a documentação e gerar automaticamente o arquivo `hiperparametros.md` com os gráficos Mermaid:

```bash
cd src
python experimentos.py
```

## Saída do Programa

Durante a execução, o terminal exibirá a evolução do algoritmo mostrando o custo (Pior, Médio e Melhor) a cada 10 gerações. 

Ao final da execução (por limite de gerações ou detecção de convergência por estagnação), o sistema imprimirá o **Relatório Final de Reabastecimento**, estruturado em tabelas de texto contendo:
* O cronograma exato de pedidos (produto, quantidade e dia) para cada filial.
* O custo total detalhado (Gasto com Produtos, Custo de Pedidos/Frete, Multas por Rupturas e Excessos).
* O número de violações de restrições críticas na solução final.
* O valor absoluto da Função de Aptidão (Fitness) alcançado pela melhor solução.