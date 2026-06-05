# 🎥 ROTEIRO DE VÍDEO - FARMTECH SOLUTIONS (5 MINUTOS)

## 📋 Checklist Pré-Gravação

### Preparação do Ambiente
- [ ] Dashboard rodando em http://localhost:8502
- [ ] Sistema de auto-ingestão gerando dados: `python database/database_manager.py`
- [ ] Banco com pelo menos 50 leituras (verificar com `python consulta_db.py`)
- [ ] Navegador em tela cheia (F11)
- [ ] Fechar abas desnecessárias
- [ ] OBS Studio ou ferramenta de gravação configurada
- [ ] Áudio testado (microfone claro)
- [ ] Resolução mínima: 1280x720 (HD)

### Preparação do Conteúdo
- [ ] Notas com valores reais do banco (temperatura, umidade, etc.)
- [ ] Exemplos de insights para comentar
- [ ] Script ensaiado (ler este documento)

---

## 🎬 ROTEIRO DETALHADO (5 MINUTOS)

### **SEGMENTO 1: INTRODUÇÃO (30 segundos - 0:00-0:30)**

**[TELA: Página Principal do Dashboard]**

> 🎤 **FALA:**
> 
> "Olá! Sou [SEU NOME], aluno da FIAP, e vou apresentar o FarmTech Solutions, um sistema completo de agricultura de precisão desenvolvido para o Capítulo 1 da Fase 2. Nossa solução integra sensores IoT, banco de dados SQLite e Machine Learning para otimizar a irrigação e gestão de nutrientes em cultivos de banana e milho."

**[AÇÃO: Scroll suave pela página principal]**

---

### **SEGMENTO 2: VISÃO GERAL DO SISTEMA (45 segundos - 0:30-1:15)**

**[TELA: Permanecer na página principal, destacar métricas]**

> 🎤 **FALA:**
> 
> "No painel principal, temos métricas em tempo real. Atualmente, registramos [X] leituras de sensores com temperatura média de [Y]°C, umidade do solo em [Z]%, e pH médio de [W]. O sistema monitora continuamente [N] irrigações ativas e [M] registros com NPK adequado."
> 
> "Os gráficos inferiores mostram a evolução da temperatura e distribuição de pH ao longo do tempo, permitindo identificar padrões e anomalias rapidamente."

**[AÇÃO: Apontar para cada métrica enquanto fala, depois scroll pelos gráficos]**

---

### **SEGMENTO 3: ANÁLISE DE CORRELAÇÕES (1 minuto - 1:15-2:15)**

**[TELA: Navegar para página "📊 Correlacoes"]**

> 🎤 **FALA:**
> 
> "Na página de Correlações, utilizamos análise estatística avançada. Este mapa de calor mostra as relações entre variáveis agrícolas. Observe que umidade do solo tem correlação [positiva/negativa] com pH, indicando [interpretação]."

**[AÇÃO: Destacar com cursor as células mais relevantes do heatmap]**

> 🎤 **FALA (continuação):**
> 
> "Nos scatter plots interativos, podemos selecionar diferentes variáveis. Vou escolher Umidade vs Temperatura. A linha de tendência OLS mostra [tendência crescente/decrescente], confirmando que [explicação técnica]."

**[AÇÃO: Mudar seletores de variáveis X e Y, mostrar diferentes combinações]**

> 🎤 **FALA (conclusão):**
> 
> "Este grid de correlações permite ao gestor agrícola identificar rapidamente quais fatores mais influenciam a produtividade."

---

### **SEGMENTO 4: PREVISÕES DE MACHINE LEARNING (1 minuto - 2:15-3:15)**

**[TELA: Navegar para página "🔮 Previsoes"]**

> 🎤 **FALA:**
> 
> "A página de Previsões utiliza modelos de Machine Learning treinados com Scikit-Learn. Implementamos três algoritmos: Random Forest, Gradient Boosting e Regressão Linear."

**[AÇÃO: Scroll para mostrar os 3 modelos]**

> 🎤 **FALA (continuação):**
> 
> "O Random Forest obteve o melhor desempenho com R² de [VALOR] e MAE de [VALOR] kg/ha. Vou fazer uma previsão interativa: ajustando temperatura para 28°C, umidade para 65%, pH 6.5, e todos os nutrientes adequados."

**[AÇÃO: Ajustar sliders conforme valores mencionados]**

> 🎤 **FALA (continuação):**
> 
> "O modelo prevê um rendimento de [X] kg/ha com [Y]% de confiança, recomendando irrigação de [Z] litros por metro quadrado. Essas previsões auxiliam na tomada de decisão preventiva."

**[AÇÃO: Mostrar resultado da previsão, destacar valores]**

---

### **SEGMENTO 5: TENDÊNCIAS TEMPORAIS (45 segundos - 3:15-4:00)**

**[TELA: Navegar para página "📈 Tendencias"]**

> 🎤 **FALA:**
> 
> "A análise de Tendências permite visualizar séries temporais. Filtrando por 'Últimos 7 dias' e cultura 'banana', observamos padrões claros."

**[AÇÃO: Selecionar filtros mencionados]**

> 🎤 **FALA (continuação):**
> 
> "Este gráfico mostra evolução da umidade e ações de irrigação. Note que sempre que a umidade cai abaixo de 40%, o sistema ativa a irrigação automaticamente. O consumo acumulado de água está em [X] litros."

**[AÇÃO: Scroll pelos gráficos de série temporal]**

---

### **SEGMENTO 6: ANÁLISE INTELIGENTE COM IA (45 segundos - 4:00-4:45)**

**[TELA: Navegar para página "💡 Analise"]**

> 🎤 **FALA:**
> 
> "A Análise Inteligente é o diferencial do FarmTech. O sistema gera insights automáticos baseados em regras agronômicas da EMBRAPA."

**[AÇÃO: Scroll para mostrar cards de insights]**

> 🎤 **FALA (continuação):**
> 
> "Veja: o sistema detectou automaticamente [LER INSIGHT REAL, ex: 'Solo Muito Seco com umidade de 35%'] e recomenda irrigação urgente com volume específico. Também identifica [OUTRO INSIGHT, ex: 'Deficiência de Nitrogênio'] sugerindo aplicação de ureia com dosagem exata."

**[AÇÃO: Destacar cards de alertas críticos (vermelhos) e warnings (amarelos)]**

> 🎤 **FALA (conclusão):**
> 
> "Essas recomendações acionáveis transformam dados em decisões práticas para o gestor."

---

### **SEGMENTO 7: ARQUITETURA E INTEGRAÇÃO (15 segundos - 4:45-5:00)**

**[TELA: Voltar rapidamente para página principal ou mostrar terminal com auto-ingestão]**

> 🎤 **FALA:**
> 
> "A arquitetura completa integra sensores ESP32 simulados no Wokwi, banco SQLite com 4 tabelas relacionais, pipeline de ML com Pandas e Scikit-Learn, e este dashboard Streamlit responsivo. O sistema opera em tempo real com auto-ingestão de dados a cada 5 segundos."

**[AÇÃO: Se possível, mostrar brevemente terminal com logs do database_manager.py]**

---

### **ENCERRAMENTO (últimos segundos)**

**[TELA: Página principal]**

> 🎤 **FALA:**
> 
> "Obrigado pela atenção! O FarmTech Solutions demonstra viabilidade técnica de IoT e IA aplicados ao agronegócio brasileiro."

**[FADE OUT]**

---

## 🎯 PONTOS-CHAVE PARA MARCAR PONTOS NA AVALIAÇÃO

### ✅ Critério: Funcionalidade do Dashboard
- Demonstrar **TODAS as 5 páginas** funcionando
- Mostrar **interatividade** (sliders, filtros, seletores)
- Destacar **dados reais** gerados pela auto-ingestão

### ✅ Critério: Visualizações (Gráficos, Correlações, Tendências)
- **Heatmap de correlações** com interpretação
- **Scatter plots com trendline OLS** (statsmodels)
- **Séries temporais** com filtros dinâmicos
- **Gráficos de distribuição** (pH, temperatura)

### ✅ Critério: Interpretação de Resultados
- Explicar **significado dos valores** (ex: "pH 6.5 é ideal para banana")
- Comentar **insights automáticos** gerados pela IA
- Relacionar dados com **recomendações práticas**

### ✅ Critério: Usabilidade para Gestor Agrícola
- Destacar **métricas resumidas** no topo (visão executiva)
- Mostrar **navegação intuitiva** entre páginas
- Enfatizar **alertas visuais** (cores, ícones)
- Mencionar **ações práticas** sugeridas

### ✅ Critério: Integração Sensores-DB-IA
- Mencionar **fluxo de dados**: ESP32 → SQLite → ML → Dashboard
- Mostrar **auto-ingestão em tempo real** (terminal com logs)
- Explicar **pipeline completo** (coleta → armazenamento → análise → visualização)

### ✅ Critério: Clareza e Domínio Técnico
- Usar **terminologia correta** (R², MAE, Random Forest, OLS)
- Citar **tecnologias específicas** (Streamlit, Plotly, Scikit-Learn, SQLite)
- Mencionar **dados reais** (EMBRAPA para requisitos agrícolas)

### ✅ Critério: Estética e Navegabilidade
- Mostrar **design limpo** com cores da identidade verde
- Destacar **responsividade** (ajuste de colunas)
- Demonstrar **feedback visual** (loading spinners, alertas)

---

## 📊 DADOS PARA MENCIONAR (Consultar antes de gravar)

Execute `python consulta_db.py` e anote:

```
Total de leituras: _______
Total de previsões: _______
Total de irrigações: _______
Temperatura média: _______°C
Umidade média: _______%
pH médio: _______
NPK adequado: _______
```

Execute `python models/train_models.py` para obter métricas reais:

```
Random Forest R²: _______
Random Forest MAE: _______ kg/ha
Gradient Boosting R²: _______
Linear Regression R²: _______
```

---

## 🛠️ COMANDOS PARA RODAR ANTES DA GRAVAÇÃO

```powershell
# 1. Limpar terminal
cd "c:\Fiap Projeto\Fase2\cursotiaor\pbl\Fase2\Cap 1"

# 2. Iniciar auto-ingestão (deixar rodando em background)
python database/database_manager.py

# 3. Em outro terminal, iniciar dashboard
streamlit run dashboard/app.py

# 4. Verificar dados disponíveis
python consulta_db.py
# Escolher opção 1 (Estatísticas)
```

---

## 🎥 DICAS DE GRAVAÇÃO

### Técnicas de Apresentação
1. **Velocidade da fala**: Moderada (não muito rápido!)
2. **Tom**: Confiante e didático
3. **Pausas**: Respire entre seções
4. **Cursor**: Use seta do mouse para destacar elementos

### Qualidade Técnica
1. **Resolução**: Mínimo 1280x720 (HD)
2. **FPS**: 30fps ou superior
3. **Áudio**: Microfone próximo, sem ruído de fundo
4. **Lighting**: Tela clara, sem reflexos

### Edição (Opcional)
1. **Intro**: 2-3 segundos com título "FarmTech Solutions - FIAP Fase 2 Cap 1"
2. **Transições**: Suaves entre páginas
3. **Zoom**: Em elementos específicos (opcional)
4. **Legenda**: Seu nome e RM no canto inferior

### Checklist Final
- [ ] Vídeo tem menos de 5 minutos?
- [ ] Áudio está claro?
- [ ] Todas as 5 páginas foram mostradas?
- [ ] Mencionou tecnologias (Streamlit, ML, SQLite)?
- [ ] Interpretou resultados (não apenas leu números)?
- [ ] Mostrou usabilidade (interação com interface)?
- [ ] Formato compatível (MP4, MOV)?

---

## 📤 FORMATO DE ENTREGA

**Nome do arquivo:** `FARMTECH_FASE2_CAP1_[SEU_RM].mp4`

**Exemplo:** `FARMTECH_FASE2_CAP1_RM12345.mp4`

**Upload:** Portal FIAP conforme instruções do professor

---

## ⚠️ AVISOS IMPORTANTES

1. **NÃO ULTRAPASSAR 5 MINUTOS** - vídeos longos podem ser penalizados
2. **MOSTRAR CÓDIGO EM EXECUÇÃO** - não apenas slides
3. **DADOS REAIS** - não fake/mockado
4. **SEM MUSICA DE FUNDO** - pode atrapalhar o áudio
5. **TESTAR UPLOAD** - verificar se o arquivo abre corretamente

---

## 🎓 BOA SORTE NA GRAVAÇÃO!

**Lembre-se:** Confiança vem da preparação. Ensaie algumas vezes antes da gravação final! 🚀
