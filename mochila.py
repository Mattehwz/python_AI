import random

num_geracoes = 0
peso_max = 40
chance_mutacao = 0.1

# Definindo os novos itens da mochila com valores e pesos diferentes
itens = [
    {"nome": "Item 1", "peso": 3, "valor": 100, "quantidade_maxima": 7},
    {"nome": "Item 2", "peso": 6, "valor": 200, "quantidade_maxima": 2},
    {"nome": "Item 3", "peso": 4, "valor": 50, "quantidade_maxima": 5}
]

# Função para criar um indivíduo aleatório
def criar_individuo():
    while True:
        individuo = [random.randint(0, item["quantidade_maxima"]) for item in itens]
        peso_total = sum(item["peso"] * quantidade for item, quantidade in zip(itens, individuo))
        if peso_total <= peso_max:
            return individuo

# Criar 4 indivíduos
individuos = [criar_individuo() for _ in range(4)]

# Lista para armazenar os valores dos indivíduos
valores_individuos = []

# Loop principal
while True:
    # Exibir os indivíduos com seus valores, quantidades e peso total
    for i, individuo in enumerate(individuos, start=1):    
        num_geracoes+=1
        valor = sum(item["valor"] * quantidade for item, quantidade in zip(itens, individuo))
        peso_total = sum(item["peso"] * quantidade for item, quantidade in zip(itens, individuo))
        valores_individuos.append(valor)

    # Classificar os indivíduos com base no valor de cada um 
    individuos_classificados = sorted(individuos, key=lambda x: sum(item["valor"] * quantidade for item, quantidade in zip(itens, x)), reverse=True)

    # Separar os dois melhores e os dois piores indivíduos
    melhores = individuos_classificados[:2]
    piores = individuos_classificados[-2:]

    # Identificação dos indivíduos nos grupos
    identificacao = {tuple(individuo): f"Indivíduo {i+1}" for i, individuo in enumerate(individuos)}

    # Escolher aleatoriamente um indivíduo de cada grupo baseado em seu valor
    individuo_melhor = random.choices(melhores, weights=[sum(item["valor"] for item, quantidade in zip(itens, individuo)) for individuo in melhores])[0]
    individuo_pior = random.choices(piores, weights=[sum(item["valor"] for item, quantidade in zip(itens, individuo)) for individuo in piores])[0]

    # Encontrar a identificação de cada indivíduo escolhido
    identificacao_melhor = identificacao[tuple(individuo_melhor)]
    identificacao_pior = identificacao[tuple(individuo_pior)]

    # Fazer a troca entre um item dos dois indivíduos escolhidos
    item_troca = random.choice(range(len(itens)))
    individuo_melhor[item_troca], individuo_pior[item_troca] = individuo_pior[item_troca], individuo_melhor[item_troca]

    # Calcular o novo peso total de cada indivíduo
    peso_total_melhor = sum(item["peso"] * quantidade for item, quantidade in zip(itens, individuo_melhor))
    peso_total_pior = sum(item["peso"] * quantidade for item, quantidade in zip(itens, individuo_pior))

    # Verificar se o novo peso total excede o limite
    if peso_total_melhor > peso_max or peso_total_pior > peso_max:
        while peso_total_melhor > peso_max or peso_total_pior > peso_max:
            item_troca = random.choice(range(len(itens)))
            individuo_melhor[item_troca], individuo_pior[item_troca] = individuo_pior[item_troca], individuo_melhor[item_troca]
            peso_total_melhor = sum(item["peso"] * quantidade for item, quantidade in zip(itens, individuo_melhor))
            peso_total_pior = sum(item["peso"] * quantidade for item, quantidade in zip(itens, individuo_pior))

    # Função para realizar a mutação em um indivíduo
    def mutacao(individuo):
        for i in range(len(itens)):
            if random.random() < chance_mutacao:
                novo_valor = random.randint(0, itens[i]["quantidade_maxima"])
                individuo[i] = novo_valor
        peso_total = sum(item["peso"] * quantidade for item, quantidade in zip(itens, individuo))
         # Verificar se o peso total excede o limite
        if peso_total > peso_max: 
            # Se exceder, realizar outra mutação
            mutacao(individuo)  


    # Aplicar a mutação em um dos indivíduos
    mutacao(random.choice([individuo_melhor, individuo_pior]))

    # Identificar o indivíduo escolhido após a mutação
    individuo_mutado = individuo_melhor if individuo_melhor != individuo_pior else individuo_pior
    identificacao_mutado = identificacao_melhor if individuo_melhor != individuo_pior else identificacao_pior

    # Verificar se os 200 maiores valores são iguais
    lista_maiores = sorted(valores_individuos, reverse=True)[:200]
    if len(set(lista_maiores)) == 1:
        print("Valor do maior indivíduo:", lista_maiores[0])
        maior_valor = max(individuos, key=lambda x: sum(item["valor"] * quantidade for item, quantidade in zip(itens, x)))
        print("Itens do maior indivíduo:", maior_valor)
        print("Número total de gerações:",num_geracoes)
        break
