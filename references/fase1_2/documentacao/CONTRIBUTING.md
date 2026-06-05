# Guia de Contribuição - FarmTech Solutions

Obrigado por considerar contribuir para o FarmTech Solutions! Este documento fornece diretrizes para colaboradores.

## 📋 Índice
1. [Como Contribuir](#como-contribuir)
2. [Configuração do Ambiente](#configuração-do-ambiente)
3. [Padrões de Código](#padrões-de-código)
4. [Processo de Desenvolvimento](#processo-de-desenvolvimento)
5. [Testes](#testes)
6. [Documentação](#documentação)
7. [Relatando Bugs](#relatando-bugs)
8. [Solicitando Features](#solicitando-features)

## 🤝 Como Contribuir

### Tipos de Contribuições
- 🐛 **Correção de bugs**
- ✨ **Novas funcionalidades**
- 📚 **Melhorias na documentação**
- 🎨 **Melhorias na interface**
- ⚡ **Otimizações de performance**
- 🧪 **Adição de testes**

### Processo Rápido
1. Fork o repositório
2. Crie uma branch (`git checkout -b feature/nova-funcionalidade`)
3. Faça commit das mudanças (`git commit -m 'Adiciona nova funcionalidade'`)
4. Push para a branch (`git push origin feature/nova-funcionalidade`)
5. Abra um Pull Request

## 🛠️ Configuração do Ambiente

### Pré-requisitos
- Python 3.6+ instalado
- Git configurado
- Editor de código (recomendado: VS Code)

### Configuração Local
```bash
# Clone o repositório
git clone https://github.com/Phemassa/FarmTechSolutions.git
cd FarmTechSolutions

# Entre no diretório da aplicação Python
cd python_app

# Teste a aplicação
python main.py
```

### Verificação da Instalação
```bash
# Teste se o Python está funcionando
python --version

# Execute os testes básicos
python -c "import csv, os, re; print('Módulos importados com sucesso')"
```

## 📏 Padrões de Código

### Convenções Python
- **PEP 8**: Seguir padrões de estilo Python
- **Indentação**: 4 espaços (não tabs)
- **Encoding**: UTF-8 sempre
- **Linhas**: Máximo 79 caracteres por linha

### Nomenclatura
```python
# Variáveis e funções: snake_case
def calcular_area_retangulo(comprimento, largura):
    area_total = comprimento * largura
    return area_total

# Constantes: UPPER_CASE
PI = 3.1416
INSUMOS_PADRAO = ["Fosfato", "Nitrogênio", "Potássio"]

# Classes: PascalCase (se necessário no futuro)
class GerenciadorDados:
    pass
```

### Comentários e Docstrings
```python
def get_numeric_input(prompt, allow_exit=True):
    """
    Solicita entrada numérica do usuário com validação.
    
    Args:
        prompt (str): Mensagem para o usuário
        allow_exit (bool): Se permite saída com 'X'
    
    Returns:
        float: Valor numérico inserido pelo usuário
        None: Se usuário digitou 'X' para sair
    
    Raises:
        ValueError: Se entrada não for numérica válida
    """
    # Implementação...
```

### Tratamento de Erros
```python
# BOM: Tratamento específico
try:
    valor = float(entrada)
except ValueError:
    print("❌ Erro: Digite um número válido.")
    return None

# EVITAR: Except genérico
try:
    # código...
except:
    pass
```

## 🔄 Processo de Desenvolvimento

### Fluxo de Branches
```
main (produção)
├── develop (desenvolvimento)
│   ├── feature/nova-cultura
│   ├── feature/interface-melhorada
│   └── bugfix/calculo-area
└── hotfix/erro-critico
```

### Commits
#### Formato
```
tipo(escopo): descrição

[corpo opcional]

[rodapé opcional]
```

#### Tipos
- **feat**: Nova funcionalidade
- **fix**: Correção de bug
- **docs**: Documentação
- **style**: Formatação (não afeta lógica)
- **refactor**: Refatoração
- **test**: Adição de testes
- **chore**: Tarefas de manutenção

#### Exemplos
```bash
git commit -m "feat(culturas): adiciona suporte a cultura de soja"
git commit -m "fix(input): corrige validação de números decimais"
git commit -m "docs(readme): atualiza instruções de instalação"
```

## 🧪 Testes

### Testes Manuais Básicos
```python
# Teste de validação numérica
def test_numeric_input():
    # Teste com números válidos
    assert parse_float("10.5") == 10.5
    assert parse_float("10,5") == 10.5
    
    # Teste com entradas inválidas
    assert parse_float("abc") is None
    assert parse_float("") is None

# Teste de cálculo de área
def test_area_calculations():
    # Retângulo
    assert calcular_area_retangulo(10, 5) == 50
    
    # Círculo
    assert calcular_area_circulo(2) == 12.5664  # π * 2²
```

### Checklist de Testes
- [x] Validação de entrada funciona corretamente
- [x] Cálculos de área estão precisos
- [x] Salvamento de CSV preserva dados
- [X] Carregamento de CSV funciona
- [X] Menu de navegação responde corretamente
- [X] Tratamento de erros não quebra aplicação

## 📚 Documentação

### Arquivos a Atualizar
- **README.md**: Para mudanças na funcionalidade
- **TECHNICAL_DOCS.md**: Para mudanças na API/funções
- **CHANGELOG.md**: Para todas as mudanças
- **INSTALL.md**: Para mudanças na instalação

### Padrão de Documentação
```markdown
## Nome da Funcionalidade

### Descrição
Breve descrição do que faz.

### Uso
```python
exemplo_de_codigo()
```

### Parâmetros
- **param1** (tipo): Descrição
- **param2** (tipo): Descrição

### Retorno
- **tipo**: Descrição do retorno

### Exemplo
```python
resultado = exemplo_funcao("teste", 123)
print(resultado)  # Output esperado
```
```

## 🐛 Relatando Bugs

### Template de Bug Report
```markdown
**Descrição do Bug**
Descrição clara e concisa do bug.

**Para Reproduzir**
1. Vá para '...'
2. Clique em '....'
3. Role até '....'
4. Veja o erro

**Comportamento Esperado**
Descrição do que deveria acontecer.

**Screenshots**
Se aplicável, adicione screenshots.

**Ambiente:**
- OS: [ex: Windows 10]
- Versão Python: [ex: 3.9.0]
- Versão do Projeto: [ex: 1.0.0]

**Contexto Adicional**
Qualquer outro contexto sobre o problema.
```

### Prioridades
- 🔴 **Crítico**: Aplicação não funciona
- 🟡 **Alto**: Funcionalidade principal quebrada
- 🟢 **Médio**: Funcionalidade secundária com problema
- 🔵 **Baixo**: Melhoria de UX/Performance

## ✨ Solicitando Features

### Template de Feature Request
```markdown
**Sua solicitação de feature está relacionada a um problema?**
Descrição clara do problema. Ex: Estou sempre frustrado quando [...]

**Descreva a solução que você gostaria**
Descrição clara e concisa do que você quer que aconteça.

**Descreva alternativas consideradas**
Descrição de soluções ou features alternativas consideradas.

**Contexto adicional**
Contexto ou screenshots sobre a solicitação.
```

### Avaliação de Features
Features são avaliadas baseadas em:
- **Utilidade**: Quantos usuários se beneficiariam
- **Complexidade**: Esforço de implementação
- **Alinhamento**: Se encaixa na visão do projeto
- **Recursos**: Disponibilidade da equipe

## 🎯 Áreas de Contribuição Prioritárias

### Immediate (v1.1.0)
- [ ] Melhorar validação de entrada
- [ ] Adicionar cores ao terminal
- [ ] Implementar confirmação antes de deletar
- [ ] Otimizar performance do carregamento CSV

### Short-term (v1.2.0)
- [ ] Adicionar mais tipos de cultura
- [ ] Implementar relatórios estatísticos
- [ ] Melhorar tratamento de erros
- [ ] Adicionar testes automatizados

### Long-term (v2.0.0)
- [ ] Interface gráfica
- [ ] Sistema de usuários
- [ ] Base de dados real
- [ ] API REST

## 📞 Contato

- **Issues**: Use o sistema de issues do GitHub
- **Discussões**: GitHub Discussions
- **Email**: [Email do projeto se disponível]

## 📄 Licença

Ao contribuir, você concorda que suas contribuições serão licenciadas sob a mesma licença do projeto.

---

**Obrigado por contribuir para o FarmTech Solutions!** 🚜🌱
