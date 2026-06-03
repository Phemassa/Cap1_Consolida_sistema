# Plano de Implementacao - Fase 7

## Epics

1. Baseline e governanca tecnica
2. Consolidacao de fases em projeto unico
3. Orquestracao hibrida (dashboard + CLI)
4. Alertas AWS por e-mail
5. Qualidade e validacao ponta a ponta
6. Documentacao final e evidencias
7. Trilha paralela de Ir Alem

## Histories

1. Como time, queremos um ambiente padrao para evitar conflitos entre fases.
2. Como time, queremos reaproveitar modulos das fases anteriores em uma arquitetura unica.
3. Como usuario, quero executar servicos por dashboard e por terminal.
4. Como operacao, quero receber alertas por e-mail com acao corretiva.
5. Como avaliador, quero evidencias claras de funcionamento e documentacao objetiva.

## Tasks iniciais (Sprint 0)

1. Criar estrutura do projeto consolidado.
2. Definir configuracao e variaveis de ambiente.
3. Criar app Streamlit principal com botoes de orquestracao.
4. Criar CLI com comandos equivalentes.
5. Criar wrappers por fase (1-2, 3, 4, 6).
6. Criar servico de alerta AWS com modo dry-run.
7. Criar health check de dependencias e configuracoes.
8. Preparar README com setup e execucao.

## Tasks proximas (Sprint 1)

1. Migrar logica real da Fase 1-2.
2. Integrar Oracle real da Fase 3 com fallback CSV.
3. Integrar pipeline ML da Fase 4.
4. Integrar inferencia de visao da Fase 6.
5. Definir regras oficiais de alertas por cultura.
