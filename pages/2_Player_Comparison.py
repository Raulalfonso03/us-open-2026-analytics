import streamlit as st
import pandas as pd
import numpy as np
import plotly.graph_objects as go

st.set_page_config(page_title="Player Comparison", page_icon="⚖️", layout="wide")

st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;600;700;900&display=swap');
    * { font-family: 'Inter', sans-serif; }
    .stApp { background-color: #0a0a0f; }
    [data-testid="stSidebar"] { background: linear-gradient(180deg, #0d1117 0%, #0a0a0f 100%); border-right: 1px solid #1a472a; }
    .section-header { font-size: 1.2rem; font-weight: 700; color: #00ff88; border-bottom: 2px solid #1a472a; padding-bottom: 8px; margin: 20px 0 12px 0; }
    [data-testid="metric-container"] { background: #0d1117; border: 1px solid #1a472a; border-radius: 12px; padding: 12px; }
</style>
""", unsafe_allow_html=True)

@st.cache_data
def load_data():
    url = "https://raw.githubusercontent.com/Raulalfonso03/us-open-2026-analytics/main/df_master_final.csv"
    return pd.read_csv(url, sep=None, engine="python")

df = load_data()

with st.sidebar:
    st.markdown("## 🎾 US Open 2026")
    st.markdown("---")
    st.markdown("""
    - 🏠 Home
    - 👤 Player Profiles
    - ⚖️ **Player Comparison**
    - 🔮 Match Prediction
    - 🏆 Tournament Prediction
    - 📊 Analytics Dashboard
    - 🤖 ML Model
    - ℹ️ About
    """)

st.markdown("# ⚖️ Player Comparison")
st.markdown("Compara estadísticas de dos jugadores cara a cara")
st.markdown("---")

jugadores = sorted(df["player_name"].dropna().unique().tolist())

col1, col_vs, col2 = st.columns([2, 0.4, 2])
with col1:
    p1 = st.selectbox("🎾 Jugador 1", jugadores,
                       index=jugadores.index("Jannik Sinner") if "Jannik Sinner" in jugadores else 0)
with col_vs:
    st.markdown("<br><br><div style='text-align:center;font-size:1.5rem;font-weight:900;color:#00ff88'>VS</div>", unsafe_allow_html=True)
with col2:
    p2 = st.selectbox("🎾 Jugador 2", jugadores,
                       index=jugadores.index("Carlos Alcaraz") if "Carlos Alcaraz" in jugadores else 1)

player1 = df[df["player_name"] == p1].iloc[0]
player2 = df[df["player_name"] == p2].iloc[0]

st.markdown("---")

# Headers
col1, col2 = st.columns(2)
with col1:
    r1 = int(player1["atp_rank_current"]) if pd.notna(player1.get("atp_rank_current")) else "N/A"
    w1 = f"{player1['winpct_overall_52w']*100:.1f}%" if pd.notna(player1.get("winpct_overall_52w")) and player1.get("winpct_overall_52w")<=1 else "N/A"
    st.markdown(f"""
    <div style="background:linear-gradient(135deg,#0d1117,#161b22);border:2px solid #00ff88;
                border-radius:16px;padding:20px;text-align:center">
        <h2 style="color:#00ff88;margin:0;font-size:1.6rem">{p1}</h2>
        <p style="color:#555;margin:4px 0">ATP #{r1} · Win% {w1}</p>
    </div>""", unsafe_allow_html=True)
with col2:
    r2 = int(player2["atp_rank_current"]) if pd.notna(player2.get("atp_rank_current")) else "N/A"
    w2 = f"{player2['winpct_overall_52w']*100:.1f}%" if pd.notna(player2.get("winpct_overall_52w")) and player2.get("winpct_overall_52w")<=1 else "N/A"
    st.markdown(f"""
    <div style="background:linear-gradient(135deg,#0d1117,#161b22);border:2px solid #2e8b57;
                border-radius:16px;padding:20px;text-align:center">
        <h2 style="color:#2e8b57;margin:0;font-size:1.6rem">{p2}</h2>
        <p style="color:#555;margin:4px 0">ATP #{r2} · Win% {w2}</p>
    </div>""", unsafe_allow_html=True)

st.markdown("---")

def compare_row(label, col, p1d, p2d, higher_better=True, pct=True, divisor=1):
    v1 = pd.to_numeric(p1d.get(col), errors="coerce")
    v2 = pd.to_numeric(p2d.get(col), errors="coerce")
    if pd.isna(v1) and pd.isna(v2): return
    
    def fmt(v):
        if pd.isna(v): return "N/A"
        if pct and v <= 1: return f"{v*100:.1f}%"
        if pct: return f"{v:.1f}%"
        return f"{v/divisor:.0f}"
    
    if pd.notna(v1) and pd.notna(v2):
        p1w = v1 > v2 if higher_better else v1 < v2
        c1 = "#00ff88" if p1w else "#ffffff"
        c2 = "#2e8b57" if not p1w else "#ffffff"
        arrow = "◀" if p1w else "▶"
    else:
        c1, c2, arrow = "#ffffff", "#ffffff", "—"

    st.markdown(f"""
    <div style="display:grid;grid-template-columns:1fr auto 1fr;align-items:center;
                padding:10px 0;border-bottom:1px solid #1a1a2e;gap:8px">
        <div style="text-align:right;color:{c1};font-weight:700;font-size:1rem">{fmt(v1)}</div>
        <div style="text-align:center;color:#444;font-size:0.8rem;min-width:150px">{arrow} {label} {arrow}</div>
        <div style="text-align:left;color:{c2};font-weight:700;font-size:1rem">{fmt(v2)}</div>
    </div>""", unsafe_allow_html=True)

st.markdown('<p class="section-header">📊 ESTADÍSTICAS GENERALES</p>', unsafe_allow_html=True)
compare_row("Ranking ATP", "atp_rank_current", player1, player2, higher_better=False, pct=False)
compare_row("Win% Overall", "winpct_overall_52w", player1, player2)
compare_row("Win% en Hard", "winpct_en_hard_52w", player1, player2)
compare_row("Win% Grand Slams", "winpct_grand_slams_52w", player1, player2)
compare_row("Win% Masters 1000", "winpct_masters_1000_52w", player1, player2)
compare_row("Títulos (52w)", "titulos_52w", player1, player2, pct=False)

st.markdown('<p class="section-header">🎾 SERVICIO 2026</p>', unsafe_allow_html=True)
compare_row("1er Saque %", "1er_saque_pct_2026", player1, player2, pct=True, divisor=1)
compare_row("1er Saque Ganado %", "1er_saque_ganado_pct_2026", player1, player2, pct=True)
compare_row("2do Saque Ganado %", "2do_saque_ganado_pct_2026", player1, player2, pct=True)
compare_row("BP Salvados %", "bp_salvados_pct_2026", player1, player2, pct=True)
compare_row("Aces 2026", "aces_2026", player1, player2, pct=False)

st.markdown('<p class="section-header">🏓 RESTO 2026</p>', unsafe_allow_html=True)
compare_row("Resto 1er Saque %", "resto_1er_pct_2026", player1, player2, pct=True)
compare_row("Resto 2do Saque %", "resto_2do_pct_2026", player1, player2, pct=True)
compare_row("BP Convertidos %", "bp_convertidos_pct_2026", player1, player2, pct=True)

st.markdown('<p class="section-header">💪 RENDIMIENTO BAJO PRESIÓN</p>', unsafe_allow_html=True)
compare_row("Tras ganar 1er set", "winpct_tras_ganar_set1_52w", player1, player2)
compare_row("Tras perder 1er set", "winpct_tras_perder_set1_52w", player1, player2)
compare_row("Set decisivo", "winpct_set_decisivo_52w", player1, player2)
compare_row("Tiebreak", "winpct_tiebreak_52w", player1, player2)
compare_row("Finales", "winpct_finales_52w", player1, player2)
compare_row("vs Top 10", "winpct_vs_top10_52w", player1, player2)

st.markdown("---")
st.markdown('<p class="section-header">📊 RADAR COMPARATIVO</p>', unsafe_allow_html=True)

cats = ["Win%\nHard","Win%\nGS","1er Saque\nGanado","BP\nSalvados","Set\nDecisivo","Win%\nOverall"]
cols_r = ["winpct_en_hard_52w","winpct_grand_slams_52w","1er_saque_ganado_pct_2026",
          "bp_salvados_pct_2026","winpct_set_decisivo_52w","winpct_overall_52w"]

def get_vals(player, cols):
    vals = []
    for c in cols:
        v = pd.to_numeric(player.get(c), errors="coerce")
        if pd.isna(v): vals.append(50)
        elif v <= 1: vals.append(v*100)
        else: vals.append(v)
    return vals

v1 = get_vals(player1, cols_r)
v2 = get_vals(player2, cols_r)

fig = go.Figure()
fig.add_trace(go.Scatterpolar(r=v1+[v1[0]], theta=cats+[cats[0]], fill="toself", name=p1,
                               line=dict(color="#00ff88", width=2), fillcolor="rgba(0,255,136,0.1)"))
fig.add_trace(go.Scatterpolar(r=v2+[v2[0]], theta=cats+[cats[0]], fill="toself", name=p2,
                               line=dict(color="#2e8b57", width=2), fillcolor="rgba(46,139,87,0.1)"))
fig.update_layout(polar=dict(bgcolor="#0d1117", radialaxis=dict(visible=True, range=[0,100], tickfont=dict(color="#555"))),
                  template="plotly_dark", paper_bgcolor="rgba(0,0,0,0)",
                  height=400, legend=dict(font=dict(color="white")), margin=dict(l=40,r=40,t=40,b=40))
st.plotly_chart(fig, use_container_width=True)

st.markdown("---")
st.markdown('<p style="text-align:center;color:#333;font-size:0.8rem">US Open 2026 Analytics Platform · Capstone Project</p>', unsafe_allow_html=True)

