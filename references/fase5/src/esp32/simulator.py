import json
import random
import time
from datetime import datetime, timezone
from typing import Dict, Optional, Tuple
from urllib import error, request


def validate_reading(data: Dict) -> Tuple[bool, Optional[str]]:
    required = ["device_id", "timestamp", "temperatura", "umidade_ar", "umidade_solo_raw"]
    for key in required:
        if key not in data:
            return False, f"campo ausente: {key}"

    if not (-20 <= data["temperatura"] <= 70):
        return False, "temperatura fora da faixa"
    if not (0 <= data["umidade_ar"] <= 100):
        return False, "umidade do ar fora da faixa"
    if not (0 <= data["umidade_solo_raw"] <= 4095):
        return False, "umidade do solo raw fora da faixa"

    return True, None


class ESP32FarmSimulator:
    def __init__(self, device_id: str = "ESP32_FARM_001"):
        self.device_id = device_id
        self.sequence = 0

    def read_once(self) -> Dict:
        self.sequence += 1

        payload = {
            "device_id": self.device_id,
            "seq": self.sequence,
            "timestamp": datetime.now(timezone.utc).isoformat(),
            "temperatura": round(random.uniform(18.0, 36.0), 2),
            "umidade_ar": round(random.uniform(35.0, 95.0), 2),
            "umidade_solo_raw": random.randint(900, 3200),
        }

        ok, error_message = validate_reading(payload)
        payload["valid"] = ok
        if not ok:
            payload["error"] = error_message

        return payload


def post_json(url: str, payload: Dict, timeout: int = 10) -> Tuple[bool, str]:
    body = json.dumps(payload).encode("utf-8")
    req = request.Request(url=url, data=body, method="POST")
    req.add_header("Content-Type", "application/json")

    try:
        with request.urlopen(req, timeout=timeout) as response:
            return True, f"HTTP {response.status}"
    except error.HTTPError as exc:
        return False, f"HTTP {exc.code}"
    except Exception as exc:
        return False, f"erro: {exc}"


def run(endpoint: str, interval_seconds: int = 10, max_readings: int = 10):
    simulator = ESP32FarmSimulator()

    print("=== Simulador ESP32 FarmTech ===")
    print(f"Endpoint: {endpoint}")
    print(f"Intervalo: {interval_seconds}s | Leituras: {max_readings}")

    for _ in range(max_readings):
        packet = simulator.read_once()
        print(f"\n[Leitura {packet['seq']}] {json.dumps(packet, ensure_ascii=False)}")

        if packet["valid"]:
            ok, result = post_json(endpoint, packet)
            print(f"Envio: {'OK' if ok else 'FALHA'} | {result}")
        else:
            print("Envio: ignorado (payload inválido)")

        time.sleep(interval_seconds)


if __name__ == "__main__":
    API_ENDPOINT = "http://localhost:8000/sensores"
    run(endpoint=API_ENDPOINT, interval_seconds=5, max_readings=5)
