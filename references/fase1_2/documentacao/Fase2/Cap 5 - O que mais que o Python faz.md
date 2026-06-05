# Cap 5 - O que mais que o Python faz

## Sumário

# Cap 5 - O que mais que o Python faz

O que mais que o Python faz?

Por padrão, é neste momento queinserimos a extensão .json para diferenciaro arquivoJSON dos demais.3.3.6 JSON: Carregando dados do arquivoAgora  vamos  carregar  o  conteúdo  do  arquivo.json  em  um  objeto(ou  um dicionário)dentro do Python:PYTHON:with open("arquivo.json", "r") as file:
```python
# Lendo o arquivo .jsonpessoas_json = file.read()pessoas= json.loads(pessoas_json)Código-fonte 37-Carregando dados do arquivo JSONFonte: Elaborado pelo autor (2023)Neste caso, colocamos o conteúdo do arquivo dentro de um dicionário de nome ‘pessoas’através   do   método   ‘loads’(linha    de    comando:    pessoas    = json.loads(pessoas_json); o método loads é o complemento do dumps, ele carrega os dados gravados no arquivo e ostransporta para um objeto dentro do código Python. 3.3.7 JSON: Exibindo os dados do arquivo na telaCom  o  objeto  (pessoas_json)  e dicionário(pessoas)  carregados,  fica  fácil exibirmos  o  conteúdo  na  tela.

O  comando print(pessoas)simplesmente  exibe  de forma bruta o conteúdo do dicionário:PROMPT:Comando de prompt 15-Exibição dos dados do dicionário na telaFonte: Elaborado pelo autor (2023)Exibir  na  tela  com  a indentação,  comono  caso  da  gravação,é  indiferente, porque o usuário da aplicação não possuiautonomia para compreender o conteúdo do arquivoJSON, ainda que esteja indentado.{'pessoa1': {'nome': 'Edson', 'idade': 48, 'email': 'eds@fiap.com.br'}, 'pessoa2': {'nome': 'Jose', 'idade': 23,'email': 'jose@fiap.com.br'}, 'pessoa3': {'nome': 'Maria', 'idade': 29, 'email': 'maria@fiap.com.br'}}
O que mais que o Python faz?

Contudo,   se   quisermos   exibir   na   forma   indentada,   usamos   o   objeto pessoas_json que foi carregado pelo file.read()na linha de comando pessoas_json = file.read(), veja como ficará a apresentação:PROMPT:Comando de prompt 16-Exibição dos dados do objeto JSONFonte: Elaborado pelo autor (2023)3.3.8 JSON: Exibindo os dados formatados na telaO programador é quemdeve se preocupar com a exibição dos dados na tela.

A  partir  de  agora, utilizaremos todos  os  recursosaprendidosna  disciplinapara  dar uma melhor visualização nos dados carregados do arquivo para o console.

Lembrando  que  neste  caso  estamos utilizando o  dicionário‘pessoas’ que foi carregada do arquivo:{"pessoa1": {"nome": "Edson","idade": 48,"email": "eds@fiap.com.br"},"pessoa2": {"nome": "Jose","idade": 23,"email": "jose@fiap.com.br"},"pessoa3": {"nome": "Maria","idade": 29,"email": "maria@fiap.com.br"}}
O que mais que o Python faz?

PYTHON:# exibição apresentável para o usuáriofor k, v in pessoas.items():print(f"Registro....: {k}")for k1, v1 in v.items():print("\t" + k1 + ":" + str(v1))Código-fonte 38-Código de exibição formatada do DicionárioFonte: Elaborado pelo autor (2023)No primeiro for o krepresenta pessoa1, pessoa2, pessoa3...e vo dicionário aninhado destas pessoas.

No segundo for o v(que é um dicionário) é colocado em evidência, sendo o k1representando as chaves (keys) nome, idade e e-mail e v1os conteúdos das chaves anteriores.

Com o acréscimo deste código, a exibição será:PROMPT:Comando de prompt 17-Exibição dos dados do objeto JSON formatadoFonte: Elaborado pelo autor (2023)3.3.9 Código JSON na íntegraPara explicar o funcionamento do conteúdo JSON no Python, fragmentamos o código para um melhor entendimento.

Para contextualizar o aprendizado, segue o código na íntegra:Registro....: pessoa1nome:Edsonidade:48email:eds@fiap.com.brRegistro....: pessoa2nome:Joseidade:23email:jose@fiap.com.brRegistro....: pessoa3nome:Mariaidade:29email:maria@fiap.com.br
```

O que mais que o Python faz?

PYTHON:
```python
# MANIPULACAO DE ARQUIVOS JSON# Criando o dicionário 'pessoas'pessoas = {'pessoa1':{'nome': 'Edson','idade': 48,'email': 'eds@fiap.com.br'},'pessoa2':{'nome': 'Jose','idade': 23,'email': 'jose@fiap.com.br'},'pessoa3': {'nome': 'Maria','idade': 29,'email': 'maria@fiap.com.br'},}# Importando a biblioteca JSONimport json# Criando o objeto pessoas_jsonpessoas_json = json.dumps(pessoas, indent=4)# Exibindo o dicionário pessoasprint("Exibição do dicionário: ")print(pessoas)# Exibindo o objeto JSONprint("\nExibição do objeto JSON: ")print(pessoas_json)# Abrindo o arquivo JSON para gravaçãowith open("arquivo.json", "w+") as file:# Gravando o objeto no arquivo .jsonfile.write(pessoas_json)with open("arquivo.json", "r") as file:# Lendo o arquivo .jsonfile.seek(0)pessoas_json = file.read()pessoas = json.loads(pessoas_json)# exibição 'rústica' do dicionário pessoasprint("\nExibição bruta do dicionário: ")print(pessoas)
O que mais que o Python faz?# Exibiçãodo objeto com os dados edentadosprint("\nExibição do objeto:")print(pessoas_json)# exibição apresentável para o usuárioprint("Exibição formatada dos dados:")for k, v in pessoas.items():print(f"Registro....: {k}")for k1, v1 in v.items():print("\t" + k1 + ":" + str(v1))Código-fonte 39-Código fonte JSON na íntegraFonte: Elaborado pelo autor (2023)Agora a execução deste código:Exibição do dicionário: PROMPT:
```

O que mais que o Python faz?

Comando de prompt 18-Exibição na íntegra –parte 1/2Fonte: Elaborado pelo autor (2023){'pessoa1': {'nome': 'Edson', 'idade': 48,'email': 'eds@fiap.com.br'}, 'pessoa2': {'nome': 'Jose', 'idade': 23, 'email': 'jose@fiap.com.br'}, 'pessoa3': {'nome': 'Maria', 'idade': 29, 'email': 'maria@fiap.com.br'}}Exibição do objeto JSON: {"pessoa1": {"nome": "Edson","idade": 48,"email": "eds@fiap.com.br"},"pessoa2": {"nome": "Jose","idade": 23,"email": "jose@fiap.com.br"},"pessoa3": {"nome": "Maria","idade": 29,"email": "maria@fiap.com.br"}}Exibição bruta do dicionário: {'pessoa1': {'nome': 'Edson', 'idade': 48, 'email': 'eds@fiap.com.br'}, 'pessoa2': {'nome': 'Jose', 'idade': 23, 'email': 'jose@fiap.com.br'}, 'pessoa3': {'nome': 'Maria', 'idade': 29, 'email': 'maria@fiap.com.br'}}
O que mais que o Python faz?

Comando de prompt 19-Exibição na íntegra –parte 2/2Fonte: Elaborado pelo autor (2023)Exibição do objeto:{"pessoa1": {"nome": "Edson","idade": 48,"email": "eds@fiap.com.br"},"pessoa2": {"nome": "Jose","idade": 23,"email": "jose@fiap.com.br"},"pessoa3": {"nome": "Maria","idade": 29,"email": "maria@fiap.com.br"}}Exibição formatada dos dados:Registro....: pessoa1nome:Edsonidade:48email:eds@fiap.com.brRegistro....: pessoa2nome:Joseidade:23email:jose@fiap.com.brRegistro....: pessoa3nome:Mariaidade:29email:maria@fiap.com.br
O que mais que o Python faz?

Com  a  construção  desta  solução conseguimoscontemplaros  conteúdos: Tupla, Lista, Dicionários, arquivos texto e JSON naprática.

Todos  os  sistemas  profissionais  utilizam  algum  meio  de  gravação  de  dados, geralmente através de Sistemas gerenciadores de banco de dados, como o Oracle ou SQL Server, mas este é assunto para o próximo episódio.

Quem estuda cria asas, então voem que nos encontraremoslá em cima.

O que mais que o Python faz?## Referências

UMA  INTRODU.ÇÃO  A  ASCII  E  UNICODE.

Treina  Web. 2021.

Disponível  em: https://www.treinaweb.com.br/blog/uma-introducao-a-ascii-e-unicode.

Acesso em: 16 jan. 2024.

O que mais que o Python faz?

GLOSSÁRIOArquivo textoArquivo gravado com texto sem formatações.

Arquivo JSONTipo de arquivo facilitador para integração de dados em sistemas
