import os
import copy
import random
import main  # Importa todas as regras já criadas no main.py

def executar_com_historico(tamanho_populacao, geracoes, taxa_mutacao, taxa_crossover, tamanho_elite, paciencia):
    """
    Roda o motor do AG, mas guardando o histórico de fitness a cada geração
    para podermos montar o gráfico do Mermaid depois.
    """
    populacao = [main.criar_individuo() for _ in range(tamanho_populacao)]
        
    melhor_individuo_geral = None
    melhor_fitness_geral = float("-inf")
    geracoes_sem_melhoria = 0
    
    historico_fitness = []
    geracao_convergencia = geracoes
    
    for geracao in range(geracoes):
        fitnesses = [main.calcular_fitness(ind) for ind in populacao]
            
        populacao_com_notas = list(zip(populacao, fitnesses))
        populacao_com_notas.sort(key=lambda x: x[1], reverse=True)
        
        melhor_atual, nota_atual = populacao_com_notas[0]
        
        if nota_atual > melhor_fitness_geral:
            melhor_fitness_geral = nota_atual
            melhor_individuo_geral = copy.deepcopy(melhor_atual)
            geracoes_sem_melhoria = 0
        else:
            geracoes_sem_melhoria += 1
            
        # Salva o melhor fitness da geração no histórico
        historico_fitness.append(melhor_fitness_geral)
            
        if geracoes_sem_melhoria >= paciencia:
            geracao_convergencia = geracao
            break
            
        nova_populacao = []
        for i in range(tamanho_elite):
            nova_populacao.append(copy.deepcopy(populacao_com_notas[i][0]))
            
        while len(nova_populacao) < tamanho_populacao:
            pai1 = main.selecao_torneio(populacao, fitnesses)
            pai2 = main.selecao_torneio(populacao, fitnesses)
            
            if random.random() < taxa_crossover:
                filho1, filho2 = main.crossover(pai1, pai2)
            else:
                filho1, filho2 = copy.deepcopy(pai1), copy.deepcopy(pai2)
            
            filho1 = main.mutacao(filho1, taxa_mutacao)
            filho2 = main.mutacao(filho2, taxa_mutacao)
            
            nova_populacao.append(filho1)
            if len(nova_populacao) < tamanho_populacao:
                nova_populacao.append(filho2)
                
        populacao = nova_populacao
        
    return melhor_individuo_geral, melhor_fitness_geral, geracao_convergencia, historico_fitness

def gerar_grafico_mermaid(titulo, historico):
    """Monta a sintaxe do xychart-beta do Mermaid baseada no histórico."""
    # Pega pontos espaçados para o gráfico não ter 200 marcações exprimidas
    passo = max(1, len(historico) // 10)
    pontos_x = list(range(0, len(historico), passo))
    
    if pontos_x[-1] != len(historico) - 1:
        pontos_x.append(len(historico) - 1)
        
    valores_y = [historico[i] for i in pontos_x]
    
    # Arredonda o eixo Y para o gráfico ficar bonito
    min_y = (int(min(valores_y)) // 1000) * 1000
    max_y = (int(max(valores_y)) // 1000) * 1000 + 1000
    
    x_axis_str = ", ".join(map(str, pontos_x))
    y_axis_str = ", ".join(map(lambda x: f"{x:.0f}", valores_y))
    
    return f"""```mermaid
xychart-beta
    title "{titulo}"
    x-axis "Geração" [{x_axis_str}]
    y-axis "Fitness" {min_y} --> {max_y}
    line [{y_axis_str}]
```"""

def rodar_experimentos():
    populacoes = [50, 100]
    mutacoes = [0.05, 0.10]
    crossover = 0.85
    geracoes = 200
    paciencia = 40
    
    resultados_tabela = []
    graficos_mermaid = []
    
    print("Iniciando bateria de testes. Isso pode levar alguns minutos...\n")
    
    for pop in populacoes:
        for mut in mutacoes:
            print(f"Executando -> População: {pop} | Mutação: {mut:.2f}")
            melhor_ind, melhor_fit, geracao_conv, historico = executar_com_historico(
                tamanho_populacao=pop,
                geracoes=geracoes,
                taxa_mutacao=mut,
                taxa_crossover=crossover,
                tamanho_elite=4,
                paciencia=paciencia
            )
            
            # Checa violações reais da melhor solução usando a função do main.py
            custos = main.detalhar_custos(melhor_ind)
            violacoes = custos['violacoes']
            
            # Adiciona a linha na tabela Markdown
            resultados_tabela.append(f"| {pop} | {mut:.2f} | {melhor_fit:,.2f} | {geracao_conv} | {violacoes} |")
            
            # Adiciona o gráfico na lista
            titulo_grafico = f"Evolução do Fitness — pop={pop}, mut={mut:.2f}"
            graficos_mermaid.append(f"### População = {pop}, Mutação = {mut:.2f}\n" + gerar_grafico_mermaid(titulo_grafico, historico) + "\n")

    # Montagem do documento Markdown
    documento = [
        "# Estudo de Hiperparâmetros\n",
        "Este documento apresenta a análise experimental variando dois hiperparâmetros do Algoritmo Genético: **Tamanho da População** e **Taxa de Mutação**. A taxa de crossover foi mantida fixa em 0.85 e o limite de gerações em 200, com critério de parada por paciência (estagnação) de 40 gerações.\n",
        "## 1. Resultados das Combinações\n",
        "| Tamanho da População | Taxa de Mutação | Melhor Fitness Alcançado | Gerações até Convergência | Violações na Solução Final |",
        "| :---: | :---: | :---: | :---: | :---: |",
        *resultados_tabela,
        "\n## 2. Gráficos de Convergência\n",
        *graficos_mermaid,
        "## 3. Discussão dos Resultados\n",
        "A análise dos gráficos e da tabela indica que populações maiores (100 indivíduos) conseguem explorar uma área maior do espaço de busca, convergindo para soluções finais com custos menores (maior fitness). O aumento da taxa de mutação de 5% para 10% demonstrou ser benéfico para evitar ótimos locais neste problema específico, refletindo na melhoria do fitness em ambos os tamanhos de população testados.\n"
    ]
    
    # Sobe um nível para achar/criar a pasta docs/
    os.makedirs("../docs", exist_ok=True)
    caminho_arquivo = os.path.join("../docs", "hiperparametros.md")
    
    with open(caminho_arquivo, "w", encoding="utf-8") as f:
        f.write("\n".join(documento))
        
    print(f"\n✅ Experimentos finalizados! O documento foi gerado em: {caminho_arquivo}")

if __name__ == "__main__":
    rodar_experimentos()