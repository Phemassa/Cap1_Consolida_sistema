import os
from dataclasses import dataclass

from dotenv import load_dotenv


load_dotenv()


@dataclass(frozen=True)
class Settings:
    oracle_host: str = os.getenv("ORACLE_HOST", "localhost")
    oracle_port: int = int(os.getenv("ORACLE_PORT", "1521"))
    oracle_service_name: str = os.getenv("ORACLE_SERVICE_NAME", "XE")
    oracle_user: str = os.getenv("ORACLE_USER", "")
    oracle_password: str = os.getenv("ORACLE_PASSWORD", "")

    aws_region: str = os.getenv("AWS_REGION", "sa-east-1")
    aws_sns_topic_arn: str = os.getenv("AWS_SNS_TOPIC_ARN", "")
    alert_email_to: str = os.getenv("ALERT_EMAIL_TO", "")

    app_env: str = os.getenv("APP_ENV", "dev")


settings = Settings()
