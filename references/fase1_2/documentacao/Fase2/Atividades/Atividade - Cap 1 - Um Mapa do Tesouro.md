# Cap 1 - Um Mapa do Tesouro - Atividade Avaliativa

## Sumário

- [1. Informações da Atividade](#1-informações-da-atividade)
- [2. Introdução](#2-introdução)  
- [3. Descrição do Projeto](#3-descrição-do-projeto)
  - [3.1 Sistema de Irrigação Inteligente](#31-sistema-de-irrigação-inteligente)
  - [3.2 Componentes e Sensores](#32-componentes-e-sensores)
  - [3.3 Lógica de Funcionamento](#33-lógica-de-funcionamento)
- [4. Atividades Opcionais - Ir Além](#4-atividades-opcionais---ir-além)
  - [4.1 Integração Python com API Pública](#41-integração-python-com-api-pública)
  - [4.2 Análise Estatística em R](#42-análise-estatística-em-r)
- [5. Benefícios Esperados](#5-benefícios-esperados)
- [6. Entregáveis](#6-entregáveis)
- [7. Observações Importantes](#7-observações-importantes)

---

## 1. Informações da Atividade

**Atividade:** PROJETO 2 - Iniciando a coleta de Dados  
**Período:** 18/09/2025 a 15/10/2025  
**Status:** Entrega pendente  

> **⚠️ Atenção:** Atividades entregues até 3 dias após o prazo receberão até 70% da nota. O cálculo é feito automaticamente pelo sistema, o professor não tem controle sobre o percentual da nota atribuída.

---

## 2. Introdução

Você e seu grupo estão na **Startup FarmTech Solutions**, trabalhando na equipe de desenvolvedores. A FIAP não condena o uso de IAs (ChatGPT, Gemini) em seus estudos, desde que o aluno tenha olhar crítico para filtrar erros e acertos das respostas e monte sua própria resposta de forma autoral.

> **⚠️ Importante:** Caso a solução apresentada seja exatamente um "copy-paste" do GPT para o portal da FIAP, o resultado poderá ser idêntico entre grupos, caracterizando **plágio** e os grupos envolvidos não terão nota.

A FarmTech Solutions continua seu desenvolvimento na **Agricultura Digital**. Nesta atividade, trabalharemos em grupo para construir/simular um dispositivo eletrônico capaz de coletar dados em uma fazenda.

---

## 3. Descrição do Projeto

### 3.1 Sistema de Irrigação Inteligente

Considerando como base a **Fase anterior** do projeto (cálculo de área plantada, monitoramento climático), a **Fase 2** avançará no sistema de gestão agrícola usando um dispositivo construído pelo grupo.

O objetivo é conectar sensores físicos para **otimizar a irrigação agrícola** e criar um sistema de irrigação inteligente baseado nos elementos essenciais para culturas agrícolas.

### 3.2 Componentes e Sensores

#### 3.2.1 Elementos NPK
Toda cultura agrícola depende de três elementos químicos fundamentais:
- **N** - Nitrogênio
- **P** - Fósforo  
- **K** - Potássio

Estes elementos influenciam o **pH da terra** e a produtividade da planta.

#### 3.2.2 Sensores Utilizados (Simulação Wokwi.com)

Como a plataforma **Wokwi.com** não possui sensores exclusivamente agrícolas, faremos substituições didáticas:

| Sensor Real | Sensor Simulado | Descrição |
|-------------|-----------------|-----------|
| Sensor N, P, K | **3 Botões Verdes** | Cada botão simula o nível de um elemento (true/false) |
| Sensor pH | **LDR** (Light Dependent Resistor) | Dados analógicos representando pH (0-14, neutro ≈ 7) |
| Sensor Umidade Solo | **DHT22** | Medidor de umidade do ar (simulando solo) |
| Bomba d'Água | **Relé Azul** | Acionamento da irrigação |

### 3.3 Lógica de Funcionamento

1. **Monitoramento NPK:** Botões representam níveis de nutrientes
2. **pH da Terra:** Sensor LDR fornece dados analógicos
3. **Umidade:** DHT22 monitora umidade em tempo real
4. **Irrigação:** Relé azul liga/desliga conforme necessário

> **💡 Dica:** Quando alterar os botões NPK, ajustar o sensor LDR (pH), pois na prática você estaria alterando o pH da terra.

**Escolha da Cultura:** O grupo deve escolher uma cultura agrícola e pesquisar suas necessidades reais de nutrientes, documentando a lógica de decisão para ligar/desligar a bomba d'água.

---

## 4. Atividades Opcionais - Ir Além

### 4.1 Integração Python com API Pública (Opcional 1)

**Objetivo:** Integrar dados meteorológicos de APIs públicas (ex: OpenWeather) para ajustar irrigação automaticamente.

**Funcionalidades:**
- Previsão de chuva → suspender irrigação
- Economia de recursos hídricos
- Transferência manual de dados entre Python e ESP32 (se integração automática não for possível)

**Alternativa:** Usar funções `Serial.available()` e `Serial.read()` para inserir dados via Monitor Serial.

### 4.2 Análise Estatística em R (Opcional 2)

**Objetivo:** Implementar análise estatística em R para decisão de irrigação.

**Benefícios:**
- Conhecimento em Data Science
- Cargo procurado no mercado de trabalho
- Desenvolvimento de competências analíticas

> **🏆 Vantagem:** Grupos que desenvolverem itens opcionais serão monitorados internamente e poderão ser convidados para outros programas da FIAP.

---

## 5. Benefícios Esperados

Este desafio permitirá aplicar conhecimentos em:

- **Sensoriamento** e **IoT**
- **Consulta de APIs**
- **Data Science**
- **Visão prática** de IoT e IA para otimização agrícola

A integração é fundamental para o sucesso da **FarmTech Solutions** e para o projeto de **fazenda inteligente**, garantindo:
- Uso eficiente da água
- Redução de desperdícios
- Maximização da produtividade agrícola

---

## 6. Entregáveis

### 6.1 Organização no GitHub
- Separar repositório: `meugit/cursotiaor/pbl/fase3/pastas`

### 6.2 Documentação
- **README.MD** em markdown explicando funcionamento completo
- Documentar toda lógica e especificidades
- Incluir imagens do circuito Wokwi.com
- Demonstrar conexões dos sensores

### 6.3 Códigos Fonte
- Código **C/C++** desenvolvido no ESP32
- Códigos do **Programa Ir Além** (opcionais 1 e/ou 2)

### 6.4 Vídeo Demonstrativo
- **Link do YouTube** (sem listagem)
- **Duração:** até 5 minutos
- Demonstrar funcionamento completo do projeto

---

## 7. Observações Importantes

### 7.1 Reforçando Orientações

> **📝 Reforçando:** Não temos o sensor de pH, então você altera manualmente o nível do LDR. Assim, o NPK alterou o pH, certo?

### 7.2 Fontes de Dados Sugeridas

> **💡 Dica:** Existem várias fontes de dados públicos de Agronegócio: **EMBRAPA**, **CONAB**, **IBGE**, **CEPEA** e/ou **MAPA**.

### 7.3 Controle de Versão

> **⚠️ Importante:** Não altere o repositório GitHub após a data de entrega do portal da FIAP. Alterações no Git após entrega resultarão em desconto na nota. **O grupo deve ser de 1 a 5 alunos**.

---

## Conclusão

Este projeto representa um marco importante no desenvolvimento da **Agricultura 4.0**, combinando tecnologias de **IoT**, **sensoriamento** e **análise de dados** para criar soluções inteligentes e sustentáveis no agronegócio.

A implementação bem-sucedida deste sistema de irrigação automatizado demonstrará a capacidade técnica da equipe e contribuirá significativamente para o portfólio da **FarmTech Solutions**.

---

**Data:** 28/09/2025  
**Curso:** Tecnologia em Inteligência Artificial e Robótica  
**Disciplina:** Projeto Interdisciplinar  
**Instituição:** FIAP