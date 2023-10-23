
import json

def ler_sabores():
    # Verifica se o arquivo do banco de dados já existe
    try:
        with open('db_Sabores.json', 'r+') as arquivo:
            banco_de_dados = json.load(arquivo)
            return banco_de_dados
    except FileNotFoundError:
        # Se o arquivo não existir, cria um novo banco de dados vazio
        banco_de_dados = []

def ler_pedidos():
    # Verifica se o arquivo do banco de dados já existe
    try:
        with open('db_Pedidos.json', 'r+') as arquivo:
            banco_de_dados = json.load(arquivo)
            return banco_de_dados
    except FileNotFoundError:
        # Se o arquivo não existir, cria um novo banco de dados vazio
        banco_de_dados = []

def adicionar_sabor():
    try:
        with open("banco_de_dados.json", "r") as arquivo:
            db = json.load(arquivo)
    except (FileNotFoundError, json.JSONDecodeError):
        db = {"Sabores": []}

    sabor = input("Digite o sabor: ")

    for item in db["Sabores"]:
        if sabor in item:
            print("Sabor já existe")
            pergunta = input("Deseja alterar o valor? S/N: ")
            if pergunta.lower() == "s":
                valor = input(f"Digite o valor do {sabor}: ")
                item[sabor] = valor
                print("Valor alterado com sucesso")
            break
    else:
        valor = input(f"Digite o valor do {sabor}: ")
        novo_sabor = {sabor: valor}
        db["Sabores"].append(novo_sabor)
        print("Sabor adicionado com sucesso")

    with open("banco_de_dados.json", "w") as arquivo:
        json.dump(db, arquivo, indent=4)

def obter_valor_sabor():
    try:
        with open("banco_de_dados.json", "r") as arquivo:
            db = json.load(arquivo)
    except (FileNotFoundError, json.JSONDecodeError):
        print("O banco de dados está vazio.")
        return

    sabor = input("Digite o sabor: ")
    for item in db["Sabores"]:
        if sabor in item:
            valor = item[sabor]
            print(f"O valor do sabor {sabor} é: {valor}")
            return

    print(f"O sabor {sabor} não foi encontrado no banco de dados.")

def criar_banco_dados_clientes():
    try:
        with open("dbPedidos.json", "r") as arquivo:
            db = json.load(arquivo)
    except (FileNotFoundError, json.JSONDecodeError):
        db = {"Clientes": []}

    while True:
        nome_cliente = input("Digite o nome do cliente (ou 'sair' para finalizar): ")
        if nome_cliente.lower() == "sair":
            break

        cliente_existente = False
        for cliente in db["Clientes"]:
            if cliente["nome"] == nome_cliente:
                cliente_existente = True
                break

        if not cliente_existente:
            cliente = {"nome": nome_cliente, "pedidos": []}
            db["Clientes"].append(cliente)
        else:
            print("Cliente já existe. Adicionando pedidos ao cliente existente.")

        while True:
            sabor_pizza = input("Digite o sabor da pizza (ou 'sair' para finalizar o cliente): ")
            if sabor_pizza.lower() == "sair":
                break

            quantidade = input("Digite a quantidade da pizza: ")

            for pedido in cliente["pedidos"]:
                if sabor_pizza in pedido:
                    pedido[sabor_pizza] = str(int(pedido[sabor_pizza]) + int(quantidade))
                    break
            else:
                pedido = {sabor_pizza: quantidade}
                cliente["pedidos"].append(pedido)

    with open("dbPedidos.json", "w") as arquivo:
        json.dump(db, arquivo, indent=4)

    print("Banco de dados de clientes atualizado com sucesso.")

criar_banco_dados_clientes()