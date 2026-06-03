# Cap1 Consolida Sistema - Fase 7

Projeto consolidado da Fase 7 para integrar as fases 1 a 6 em uma base unica Python, com operacao por dashboard e por CLI.

## Objetivo

- Integrar modulos das fases 1, 2, 3, 4 e 6.
- Usar dashboard central para acionar servicos.
- Disponibilizar comandos de terminal equivalentes.
- Disparar alertas AWS por e-mail com base em sensores da Fase 3.

## Estrutura

```text
Cap1_Consolida_sistema/
  app/                     # Streamlit principal e configuracoes
  phases/                  # Modulos por fase
    fase1_2/
    fase3/
    fase4/
    fase6/
  services/                # Orquestracao, health check e alertas
  dashboard/pages/         # Reservado para expansao de paginas
  docs/                    # Documentacao e planejamento
  tests/                   # Testes
  cli.py                   # Comandos de terminal
```

## Setup rapido

1. Criar ambiente virtual e instalar dependencias:

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

2. Configurar variaveis:

```bash
cp .env.example .env
```

3. Executar dashboard:

```bash
streamlit run app/main.py
```

4. Executar CLI:

```bash
python cli.py health
python cli.py run fase3
python cli.py monitor-fase3 --limit 20
python cli.py monitor-fase3 --limit 20 --send-alerts
python cli.py alert-test --value 15
```

## Status atual

- Scaffold de consolidacao criado.
- Orquestracao hibrida inicial pronta (dashboard + CLI).
- Fase 3 com Oracle + fallback CSV e regras de alerta operacional implementada.
- Integracoes de modelos ML e YOLO seguem como wrappers para proxima etapa.
