import random
import copy
import argparse

# ==========================================
# 1. BASE DE DADOS (Tabelas do Problema)
# ==========================================

FILIAIS = {
    'F1': {'capacidade': 2000, 'dias_entrega': [0, 2, 4]}, # Seg, Qua, Sex
    'F2': {'capacidade': 1500, 'dias_entrega': [1, 3, 5]}, # Ter, Qui, Sab
    'F3': {'capacidade': 1800, 'dias_entrega': [0, 2, 4]}, # Seg, Qua, Sex
    'F4': {'capacidade': 1200, 'dias_entrega': [1, 3, 6]}  # Ter, Qui, Dom
}

PRODUTOS = {
    'PR01': {'nome': 'Arroz 5kg',       'val': 180, 'forn': 'FO1', 'min': 50,  'custo': 18.00, 'frete': 35.00},
    'PR02': {'nome': 'Feijão 1kg',      'val': 120, 'forn': 'FO1', 'min': 30,  'custo': 7.50,  'frete': 35.00},
    'PR03': {'nome': 'Óleo de soja 1L', 'val': 90,  'forn': 'FO2', 'min': 40,  'custo': 6.00,  'frete': 28.00},
    'PR04': {'nome': 'Açúcar 1kg',      'val': 180, 'forn': 'FO1', 'min': 60,  'custo': 4.20,  'frete': 35.00},
    'PR05': {'nome': 'Sal 1kg',         'val': 365, 'forn': 'FO3', 'min': 20,  'custo': 1.80,  'frete': 20.00},
    'PR06': {'nome': 'Macarrão 500g',   'val': 120, 'forn': 'FO2', 'min': 30,  'custo': 3.50,  'frete': 28.00},
    'PR07': {'nome': 'Leite UHT 1L',    'val': 60,  'forn': 'FO4', 'min': 100, 'custo': 4.80,  'frete': 45.00},
    'PR08': {'nome': 'Iogurte 170g',    'val': 21,  'forn': 'FO4', 'min': 80,  'custo': 2.20,  'frete': 45.00},
    'PR09': {'nome': 'Queijo 200g',     'val': 30,  'forn': 'FO4', 'min': 40,  'custo': 9.50,  'frete': 45.00},
    'PR10': {'nome': 'Manteiga 200g',   'val': 45,  'forn': 'FO4', 'min': 30,  'custo': 8.00,  'frete': 45.00},
    'PR11': {'nome': 'Frango kg',       'val': 5,   'forn': 'FO5', 'min': 50,  'custo': 12.00, 'frete': 60.00},
    'PR12': {'nome': 'Carne bovina kg', 'val': 7,   'forn': 'FO5', 'min': 30,  'custo': 38.00, 'frete': 60.00},
    'PR13': {'nome': 'Pão de forma',    'val': 7,   'forn': 'FO5', 'min': 40,  'custo': 5.50,  'frete': 60.00},
    'PR14': {'nome': 'Biscoito 200g',   'val': 90,  'forn': 'FO2', 'min': 50,  'custo': 2.80,  'frete': 28.00},
    'PR15': {'nome': 'Café 250g',       'val': 180, 'forn': 'FO1', 'min': 40,  'custo': 9.00,  'frete': 35.00},
    'PR16': {'nome': 'Sabão em pó 1kg', 'val': 365, 'forn': 'FO3', 'min': 30,  'custo': 7.20,  'frete': 20.00},
    'PR17': {'nome': 'Detergente 500ml','val': 365, 'forn': 'FO3', 'min': 50,  'custo': 2.50,  'frete': 20.00},
    'PR18': {'nome': 'Shampoo 350ml',   'val': 365, 'forn': 'FO3', 'min': 20,  'custo': 11.00, 'frete': 20.00},
    'PR19': {'nome': 'Papel higiênico', 'val': 365, 'forn': 'FO3', 'min': 60,  'custo': 3.80,  'frete': 20.00},
    'PR20': {'nome': 'Refrigerante 2L', 'val': 120, 'forn': 'FO2', 'min': 40,  'custo': 6.50,  'frete': 28.00}
}

ESTOQUE_INICIAL = {
    'F1': {'PR01': 120, 'PR02': 80, 'PR03': 90, 'PR04': 100, 'PR05': 60, 'PR06': 70, 'PR07': 150, 'PR08': 100, 'PR09': 60, 'PR10': 50, 'PR11': 80, 'PR12': 60, 'PR13': 70, 'PR14': 90, 'PR15': 80, 'PR16': 70, 'PR17': 100, 'PR18': 50, 'PR19': 120, 'PR20': 90},
    'F2': {'PR01': 80, 'PR02': 50, 'PR03': 60, 'PR04': 70, 'PR05': 40, 'PR06': 45, 'PR07': 100, 'PR08': 65, 'PR09': 40, 'PR10': 30, 'PR11': 50, 'PR12': 40, 'PR13': 45, 'PR14': 60, 'PR15': 50, 'PR16': 45, 'PR17': 65, 'PR18': 30, 'PR19': 80, 'PR20': 60},
    'F3': {'PR01': 100, 'PR02': 70, 'PR03': 80, 'PR04': 90, 'PR05': 50, 'PR06': 60, 'PR07': 130, 'PR08': 85, 'PR09': 50, 'PR10': 40, 'PR11': 70, 'PR12': 50, 'PR13': 60, 'PR14': 75, 'PR15': 65, 'PR16': 55, 'PR17': 85, 'PR18': 40, 'PR19': 100, 'PR20': 75},
    'F4': {'PR01': 60, 'PR02': 40, 'PR03': 50, 'PR04': 55, 'PR05': 30, 'PR06': 35, 'PR07': 80, 'PR08': 50, 'PR09': 30, 'PR10': 25, 'PR11': 40, 'PR12': 30, 'PR13': 35, 'PR14': 45, 'PR15': 40, 'PR16': 35, 'PR17': 50, 'PR18': 25, 'PR19': 60, 'PR20': 45}
}

DEMANDA_DIARIA = {
    'F1': {'PR01': 25, 'PR02': 15, 'PR03': 20, 'PR04': 18, 'PR05': 8, 'PR06': 14, 'PR07': 35, 'PR08': 22, 'PR09': 12, 'PR10': 10, 'PR11': 20, 'PR12': 15, 'PR13': 18, 'PR14': 16, 'PR15': 14, 'PR16': 10, 'PR17': 15, 'PR18': 8, 'PR19': 20, 'PR20': 18},
    'F2': {'PR01': 18, 'PR02': 10, 'PR03': 14, 'PR04': 12, 'PR05': 5, 'PR06': 9, 'PR07': 24, 'PR08': 14, 'PR09': 8, 'PR10': 6, 'PR11': 13, 'PR12': 10, 'PR13': 11, 'PR14': 10, 'PR15': 9, 'PR16': 6, 'PR17': 10, 'PR18': 5, 'PR19': 13, 'PR20': 12},
    'F3': {'PR01': 22, 'PR02': 13, 'PR03': 17, 'PR04': 16, 'PR05': 7, 'PR06': 12, 'PR07': 30, 'PR08': 18, 'PR09': 10, 'PR10': 8, 'PR11': 17, 'PR12': 12, 'PR13': 15, 'PR14': 13, 'PR15': 11, 'PR16': 8, 'PR17': 13, 'PR18': 6, 'PR19': 17, 'PR20': 15},
    'F4': {'PR01': 14, 'PR02': 8, 'PR03': 11, 'PR04': 10, 'PR05': 4, 'PR06': 7, 'PR07': 18, 'PR08': 11, 'PR09': 6, 'PR10': 5, 'PR11': 10, 'PR12': 7, 'PR13': 9, 'PR14': 8, 'PR15': 7, 'PR16': 5, 'PR17': 8, 'PR18': 4, 'PR19': 10, 'PR20': 9}
}

# ==========================================
# 2. FUNÇÃO DE CRIAÇÃO DO INDIVÍDUO
# ==========================================

def criar_individuo():
    individuo = {}
    for f, info_filial in FILIAIS.items():
        individuo[f] = {}
        dias_permitidos = info_filial['dias_entrega']
        for p, info_prod in PRODUTOS.items():
            plano_semanal = [0, 0, 0, 0, 0, 0, 0]
            estoque_atual = ESTOQUE_INICIAL[f][p]
            demanda = DEMANDA_DIARIA[f][p]
            
            for dia in range(7):
                if estoque_atual <= demanda:
                    dia_pedido = dia
                    while dia_pedido not in dias_permitidos and dia_pedido >= 0:
                        dia_pedido -= 1
                    if dia_pedido < 0:
                        dia_pedido = dias_permitidos[0]
                        
                    if plano_semanal[dia_pedido] == 0:
                        qtd_pedir = max(info_prod['min'], demanda * 4)
                        plano_semanal[dia_pedido] += qtd_pedir
                        estoque_atual += qtd_pedir
                estoque_atual -= demanda
            individuo[f][p] = plano_semanal
    return individuo

# ==========================================
# 3. FUNÇÃO DE AVALIAÇÃO (FITNESS E RESTRIÇÕES)
# ==========================================

def calcular_fitness(individuo):
    custo_produtos = 0
    custo_pedidos = 0
    custo_ruptura = 0
    custo_excesso = 0
    multa_violacoes = 0
    
    for f, plano_filial in individuo.items():
        capacidade_filial = FILIAIS[f]['capacidade']
        dias_permitidos = FILIAIS[f]['dias_entrega']
        estoque_diario_filial = [0, 0, 0, 0, 0, 0, 0]
        fornecedores_por_dia = {0: [], 1: [], 2: [], 3: [], 4: [], 5: [], 6: []}
        
        for p, plano_produto in plano_filial.items():
            estoque_atual = ESTOQUE_INICIAL[f][p]
            demanda = DEMANDA_DIARIA[f][p]
            info_prod = PRODUTOS[p]
            
            limite_validade_dias = min(info_prod['val'], 14)
            quantidade_maxima_permitida = demanda * limite_validade_dias
            
            for dia in range(7):
                qtd_pedida = plano_produto[dia]
                if qtd_pedida > 0:
                    if dia not in dias_permitidos:
                        multa_violacoes += 5000 
                    if qtd_pedida < info_prod['min']:
                        multa_violacoes += 2000
                    if qtd_pedida > quantidade_maxima_permitida:
                        multa_violacoes += 2000
                        
                    fornecedor = info_prod['forn']
                    if fornecedor not in fornecedores_por_dia[dia]:
                        fornecedores_por_dia[dia].append(fornecedor)
                        
                    custo_produtos += (qtd_pedida * info_prod['custo'])
                    estoque_atual += qtd_pedida
                    
                estoque_atual -= demanda
                
                if estoque_atual < 0:
                    unidades_faltantes = abs(estoque_atual)
                    custo_ruptura += (unidades_faltantes * 50)
                    multa_violacoes += 10000 
                    estoque_atual = 0 
                    
                if estoque_atual > (20 * demanda):
                    multa_violacoes += 1000
                    
                estoque_diario_filial[dia] += estoque_atual
                
            limite_isento = 10 * demanda
            if estoque_atual > limite_isento:
                custo_excesso += (estoque_atual - limite_isento) * 2
                
        for dia in range(7):
            if estoque_diario_filial[dia] > capacidade_filial:
                excesso_fisico = estoque_diario_filial[dia] - capacidade_filial
                multa_violacoes += (excesso_fisico * 100)
                
        for dia in range(7):
            for fornecedor in fornecedores_por_dia[dia]:
                for info in PRODUTOS.values():
                    if info['forn'] == fornecedor:
                        custo_pedidos += info['frete']
                        break
                
    custo_total = custo_produtos + custo_pedidos + custo_ruptura + custo_excesso + multa_violacoes
    return -custo_total

# ==========================================
# 4. OPERADORES GENÉTICOS
# ==========================================

def selecao_torneio(populacao, fitnesses, tamanho_torneio=3):
    melhor_indice = -1
    melhor_fitness = float("-inf")
    for _ in range(tamanho_torneio):
        indice_sorteado = random.randint(0, len(populacao) - 1)
        if fitnesses[indice_sorteado] > melhor_fitness:
            melhor_fitness = fitnesses[indice_sorteado]
            melhor_indice = indice_sorteado
    return copy.deepcopy(populacao[melhor_indice])

def crossover(pai1, pai2):
    filho1 = copy.deepcopy(pai1)
    filho2 = copy.deepcopy(pai2)
    for f in FILIAIS.keys():
        for p in PRODUTOS.keys():
            ponto_corte = random.randint(1, 6)
            filho1[f][p] = pai1[f][p][:ponto_corte] + pai2[f][p][ponto_corte:]
            filho2[f][p] = pai2[f][p][:ponto_corte] + pai1[f][p][ponto_corte:]
    return filho1, filho2

def mutacao(individuo, taxa_mutacao):
    novo_individuo = copy.deepcopy(individuo)
    for f, info_filial in FILIAIS.items():
        dias_permitidos = info_filial['dias_entrega']
        for p, info_prod in PRODUTOS.items():
            for dia in range(7):
                if random.random() < taxa_mutacao:
                    tipo_mutacao = random.randint(1, 3)
                    if tipo_mutacao == 1:
                        novo_individuo[f][p][dia] = 0
                    elif tipo_mutacao == 2:
                        demanda_estimada = DEMANDA_DIARIA[f][p] * 5
                        max_pedir = max(info_prod['min'], demanda_estimada)
                        novo_individuo[f][p][dia] = random.randint(info_prod['min'], max_pedir)
                    elif tipo_mutacao == 3:
                        qtd_atual = novo_individuo[f][p][dia]
                        if qtd_atual > 0:
                            novo_dia = random.choice(dias_permitidos)
                            novo_individuo[f][p][novo_dia] += qtd_atual
                            novo_individuo[f][p][dia] = 0
    return novo_individuo

# ==========================================
# 5. MOTOR DO ALGORITMO GENÉTICO
# ==========================================

def executar_algoritmo_genetico(tamanho_populacao, geracoes, taxa_mutacao, taxa_crossover, tamanho_elite, paciencia):
    print(f"Gerando população inicial inteligente ({tamanho_populacao} indivíduos)...")
    populacao = [criar_individuo() for _ in range(tamanho_populacao)]
        
    melhor_individuo_geral = None
    melhor_fitness_geral = float("-inf")
    geracoes_sem_melhoria = 0
    
    for geracao in range(geracoes):
        fitnesses = [calcular_fitness(ind) for ind in populacao]
            
        populacao_com_notas = list(zip(populacao, fitnesses))
        populacao_com_notas.sort(key=lambda x: x[1], reverse=True)
        
        melhor_atual, nota_atual = populacao_com_notas[0]
        pior_atual = populacao_com_notas[-1][1]
        media_atual = sum(fitnesses) / len(fitnesses)
        
        if nota_atual > melhor_fitness_geral:
            melhor_fitness_geral = nota_atual
            melhor_individuo_geral = copy.deepcopy(melhor_atual)
            geracoes_sem_melhoria = 0
        else:
            geracoes_sem_melhoria += 1
            
        # Exibição do Pior, Médio e Melhor (Min, Médio, Máx - invertido porque é custo)
        if geracao % 10 == 0 or geracao == geracoes - 1:
            print(f"Geração {geracao:03d} | Pior Custo: R$ {pior_atual * -1:10,.2f} | Custo Médio: R$ {media_atual * -1:10,.2f} | Melhor Custo: R$ {nota_atual * -1:10,.2f}")
            
        if geracoes_sem_melhoria >= paciencia:
            print(f"\n-> O algoritmo convergiu (parou de melhorar) na geração {geracao}!")
            break
            
        nova_populacao = []
        for i in range(tamanho_elite):
            nova_populacao.append(copy.deepcopy(populacao_com_notas[i][0]))
            
        while len(nova_populacao) < tamanho_populacao:
            pai1 = selecao_torneio(populacao, fitnesses)
            pai2 = selecao_torneio(populacao, fitnesses)
            
            if random.random() < taxa_crossover:
                filho1, filho2 = crossover(pai1, pai2)
            else:
                filho1, filho2 = copy.deepcopy(pai1), copy.deepcopy(pai2)
            
            filho1 = mutacao(filho1, taxa_mutacao)
            filho2 = mutacao(filho2, taxa_mutacao)
            
            nova_populacao.append(filho1)
            if len(nova_populacao) < tamanho_populacao:
                nova_populacao.append(filho2)
                
        populacao = nova_populacao
        
    return melhor_individuo_geral, melhor_fitness_geral

# ==========================================
# 6. RELATÓRIO E EXECUÇÃO PRINCIPAL
# ==========================================

def detalhar_custos(individuo):
    custos = {'produtos': 0, 'pedidos': 0, 'rupturas': 0, 'excessos': 0, 'violacoes': 0}
    
    for f, plano_filial in individuo.items():
        fornecedores_por_dia = {0: [], 1: [], 2: [], 3: [], 4: [], 5: [], 6: []}
        for p, plano_produto in plano_filial.items():
            estoque_atual = ESTOQUE_INICIAL[f][p]
            demanda = DEMANDA_DIARIA[f][p]
            info_prod = PRODUTOS[p]
            
            for dia in range(7):
                qtd_pedida = plano_produto[dia]
                if qtd_pedida > 0:
                    custos['produtos'] += (qtd_pedida * info_prod['custo'])
                    estoque_atual += qtd_pedida
                    forn = info_prod['forn']
                    if forn not in fornecedores_por_dia[dia]:
                        fornecedores_por_dia[dia].append(forn)
                        
                estoque_atual -= demanda
                if estoque_atual < 0:
                    custos['rupturas'] += (abs(estoque_atual) * 50)
                    custos['violacoes'] += 1
                    estoque_atual = 0
                    
            if estoque_atual > (10 * demanda):
                custos['excessos'] += (estoque_atual - (10 * demanda)) * 2
                
        for dia in range(7):
            for fornecedor in fornecedores_por_dia[dia]:
                for info in PRODUTOS.values():
                    if info['forn'] == fornecedor:
                        custos['pedidos'] += info['frete']
                        break
    return custos

def imprimir_relatorio_final(individuo, fitness_final):
    print("\n" + "="*50)
    print(" RELATÓRIO FINAL DE REABASTECIMENTO ")
    print("="*50 + "\n")
    
    dias_nome = ["Seg", "Ter", "Qua", "Qui", "Sex", "Sáb", "Dom"]
    
    for f, plano_filial in individuo.items():
        print(f"Filial {f}:")
        entregas_no_dia = False
        for dia in range(7):
            pedidos_do_dia = []
            for p, plano_produto in plano_filial.items():
                qtd = plano_produto[dia]
                if qtd > 0:
                    pedidos_do_dia.append(f"{p} ({qtd} un.)")
            
            if pedidos_do_dia:
                entregas_no_dia = True
                print(f"  Dia {dia+1} ({dias_nome[dia]}): {', '.join(pedidos_do_dia)}")
                
        if not entregas_no_dia:
            print("  Nenhuma entrega programada para esta filial na semana.")
        print("-" * 30)
        
    custos = detalhar_custos(individuo)
    custo_total_real = custos['produtos'] + custos['pedidos'] + custos['rupturas'] + custos['excessos']
    
    print("\nCusto Total Semanal:")
    print(f"  Produtos:  R$ {custos['produtos']:10,.2f}")
    print(f"  Pedidos:   R$ {custos['pedidos']:10,.2f}")
    print(f"  Rupturas:  R$ {custos['rupturas']:10,.2f}")
    print(f"  Excessos:  R$ {custos['excessos']:10,.2f}")
    print(f"  Total:     R$ {custo_total_real:10,.2f}")
    print(f"\nValor da Função de Aptidão (Fitness): {fitness_final:,.2f}")
    print(f"Violações críticas (Rupturas registradas): {custos['violacoes']}")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="AG para Otimização de Estoque em Supermercados")
    parser.add_argument("--populacao", type=int, default=100, help="Tamanho da população")
    parser.add_argument("--geracoes", type=int, default=200, help="Número máximo de gerações")
    parser.add_argument("--mutacao", type=float, default=0.05, help="Taxa de mutação (0.0 a 1.0)")
    parser.add_argument("--crossover", type=float, default=0.85, help="Taxa de crossover (0.0 a 1.0)")
    
    args = parser.parse_args()

    print(f"=== Iniciando Otimização ===")
    print(f"População: {args.populacao} | Gerações: {args.geracoes} | Mutação: {args.mutacao} | Crossover: {args.crossover}\n")
    
    melhor_solucao, melhor_nota = executar_algoritmo_genetico(
        tamanho_populacao=args.populacao,
        geracoes=args.geracoes,
        taxa_mutacao=args.mutacao,
        taxa_crossover=args.crossover,
        tamanho_elite=4,
        paciencia=40
    )
    
    imprimir_relatorio_final(melhor_solucao, melhor_nota)