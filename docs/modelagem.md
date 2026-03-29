# Documentação Técnica: Modelagem do AG para Reabastecimento de Estoque

## 1. Cromossomo
O cromossomo foi modelado como uma estrutura de dicionários aninhados para refletir com fidelidade a complexidade logística do problema, sem perder a semântica dos dados. 

* **Estrutura e Representação:** A hierarquia do dicionário é `Filial` -> `Produto` -> `Lista de 7 dias`. Cada gene (a menor unidade de informação) é um número inteiro `q` posicionado dentro da lista de 7 dias, representando a **quantidade pedida** de um determinado produto para uma filial específica naquele dia.
* **Domínio dos valores:** $q \in \mathbb{N}$, onde `q = 0` (nenhum pedido) ou `q >= pedido_minimo`.
* **Tamanho do cromossomo:** O cromossomo possui tamanho fixo de **560 genes**, resultado da combinação de 4 filiais x 20 produtos x 7 dias de planejamento.

## 2. Função de Aptidão (Fitness)
Como o Algoritmo Genético padrão busca maximizar o fitness, a função foi construída para retornar o custo total em valor negativo. Dessa forma, o menor custo real se torna o maior valor de aptidão (mais próximo de zero).

* **Fórmula base:**
$$f = -(C_{produtos} + C_{pedidos} + C_{ruptura} + C_{excesso} + Multas_{restricoes})$$

* **Componentes e Penalidades:**
  * **Custo de Produtos:** Soma do volume pedido multiplicado pelo custo unitário de cada produto.
  * **Custo de Pedidos:** Custo de frete consolidado. Calculado agrupando os pedidos do mesmo fornecedor, para a mesma filial, no mesmo dia (atendendo à restrição R6).
  * **Custo de Ruptura (R1):** Multa operacional de R$ 50,00 por unidade de produto em falta na prateleira. Adicionalmente, aplica-se uma penalidade restritiva de **R$ 10.000,00** por ocorrência diária de estoque negativo.
  * **Custo de Excesso:** Custo de R$ 2,00 por unidade que exceder a margem de 10 dias de demanda ao final da semana.
  * **Capacidade Violada (R2):** Multa de R$ 100,00 por unidade física que ultrapasse o limite do armazém da filial.
  * **Dia Inválido (R3):** Multa de R$ 5.000,00 se houver pedido agendado fora dos dias de recebimento da filial.
  * **Pedido Mínimo (R4) e Validade (R5):** Multa de R$ 2.000,00 por ocorrência de desrespeito às regras do fornecedor ou ao tempo de prateleira (limite de 14 dias de demanda).
  * **Estoque de Segurança (R7):** Multa de R$ 1.000,00 caso o estoque ultrapasse 20 dias de demanda.
* **Justificativa dos Pesos:** As penalidades possuem valores deliberadamente desproporcionais aos custos de operação (na casa dos milhares). Essa abordagem de "Muralha de Penalidades" força o AG a priorizar o descarte rápido de soluções infactíveis (como entregar em dias fechados ou causar desabastecimento), focando a otimização apenas no espaço de soluções válidas do problema.

## 3. Operadores
* **Seleção:** Foi adotado o **Torneio** (com tamanho `k = 3`). O torneio é computacionalmente rápido e mantém uma pressão seletiva adequada, evitando que indivíduos razoavelmente bons dominem a população de forma prematura (o que aconteceria frequentemente na seleção por Roleta neste problema de custos altos).
* **Crossover:** Implementado um **Crossover de Ponto Único Adaptado**. Em vez de cortar o cromossomo linearmente (o que destruiria a coerência entre filiais e produtos), o corte é feito individualmente na semana (vetor de 7 dias) de cada produto. O ponto de corte é sorteado (entre terça e sábado), garantindo que os filhos herdem estratégias válidas de início e fim de semana de seus pais.
* **Mutação:** A mutação atua de forma heurística para tentar reparar restrições. Ao rolar a probabilidade de mutação em um gene, o operador sorteia equiprovavelmente entre três ações:
  1. **Zerar o pedido:** Ajuda a eliminar excessos de estoque e economizar fretes desnecessários.
  2. **Mudar a quantidade:** Sorteia um novo valor respeitando o limite mínimo do fornecedor (R4).
  3. **Deslocar a entrega:** Move uma carga programada para outro dia válido daquela filial específica, auxiliando ativamente na reparação da restrição R3 (Dias de entrega permitidos).

## 4. Inicialização
Para contornar o amplo espaço de busca que geraria indivíduos 100% infactíveis em uma inicialização aleatória pura, adotou-se uma **Heurística Gulosa de Simulação**.
* **Estratégia:** O algoritmo projeta o consumo diário subtraindo a demanda do estoque inicial. Assim que detecta que o estoque ficará insuficiente para o dia seguinte, ele retrocede até o dia de entrega permitido da filial mais próximo e aloca um pedido de lote mínimo (ou equivalente a 4 dias de demanda).
* **Garantia de Restrições:** Essa inteligência na Geração 0 garante que a grande maioria da população inicial já nasça respeitando rigorosamente as restrições R1 (Sem ruptura), R3 (Dias permitidos) e R4 (Pedido mínimo), acelerando drasticamente a convergência do AG.

## 5. Critério de Parada
O AG utiliza uma **combinação** de duas condições de parada:
1. **Número máximo de gerações:** Um limite fixo configurável via linha de comando (padrão: 200 gerações) para garantir que a execução finalize em tempo hábil.
2. **Convergência por estagnação (Paciência):** O algoritmo rastreia o número de gerações consecutivas em que não há melhoria no melhor fitness global. Se o fitness estagnar por 40 gerações, assume-se que a população convergiu para um ótimo (local ou global) e a execução é encerrada antecipadamente, poupando recursos computacionais.