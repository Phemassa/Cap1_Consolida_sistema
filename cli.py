import argparse
import json

from services.alert_service import AlertService
from services.healthcheck import collect_health
from services.orchestrator import monitor_fase3, run_phase


def main() -> None:
    parser = argparse.ArgumentParser(description="CLI de orquestracao FarmTech Fase 7")
    sub = parser.add_subparsers(dest="command", required=True)

    sub.add_parser("health", help="Exibe estado de saude dos modulos")

    run_parser = sub.add_parser("run", help="Executa uma fase")
    run_parser.add_argument("phase", choices=["fase1_2", "fase3", "fase4", "fase6"])

    alert_parser = sub.add_parser("alert-test", help="Dispara teste de alerta")
    alert_parser.add_argument("--value", type=float, required=True)
    alert_parser.add_argument("--threshold", type=float, default=20.0)

    monitor_parser = sub.add_parser("monitor-fase3", help="Coleta snapshot da Fase 3")
    monitor_parser.add_argument("--limit", type=int, default=20)
    monitor_parser.add_argument("--send-alerts", action="store_true")

    args = parser.parse_args()

    if args.command == "health":
        print(json.dumps(collect_health(), indent=2, ensure_ascii=True))
        return

    if args.command == "run":
        print(json.dumps(run_phase(args.phase), indent=2, ensure_ascii=True))
        return

    if args.command == "alert-test":
        service = AlertService()
        payload = {
            "source": "fase3",
            "metric": "umidade_solo",
            "value": args.value,
            "threshold": args.threshold,
            "action": "Verificar irrigacao e iniciar ajuste corretivo",
        }
        print(json.dumps(service.send_alert(payload), indent=2, ensure_ascii=True))
        return

    if args.command == "monitor-fase3":
        result = monitor_fase3(limit=args.limit, send_alerts=args.send_alerts)
        print(json.dumps(result, indent=2, ensure_ascii=True))


if __name__ == "__main__":
    main()
