from datetime import datetime

from app.config import settings

try:
    import boto3
except ImportError:
    boto3 = None


class AlertService:
    def __init__(self) -> None:
        self.enabled = bool(settings.aws_sns_topic_arn and boto3 is not None)

    def send_alert(self, payload: dict) -> dict:
        message = (
            f"ALERTA FARMTECH\n"
            f"Origem: {payload.get('source')}\n"
            f"Metrica: {payload.get('metric')}\n"
            f"Valor: {payload.get('value')}\n"
            f"Limiar: {payload.get('threshold')}\n"
            f"Acao sugerida: {payload.get('action')}\n"
            f"Timestamp: {datetime.utcnow().isoformat()}Z"
        )

        if not self.enabled:
            return {
                "status": "dry-run",
                "message": "AWS SNS nao configurado. Alerta simulado.",
                "payload": payload,
            }

        client = boto3.client("sns", region_name=settings.aws_region)
        result = client.publish(
            TopicArn=settings.aws_sns_topic_arn,
            Subject="FarmTech - Alerta de Sensor",
            Message=message,
        )
        return {"status": "sent", "message_id": result.get("MessageId"), "payload": payload}
