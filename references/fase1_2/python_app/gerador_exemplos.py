import csv
import random

# Função para gerar exemplos e salvar nos CSV

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

if __name__ == "__main__":
    gerar_exemplos()
