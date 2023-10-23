import json
import requests

def get_file_name():
    file_name = f"Database.json"
    return file_name

def get_json():
    file_name = get_file_name()
    try:
        with open(file_name, "r") as file:
            database = json.load(file)
    except FileNotFoundError:
        database = {"Clientes": [], "Sabores": []}
        with open(file_name, "w+") as file:
            json.dump(database, file, indent=2)
    return database

def save_json(data):
    with open(get_file_name(), 'w') as file:
        json.dump(data, file, indent=2)

def add_flavor():
    database = get_json()
    while True:
        flavor = input("Digite o sabor a ser adicionado: ")

        check_flavor = input(f"{flavor} está correto? S/N: ").lower()
        if check_flavor == "s":
            for flavors in database["Sabores"]:
                if flavor in flavors["Sabor"]:
                    print("Sabor já existe no Banco de Dados.")
                    change_price = input(f"Deseja alterar o valor({flavors['Preco']})? S/N: ").lower()
                    if change_price == "s":
                        price = str(input(f"Informe um novo valor para {flavor} (ex: 12,34): "))
                        flavors["Preco"] = f"R${price}"
                        print(f"Valor da {flavor} alterado para {flavors['Preco']}")
                        break
                else:
                    new_flavor = get_price(flavor)
                    database["Sabores"].append(new_flavor)
                    print(f"{new_flavor['Sabor']} adicionado ao banco de dados.")
                    break
            break 

    save_json(database)

def get_price(flavor):
    price = str(input(f"Informe um valor para {flavor} (ex: 12,34): "))
    check_price = input(f"{flavor} : R${price} está correto? S/N: ").lower()

    if check_price == "s":
        new_flavor = {
            "Sabor": flavor,
            "Preco": f"R${price}"
            }
    else:
        price = str(input(f"Digite o valor do(a) {flavor}: "))
        new_flavor = {
            "Sabor": flavor,
            "Preco": f"R${price}"
            }
    return new_flavor

def remove_flavor():
    database = get_json()

    if len(database["Sabores"]) == 0:
        print("Não ha sabores para remover.")
        return
    
    for index, flavors in enumerate(database["Sabores"], 1):
        print(f"{index} - {flavors['Sabor']}")
    print("")

    indice = int(input("Digite o indice do sabor que deseja remover: "))
    
    flavor_name = database["Sabores"][indice-1]
    database["Sabores"].pop(indice-1)

    save_json(database)

    print (f"\n{flavor_name['Sabor']} removido.")

def get_address():
    cep = input("Digite o CEP do cliente: ")
    url = f"https://www.cepaberto.com/api/v3/cep?cep={cep}"
    headers = {"Authorization": "Token token=6d14a2cd9f82e0d7a84613439858a646"}

    try:
        response = requests.get(url, headers=headers)
        road = response.json()["logradouro"]
        district = response.json()["bairro"]
    except:
        print("Não foi possível encontrar o endereço pelo CEP.")
        road = input("Digite a rua do cliente: ")
        district = input("Digite o bairro do cliente: ")

    house_number = input("Digite o número da residência: ")
    complement = input("Digite o complemento do cliente: ")
    address = f"{road}, {district} - {house_number} ({complement}), {cep}"
    return address

def get_phone():
    ddd = input("Digite o DDD do cliente: ")
    phone_number = input("Digite o numero do cliente (sem caracteres especiais): ")
    phone = f"+55 ({ddd}) {phone_number[:5]}-{phone_number[5:9]}"
    check_phone = input(f"{phone} está correto? S/N: ").lower()
    if (check_phone == "s"):
        pass
    else:
        phone_number = input("Digite o numero do cliente (sem caracteres especiais): ")
        phone = f"+55 ({ddd}) {phone_number[:5]}-{phone_number[5:9]}"
    return phone

def get_client():
    database = get_json()
    client_name = input("Digite o nome e sobrenome do cliente: ")
    client_registered = False

    for clients in database["Clientes"]:
        if client_name in clients["Nome"]:
            print("Cliente já cadastrado.")                   
            client_registered = True
            change_data = input("Deseja alterar os dados do cliente? S/N: ").lower()
            if change_data == "s":
                database["Clientes"].remove(clients)
                client_registered = False
            break
    
    if not client_registered:
        address = get_address()
        phone = get_phone()
        cpf = input("Digite o CPF do cliente: ")
        new_client = {
            'Nome': client_name,
            'Endereco': address,
            'Telefone': phone,
            'CPF': f"{cpf[:3]}.{cpf[3:6]}.{cpf[6:9]}-{cpf[9:11]}"
        }
    
    return new_client

def add_client():
    database = get_json()
    
    new_client = get_client()
    database["Clientes"].append(new_client)

    save_json(database)

    print(f"\nCliente {new_client['Nome']} adicionado ao banco de dados")

def remove_client():
    database = get_json()

    if len(database["Clientes"]) == 0:
            print("Não há clientes para remover.")
            return
    
    for index, clients in enumerate(database["Clientes"], 1):
        print(f"{index} - Nome: {clients['Nome']}")
    print("")
    try:
        indice = int(input("Digite o indice do cliente que deseja remover: \n"))
    except:
        print("Erro")
        return
    
    client_name = database["Clientes"][indice-1]
    database["Clientes"].pop(indice-1)

    save_json(database)
    
    print(f"\n{client_name['Nome']} removido.")

def main():
    while True:
        print("\nEscolha uma ação:")
        print("1. Adicionar sabor")
        print("2. Remover sabor")
        print("3. Adicionar cliente")
        print("4. Remover Cliente")
        print("5. Sair")
        
        choice = input("Digite o número da ação desejada: ")
        print("")
        
        if choice == "1":
            add_flavor()
        elif choice == "2":
            remove_flavor()
        elif choice == "3":
            add_client()
        elif choice == "4":
            remove_client()
        elif choice == "5":
            break
        else:
            print("Opção inválida. Tente novamente.")

if __name__ == "__main__":
    main()