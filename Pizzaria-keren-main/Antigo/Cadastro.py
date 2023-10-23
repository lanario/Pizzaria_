import Main_Pizzaria
import requests

def carregar_clientes(book):
    clientes_sheet = book["clientes"]
    clientes_existentes = {}

    for linha in clientes_sheet.iter_rows(min_row=2, values_only=True):
        cliente = linha[0]
        numero = linha[1]
        cpf = linha[2]
        endereco = linha[3]
        clientes_existentes[cliente] = (numero, cpf, endereco)

    return clientes_existentes

def obter_endereco():
    resposta = input("Cliente sabe o cep? S/N")
    if (resposta.lower() == "s"):
        cep = input("Digite o cep do cliente :")
        
        url = f"https://www.cepaberto.com/api/v3/cep?cep={cep}"
        try:
            headers = {'Authorization': 'Token token=6d14a2cd9f82e0d7a84613439858a646'}
            response = requests.get(url, headers=headers)
            rua = response.json()['logradouro']
            bairro = response.json()['bairro']
            numero = input("Digite o número do endereço do cliente: ")
            complemento = input("Digite o complemento do cliente: ")
            nome_rua = f'{rua} - {bairro}, {numero} ({complemento}) - {cep}'
            print(nome_rua)
            return nome_rua
        except:
            print("cep nao encontrado")
            pass
    else:
        return obter_endereco_sem_cep()

def obter_endereco_sem_cep():
    bairro = input("Digite o bairro do cliente :")
    rua = input("Digite a rua do cliente :")
    numero = input("Digite o número do endereço do cliente :")
    complemento = input("Digite o complemento do cliente :")
    endereco = (f'{rua} - {bairro}, {numero} ({complemento})')
    return endereco

def atualizar_cliente(cliente, clientes_existentes):
    if cliente in clientes_existentes:
        resposta = input("Deseja atualizar os dados do cliente? (S/N): ")
        if resposta.lower() == "s":
            numero_existente, cpf, endereco_existente = clientes_existentes[cliente]
            novo_numero = int(input("Digite o novo número do cliente: "))
            novo_endereco = obter_endereco()
            clientes_existentes[cliente] = (novo_numero, cpf, novo_endereco)
    else:
        numero = int(input("Digite o número do cliente: "))
        cpf = input("Digite o CPF do cliente: ")
        endereco = obter_endereco()
        clientes_existentes[cliente] = (numero, cpf, endereco)

def atualizar_planilha_clientes(book, clientes_existentes):
    clientes_sheet = book["clientes"]
    clientes_sheet.delete_rows(2, clientes_sheet.max_row)

    linha_atual = 2
    for cliente, dados in clientes_existentes.items():
        numero, cpf, endereco = dados
        clientes_sheet[f"A{linha_atual}"] = cliente
        clientes_sheet[f"B{linha_atual}"] = numero
        clientes_sheet[f"C{linha_atual}"] = cpf
        clientes_sheet[f"D{linha_atual}"] = endereco
        linha_atual += 1

    book.save(Main_Pizzaria.get_nome_arquivo())

def get_nome_cliente():
    book = Main_Pizzaria.carregar_planilha(Main_Pizzaria.get_nome_arquivo())
    clientes_existentes = carregar_clientes(book)

    while True:
        cliente = input("Digite o nome do cliente (ou digite 'sair' para sair): ")
        if cliente.lower() == "sair":
            break

        atualizar_cliente(cliente, clientes_existentes)

    atualizar_planilha_clientes(book, clientes_existentes)
