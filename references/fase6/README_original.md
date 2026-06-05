# FIAP - Faculdade de Informática e Administração Paulista

# FarmTech Solutions - Fase 6: Redes Neurais e Visao Computacional

## Grupo FlexMedia

## Integrantes

- Cesar Martinho de Azeredo - RM568140
- Carlos Alberto Florindo Costato - RM567005
- Phellype Matheus Giacoia Flaibam Massarente - RM566826

## Professores

### Tutor(a)

- Andre Godoy

### Coordenador(a)

- Ana Cristina dos Santos

---

## Descricao

Este repositorio reune a entrega da Fase 6 da FIAP para a disciplina de Redes Neurais, no contexto da FarmTech Solutions. O projeto tem como objetivo demonstrar o uso de visao computacional para identificar objetos em imagens, utilizando YOLO e abordagens comparativas de classificacao.

A base escolhida possui duas classes principais:

- **Carros**
- **Motos**

As imagens foram separadas para treino, validacao e teste, conforme solicitado no escopo da atividade.

---

## Entrega 1 - YOLO customizada

Nesta etapa, sera desenvolvido um sistema de deteccao de objetos com YOLO treinado com imagens das classes **Carros** e **Motos**.

O notebook Jupyter/Colab devera conter:

- Conexao com o Google Drive.
- Organizacao da base de imagens.
- Treinamento do modelo YOLO customizado.
- Validacao e testes do modelo.
- Comparacao entre treinamentos com quantidades diferentes de epocas.
- Prints ou resultados das imagens de teste processadas pelo modelo.
- Conclusoes sobre acuracia, erro, desempenho, pontos fortes e limitacoes.

---

## Entrega 2 - Comparacao de abordagens

Nesta etapa, a mesma base sera utilizada para comparar diferentes solucoes de visao computacional:

- YOLO customizada da Entrega 1.
- YOLO tradicional/padrao.
- CNN treinada do zero para classificacao das imagens.

A avaliacao devera comparar as abordagens em termos de:

- Facilidade de uso e integracao.
- Precisao do modelo.
- Tempo de treinamento ou customizacao.
- Tempo de inferencia.

---

## Dataset

As imagens da base foram organizadas no Google Drive, separadas por classe:

| Classe | Pasta no Google Drive |
|--------|------------------------|
| Motos | [Acessar pasta](https://drive.google.com/drive/folders/1muSD2ofgKrm_ijeSDrRdTQU02itRvgp2?usp=drive_link) |
| Carros | [Acessar pasta](https://drive.google.com/drive/folders/1EmW9hLKAH1ISMD3a4YamgiE7MxtIFdWk?usp=drive_link) |

### Rotulacoes

Os arquivos CSV presentes na raiz do projeto sao as rotulacoes exportadas do AI Sense/Make Sense IA:

- [labels_carro.csv](labels_carro.csv): rotulacoes da classe **Carros**.
- [labels_moto.csv](labels_moto.csv): rotulacoes da classe **Motos**.

Cada arquivo contem as informacoes de classe, coordenadas da bounding box, nome da imagem e dimensoes da imagem original.

---

## Notebook Jupyter/Colab

O notebook com a implementacao completa está disponível em:

[PhellypeMatheusGiacoiaFlaibamMassarente_rm566826_pbl_fase6.ipynb](PhellypeMatheusGiacoiaFlaibamMassarente_rm566826_pbl_fase6.ipynb)

Visualizacao no Google Drive: [Abrir notebook no Google Drive](https://drive.google.com/file/d/1b30nXLhVzoVZacfVe8HR73oVvIB4UDuP/view?usp=sharing)

O notebook é o documento principal da solucao, contendo codigo executado, resultados, comparacoes e conclusoes.

---

## Video demonstrativo

[🎬 Assistir no YouTube](https://youtu.be/MTVtTXqwMz4)

---

## Estrutura de arquivos

Dentre os arquivos presentes na raiz do projeto, definem-se:

- [atividade.txt](atividade.txt): escopo completo da atividade da Fase 6.
- [Fiap-FlexMedia-fase6-RM568140-RM567005-RM566826.txt](Fiap-FlexMedia-fase6-RM568140-RM567005-RM566826.txt): resumo da entrega com dados do grupo.
- [labels_carro.csv](labels_carro.csv): rotulacoes da classe Carros exportadas do AI Sense/Make Sense IA.
- [labels_moto.csv](labels_moto.csv): rotulacoes da classe Motos exportadas do AI Sense/Make Sense IA.
- [README.md](README.md): documentacao introdutoria do projeto.
- [README2.md](README2.md): modelo de referencia usado como padrao de documentacao FIAP.

```text
Cap_1_Rede_Neural/
├── atividade.txt
├── Fiap-FlexMedia-fase6-RM568140-RM567005-RM566826.txt
├── labels_carro.csv
├── labels_moto.csv
├── README.md
└── README2.md
```

---

## Como executar

A execucao completa sera realizada pelo notebook Jupyter/Colab, que ainda sera adicionado ao repositorio.

Fluxo previsto:

1. Abrir o notebook Jupyter/Colab.
2. Conectar o Google Drive com a base de imagens.
3. Executar as celulas de preparacao dos dados.
4. Executar as celulas de treinamento, validacao e teste.
5. Avaliar os resultados gerados pelos modelos.

---

## Status da entrega

| Item | Status |
|------|--------|
| Escopo da atividade | Disponivel em [atividade.txt](atividade.txt) |
| Dataset no Google Drive | Disponivel |
| Rotulacoes CSV | Disponiveis |
| Notebook Jupyter/Colab | ✅ Disponivel |
| Codigo final | ✅ Incluído no notebook |
| Video demonstrativo | ✅ [Assistir no YouTube](https://youtu.be/MTVtTXqwMz4) |

---

## Repositorio

GitHub: <https://github.com/Phemassa/Cap_1_Rede_Neural>
