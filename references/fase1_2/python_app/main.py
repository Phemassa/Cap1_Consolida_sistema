import csv
import os

def carregar_csv_banana():
    if os.path.exists('banana.csv'):
        with open('banana.csv', newline='', encoding='utf-8') as f:
            reader = csv.DictReader(f)
            return [
                {k: float(v) if k in ['comprimento','largura','qtd_insumo','area'] and v != '' else (None if v == '' else v) for k, v in row.items()}
                for row in reader
            ]
    return []

def carregar_csv_milho():
    if os.path.exists('milho.csv'):
        with open('milho.csv', newline='', encoding='utf-8') as f:
            reader = csv.DictReader(f)
            return [
                {k: float(v) if k in ['raio','comprimento','largura','qtd_insumo','area'] and v != '' else (None if v == '' else v) for k, v in row.items()}
                for row in reader
            ]
    return []

dados_banana = carregar_csv_banana()
dados_milho = carregar_csv_milho()


# Função para gerar exemplos e salvar nos CSV
import random
def gerar_exemplos():
    figuras = ['1', '2', '3']
    insumos = ["Fosfato", "Nitrogênio", "Potássio", "Pulverizar 500 mL/metro", "Herbicida", "Inseticida"]
    unidades = ["mL", "L", "kg", "g"]
    banana = []
    milho = []
    for i in range(20):
        figura = random.choice(figuras)
        insumo = random.choice(insumos)
        unidade = random.choice(unidades)
        if figura == '1':
            comprimento = random.randint(5, 50)
            largura = random.randint(5, 50)
            area = comprimento * largura
            raio = None
        elif figura == '2':
            comprimento = random.randint(5, 50)
            largura = random.randint(5, 50)
            area = (comprimento * largura) / 2
            raio = None
        else:
            raio = random.randint(3, 25)
            area = 3.1416 * raio ** 2
            comprimento = raio * 2
            largura = raio * 2
        qtd_insumo = round(random.uniform(10, 500), 2)
        banana.append({'comprimento': comprimento, 'largura': largura, 'insumo': insumo, 'qtd_insumo': qtd_insumo, 'unidade': unidade, 'area': area, 'figura': figura})
    for i in range(20):
        figura = random.choice(figuras)
        insumo = random.choice(insumos)
        unidade = random.choice(unidades)
        if figura == '1':
            comprimento = random.randint(5, 50)
            largura = random.randint(5, 50)
            area = comprimento * largura
            raio = None
        elif figura == '2':
            comprimento = random.randint(5, 50)
            largura = random.randint(5, 50)
            area = (comprimento * largura) / 2
            raio = None
        else:
            raio = random.randint(3, 25)
            area = 3.1416 * raio ** 2
            comprimento = raio * 2
            largura = raio * 2
        qtd_insumo = round(random.uniform(10, 500), 2)
        milho.append({'raio': raio, 'comprimento': comprimento, 'largura': largura, 'insumo': insumo, 'qtd_insumo': qtd_insumo, 'unidade': unidade, 'area': area, 'figura': figura})
    # Salvar nos CSV
    with open('banana.csv', 'w', newline='', encoding='utf-8') as f:
        writer = csv.DictWriter(f, fieldnames=banana[0].keys())
        writer.writeheader()
        writer.writerows(banana)
    with open('milho.csv', 'w', newline='', encoding='utf-8') as f:
        writer = csv.DictWriter(f, fieldnames=milho[0].keys())
        writer.writeheader()
        writer.writerows(milho)
    print('20 exemplos de cada cultura gerados e salvos nos CSV.')
# Aplicação FarmTech Solutions
# Suporte a duas culturas: Soja (retângulo) e Milho (círculo)

culturas = ['Banana', 'Milho']
dados_banana = []  # Cada item: {'comprimento': x, 'largura': y, 'insumo': z, 'qtd_insumo': w}
dados_milho = []   # Cada item: {'raio': r, 'insumo': z, 'qtd_insumo': w}


def menu():
    print("\n--- Menu FarmTech Solutions ---")
    print("1. Entrada de dados")
    print("2. Saída de dados")
    print("3. Atualizar dados")
    print("4. Deletar dados")
    print("5. Exportar dados para CSV")
    print("6. Sair")
    return input("Escolha uma opção: ")
# Função para exportar dados para CSV
import csv

def exportar_csv():
    # Exporta dados_banana
    if dados_banana:
        with open('banana.csv', 'w', newline='', encoding='utf-8') as f:
            writer = csv.DictWriter(f, fieldnames=['comprimento', 'largura', 'insumo', 'qtd_insumo'])
            writer.writeheader()
            writer.writerows(dados_banana)
        print('Dados de Banana exportados para banana.csv')
    else:
        print('Nenhum dado de Banana para exportar.')
    # Exporta dados_milho
    if dados_milho:
        with open('milho.csv', 'w', newline='', encoding='utf-8') as f:
            writer = csv.DictWriter(f, fieldnames=['raio', 'insumo', 'qtd_insumo'])
            writer.writeheader()
            writer.writerows(dados_milho)
        print('Dados de Milho exportados para milho.csv')
    else:
        print('Nenhum dado de Milho para exportar.')


def entrada_dados():
    print("\nEscolha a cultura:")
    print("1. Banana")
    print("2. Milho")
    op = input("Opção: ")
    def parse_float(text):
        import re
        match = re.search(r"[\d,.]+", text)
        if match:
            return float(match.group(0).replace(",", "."))
        else:
            raise ValueError("Valor numérico inválido!")
    print("\nEscolha a figura geométrica para o cálculo da área:")
    print("1. Retângulo")
    print("2. Triângulo")
    print("3. Círculo")
    figura = input("Opção: ")
    # Menu de insumos
    insumos_exemplo = [
        "Fosfato",
        "Nitrogênio",
        "Potássio",
        "Pulverizar 500 mL/metro",
        "Herbicida",
        "Inseticida",
        "Outro (digite manualmente)"
    ]
    print("\nEscolha o insumo:")
    for idx, nome in enumerate(insumos_exemplo, 1):
        print(f"{idx}. {nome}")
    escolha_insumo = input("Opção: ")
    if escolha_insumo.isdigit() and 1 <= int(escolha_insumo) <= len(insumos_exemplo):
        if int(escolha_insumo) == len(insumos_exemplo):
            insumo = input("Digite o nome do insumo: ")
        else:
            insumo = insumos_exemplo[int(escolha_insumo)-1]
    else:
        print("Opção de insumo inválida.")
        return
    if op == '1':
        if figura == '1':
            comprimento = parse_float(input("Comprimento do terreno (m): "))
            largura = parse_float(input("Largura do terreno (m): "))
            area = comprimento * largura
        elif figura == '2':
            base = parse_float(input("Base do terreno (m): "))
            altura = parse_float(input("Altura do terreno (m): "))
            area = (base * altura) / 2
            comprimento = base
            largura = altura
        elif figura == '3':
            raio = parse_float(input("Raio do terreno (m): "))
            area = 3.1416 * raio ** 2
            comprimento = raio * 2
            largura = raio * 2
        else:
            print("Opção de figura inválida.")
            return
        print("\nEscolha a unidade de medida da quantidade de insumo:")
        unidades = ["mL", "L", "kg", "g", "Outro (digite manualmente)"]
        for idx, u in enumerate(unidades, 1):
            print(f"{idx}. {u}")
        escolha_unidade = input("Opção: ")
        if escolha_unidade.isdigit() and 1 <= int(escolha_unidade) <= len(unidades):
            if int(escolha_unidade) == len(unidades):
                unidade = input("Digite a unidade: ")
            else:
                unidade = unidades[int(escolha_unidade)-1]
        else:
            print("Opção de unidade inválida.")
            return
        qtd = parse_float(input(f"Quantidade de insumo por metro quadrado ({unidade}): "))
        dados_banana.append({'comprimento': comprimento, 'largura': largura, 'insumo': insumo, 'qtd_insumo': qtd, 'unidade': unidade, 'area': area, 'figura': figura})
    elif op == '2':
        if figura == '1':
            comprimento = parse_float(input("Comprimento do terreno (m): "))
            largura = parse_float(input("Largura do terreno (m): "))
            area = comprimento * largura
            raio = None
        elif figura == '2':
            base = parse_float(input("Base do terreno (m): "))
            altura = parse_float(input("Altura do terreno (m): "))
            area = (base * altura) / 2
            comprimento = base
            largura = altura
            raio = None
        elif figura == '3':
            raio = parse_float(input("Raio do terreno (m): "))
            area = 3.1416 * raio ** 2
            comprimento = raio * 2
            largura = raio * 2
        else:
            print("Opção de figura inválida.")
            return
        print("\nEscolha a unidade de medida da quantidade de insumo:")
        unidades = ["mL", "L", "kg", "g", "Outro (digite manualmente)"]
        for idx, u in enumerate(unidades, 1):
            print(f"{idx}. {u}")
        escolha_unidade = input("Opção: ")
        if escolha_unidade.isdigit() and 1 <= int(escolha_unidade) <= len(unidades):
            if int(escolha_unidade) == len(unidades):
                unidade = input("Digite a unidade: ")
            else:
                unidade = unidades[int(escolha_unidade)-1]
        else:
            print("Opção de unidade inválida.")
            return
        qtd = parse_float(input(f"Quantidade de insumo por metro quadrado ({unidade}): "))
        dados_milho.append({'raio': raio, 'comprimento': comprimento, 'largura': largura, 'insumo': insumo, 'qtd_insumo': qtd, 'unidade': unidade, 'area': area, 'figura': figura})
    else:
        print("Opção inválida.")

def saida_dados():
    print("\n--- Dados Banana ---")
    for i, d in enumerate(dados_banana):
        total_insumo = d['area'] * d['qtd_insumo']
        figuras = {'1': 'Retângulo', '2': 'Triângulo', '3': 'Círculo'}
        print(f"[{i}] Figura: {figuras.get(d['figura'], 'N/A')} | Área: {d['area']:.2f} m² | Insumo: {d['insumo']} | Unidade: {d['unidade']} | Total: {total_insumo:.2f} {d['unidade']}")
    print("\n--- Dados Milho ---")
    for i, d in enumerate(dados_milho):
        total_insumo = d['area'] * d['qtd_insumo']
        figuras = {'1': 'Retângulo', '2': 'Triângulo', '3': 'Círculo'}
        print(f"[{i}] Figura: {figuras.get(d['figura'], 'N/A')} | Área: {d['area']:.2f} m² | Insumo: {d['insumo']} | Unidade: {d['unidade']} | Total: {total_insumo:.2f} {d['unidade']}")

def atualizar_dados():
    print("\nAtualizar dados de qual cultura?")
    print("1. Banana")
    print("2. Milho")
    op = input("Opção: ")
    if op == '1' and dados_banana:
        idx = int(input(f"Índice (0 a {len(dados_banana)-1}): "))
        if 0 <= idx < len(dados_banana):
            print("\nAtualizando Banana:")
            print("Escolha a figura geométrica para o cálculo da área:")
            print("1. Retângulo")
            print("2. Triângulo")
            print("3. Círculo")
            figura = input("Opção: ")
            insumos_exemplo = [
                "Fosfato",
                "Nitrogênio",
                "Potássio",
                "Pulverizar 500 mL/metro",
                "Herbicida",
                "Inseticida",
                "Outro (digite manualmente)"
            ]
            print("\nEscolha o insumo:")
            for i, nome in enumerate(insumos_exemplo, 1):
                print(f"{i}. {nome}")
            escolha_insumo = input("Opção: ")
            if escolha_insumo.isdigit() and 1 <= int(escolha_insumo) <= len(insumos_exemplo):
                if int(escolha_insumo) == len(insumos_exemplo):
                    insumo = input("Digite o nome do insumo: ")
                else:
                    insumo = insumos_exemplo[int(escolha_insumo)-1]
            else:
                print("Opção de insumo inválida.")
                return
            if figura == '1':
                comprimento = float(input("Novo comprimento: "))
                largura = float(input("Nova largura: "))
                area = comprimento * largura
            elif figura == '2':
                base = float(input("Nova base: "))
                altura = float(input("Nova altura: "))
                area = (base * altura) / 2
                comprimento = base
                largura = altura
            elif figura == '3':
                raio = float(input("Novo raio: "))
                area = 3.1416 * raio ** 2
                comprimento = raio * 2
                largura = raio * 2
            else:
                print("Opção de figura inválida.")
                return
            print("\nEscolha a unidade de medida da quantidade de insumo:")
            unidades = ["mL", "L", "kg", "g", "Outro (digite manualmente)"]
            for i, u in enumerate(unidades, 1):
                print(f"{i}. {u}")
            escolha_unidade = input("Opção: ")
            if escolha_unidade.isdigit() and 1 <= int(escolha_unidade) <= len(unidades):
                if int(escolha_unidade) == len(unidades):
                    unidade = input("Digite a unidade: ")
                else:
                    unidade = unidades[int(escolha_unidade)-1]
            else:
                print("Opção de unidade inválida.")
                return
            qtd = float(input(f"Nova quantidade de insumo por metro quadrado ({unidade}): "))
            dados_banana[idx] = {'comprimento': comprimento, 'largura': largura, 'insumo': insumo, 'qtd_insumo': qtd, 'unidade': unidade, 'area': area, 'figura': figura}
    elif op == '2' and dados_milho:
        idx = int(input(f"Índice (0 a {len(dados_milho)-1}): "))
        if 0 <= idx < len(dados_milho):
            print("\nAtualizando Milho:")
            print("Escolha a figura geométrica para o cálculo da área:")
            print("1. Retângulo")
            print("2. Triângulo")
            print("3. Círculo")
            figura = input("Opção: ")
            insumos_exemplo = [
                "Fosfato",
                "Nitrogênio",
                "Potássio",
                "Pulverizar 500 mL/metro",
                "Herbicida",
                "Inseticida",
                "Outro (digite manualmente)"
            ]
            print("\nEscolha o insumo:")
            for i, nome in enumerate(insumos_exemplo, 1):
                print(f"{i}. {nome}")
            escolha_insumo = input("Opção: ")
            if escolha_insumo.isdigit() and 1 <= int(escolha_insumo) <= len(insumos_exemplo):
                if int(escolha_insumo) == len(insumos_exemplo):
                    insumo = input("Digite o nome do insumo: ")
                else:
                    insumo = insumos_exemplo[int(escolha_insumo)-1]
            else:
                print("Opção de insumo inválida.")
                return
            if figura == '1':
                comprimento = float(input("Novo comprimento: "))
                largura = float(input("Nova largura: "))
                area = comprimento * largura
                raio = None
            elif figura == '2':
                base = float(input("Nova base: "))
                altura = float(input("Nova altura: "))
                area = (base * altura) / 2
                comprimento = base
                largura = altura
                raio = None
            elif figura == '3':
                raio = float(input("Novo raio: "))
                area = 3.1416 * raio ** 2
                comprimento = raio * 2
                largura = raio * 2
            else:
                print("Opção de figura inválida.")
                return
            print("\nEscolha a unidade de medida da quantidade de insumo:")
            unidades = ["mL", "L", "kg", "g", "Outro (digite manualmente)"]
            for i, u in enumerate(unidades, 1):
                print(f"{i}. {u}")
            escolha_unidade = input("Opção: ")
            if escolha_unidade.isdigit() and 1 <= int(escolha_unidade) <= len(unidades):
                if int(escolha_unidade) == len(unidades):
                    unidade = input("Digite a unidade: ")
                else:
                    unidade = unidades[int(escolha_unidade)-1]
            else:
                print("Opção de unidade inválida.")
                return
            qtd = float(input(f"Nova quantidade de insumo por metro quadrado ({unidade}): "))
            dados_milho[idx] = {'raio': raio, 'comprimento': comprimento, 'largura': largura, 'insumo': insumo, 'qtd_insumo': qtd, 'unidade': unidade, 'area': area, 'figura': figura}
    else:
        print("Opção inválida ou sem dados.")

def deletar_dados():
    print("\nDeletar dados de qual cultura?")
    print("1. Banana")
    print("2. Milho")
    op = input("Opção: ")
    if op == '1' and dados_banana:
        idx = int(input(f"Índice (0 a {len(dados_banana)-1}): "))
        if 0 <= idx < len(dados_banana):
            dados_banana.pop(idx)
    elif op == '2' and dados_milho:
        idx = int(input(f"Índice (0 a {len(dados_milho)-1}): "))
        if 0 <= idx < len(dados_milho):
            dados_milho.pop(idx)
    else:
        print("Opção inválida ou sem dados.")

# Loop principal
while True:
    op = menu()
    if op == '1':
        entrada_dados()
    elif op == '2':
        saida_dados()
    elif op == '3':
        atualizar_dados()
    elif op == '4':
        deletar_dados()
    elif op == '5':
        exportar_csv()
    elif op == '6':
        print("Saindo...")
        break
    else:
        print("Opção inválida.")
