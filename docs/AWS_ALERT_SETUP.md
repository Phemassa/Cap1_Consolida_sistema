# AWS Alert Setup - Fase 5/7

Este guia documenta a configuracao minima para disparo de alertas por e-mail via AWS (SNS/SES), integrada ao monitoramento da Fase 3.

## Objetivo

- Detectar condicoes criticas de sensores (Fase 3).
- Disparar mensagem para equipe operacional por e-mail.
- Registrar historico local de eventos em data/runtime/alerts_history.jsonl.

## Passos AWS (SNS)

1. Criar um Topic SNS (ex.: farmtech-alertas).
2. Criar assinatura do tipo E-mail para o destinatario operacional.
3. Confirmar assinatura no e-mail recebido.
4. Garantir permissoes IAM para sns:Publish.

## Variaveis no .env

```env
AWS_REGION=sa-east-1
AWS_SNS_TOPIC_ARN=arn:aws:sns:sa-east-1:123456789012:farmtech-alertas
ALERT_EMAIL_TO=operacao@example.com
```

## Testes locais

```bash
python3 cli.py alert-test --value 15 --threshold 20
python3 cli.py monitor-now --limit 20
python3 cli.py alerts-history --limit 20
```

## Evidencias para README

- Print do SNS Topic e ARN.
- Print da assinatura de e-mail confirmada.
- Print do comando monitor-now com dispatch de alertas.
- Print da caixa de e-mail recebendo alerta.
