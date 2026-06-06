"""Cockpit Operacional - Mission Control da FarmTech (Fase 7).

Esta pagina opera o pipeline REAL end-to-end que interliga todas as fases:

    Fase 1-2 (areas) -> Fase 3 (telemetria) -> Fase 4 (ML)
    -> Motor de decisao -> Fase 5 (alertas) -> Fase 6 (visao)

Toda a logica vem de services.orchestrator.run_pipeline (backend unico,
o mesmo usado pela CLI `python cli.py pipeline`). Nada aqui e mock.
"""

from __future__ import annotations

import sys
import time
from datetime import datetime
from pathlib import Path

import pandas as pd
import plotly.graph_objects as go
import streamlit as st

# Garante imports absolutos a partir da raiz do projeto.
ROOT = Path(__file__).resolve().parents[2]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from services.healthcheck import collect_health
from services.orchestrator import alerts_history, run_pipeline


st.set_page_config(
    page_title="FarmTech \u2022 Cockpit Operacional",
    layout="wide",
    page_icon=":satellite:",
    initial_sidebar_state="expanded",
)


# ============================== DESIGN SYSTEM ============================== #
st.markdown(
    """
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800;900&family=JetBrains+Mono:wght@500;600&display=swap');

    :root {
        --bg-1:#070b14; --bg-2:#0d1424; --bg-3:#131c33; --bg-4:#1a2440;
        --line:rgba(148,163,184,0.12); --line-2:rgba(148,163,184,0.22);
        --ink:#f1f5f9; --ink-2:#cbd5e1; --muted:#94a3b8;
        --green:#10b981; --green-2:#34d399; --amber:#f59e0b;
        --red:#ef4444; --blue:#3b82f6; --violet:#8b5cf6;
    }
    html, body, [class*="css"] {font-family:'Inter',sans-serif !important; letter-spacing:-0.005em;}
    .stApp {background:radial-gradient(1200px 800px at 85% -20%, rgba(16,185,129,0.08), transparent 60%), var(--bg-1);}
    .block-container {padding-top:1rem; padding-bottom:4rem; max-width:1500px;}
    header[data-testid="stHeader"] {background:transparent;}
    code, pre {font-family:'JetBrains Mono',monospace !important;}

    .mc-top {
        display:flex; align-items:center; justify-content:space-between;
        padding:16px 24px; border:1px solid var(--line); border-radius:16px;
        background:linear-gradient(180deg, var(--bg-3), var(--bg-2));
        box-shadow:0 14px 34px rgba(0,0,0,0.45);
    }
    .mc-brand {display:flex; align-items:center; gap:16px;}
    .mc-logo {
        width:46px; height:46px; border-radius:13px;
        background:conic-gradient(from 200deg, #10b981, #34d399, #3b82f6, #10b981);
        display:grid; place-items:center; color:#04140d; font-weight:900; font-size:1.2rem;
        box-shadow:0 8px 24px rgba(16,185,129,0.45); border:1px solid rgba(255,255,255,0.2);
    }
    .mc-brand .t {color:var(--ink); font-size:1.12rem; font-weight:800;}
    .mc-brand .s {color:var(--muted); font-size:0.78rem; margin-top:2px;}
    .mc-brand .t .ac {color:var(--green-2);}
    .mc-chips {display:flex; gap:8px; flex-wrap:wrap; justify-content:flex-end;}
    .chip {display:inline-flex; align-items:center; gap:7px; padding:6px 12px; border-radius:999px;
           font-size:0.74rem; font-weight:700; background:rgba(255,255,255,0.04);
           border:1px solid var(--line); color:var(--muted);}
    .chip .d {width:7px; height:7px; border-radius:50%; background:var(--muted);}
    .chip.ok {color:var(--green-2); border-color:rgba(52,211,153,0.45); background:rgba(16,185,129,0.10);}
    .chip.ok .d {background:var(--green-2); box-shadow:0 0 0 4px rgba(52,211,153,0.16);}
    .chip.warn {color:var(--amber); border-color:rgba(245,158,11,0.45); background:rgba(245,158,11,0.10);}
    .chip.warn .d {background:var(--amber);}

    .verdict {
        margin-top:18px; padding:28px 30px; border-radius:20px; position:relative; overflow:hidden;
        border:1px solid var(--line);
    }
    .verdict.irrigar  {background:linear-gradient(135deg, rgba(59,130,246,0.18), rgba(13,20,36,0.7)); border-color:rgba(59,130,246,0.45);}
    .verdict.monitorar{background:linear-gradient(135deg, rgba(245,158,11,0.18), rgba(13,20,36,0.7)); border-color:rgba(245,158,11,0.45);}
    .verdict.manter   {background:linear-gradient(135deg, rgba(16,185,129,0.18), rgba(13,20,36,0.7)); border-color:rgba(52,211,153,0.45);}
    .verdict .eyebrow {font-size:0.74rem; font-weight:800; letter-spacing:0.18em; text-transform:uppercase; color:var(--ink-2);}
    .verdict h1 {margin:8px 0 6px 0; font-size:3rem; font-weight:900; letter-spacing:-0.02em; line-height:1;}
    .verdict.irrigar h1 {color:#93c5fd;} .verdict.monitorar h1 {color:#fcd34d;} .verdict.manter h1 {color:#6ee7b7;}
    .verdict p {margin:6px 0 0 0; color:var(--ink-2); font-size:1rem; max-width:880px; line-height:1.5;}
    .verdict .meta {display:flex; gap:10px; flex-wrap:wrap; margin-top:16px;}
    .verdict .pill {display:inline-flex; align-items:center; gap:7px; padding:6px 13px; border-radius:999px;
                    font-size:0.8rem; font-weight:700; background:rgba(255,255,255,0.06);
                    border:1px solid var(--line-2); color:var(--ink);}

    .kpi {background:linear-gradient(180deg, var(--bg-3), var(--bg-2)); border:1px solid var(--line);
          border-radius:14px; padding:16px 18px; height:100%; transition:all .2s ease;}
    .kpi:hover {border-color:rgba(52,211,153,0.45); transform:translateY(-2px); box-shadow:0 14px 30px rgba(0,0,0,0.4);}
    .kpi .l {color:var(--muted); font-size:0.74rem; font-weight:700; letter-spacing:0.04em; text-transform:uppercase;}
    .kpi .v {color:var(--ink); font-size:1.55rem; font-weight:800; letter-spacing:-0.02em; margin-top:6px;}
    .kpi .ic {float:right; opacity:0.5; font-size:1.2rem;}

    .step {
        display:grid; grid-template-columns:54px 1fr auto; gap:16px; align-items:center;
        padding:14px 18px; border-radius:13px; margin:8px 0;
        background:linear-gradient(180deg, var(--bg-3), var(--bg-2)); border:1px solid var(--line);
        position:relative;
    }
    .step::before {content:""; position:absolute; left:0; top:10px; bottom:10px; width:3px; border-radius:3px;}
    .step.ok::before    {background:var(--green-2);}
    .step.skip::before  {background:var(--amber);}
    .step.error::before {background:var(--red);}
    .step .num {width:40px; height:40px; border-radius:11px; display:grid; place-items:center;
                font-weight:900; font-size:1rem; color:#04140d;
                background:linear-gradient(135deg, #10b981, #34d399);}
    .step.skip .num  {background:linear-gradient(135deg, #f59e0b, #fbbf24);}
    .step.error .num {background:linear-gradient(135deg, #ef4444, #f87171); color:#fff;}
    .step .phase {color:var(--green-2); font-size:0.68rem; font-weight:800; letter-spacing:0.10em; text-transform:uppercase;}
    .step .ttl {color:var(--ink); font-weight:800; font-size:1rem; margin:2px 0;}
    .step .dt {color:var(--muted); font-size:0.86rem; line-height:1.4;}
    .step .badge {padding:5px 12px; border-radius:999px; font-weight:800; font-size:0.74rem;}
    .step.ok .badge    {color:#04140d; background:var(--green-2);}
    .step.skip .badge  {color:#42210b; background:var(--amber);}
    .step.error .badge {color:#fff; background:var(--red);}

    .card {background:linear-gradient(180deg, var(--bg-3), var(--bg-2)); border:1px solid var(--line);
           border-radius:14px; padding:18px 20px; height:100%;}
    .card h4 {margin:6px 0; color:var(--ink); font-size:1rem; font-weight:800;}
    .card p {margin:0; color:var(--muted); font-size:0.88rem; line-height:1.5;}
    .tag {display:inline-block; padding:3px 10px; border-radius:999px; background:rgba(16,185,129,0.12);
          color:var(--green-2); font-size:0.66rem; font-weight:800; letter-spacing:0.08em; text-transform:uppercase;
          border:1px solid rgba(52,211,153,0.25);}
    .tag.blue {background:rgba(59,130,246,0.12); color:#93c5fd; border-color:rgba(59,130,246,0.3);}
    .tag.amber {background:rgba(245,158,11,0.14); color:#fcd34d; border-color:rgba(245,158,11,0.3);}

    .sect {display:flex; align-items:center; gap:10px; margin:22px 0 8px 0; color:var(--ink);
           font-size:1.08rem; font-weight:800;}
    .sect .b {width:3px; height:18px; background:var(--green-2); border-radius:2px;}

    .stButton > button[kind="primary"] {
        background:linear-gradient(135deg, #10b981, #34d399); color:#ffffff !important; border:0;
        font-weight:900; font-size:1rem; padding:12px 18px; border-radius:12px;
        box-shadow:0 12px 30px rgba(16,185,129,0.4);
    }
    .stButton > button[kind="primary"]:hover {filter:brightness(1.08); transform:translateY(-2px);}
    [data-testid="stSidebar"] {background:linear-gradient(180deg, var(--bg-3), var(--bg-2)); border-right:1px solid var(--line);}
    [data-testid="stSidebar"] label {color:var(--ink-2) !important; font-weight:600;}
    [data-testid="stProgress"] > div > div > div {background:linear-gradient(90deg, var(--green), var(--green-2)) !important;}
    .footer {color:var(--muted); font-size:0.78rem; text-align:center; margin-top:30px; padding-top:18px; border-top:1px solid var(--line);}
    </style>
    """,
    unsafe_allow_html=True,
)


GREEN = "#34d399"
BLUE = "#60a5fa"
AMBER = "#fbbf24"
RED = "#f87171"
MUTED = "#94a3b8"


def _gauge(value, title, vmin, vmax, good_band, danger_high=None):
    """Cria um gauge de telemetria com faixa saudavel destacada."""
    val = float(value) if isinstance(value, (int, float)) else 0.0
    steps = [
        {"range": [vmin, good_band[0]], "color": "rgba(248,113,113,0.25)"},
        {"range": [good_band[0], good_band[1]], "color": "rgba(52,211,153,0.30)"},
        {"range": [good_band[1], vmax], "color": "rgba(251,191,36,0.22)"},
    ]
    fig = go.Figure(go.Indicator(
        mode="gauge+number",
        value=val,
        title={"text": title, "font": {"size": 14, "color": "#cbd5e1"}},
        number={"font": {"size": 30, "color": "#f1f5f9"}},
        gauge={
            "axis": {"range": [vmin, vmax], "tickcolor": MUTED, "tickfont": {"color": MUTED, "size": 10}},
            "bar": {"color": GREEN, "thickness": 0.28},
            "bgcolor": "rgba(0,0,0,0)",
            "borderwidth": 0,
            "steps": steps,
            "threshold": {
                "line": {"color": RED if danger_high else BLUE, "width": 3},
                "thickness": 0.8,
                "value": danger_high if danger_high else good_band[0],
            },
        },
    ))
    fig.update_layout(
        paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)",
        height=220, margin=dict(l=18, r=18, t=42, b=8),
        font=dict(family="Inter, sans-serif"),
    )
    return fig


# ============================== HEALTH / TOP BAR ============================== #
health = collect_health()
aws_ok = bool(health.get("aws_configured"))
oracle_ok = bool(health.get("oracle_configured"))
env = (health.get("app_env") or "?").upper()
build_ts = datetime.utcnow().strftime("%d/%m/%Y %H:%M")

st.markdown(
    f"""
    <div class="mc-top">
      <div class="mc-brand">
        <div class="mc-logo">FT</div>
        <div>
          <div class="t">FarmTech <span class="ac">Mission Control</span></div>
          <div class="s">Cockpit operacional &middot; pipeline interligado &middot; build {build_ts} UTC</div>
        </div>
      </div>
      <div class="mc-chips">
        <span class="chip ok"><span class="d"></span>sistema operante</span>
        <span class="chip">env &middot; {env}</span>
        <span class="chip {'ok' if oracle_ok else 'warn'}"><span class="d"></span>Oracle {'on' if oracle_ok else 'csv fallback'}</span>
        <span class="chip {'ok' if aws_ok else 'warn'}"><span class="d"></span>AWS {'SNS' if aws_ok else 'dry-run'}</span>
      </div>
    </div>
    """,
    unsafe_allow_html=True,
)


# ============================== SIDEBAR ============================== #
with st.sidebar:
    st.markdown("### \U0001F6F0\ufe0f  Controles de missao")
    st.caption("Executa o fluxo real Fase 1-2 \u2192 3 \u2192 4 \u2192 5 \u2192 6.")
    limit = st.slider("Janela de telemetria", 5, 100, 20, 5)
    send_alerts = st.toggle("Despachar alertas (Fase 5)", value=True)
    include_vision = st.toggle("Incluir visao (Fase 6)", value=True)
    images_dir = st.text_input("Pasta de imagens", value="data/images")
    st.divider()
    run_now = st.button("\u25B6  Executar ciclo operacional", type="primary", use_container_width=True)
    st.caption("Cada clique roda o pipeline completo e registra no historico.")


# ============================== EXECUCAO ============================== #
def _kpi(col, label, value, icon=""):
    col.markdown(
        f"<div class='kpi'><span class='ic'>{icon}</span><div class='l'>{label}</div>"
        f"<div class='v'>{value}</div></div>",
        unsafe_allow_html=True,
    )


def _section(title):
    st.markdown(f"<div class='sect'><span class='b'></span>{title}</div>", unsafe_allow_html=True)


# Roda automaticamente na primeira carga para nunca exibir tela vazia (ideal para video).
if "cockpit_result" not in st.session_state or run_now:
    prog = st.progress(0, text="Inicializando pipeline...")
    prog.progress(20, text="Fase 1-2 / 3: contexto e telemetria...")
    result = run_pipeline(
        limit=limit,
        send_alerts=send_alerts,
        include_vision=include_vision,
        images_dir=images_dir or None,
    )
    prog.progress(80, text="Fase 4 / decisao / Fase 5-6...")
    time.sleep(0.15)
    prog.progress(100, text="Ciclo concluido")
    time.sleep(0.2)
    prog.empty()
    st.session_state["cockpit_result"] = result

result = st.session_state["cockpit_result"]
decision = result.get("decision", {})
context = result.get("context", {})
telemetry = result.get("telemetry", {})
trace = result.get("trace", [])
rule_alerts = result.get("rule_alerts", [])
dispatched = result.get("dispatched_alerts", [])
vision = result.get("vision", {})
ml = result.get("ml", {})


# ============================== VEREDITO ============================== #
verdict = decision.get("verdict", "MANTER")
vclass = {"IRRIGAR": "irrigar", "MONITORAR": "monitorar", "MANTER": "manter"}.get(verdict, "manter")
vicon = {"IRRIGAR": "\U0001F4A7", "MONITORAR": "\U0001F440", "MANTER": "\U0001F331"}.get(verdict, "\U0001F331")
prob = decision.get("ml_probability")
prob_txt = f"{prob:.0%}" if isinstance(prob, (int, float)) else "n/d"
agree = decision.get("agreement")

st.markdown(
    f"""
    <div class="verdict {vclass}">
      <div class="eyebrow">Decisao do motor operacional</div>
      <h1>{vicon} {verdict}</h1>
      <p>{decision.get('rationale', '')}</p>
      <div class="meta">
        <span class="pill">Confianca: <b>&nbsp;{decision.get('confidence', '?')}</b></span>
        <span class="pill">Regra Fase 3: <b>&nbsp;{'aciona' if decision.get('rule_signal') else 'neutra'}</b></span>
        <span class="pill">ML Fase 4: <b>&nbsp;{'irrigar' if decision.get('ml_signal') else 'manter'}</b> ({prob_txt})</span>
        <span class="pill">Consenso regra+ML: <b>&nbsp;{'SIM' if agree else 'divergente'}</b></span>
      </div>
    </div>
    """,
    unsafe_allow_html=True,
)

st.write("")

# ============================== KPIs ============================== #
c1, c2, c3, c4, c5 = st.columns(5)
_kpi(c1, "Areas monitoradas", str(context.get("areas", 0)), "\U0001F5FA\ufe0f")
_kpi(c2, "Hectares", f"{context.get('total_hectares', 0)}", "\U0001F33E")
_kpi(c3, "Fonte de dados", str(context.get("data_source", "?")), "\U0001F4E1")
_kpi(c4, "Alertas no ciclo", str(len(dispatched)), "\U0001F6A8")
_kpi(c5, "Leituras", str(telemetry.get("total_readings", 0)), "\U0001F4CA")


# ============================== TELEMETRIA (FASE 3) ============================== #
_section("Telemetria ao vivo \u00b7 Fase 3")
latest = telemetry.get("latest") or {}
g1, g2, g3 = st.columns(3)
g1.plotly_chart(
    _gauge(latest.get("umidade_solo"), "Umidade do solo (%)", 0, 100, (25, 60)),
    use_container_width=True,
)
g2.plotly_chart(
    _gauge(latest.get("temperatura"), "Temperatura (C)", 0, 50, (15, 32), danger_high=35),
    use_container_width=True,
)
g3.plotly_chart(
    _gauge(latest.get("ph_solo"), "pH do solo", 0, 14, (5.5, 7.5)),
    use_container_width=True,
)


# ============================== DECISION TRACE ============================== #
_section("Rastro de decisao \u00b7 pipeline interligado")
for step in trace:
    status = step.get("status", "ok")
    sclass = status if status in {"ok", "skip", "error"} else "ok"
    badge = {"ok": "OK", "skip": "PULADO", "error": "ERRO"}.get(sclass, "OK")
    st.markdown(
        f"""
        <div class="step {sclass}">
          <div class="num">{step.get('step', '?')}</div>
          <div>
            <div class="phase">{step.get('phase', '')}</div>
            <div class="ttl">{step.get('title', '')}</div>
            <div class="dt">{step.get('detail', '')}</div>
          </div>
          <div class="badge">{badge}</div>
        </div>
        """,
        unsafe_allow_html=True,
    )


# ============================== REGRA x ML + ALERTAS ============================== #
colL, colR = st.columns([1, 1])

with colL:
    _section("Consenso regra \u00d7 modelo")
    rule_sig = 1 if decision.get("rule_signal") else 0
    ml_sig = 1 if decision.get("ml_signal") else 0
    comp = pd.DataFrame({
        "fonte": ["Regra Fase 3", "Modelo Fase 4"],
        "sinal": [rule_sig, ml_sig],
    })
    fig = go.Figure(go.Bar(
        x=comp["fonte"], y=comp["sinal"],
        marker_color=[BLUE, GREEN],
        text=["aciona" if rule_sig else "neutra", "irrigar" if ml_sig else "manter"],
        textposition="outside",
    ))
    fig.update_layout(
        paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)",
        height=300, margin=dict(l=10, r=10, t=20, b=10),
        yaxis=dict(range=[0, 1.3], showticklabels=False, gridcolor="rgba(148,163,184,0.1)"),
        font=dict(family="Inter, sans-serif", color="#cbd5e1"),
    )
    st.plotly_chart(fig, use_container_width=True)

with colR:
    _section("Alertas despachados \u00b7 Fase 5")
    if dispatched:
        rows = []
        for d in dispatched:
            payload = d.get("payload", {})
            rows.append({
                "status": d.get("status", "?"),
                "metrica": payload.get("metric", "?"),
                "valor": payload.get("value", "?"),
                "acao": payload.get("action", "?"),
            })
        st.dataframe(pd.DataFrame(rows), use_container_width=True, hide_index=True)
    else:
        st.markdown(
            "<div class='card'><span class='tag'>Tudo sob controle</span>"
            "<h4>\u2705 Nenhum alerta necessario</h4>"
            "<p>Sensores dentro dos limites operacionais neste ciclo. "
            "O motor nao despachou mensageria.</p></div>",
            unsafe_allow_html=True,
        )


# ============================== VISAO (FASE 6) ============================== #
if vision:
    _section("Visao computacional \u00b7 Fase 6")
    counts = vision.get("counts", {})
    if counts:
        vc = pd.DataFrame([{"classe": k, "qtd": v} for k, v in counts.items() if v])
        if not vc.empty:
            cV1, cV2 = st.columns([1, 2])
            fig_v = go.Figure(go.Pie(
                labels=vc["classe"], values=vc["qtd"], hole=0.6,
                marker=dict(colors=[GREEN, AMBER, RED, BLUE, "#a78bfa"]),
            ))
            fig_v.update_layout(
                paper_bgcolor="rgba(0,0,0,0)", height=300,
                margin=dict(l=10, r=10, t=10, b=10),
                font=dict(family="Inter, sans-serif", color="#cbd5e1"),
            )
            cV1.plotly_chart(fig_v, use_container_width=True)
            cV2.metric("Imagens analisadas", vision.get("total_images", 0))
            cV2.metric("Possivel estresse", counts.get("possivel_estresse", 0))


# ============================== HISTORICO DE CICLOS ============================== #
_section("Historico de ciclos operacionais")
hist = alerts_history(limit=60).get("items", [])
pipe_runs = [h for h in hist if h.get("type") == "pipeline_e2e"]
if pipe_runs:
    hdf = pd.DataFrame(pipe_runs)
    if "verdict" in hdf.columns:
        vc = hdf["verdict"].value_counts().reset_index()
        vc.columns = ["verdict", "qtd"]
        cH1, cH2 = st.columns([1, 2])
        color_map = {"IRRIGAR": BLUE, "MONITORAR": AMBER, "MANTER": GREEN}
        fig_h = go.Figure(go.Bar(
            x=vc["verdict"], y=vc["qtd"],
            marker_color=[color_map.get(v, MUTED) for v in vc["verdict"]],
            text=vc["qtd"], textposition="outside",
        ))
        fig_h.update_layout(
            paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)",
            height=280, margin=dict(l=10, r=10, t=20, b=10),
            font=dict(family="Inter, sans-serif", color="#cbd5e1"),
            yaxis=dict(gridcolor="rgba(148,163,184,0.1)"),
        )
        cH1.plotly_chart(fig_h, use_container_width=True)
        show_cols = [c for c in ["timestamp", "verdict", "confidence", "agreement", "alerts_count", "data_source"] if c in hdf.columns]
        cH2.dataframe(hdf[show_cols].iloc[::-1], use_container_width=True, hide_index=True)
else:
    st.info("Execute o primeiro ciclo para comecar o historico.")

with st.expander("Resposta completa do pipeline (JSON)"):
    st.json(result)

st.markdown(
    "<div class='footer'>FarmTech Solutions \u00b7 Fase 7 \u00b7 Cockpit Operacional"
    "<span style='margin:0 8px;'>\u2022</span>backend unico: services.orchestrator.run_pipeline "
    "(mesmo da CLI <code>python cli.py pipeline</code>)</div>",
    unsafe_allow_html=True,
)
