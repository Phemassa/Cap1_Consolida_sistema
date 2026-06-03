from services.orchestrator import run_phase


def test_run_phase_smoke() -> None:
    result = run_phase("fase3")
    assert result["status"] == "ok"
