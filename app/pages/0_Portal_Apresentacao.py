from __future__ import annotations

import time
from datetime import datetime

import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import streamlit as st

from services.alert_service import AlertService
from services.healthcheck import collect_health
from services.orchestrator import (
    alerts_history,
    create_area,
    delete_area,
    infer_fase4,
    monitor_now,
    run_fase6_vision,
    run_phase,
    train_fase4,
)


st.set_page_config(
    page_title="FarmTech \u2022 Operations Console",
    layout="wide",
    page_icon=":seedling:",
    initial_sidebar_state="expanded",
)


# ============================== DESIGN SYSTEM ============================== #
st.markdown(
    """
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800;900&family=JetBrains+Mono:wght@500;600&display=swap');

    :root {
        --bg-1:        #070b14;
        --bg-2:        #0d1424;
        --bg-3:        #131c33;
        --bg-4:        #1a2440;
        --line:        rgba(148, 163, 184, 0.12);
        --line-strong: rgba(148, 163, 184, 0.22);
        --ink:         #f1f5f9;
        --ink-2:       #cbd5e1;
        --muted:       #94a3b8;
        --green:       #10b981;
        --green-2:     #34d399;
        --green-soft:  rgba(16, 185, 129, 0.12);
        --amber:       #f59e0b;
        --red:         #ef4444;
        --blue:        #3b82f6;
        --violet:      #8b5cf6;
    }

    html, body, [class*="css"] {
        font-family: 'Inter', -apple-system, BlinkMacSystemFont, "Segoe UI", sans-serif !important;
        letter-spacing: -0.005em;
    }
    .stApp {background: radial-gradient(1200px 800px at 80% -20%, rgba(16,185,129,0.08), transparent 60%), var(--bg-1);}
    .block-container {padding-top: 1rem; padding-bottom: 4rem; max-width: 1480px;}
    header[data-testid="stHeader"] {background: transparent;}

    code, pre {font-family: 'JetBrains Mono', monospace !important;}
    [data-testid="stMarkdownContainer"] code {
        background: rgba(16,185,129,0.10); color: var(--green-2);
        padding: 1px 7px; border-radius: 5px; font-size: 0.85em;
    }

    /* ---------- Top bar ---------- */
    .topbar {
        display: flex; align-items: center; justify-content: space-between;
        padding: 14px 22px; border: 1px solid var(--line);
        border-radius: 14px;
        background: linear-gradient(180deg, var(--bg-3) 0%, var(--bg-2) 100%);
        box-shadow: 0 12px 30px rgba(0,0,0,0.45);
    }
    .brand {display: flex; align-items: center; gap: 14px;}
    .brand .logo {
        width: 42px; height: 42px; border-radius: 12px;
        background: conic-gradient(from 220deg, #10b981, #34d399, #10b981);
        display: grid; place-items: center; color: #052e16; font-weight: 900;
        font-size: 1.1rem; box-shadow: 0 8px 22px rgba(16,185,129,0.4);
        border: 1px solid rgba(255,255,255,0.18);
    }
    .brand .name {color: var(--ink); font-size: 1.05rem; font-weight: 800; letter-spacing: -0.01em;}
    .brand .sub  {color: var(--muted); font-size: 0.78rem; margin-top: 2px;}
    .brand .name .accent {color: var(--green-2);}

    .topbar-actions {display: flex; gap: 8px; align-items: center; flex-wrap: wrap; justify-content: flex-end;}
    .chip {
        display: inline-flex; align-items: center; gap: 7px;
        padding: 6px 11px; border-radius: 999px;
        font-size: 0.75rem; font-weight: 600;
        background: rgba(255,255,255,0.04); border: 1px solid var(--line);
        color: var(--muted);
    }
    .chip .dot {width: 7px; height: 7px; border-radius: 50%; background: var(--muted);}
    .chip.ok    {color: var(--green-2); border-color: rgba(52,211,153,0.45);
                 background: rgba(16,185,129,0.10);}
    .chip.ok    .dot {background: var(--green-2); box-shadow: 0 0 0 4px rgba(52,211,153,0.18);}
    .chip.warn  {color: var(--amber);   border-color: rgba(245,158,11,0.45);
                 background: rgba(245,158,11,0.10);}
    .chip.warn  .dot {background: var(--amber);}
    .chip.off   {color: var(--red);     border-color: rgba(239,68,68,0.45);
                 background: rgba(239,68,68,0.10);}
    .chip.off   .dot {background: var(--red);}

    /* ---------- Hero ---------- */
    .hero {
        margin-top: 18px; padding: 30px 32px; border-radius: 18px;
        position: relative; overflow: hidden;
        background:
            radial-gradient(800px 300px at 100% 0%, rgba(16,185,129,0.18), transparent 60%),
            radial-gradient(600px 240px at 0% 100%, rgba(59,130,246,0.10), transparent 60%),
            linear-gradient(180deg, var(--bg-3) 0%, var(--bg-2) 100%);
        border: 1px solid var(--line);
    }
    .hero .eyebrow {
        font-size: 0.74rem; font-weight: 800; letter-spacing: 0.18em; text-transform: uppercase;
        color: var(--green-2); display: inline-flex; align-items: center; gap: 8px;
        background: var(--green-soft); padding: 5px 11px; border-radius: 999px;
        border: 1px solid rgba(52,211,153,0.35);
    }
    .hero h1 {
        margin: 14px 0 10px 0; color: var(--ink);
        font-size: 2.2rem; font-weight: 800; line-height: 1.15;
        letter-spacing: -0.015em;
    }
    .hero h1 .grad {
        background: linear-gradient(90deg, #34d399, #60a5fa);
        -webkit-background-clip: text; background-clip: text; color: transparent;
    }
    .hero p {margin: 0; color: var(--ink-2); max-width: 820px; font-size: 1rem; line-height: 1.55;}
    .hero .stack {display:flex; gap:8px; flex-wrap:wrap; margin-top: 18px;}
    .hero .pill {
        display:inline-flex; align-items:center; gap:6px;
        padding: 5px 11px; border-radius: 999px; font-size: 0.78rem; font-weight: 600;
        background: rgba(255,255,255,0.05); color: var(--ink-2);
        border: 1px solid var(--line);
    }
    .hero .pill .b {color: var(--green-2);}

    /* ---------- KPI ---------- */
    .kpi {
        background: linear-gradient(180deg, var(--bg-3), var(--bg-2));
        border: 1px solid var(--line); border-radius: 14px;
        padding: 16px 18px; transition: all .2s ease;
        height: 100%;
    }
    .kpi:hover {border-color: rgba(52,211,153,0.45); transform: translateY(-2px);
                box-shadow: 0 14px 30px rgba(0,0,0,0.4);}
    .kpi .label {color: var(--muted); font-size: 0.78rem; font-weight: 600;
                 letter-spacing: 0.04em; text-transform: uppercase; margin-bottom: 8px;}
    .kpi .value {color: var(--ink); font-size: 1.6rem; font-weight: 800; letter-spacing: -0.02em;}
    .kpi .delta {color: var(--green-2); font-size: 0.78rem; font-weight: 600; margin-top: 4px;}
    .kpi .icon  {float: right; opacity: 0.55; font-size: 1.2rem;}

    /* ---------- Card ---------- */
    .card {
        background: linear-gradient(180deg, var(--bg-3), var(--bg-2));
        border: 1px solid var(--line); border-radius: 14px;
        padding: 18px 20px; height: 100%;
        transition: all .2s ease;
    }
    .card:hover {border-color: rgba(52,211,153,0.30); transform: translateY(-1px);}
    .card h4 {margin: 6px 0; color: var(--ink); font-size: 1rem; font-weight: 700;}
    .card p  {margin: 0; color: var(--muted); font-size: 0.88rem; line-height: 1.5;}
    .tag {
        display: inline-block; padding: 3px 9px; border-radius: 999px;
        background: var(--green-soft); color: var(--green-2);
        font-size: 0.68rem; font-weight: 800; letter-spacing: 0.08em; text-transform: uppercase;
        border: 1px solid rgba(52,211,153,0.25);
    }
    .tag.blue   {background: rgba(59,130,246,0.12); color:#93c5fd; border-color: rgba(59,130,246,0.3);}
    .tag.violet {background: rgba(139,92,246,0.14); color:#c4b5fd; border-color: rgba(139,92,246,0.3);}
    .tag.amber  {background: rgba(245,158,11,0.14); color:#fcd34d; border-color: rgba(245,158,11,0.3);}

    /* ---------- Script / Step ---------- */
    .script {
        position: relative;
        display: grid; grid-template-columns: 150px 1fr; gap: 20px;
        padding: 18px 20px; border-radius: 14px;
        background: linear-gradient(180deg, var(--bg-3), var(--bg-2));
        border: 1px solid var(--line); margin: 6px 0 18px 0;
        overflow: hidden;
    }
    .script::before {
        content: ""; position: absolute; left: 0; top: 0; bottom: 0; width: 3px;
        background: linear-gradient(180deg, var(--green), var(--green-2));
    }
    .script .timecol {
        color: var(--green-2); font-weight: 800;
        font-size: 0.78rem; letter-spacing: 0.10em; text-transform: uppercase;
        font-family: 'JetBrains Mono', monospace; padding-top: 2px;
    }
    .script .title {color: var(--ink); font-weight: 800; font-size: 1.05rem;
                    letter-spacing: -0.01em; margin-bottom: 8px;}
    .script .narration {
        color: var(--ink-2); font-size: 0.92rem; line-height: 1.55;
        background: rgba(255,255,255,0.03); border-left: 2px solid var(--green-2);
        padding: 10px 14px; border-radius: 8px; margin: 6px 0 10px 0;
        font-style: italic;
    }
    .script .narration::before {content: "\\201C"; color: var(--green-2); font-size: 1.4rem;
                                margin-right: 4px; font-weight: 800;}
    .script .narration::after  {content: "\\201D"; color: var(--green-2); font-size: 1.4rem;
                                margin-left: 4px; font-weight: 800;}
    .script .action {color: var(--ink-2); font-size: 0.86rem;}
    .script .action .lbl {color: var(--green-2); font-weight: 700; letter-spacing: 0.04em;
                          text-transform: uppercase; font-size: 0.72rem; margin-right: 6px;}

    .kbd {
        background: rgba(255,255,255,0.06); border: 1px solid var(--line-strong);
        border-radius: 6px; padding: 2px 8px; font-family: 'JetBrains Mono', monospace;
        font-size: 0.78rem; color: var(--ink); font-weight: 600;
    }

    /* ---------- Badges ---------- */
    .badge       {padding: 4px 11px; border-radius: 8px; font-weight: 800; font-size: 0.78rem;
                  letter-spacing: 0.02em;}
    .badge.ok    {color: #052e16; background: var(--green-2);}
    .badge.warn  {color: #422006; background: var(--amber);}
    .badge.off   {color: #450a0a; background: var(--red);}

    /* ---------- Tabs ---------- */
    .stTabs [data-baseweb="tab-list"] {
        gap: 4px; background: var(--bg-3);
        padding: 6px; border: 1px solid var(--line); border-radius: 14px;
        margin-bottom: 8px;
    }
    .stTabs [data-baseweb="tab"] {
        padding: 8px 16px; border-radius: 10px; color: var(--muted) !important;
        font-weight: 700; font-size: 0.86rem; letter-spacing: 0.01em;
    }
    .stTabs [data-baseweb="tab"]:hover {color: var(--ink-2) !important;}
    .stTabs [aria-selected="true"] {
        background: var(--green-soft) !important; color: var(--green-2) !important;
        box-shadow: inset 0 0 0 1px rgba(52,211,153,0.35);
    }

    /* ---------- Buttons ---------- */
    .stButton > button {
        background: var(--bg-4); color: var(--ink);
        border: 1px solid var(--line-strong); border-radius: 10px;
        padding: 9px 16px; font-weight: 700; transition: all .15s ease;
        letter-spacing: 0.01em;
    }
    .stButton > button:hover {
        border-color: var(--green-2); color: var(--green-2);
        transform: translateY(-1px); box-shadow: 0 6px 20px rgba(16,185,129,0.18);
    }
    .stButton > button[kind="primary"] {
        background: linear-gradient(135deg, #10b981, #34d399);
        color: #ffffff !important; border: 0; font-weight: 900;
        font-size: 0.95rem;
        letter-spacing: 0.01em;
        box-shadow: 0 12px 28px rgba(16,185,129,0.35);
    }
    .stButton > button[kind="primary"]:hover {
        filter: brightness(1.08); transform: translateY(-2px);
        box-shadow: 0 16px 36px rgba(16,185,129,0.45);
    }

    .sidebar-callout {
        margin: 2px 0 10px 0;
        padding: 10px 12px;
        border-radius: 10px;
        border: 1px solid rgba(52,211,153,0.35);
        background: rgba(16,185,129,0.14);
        color: #e2fef1;
        font-size: 0.86rem;
        line-height: 1.45;
        font-weight: 600;
    }
    .sidebar-callout b {
        color: #ffffff;
    }

    /* ---------- Sidebar ---------- */
    [data-testid="stSidebar"] {
        background: linear-gradient(180deg, var(--bg-3), var(--bg-2));
        border-right: 1px solid var(--line);
    }
    [data-testid="stSidebar"] h1, [data-testid="stSidebar"] h2,
    [data-testid="stSidebar"] h3, [data-testid="stSidebar"] h4 {color: var(--ink);}
    [data-testid="stSidebar"] label {color: var(--ink-2) !important; font-weight: 600;}
    [data-testid="stSidebar"] .stCaption,
    [data-testid="stSidebar"] [data-testid="stMarkdownContainer"] p {color: var(--muted);}

    /* ---------- Native metric override ---------- */
    div[data-testid="stMetric"] {
        background: linear-gradient(180deg, var(--bg-3), var(--bg-2));
        border: 1px solid var(--line); padding: 14px 16px; border-radius: 12px;
    }
    div[data-testid="stMetricLabel"] {color: var(--muted) !important; font-weight: 600 !important;
                                      letter-spacing: 0.03em; text-transform: uppercase; font-size: 0.75rem;}
    div[data-testid="stMetricValue"] {color: var(--ink) !important; font-weight: 800 !important;}

    /* ---------- Plotly ---------- */
    .js-plotly-plot {background: transparent !important;}

    /* ---------- Expander ---------- */
    details {background: var(--bg-3); border: 1px solid var(--line);
             border-radius: 10px; padding: 4px 12px; margin-top: 6px;}
    details summary {color: var(--muted); font-weight: 600; font-size: 0.82rem;}

    /* ---------- DataFrame ---------- */
    [data-testid="stDataFrame"] {border: 1px solid var(--line); border-radius: 12px; overflow: hidden;}

    /* ---------- Section title ---------- */
    .section-title {
        display: flex; align-items: center; gap: 10px;
        margin: 18px 0 8px 0; color: var(--ink);
        font-size: 1.05rem; font-weight: 800; letter-spacing: -0.01em;
    }
    .section-title .bar {width: 3px; height: 18px; background: var(--green-2); border-radius: 2px;}

    /* ---------- Footer ---------- */
    .footer {color: var(--muted); font-size: 0.78rem; text-align: center;
             margin-top: 32px; padding-top: 18px; border-top: 1px solid var(--line);}
    .footer .sep {margin: 0 8px; color: var(--line-strong);}

    /* ---------- Progress ---------- */
    [data-testid="stProgress"] > div > div > div {
        background: linear-gradient(90deg, var(--green), var(--green-2)) !important;
    }
    </style>
    """,
    unsafe_allow_html=True,
)


PLOTLY_PALETTE = ["#34d399", "#60a5fa", "#fbbf24", "#f87171", "#a78bfa", "#22d3ee"]


def _styled_fig(fig: go.Figure, height: int = 320) -> go.Figure:
    fig.update_layout(
        template="plotly_dark",
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        margin=dict(l=10, r=10, t=44, b=10),
        height=height,
        font=dict(family="Inter, sans-serif", size=12, color="#cbd5e1"),
        title_font=dict(size=14, color="#f1f5f9"),
        legend=dict(bgcolor="rgba(0,0,0,0)"),
        colorway=PLOTLY_PALETTE,
    )
    fig.update_xaxes(gridcolor="rgba(148,163,184,0.10)", linecolor="rgba(148,163,184,0.18)",
                     zerolinecolor="rgba(148,163,184,0.18)")
    fig.update_yaxes(gridcolor="rgba(148,163,184,0.10)", linecolor="rgba(148,163,184,0.18)",
                     zerolinecolor="rgba(148,163,184,0.18)")
    return fig


# ============================== HEALTH ============================== #
health = collect_health()
oracle_ok = bool(health.get("oracle_configured"))
aws_ok = bool(health.get("aws_configured"))
env = (health.get("app_env") or "?").upper()
status_label = "Operational" if health.get("status") == "ok" else "Issue"
status_class = "ok" if health.get("status") == "ok" else "off"
build_ts = datetime.utcnow().strftime("%d/%m/%Y %H:%M")


# ============================== TOP BAR ============================== #
st.markdown(
    f"""
    <div class="topbar">
      <div class="brand">
        <div class="logo">FT</div>
        <div>
          <div class="name">FarmTech <span class="accent">Solutions</span> &middot; Operations Console</div>
          <div class="sub">Fase 7 &middot; build {build_ts} UTC</div>
        </div>
      </div>
      <div class="topbar-actions">
        <span class="chip {status_class}"><span class="dot"></span>{status_label}</span>
        <span class="chip">env &middot; {env}</span>
        <span class="chip {'ok' if oracle_ok else 'off'}">
          <span class="dot"></span>Oracle {'conectado' if oracle_ok else 'offline'}
        </span>
        <span class="chip {'ok' if aws_ok else 'warn'}">
          <span class="dot"></span>AWS SNS {'ativo' if aws_ok else 'dry-run'}
        </span>
      </div>
    </div>
    """,
    unsafe_allow_html=True,
)


# ============================== HERO ============================== #
st.markdown(
    """
    <div class="hero">
      <span class="eyebrow"><span class="dot" style="width:6px;height:6px;border-radius:50%;background:#34d399;"></span> Fase 7 &middot; Plataforma Consolidada</span>
      <h1>Um console unico para <span class="grad">todo o ciclo</span> da FarmTech</h1>
      <p>Ingestao de sensores, machine learning, visao computacional e mensageria reunidos em um produto Python operavel
      por dashboard e por CLI. Use o painel lateral para rodar a demonstracao completa ou navegue pelas abas para detalhar cada fase.</p>
      <div class="stack">
        <span class="pill"><span class="b">\u2713</span> Streamlit</span>
        <span class="pill"><span class="b">\u2713</span> Scikit-learn</span>
        <span class="pill"><span class="b">\u2713</span> Oracle / CSV</span>
        <span class="pill"><span class="b">\u2713</span> AWS SNS / SES</span>
        <span class="pill"><span class="b">\u2713</span> Visao computacional</span>
        <span class="pill"><span class="b">\u2713</span> CLI integrada</span>
      </div>
    </div>
    """,
    unsafe_allow_html=True,
)

st.write("")


# ============================== SIDEBAR ============================== #
with st.sidebar:
    st.markdown("### \U0001F39B\ufe0f  Controles da apresentacao")
    st.caption("Ajuste os parametros e dispare o roteiro completo.")
    images_dir = st.text_input("Pasta de imagens (Fase 6)", value="data/images")
    monitor_limit = st.slider("Janela de monitoramento", 5, 200, 20, 5)
    train_limit = st.slider("Amostras de treino (Fase 4)", 20, 300, 120, 10)
    st.markdown("**Predicao manual**")
    pred_temp = st.number_input("Temperatura", value=30.0)
    pred_umid = st.number_input("Umidade do solo", value=22.0)
    pred_ph = st.number_input("pH do solo", value=6.0)
    st.divider()
        st.markdown(
                """
                <div class="sidebar-callout">
                    <b>Demo completa:</b> aciona todas as fases em sequencia com barra de progresso.<br>
                    Ideal para iniciar a gravacao do video.
                </div>
                """,
                unsafe_allow_html=True,
        )
    run_all = st.button("\u25B6  Rodar demo completa", type="primary", use_container_width=True)
    st.divider()
    st.markdown("### \U0001F4DA  Recursos")
    st.markdown(
        "- Roteiro do video: `docs/VIDEO_SCRIPT_10MIN.md`\n"
        "- Origem das fases: `references/README.md`\n"
        "- Setup AWS: `docs/AWS_ALERT_SETUP.md`"
    )


# ============================== KPI ROW ============================== #
def kpi(col, label: str, value: str, delta: str | None = None, icon: str = "") -> None:
    delta_html = f"<div class='delta'>\u25B2 {delta}</div>" if delta else ""
    icon_html = f"<span class='icon'>{icon}</span>" if icon else ""
    col.markdown(
        f"<div class='kpi'>{icon_html}<div class='label'>{label}</div>"
        f"<div class='value'>{value}</div>{delta_html}</div>",
        unsafe_allow_html=True,
    )


k1, k2, k3, k4 = st.columns(4)
kpi(k1, "Fases integradas",   "6 / 6", "consolidado",          icon="\U0001F9E9")
kpi(k2, "Modos de execucao",  "Dashboard + CLI", "projeto unico", icon="\U0001F5A5\ufe0f")
kpi(k3, "Modelos ML",         "3", "logistic / RF / GB",       icon="\U0001F9E0")
kpi(k4, "Mensageria",         "AWS SNS", "fallback local",      icon="\U0001F4E1")

st.write("")


# ============================== TABS ============================== #
tab_h, tab12, tab3, tab4, tab5, tab6, tab_end = st.tabs(
    [
        "\U0001F3E0  Visao Geral",
        "\U0001F4D8  Fase 1\u20132",
        "\U0001F4E1  Fase 3",
        "\U0001F9E0  Fase 4",
        "\U0001F4E8  Fase 5",
        "\U0001F441\ufe0f  Fase 6",
        "\U0001F3C1  Encerramento",
    ]
)


# ============================== HELPERS ============================== #
def step_box(time_label: str, title: str, narration: str, action_html: str = "") -> None:
    action_block = (
        f"<div class='action'><span class='lbl'>Acao</span> {action_html}</div>"
        if action_html else ""
    )
    st.markdown(
        f"""
        <div class="script">
          <div class="timecol">{time_label}</div>
          <div>
            <div class="title">{title}</div>
            <div class="narration">{narration}</div>
            {action_block}
          </div>
        </div>
        """,
        unsafe_allow_html=True,
    )


def section(title: str) -> None:
    st.markdown(
        f"<div class='section-title'><span class='bar'></span>{title}</div>",
        unsafe_allow_html=True,
    )


def _render_areas(snapshot: dict) -> None:
    areas = snapshot.get("areas", [])
    if not areas:
        st.info("Sem areas cadastradas.")
        return
    df = pd.DataFrame(areas)
    c1, c2 = st.columns([2, 3])
    with c1:
        st.dataframe(df, use_container_width=True, hide_index=True)
    with c2:
        fig = px.bar(df, x="nome", y="hectares", color="cultura", title="Hectares por area")
        st.plotly_chart(_styled_fig(fig, 320), use_container_width=True)


def _render_fase3(snapshot: dict) -> None:
    summary = snapshot.get("summary", {})
    latest = summary.get("latest", {})
    c1, c2, c3, c4 = st.columns(4)
    kpi(c1, "Leituras",        str(summary.get("total_readings", 0)),        icon="\U0001F4CA")
    kpi(c2, "Umidade media",   f"{summary.get('avg_umidade_solo', 0):.2f}",  icon="\U0001F4A7")
    kpi(c3, "Temp. media",     f"{summary.get('avg_temperatura', 0):.2f}",   icon="\U0001F321\ufe0f")
    kpi(c4, "pH medio",        f"{summary.get('avg_ph_solo', 0):.2f}",       icon="\U0001F9EA")

    if latest:
        df = pd.DataFrame(
            [
                {"metrica": "Temperatura",   "valor": latest.get("temperatura")},
                {"metrica": "Umidade solo",  "valor": latest.get("umidade_solo")},
                {"metrica": "pH solo",       "valor": latest.get("ph_solo")},
            ]
        )
        fig = px.bar(df, x="metrica", y="valor", color="metrica", text="valor",
                     title="Ultima leitura dos sensores")
        fig.update_traces(textposition="outside", textfont=dict(color="#f1f5f9", size=12))
        fig.update_layout(showlegend=False)
        st.plotly_chart(_styled_fig(fig, 340), use_container_width=True)


def _render_fase4_metrics(result: dict) -> None:
    report = result.get("report", {})
    metrics = report.get("metrics", {})
    if not metrics:
        st.info("Sem metricas. Treine os modelos primeiro.")
        return

    rows = [{"modelo": model, **{k: v for k, v in m.items() if isinstance(v, (int, float))}} for model, m in metrics.items()]
    df = pd.DataFrame(rows)
    best = report.get("best_model", "?")
    best_m = metrics.get(best, {})

    # ---- Resumo do melhor modelo + dataset ----
    cR1, cR2, cR3, cR4 = st.columns(4)
    kpi(cR1, "Melhor modelo",  best,                                          icon="\U0001F3C6")
    kpi(cR2, "Acuracia",       f"{best_m.get('accuracy', 0):.2%}",            icon="\U0001F4CF")
    kpi(cR3, "F1-score",       f"{best_m.get('f1', 0):.2%}",                  icon="\U0001F3AF")
    if best_m.get("roc"):
        kpi(cR4, "AUC ROC",    f"{best_m['roc']['auc']:.3f}",                 icon="\U0001F4C8")
    else:
        kpi(cR4, "Tempo treino", f"{best_m.get('train_ms', 0):.1f} ms",       icon="\u23F1\ufe0f")

    # ---- Comparativo ponta a ponta ----
    section("Comparativo de modelos")
    metric_cols = ["accuracy", "precision", "recall", "f1"]
    df_long = df.melt(id_vars="modelo", value_vars=metric_cols,
                      var_name="metrica", value_name="valor")
    fig = px.bar(df_long, x="modelo", y="valor", color="metrica", barmode="group",
                 title="Metricas por modelo (test set)")
    fig.update_yaxes(range=[0, 1.05], tickformat=".0%")
    st.plotly_chart(_styled_fig(fig, 360), use_container_width=True)

    if "train_ms" in df.columns:
        cT1, cT2 = st.columns(2)
        with cT1:
            fig_t = px.bar(df, x="modelo", y="train_ms", color="modelo",
                           title="Tempo de treino (ms)", text="train_ms")
            fig_t.update_traces(textposition="outside")
            fig_t.update_layout(showlegend=False)
            st.plotly_chart(_styled_fig(fig_t, 280), use_container_width=True)
        with cT2:
            cv_data = []
            for model, m in metrics.items():
                if m.get("cv_f1_mean") is not None:
                    cv_data.append({
                        "modelo": model,
                        "cv_f1_mean": m["cv_f1_mean"],
                        "cv_f1_std": m["cv_f1_std"] or 0,
                    })
            if cv_data:
                cv_df = pd.DataFrame(cv_data)
                fig_cv = go.Figure()
                fig_cv.add_trace(go.Bar(
                    x=cv_df["modelo"], y=cv_df["cv_f1_mean"],
                    error_y=dict(type="data", array=cv_df["cv_f1_std"]),
                    marker_color=PLOTLY_PALETTE[:len(cv_df)],
                    text=[f"{v:.2%}" for v in cv_df["cv_f1_mean"]],
                    textposition="outside",
                ))
                fig_cv.update_layout(title="F1 medio em CV (5 folds)", yaxis_tickformat=".0%",
                                     yaxis_range=[0, 1.05])
                st.plotly_chart(_styled_fig(fig_cv, 280), use_container_width=True)

    # ---- Curva ROC sobreposta ----
    roc_traces = []
    for model, m in metrics.items():
        if m.get("roc"):
            roc_traces.append((model, m["roc"]))
    if roc_traces:
        section("Curvas ROC")
        fig_roc = go.Figure()
        for idx, (model, roc) in enumerate(roc_traces):
            fig_roc.add_trace(go.Scatter(
                x=roc["fpr"], y=roc["tpr"], mode="lines",
                name=f"{model} (AUC {roc['auc']:.3f})",
                line=dict(width=3, color=PLOTLY_PALETTE[idx % len(PLOTLY_PALETTE)]),
            ))
        fig_roc.add_trace(go.Scatter(
            x=[0, 1], y=[0, 1], mode="lines",
            name="aleatorio", line=dict(dash="dash", color="rgba(148,163,184,0.5)"),
            showlegend=False,
        ))
        fig_roc.update_layout(title="ROC \u2014 todos os modelos",
                              xaxis_title="False Positive Rate",
                              yaxis_title="True Positive Rate")
        st.plotly_chart(_styled_fig(fig_roc, 360), use_container_width=True)

    # ---- Matriz de confusao + importancia do melhor modelo ----
    section(f"Detalhe do melhor modelo \u00b7 {best}")
    cC, cI = st.columns([1, 1])
    cm = best_m.get("confusion_matrix")
    labels = report.get("labels", ["nao_irrigar", "irrigar"])
    if cm:
        fig_cm = px.imshow(
            cm,
            x=[f"pred {labels[0]}", f"pred {labels[1]}"],
            y=[f"real {labels[0]}", f"real {labels[1]}"],
            color_continuous_scale="Greens",
            text_auto=True,
            title="Matriz de confusao",
            aspect="auto",
        )
        fig_cm.update_layout(coloraxis_showscale=False)
        cC.plotly_chart(_styled_fig(fig_cm, 320), use_container_width=True)

    fi = best_m.get("feature_importance") or []
    if fi:
        fi_df = pd.DataFrame(fi).sort_values("importance", ascending=True)
        fig_fi = px.bar(fi_df, x="importance", y="feature", orientation="h",
                        title="Importancia das features",
                        text=[f"{v:.0%}" for v in fi_df["importance"]])
        fig_fi.update_traces(marker_color="#34d399", textposition="outside")
        fig_fi.update_xaxes(tickformat=".0%")
        cI.plotly_chart(_styled_fig(fig_fi, 320), use_container_width=True)

    # ---- Dataset ----
    dataset = report.get("dataset", {})
    if dataset:
        section("Dataset utilizado")
        cD1, cD2, cD3 = st.columns(3)
        kpi(cD1, "Amostras totais", str(dataset.get("total", 0)),       icon="\U0001F4DA")
        kpi(cD2, "Classe positiva", f"{dataset.get('positive_ratio', 0):.0%}", icon="\U0001F4A7")
        kpi(cD3, "Treino / Teste",  f"{report.get('train_samples', 0)} / {report.get('test_samples', 0)}", icon="\u2696\ufe0f")

        # Distribuicao de classes
        bal = pd.DataFrame([
            {"classe": labels[0], "qtd": dataset.get("negatives", 0)},
            {"classe": labels[1], "qtd": dataset.get("positives", 0)},
        ])
        cB1, cB2 = st.columns([1, 2])
        fig_bal = px.pie(bal, names="classe", values="qtd",
                         title="Balanceamento de classes", hole=0.55)
        cB1.plotly_chart(_styled_fig(fig_bal, 320), use_container_width=True)

        preview = dataset.get("preview", [])
        if preview:
            cB2.markdown("**Preview do dataset (8 primeiras linhas)**")
            cB2.dataframe(pd.DataFrame(preview), use_container_width=True, hide_index=True)

        describe = dataset.get("describe", {})
        if describe:
            with st.expander("Estatisticas descritivas das features"):
                st.dataframe(pd.DataFrame(describe).round(3),
                             use_container_width=True)


def _render_fase6(result: dict) -> None:
    report = result.get("report", {})
    counts = report.get("counts", {})
    total = report.get("total_images", 0)
    c1, c2, c3, c4 = st.columns(4)
    kpi(c1, "Imagens",            str(total),                              icon="\U0001F4F8")
    kpi(c2, "Normal",             str(counts.get("normal", 0)),            icon="\U0001F7E2")
    kpi(c3, "Possivel estresse",  str(counts.get("possivel_estresse", 0)), icon="\U0001F7E1")
    kpi(c4, "Alta reflectancia",  str(counts.get("alta_reflectancia", 0)), icon="\U0001F7E0")
    if counts:
        df = pd.DataFrame([{"classe": k, "qtd": v} for k, v in counts.items() if v])
        if not df.empty:
            fig = px.pie(df, names="classe", values="qtd",
                         title="Distribuicao das classes", hole=0.6)
            st.plotly_chart(_styled_fig(fig, 320), use_container_width=True)
    results = report.get("results", [])
    if results:
        st.dataframe(pd.DataFrame(results), use_container_width=True, hide_index=True)


def _render_history(result: dict) -> None:
    items = result.get("items", [])
    if not items:
        st.info("Sem historico ainda.")
        return
    df = pd.DataFrame(items)
    if "alerts_count" in df.columns:
        fig = px.bar(df, x="timestamp", y="alerts_count", color="type",
                     title="Alertas ao longo do tempo")
        st.plotly_chart(_styled_fig(fig, 320), use_container_width=True)
    st.dataframe(df, use_container_width=True, hide_index=True)


progress = st.progress(0, text="Aguardando...") if run_all else None


def _bump(p: int, label: str) -> None:
    if progress is not None:
        progress.progress(p, text=label)
        time.sleep(0.2)


# ============================== OVERVIEW ============================== #
with tab_h:
    step_box(
        "00:00 \u2014 00:40",
        "Abertura",
        "Ola, somos o grupo FlexMedia. Apresentamos a Fase 7 do projeto FarmTech: a consolidacao das "
        "fases 1 a 6 em uma unica plataforma Python, operavel por dashboard e por CLI.",
        "Mostre a barra superior com os chips de status e o cabecalho do produto.",
    )

    section("O que este console entrega")
    cards = [
        ("Fase 1\u20132", "Foundation", "blue",
         "CRUD de areas, culturas e insumos em CSV. Mesma API exposta na CLI."),
        ("Fase 3", "Telemetria", "blue",
         "Ingestao de sensores ESP32 com Oracle como primario e CSV como fallback."),
        ("Fase 4", "Inteligencia", "violet",
         "Tres modelos Scikit-Learn comparados ponta a ponta com predicao manual."),
        ("Fase 6", "Visao", "violet",
         "Pipeline YOLO referenciado e classificador baseline para a demo ao vivo."),
        ("Fase 5", "Mensageria", "amber",
         "Alertas via AWS SNS com fallback de historico local para demo offline."),
        ("Fase 7", "Consolidacao", "",
         "Dashboard + CLI no mesmo repositorio, com origem de cada fase documentada."),
    ]
    cols = st.columns(3)
    for idx, (title, tag, tag_color, desc) in enumerate(cards):
        klass = f"tag {tag_color}".strip()
        with cols[idx % 3]:
            st.markdown(
                f"<div class='card'><span class='{klass}'>{tag}</span>"
                f"<h4>{title}</h4><p>{desc}</p></div>",
                unsafe_allow_html=True,
            )


# ============================== FASE 1-2 ============================== #
with tab12:
    step_box(
        "00:40 \u2014 02:00",
        "Fase 1\u20132 \u00b7 CRUD de Areas",
        "Comecamos pela base do sistema: as areas de plantio. O CRUD em CSV e espelhado na CLI. "
        "Vou listar as areas, criar uma area de demo e remover um registro.",
        "Clique em <span class='kbd'>Listar areas</span>, depois <span class='kbd'>Criar area de demo</span>.",
    )
    section("Operacoes disponiveis")
    if st.button("\U0001F4CB Listar areas", key="btn_f12_list") or run_all:
        _bump(15, "Fase 1-2: listando areas...")
        snap = run_phase("fase1_2")
        _render_areas(snap)
        with st.expander("Resposta JSON"):
            st.json(snap)
    cA, cB = st.columns(2)
    with cA:
        if st.button("\u2795 Criar area de demo"):
            st.json(create_area(nome="Talhao Demo", cultura="soja", hectares=10.0))
    with cB:
        rid = st.number_input("ID para remover", min_value=0, value=0, step=1, key="rm_id")
        if st.button("\U0001F5D1\ufe0f Remover area"):
            st.json(delete_area(area_id=int(rid)))


# ============================== FASE 3 ============================== #
with tab3:
    step_box(
        "02:00 \u2014 03:20",
        "Fase 3 \u00b7 Telemetria de Sensores",
        "A Fase 3 e o IoT. Coletamos leituras dos sensores ESP32 \u2014 umidade, temperatura e pH. "
        "Quando ha Oracle, lemos do banco; do contrario, usamos o CSV como fallback.",
        "Clique em <span class='kbd'>Coletar snapshot</span> e percorra os KPIs e o grafico.",
    )
    section("Coleta em tempo real")
    if st.button("\U0001F4E1 Coletar snapshot", key="btn_f3") or run_all:
        _bump(30, "Fase 3: coletando telemetria...")
        snap = run_phase("fase3")
        _render_fase3(snap)
        with st.expander("Resposta JSON"):
            st.json(snap)


# ============================== FASE 4 ============================== #
with tab4:
    step_box(
        "03:20 \u2014 05:00",
        "Fase 4 \u00b7 Machine Learning",
        "Na Fase 4 entra o Machine Learning. Treino tres modelos Scikit-Learn \u2014 logistic, "
        "random forest e gradient boosting \u2014, comparo metricas e seleciono o melhor. Em seguida, faco uma predicao manual.",
        "Clique em <span class='kbd'>Treinar modelos</span>, depois <span class='kbd'>Prever irrigacao</span>.",
    )
    section("Treino e predicao")
    cT, cP = st.columns(2)
    with cT:
        if st.button("\U0001F3CB\ufe0f Treinar modelos", key="btn_f4t") or run_all:
            _bump(50, "Fase 4: treinando modelos...")
            res = train_fase4(limit=train_limit, force_train=True)
            _render_fase4_metrics(res)
            with st.expander("Resposta JSON"):
                st.json(res)
    with cP:
        if st.button("\U0001F52E Prever irrigacao", key="btn_f4p") or run_all:
            _bump(60, "Fase 4: predicao...")
            res = infer_fase4(temperatura=pred_temp, umidade_solo=pred_umid, ph_solo=pred_ph)
            pred = res.get("prediction", {})
            need = pred.get("needs_irrigation")
            badge = "warn" if need else "ok"
            label = "Irrigar" if need else "Nao irrigar"
            st.markdown(
                f"<div class='card'><span class='tag amber'>Recomendacao</span>"
                f"<h4><span class='badge {badge}'>{label}</span> "
                f"&middot; probabilidade {pred.get('probability', 0):.2f}</h4>"
                f"<p>Modelo aplicado: <code>{pred.get('model', '?')}</code></p></div>",
                unsafe_allow_html=True,
            )
            with st.expander("Resposta JSON"):
                st.json(res)


# ============================== FASE 6 ============================== #
with tab6:
    step_box(
        "05:00 \u2014 06:20",
        "Fase 6 \u00b7 Visao Computacional",
        "A Fase 6 e visao computacional. O pipeline original usa YOLO e esta referenciado em "
        "references/fase6. Aqui no portal, aplico um classificador baseline por brilho em uma pasta de imagens.",
        "Clique em <span class='kbd'>Rodar inferencia</span> e mostre o donut e a tabela.",
    )
    section("Inferencia em pasta de imagens")
    if st.button("\U0001F441\ufe0f Rodar inferencia", key="btn_f6") or run_all:
        _bump(75, "Fase 6: classificando imagens...")
        res = run_fase6_vision(images_dir=images_dir, limit=50)
        _render_fase6(res)
        with st.expander("Resposta JSON"):
            st.json(res)


# ============================== FASE 5 ============================== #
with tab5:
    step_box(
        "06:20 \u2014 08:20",
        "Fase 5 \u00b7 Mensageria e Alertas",
        "A Fase 5 e a camada de cloud e mensageria. Com AWS configurada, alertas saem via SNS por e-mail. "
        "Sem AWS, rodamos em dry-run com historico local. Vou monitorar, disparar um alerta e atualizar o historico.",
        "Use <span class='kbd'>Monitorar agora</span>, <span class='kbd'>Disparar alerta de teste</span> "
        "e <span class='kbd'>Atualizar historico</span>.",
    )
    section("Monitor + Alerta + Historico")
    cM, cT = st.columns(2)
    with cM:
        if st.button("\U0001F4E1 Monitorar agora", key="btn_f5m") or run_all:
            _bump(85, "Fase 5: monitorando...")
            res = monitor_now(limit=monitor_limit)
            with st.expander("Snapshot do monitor"):
                st.json(res)
        if st.button("\U0001F6A8 Disparar alerta de teste", key="btn_f5a") or run_all:
            _bump(92, "Fase 5: disparando alerta...")
            payload = {
                "source": "fase3",
                "metric": "umidade_solo",
                "value": 15.0,
                "threshold": 20.0,
                "action": "Verificar irrigacao e iniciar ajuste corretivo",
            }
            st.json(AlertService().send_alert(payload))
    with cT:
        if st.button("\U0001F4D6 Atualizar historico", key="btn_f5h") or run_all:
            _bump(98, "Fase 5: lendo historico...")
            res = alerts_history(limit=20)
            _render_history(res)


# ============================== ENCERRAMENTO ============================== #
with tab_end:
    if run_all and progress is not None:
        progress.progress(100, text="Concluido")
    step_box(
        "08:20 \u2014 10:00",
        "Arquitetura e Fechamento",
        "Para fechar, mostro a arquitetura consolidada: sensores alimentam regras e ML, que disparam "
        "alertas e atualizam a dashboard. O codigo esta em phases, services e app, com origem de cada fase em references. "
        "Obrigado \u2014 o link do video estara no README.",
        "Mostre o diagrama abaixo e abra o README no VS Code.",
    )

    section("Fluxo de dados consolidado")
    st.markdown(
        """
        <div class="card">
          <span class="tag blue">Architecture</span>
          <h4>Pipeline ponta a ponta</h4>
          <p>Telemetria &rarr; regras &rarr; ML &rarr; alertas &rarr; dashboard / CLI</p>
        </div>
        """,
        unsafe_allow_html=True,
    )

    st.code(
        """ ESP32 / CSV   ─►  Fase 1-2 (CRUD)  ─►  Fase 3 (Telemetria)  ─►  Fase 4 (ML)
                                                                  │
                                                                  ▼
                                                          Fase 6 (Visao)
                                                                  │
                                                                  ▼
                                                          Fase 5 (Alertas)
                                                                  │
                                                                  ▼
                                                       Streamlit  ·  CLI
""",
        language="text",
    )

    section("Onde encontrar")
    cE1, cE2, cE3 = st.columns(3)
    with cE1:
        st.markdown(
            "<div class='card'><span class='tag'>Documentacao</span>"
            "<h4>Roteiro do video</h4><p>docs/VIDEO_SCRIPT_10MIN.md</p></div>",
            unsafe_allow_html=True,
        )
    with cE2:
        st.markdown(
            "<div class='card'><span class='tag blue'>Referencias</span>"
            "<h4>Origem das fases</h4><p>references/README.md</p></div>",
            unsafe_allow_html=True,
        )
    with cE3:
        st.markdown(
            "<div class='card'><span class='tag amber'>Cloud</span>"
            "<h4>Setup AWS</h4><p>docs/AWS_ALERT_SETUP.md</p></div>",
            unsafe_allow_html=True,
        )

    st.markdown(
        "<div class='footer'>FarmTech Solutions \u00b7 Fase 7 \u00b7 Operations Console"
        "<span class='sep'>\u2022</span>built with Streamlit, Scikit-Learn, Plotly &amp; Pillow"
        "</div>",
        unsafe_allow_html=True,
    )
