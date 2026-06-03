import argparse
import json

from services.alert_service import AlertService
from services.healthcheck import collect_health
from services.orchestrator import create_area, delete_area, infer_fase4, monitor_fase3, run_fase6_vision, run_phase, train_fase4, update_area


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

    train_parser = sub.add_parser("train-fase4", help="Treina pipeline ML da Fase 4")
    train_parser.add_argument("--limit", type=int, default=120)
    train_parser.add_argument("--no-force", action="store_true")

    predict_parser = sub.add_parser("predict-fase4", help="Predicao com modelo da Fase 4")
    predict_parser.add_argument("--temperatura", type=float, required=True)
    predict_parser.add_argument("--umidade-solo", type=float, required=True)
    predict_parser.add_argument("--ph-solo", type=float, required=True)

    vision_parser = sub.add_parser("run-fase6", help="Executa inferencia da Fase 6 em pasta de imagens")
    vision_parser.add_argument("--images-dir", type=str, default=None)
    vision_parser.add_argument("--limit", type=int, default=50)

    area_add = sub.add_parser("area-add", help="Cria area (Fase 1-2)")
    area_add.add_argument("--nome", required=True)
    area_add.add_argument("--cultura", required=True)
    area_add.add_argument("--hectares", type=float, required=True)

    area_update = sub.add_parser("area-update", help="Atualiza area (Fase 1-2)")
    area_update.add_argument("--id", type=int, required=True)
    area_update.add_argument("--nome", default=None)
    area_update.add_argument("--cultura", default=None)
    area_update.add_argument("--hectares", type=float, default=None)

    area_delete = sub.add_parser("area-delete", help="Remove area (Fase 1-2)")
    area_delete.add_argument("--id", type=int, required=True)

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
        return

    if args.command == "train-fase4":
        result = train_fase4(limit=args.limit, force_train=not args.no_force)
        print(json.dumps(result, indent=2, ensure_ascii=True))
        return

    if args.command == "predict-fase4":
        result = infer_fase4(
            temperatura=args.temperatura,
            umidade_solo=args.umidade_solo,
            ph_solo=args.ph_solo,
        )
        print(json.dumps(result, indent=2, ensure_ascii=True))
        return

    if args.command == "run-fase6":
        result = run_fase6_vision(images_dir=args.images_dir, limit=args.limit)
        print(json.dumps(result, indent=2, ensure_ascii=True))
        return

    if args.command == "area-add":
        result = create_area(nome=args.nome, cultura=args.cultura, hectares=args.hectares)
        print(json.dumps(result, indent=2, ensure_ascii=True))
        return

    if args.command == "area-update":
        result = update_area(area_id=args.id, nome=args.nome, cultura=args.cultura, hectares=args.hectares)
        print(json.dumps(result, indent=2, ensure_ascii=True))
        return

    if args.command == "area-delete":
        result = delete_area(area_id=args.id)
        print(json.dumps(result, indent=2, ensure_ascii=True))


if __name__ == "__main__":
    main()
