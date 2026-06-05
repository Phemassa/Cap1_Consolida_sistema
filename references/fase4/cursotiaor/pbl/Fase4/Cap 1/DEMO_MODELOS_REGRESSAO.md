# 📊 DEMONSTRAÇÃO: Modelos de Regressão ML

## 🎯 RESUMO EXECUTIVO

✅ **3 Modelos Implementados:**
1. **Regressão Linear** (baseline - regressão múltipla)
2. **Random Forest** (ensemble não-linear - 100 árvores)
3. **Gradient Boosting** (ensemble não-linear - boosting iterativo)

✅ **Pipeline Completo:** Treinamento → Validação → Seleção → Deployment

---

## 🎬 ROTEIRO PARA DEMONSTRAÇÃO (60 segundos)

### **[TELA: Página "🔮 Previsoes" do Dashboard]**

> 🎤 **Texto 1 (15 seg):**
> 
> "O sistema implementa três modelos de regressão: Linear Múltipla como baseline, Random Forest com 100 árvores de decisão, e Gradient Boosting com learning rate 0.1. Todos validados com cross-validation de 5 folds."

> 🎤 **Texto 2 (20 seg):**
> 
> "Os modelos foram treinados com mil amostras contendo 8 features: temperatura, umidade, pH, status NPK e cultura. O Random Forest obteve melhor performance com R² de [VALOR] e MAE de [VALOR] kg/ha, sendo selecionado automaticamente."

**[AÇÃO: Ajustar sliders - temp 28°C, umidade 65%, pH 6.5]**

> 🎤 **Texto 3 (25 seg):**
> 
> "Vou fazer uma previsão: com temperatura 28°C, umidade 65%, pH 6.5 e NPK adequado. O modelo prevê rendimento de [X] kg/ha com [Y]% de confiança, recomendando irrigação de [Z] litros por metro quadrado. A análise de feature importance mostra que umidade contribui com maior peso na decisão."

---

## 📊 DADOS PARA ANOTAR ANTES DA GRAVAÇÃO

Execute `python models/train_models.py` e anote:

```
┌─────────────────────┬──────────┬──────────┬──────────┐
│ Modelo              │ R² Test  │ MAE      │ RMSE     │
├─────────────────────┼──────────┼──────────┼──────────┤
│ Linear Regression   │ ________ │ ________ │ ________ │
│ Random Forest       │ ________ │ ________ │ ________ │
│ Gradient Boosting   │ ________ │ ________ │ ________ │
└─────────────────────┴──────────┴──────────┴──────────┘

🏆 Melhor Modelo: ________________
```

---

## 🔍 DETALHES TÉCNICOS (para mencionar se perguntado)

### Regressão Linear Múltipla
```
Equação: y = β₀ + β₁x₁ + β₂x₂ + ... + β₈x₈
Método: Mínimos Quadrados Ordinários (OLS)
Biblioteca: sklearn.linear_model.LinearRegression
Features: 8 variáveis preditoras
Complexidade: O(n·p²) onde n=amostras, p=features
```

### Random Forest
```
Algoritmo: Bagging de Árvores de Decisão
n_estimators: 100 árvores
max_depth: 10 níveis
Votação: Média das previsões
Vantagem: Captura não-linearidade e interações
```

### Gradient Boosting
```
Algoritmo: Boosting iterativo
n_estimators: 100 árvores sequenciais
learning_rate: 0.1
max_depth: 5
Método: Gradient Descent em função de perda
```

---

## ✅ CHECKLIST PRÉ-DEMONSTRAÇÃO

- [ ] Modelos treinados (`ls models/*.pkl`)
- [ ] Dashboard rodando em localhost:8502
- [ ] Página Previsões acessível
- [ ] Sliders funcionando
- [ ] Valores de R² e MAE anotados
- [ ] Teste de previsão realizado

---

## 🎓 ATENDE CRITÉRIOS FIAP

✅ Regressão Linear: `LinearRegression()`  
✅ Regressão Múltipla: 8 features simultâneas  
✅ Regressão Não-Linear: Random Forest + Gradient Boosting  
✅ Validação: Cross-validation 5-fold  
✅ Métricas: R², MAE, RMSE  
✅ Comparação: 3 modelos  
✅ Deployment: Dashboard interativo  

---

## 🚀 COMANDO RÁPIDO

```powershell
# Ver performance dos modelos
cd "c:\Fiap Projeto\Fase2\cursotiaor\pbl\Fase2\Cap 1"
python models/train_models.py

# Iniciar dashboard
streamlit run dashboard/app.py
```

Acesse: http://localhost:8502 → Página "🔮 Previsoes"
