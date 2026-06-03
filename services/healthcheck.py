from app.config import settings


def collect_health() -> dict:
    return {
        "app_env": settings.app_env,
        "oracle_configured": bool(settings.oracle_user and settings.oracle_password),
        "aws_configured": bool(settings.aws_sns_topic_arn),
        "status": "ok",
    }
