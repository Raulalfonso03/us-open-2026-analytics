import streamlit as st
import pandas as pd
import numpy as np
import plotly.graph_objects as go
import plotly.express as px

st.set_page_config(page_title="Player Profiles", page_icon="👤", layout="wide")

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
    - 👤 **Player Profiles**
    - ⚖️ Player Comparison
    - 🔮 Match Prediction
    - 🏆 Tournament Prediction
    - 📊 Analytics Dashboard
    - 🤖 ML Model
    - ℹ️ About
    """)

st.markdown("# 👤 Player Profiles")
st.markdown("Estadísticas detalladas de cada jugador del circuito ATP")
st.markdown("---")

jugadores = sorted(df["player_name"].dropna().unique().tolist())
selected  = st.selectbox("🔍 Selecciona un jugador", jugadores,
                          index=jugadores.index("Jannik Sinner") if "Jannik Sinner" in jugadores else 0)

player = df[df["player_name"] == selected].iloc[0]

rank   = int(player["atp_rank_current"]) if pd.notna(player.get("atp_rank_current")) else "N/A"
points = int(player["atp_points_current"]) if pd.notna(player.get("atp_points_current")) else "N/A"
record = player.get("record_overall_52w", "N/A")
titles = int(player["titulos_52w"]) if pd.notna(player.get("titulos_52w")) else 0
estado = player.get("injury_status", "FIT")
nota   = player.get("injury_note", "")

# Color del estado
if estado == "LESIONADO":
    estado_color = "#ff4444"
    estado_icon  = "⚠️"
elif estado == "DUDA":
    estado_color = "#ffaa00"
    estado_icon  = "❓"
else:
    estado_color = "#00ff88"
    estado_icon  = "✅"

st.markdown(f"""
<div style="background:linear-gradient(135deg,#0d1117,#161b22);border:1px solid #1a472a;
            border-radius:16px;padding:28px;margin-bottom:24px">
    <div style="display:flex;justify-content:space-between;align-items:center">
        <div>
            <h1 style="color:#00ff88;margin:0;font-size:2.2rem;font-weight:900">{selected}</h1>
            <p style="color:#555;margin:4px 0;letter-spacing:2px;text-transform:uppercase;font-size:0.85rem">
                ATP Professional · Hard Court Specialist
            </p>
            <span style="background:{estado_color}22;color:{estado_color};border:1px solid {estado_color};
                         border-radius:8px;padding:4px 12px;font-size:0.85rem;font-weight:700">
                {estado_icon} {estado}
            </span>
            {f'<p style="color:#888;font-size:0.8rem;margin-top:8px">⚠️ {nota}</p>' if nota else ""}
        </div>
        <div style="text-align:right">
            <div style="font-size:3rem;font-weight:900;color:#00ff88">#{rank}</div>
            <div style="color:#555;font-size:0.85rem">ATP Ranking</div>
        </div>
    </div>
</div>
""", unsafe_allow_html=True)

# KPIs
c1, c2, c3, c4, c5 = st.columns(5)
with c1:
    overall = player.get("winpct_overall_52w")
    st.metric("📊 Win% Overall", f"{overall*100:.1f}%" if pd.notna(overall) and overall<=1 else "N/A", f"Record: {record}")
with c2:
    hard = player.get("winpct_en_hard_52w")
    st.metric("🎾 Win% Hard", f"{hard*100:.1f}%" if pd.notna(hard) and hard<=1 else "N/A")
with c3:
    gs = player.get("winpct_grand_slams_52w")
    st.metric("🏆 Win% GS", f"{gs*100:.1f}%" if pd.notna(gs) and gs<=1 else "N/A", player.get("record_grand_slams_52w",""))
with c4:
    st.metric("🏅 Títulos (52w)", str(titles))
with c5:
    m1000 = player.get("winpct_masters_1000_52w")
    st.metric("💎 Win% M1000", f"{m1000*100:.1f}%" if pd.notna(m1000) and m1000<=1 else "N/A")

st.markdown("---")

# Servicio
st.markdown('<p class="section-header">🎾 ESTADÍSTICAS DE SERVICIO (Hard Court)</p>', unsafe_allow_html=True)

col1, col2 = st.columns(2)
with col1:
    st.markdown("**Temporada 2025**")
    for label, col in [("1er Saque %","1er_saque_pct_2025"),("1er Saque Ganado %","1er_saque_ganado_pct_2025"),
                        ("2do Saque Ganado %","2do_saque_ganado_pct_2025"),("Juegos Saque G %","juegos_saque_g_pct_2025"),
                        ("BP Salvados %","bp_salvados_pct_2025")]:
        val = player.get(col)
        if pd.notna(val):
            st.markdown(f"""<div style="display:flex;justify-content:space-between;padding:8px 0;border-bottom:1px solid #1a1a2e">
                <span style="color:#888">{label}</span>
                <span style="color:#00ff88;font-weight:700">{val:.1f}%</span></div>""", unsafe_allow_html=True)

with col2:
    st.markdown("**Temporada 2026**")
    for label, col in [("1er Saque %","1er_saque_pct_2026"),("1er Saque Ganado %","1er_saque_ganado_pct_2026"),
                        ("2do Saque Ganado %","2do_saque_ganado_pct_2026"),("Juegos Saque G %","juegos_saque_g_pct_2026"),
                        ("BP Salvados %","bp_salvados_pct_2026")]:
        val = player.get(col)
        if pd.notna(val):
            st.markdown(f"""<div style="display:flex;justify-content:space-between;padding:8px 0;border-bottom:1px solid #1a1a2e">
                <span style="color:#888">{label}</span>
                <span style="color:#00ff88;font-weight:700">{val:.1f}%</span></div>""", unsafe_allow_html=True)

st.markdown("---")

# Radar
st.markdown('<p class="section-header">📊 RADAR DE SERVICIO 2026 vs MEDIA DEL TOUR</p>', unsafe_allow_html=True)

cats   = ["1er Saque %","1er Saque\nGanado %","2do Saque\nGanado %","Juegos Saque\nG %","BP\nSalvados %"]
cols_p = ["1er_saque_pct_2026","1er_saque_ganado_pct_2026","2do_saque_ganado_pct_2026","juegos_saque_g_pct_2026","bp_salvados_pct_2026"]
vals_p = [player.get(c, np.nan) for c in cols_p]
vals_m = [df[c].median() for c in cols_p]

if any(pd.notna(v) for v in vals_p):
    fig_r = go.Figure()
    fig_r.add_trace(go.Scatterpolar(
        r=[v if pd.notna(v) else 0 for v in vals_p] + [vals_p[0] if pd.notna(vals_p[0]) else 0],
        theta=cats + [cats[0]], fill="toself", name=selected,
        line=dict(color="#00ff88", width=2), fillcolor="rgba(0,255,136,0.1)"
    ))
    fig_r.add_trace(go.Scatterpolar(
        r=vals_m + [vals_m[0]], theta=cats + [cats[0]],
        fill="toself", name="Media Tour",
        line=dict(color="#555", width=1), fillcolor="rgba(85,85,85,0.1)"
    ))
    fig_r.update_layout(
        polar=dict(bgcolor="#0d1117", radialaxis=dict(visible=True, range=[0,100], tickfont=dict(color="#555"))),
        template="plotly_dark", paper_bgcolor="rgba(0,0,0,0)",
        height=380, legend=dict(font=dict(color="white")), margin=dict(l=40,r=40,t=40,b=40)
    )
    st.plotly_chart(fig_r, use_container_width=True)

st.markdown("---")

# Resto
st.markdown('<p class="section-header">🏓 ESTADÍSTICAS DE RESTO (Hard Court)</p>', unsafe_allow_html=True)

col1, col2 = st.columns(2)
with col1:
    st.markdown("**Temporada 2025**")
    for label, col in [("Resto 1er Saque %","resto_1er_pct_2025"),("Resto 2do Saque %","resto_2do_pct_2025"),
                        ("BP Convertidos %","bp_convertidos_pct_2025"),("Juegos Resto G %","juegos_resto_g_pct_2025")]:
        val = player.get(col)
        if pd.notna(val):
            st.markdown(f"""<div style="display:flex;justify-content:space-between;padding:8px 0;border-bottom:1px solid #1a1a2e">
                <span style="color:#888">{label}</span>
                <span style="color:#00ff88;font-weight:700">{val:.1f}%</span></div>""", unsafe_allow_html=True)

with col2:
    st.markdown("**Temporada 2026**")
    for label, col in [("Resto 1er Saque %","resto_1er_pct_2026"),("Resto 2do Saque %","resto_2do_pct_2026"),
                        ("BP Convertidos %","bp_convertidos_pct_2026"),("Juegos Resto G %","juegos_resto_g_pct_2026")]:
        val = player.get(col)
        if pd.notna(val):
            st.markdown(f"""<div style="display:flex;justify-content:space-between;padding:8px 0;border-bottom:1px solid #1a1a2e">
                <span style="color:#888">{label}</span>
                <span style="color:#00ff88;font-weight:700">{val:.1f}%</span></div>""", unsafe_allow_html=True)

st.markdown("---")

# Presion
st.markdown('<p class="section-header">💪 RENDIMIENTO BAJO PRESIÓN</p>', unsafe_allow_html=True)

presion = {
    "Tras ganar 1er set":  ("winpct_tras_ganar_set1_52w",  "record_tras_ganar_set1_52w"),
    "Tras perder 1er set": ("winpct_tras_perder_set1_52w", "record_tras_perder_set1_52w"),
    "Set decisivo":        ("winpct_set_decisivo_52w",      "record_set_decisivo_52w"),
    "5to set":             ("winpct_5to_set_52w",           "record_5to_set_52w"),
    "Tiebreak":            ("winpct_tiebreak_52w",          "record_tiebreak_52w"),
    "Finales":             ("winpct_finales_52w",           "record_finales_52w"),
    "Grand Slams":         ("winpct_grand_slams_52w",       "record_grand_slams_52w"),
    "Masters 1000":        ("winpct_masters_1000_52w",      "record_masters1000_52w"),
}

presion_validos = {}
for k, (col_pct, col_rec) in presion.items():
    val = player.get(col_pct)
    if pd.notna(val) and val <= 1:
        presion_validos[k] = (val, player.get(col_rec, ""))

if presion_validos:
    col1, col2 = st.columns([1.5, 1])
    with col1:
        for label, (val, rec) in presion_validos.items():
            color = "#00ff88" if val >= 0.6 else "#ffaa00" if val >= 0.45 else "#ff4444"
            st.markdown(f"""
            <div style="display:flex;justify-content:space-between;align-items:center;padding:10px 0;border-bottom:1px solid #1a1a2e">
                <span style="color:#888;width:180px">{label}</span>
                <div style="flex:1;background:#1a1a2e;border-radius:3px;height:6px;margin:0 16px">
                    <div style="width:{val*100:.0f}%;height:6px;border-radius:3px;background:{color}"></div>
                </div>
                <span style="color:{color};font-weight:700;width:45px;text-align:right">{val*100:.0f}%</span>
                <span style="color:#444;font-size:0.75rem;width:55px;text-align:right">{rec}</span>
            </div>""", unsafe_allow_html=True)
    with col2:
        labels = list(presion_validos.keys())
        values = [v[0]*100 for v in presion_validos.values()]
        colors = ["#00ff88" if v>=60 else "#ffaa00" if v>=45 else "#ff4444" for v in values]
        fig_b = go.Figure(go.Bar(x=values, y=labels, orientation="h", marker_color=colors,
                                  text=[f"{v:.0f}%" for v in values], textposition="outside",
                                  textfont=dict(color="white", size=10)))
        fig_b.update_layout(template="plotly_dark", paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)",
                             height=300, margin=dict(l=10,r=50,t=10,b=10),
                             xaxis=dict(showgrid=False, showticklabels=False, range=[0,120]),
                             yaxis=dict(tickfont=dict(size=10)), showlegend=False)
        st.plotly_chart(fig_b, use_container_width=True)

st.markdown("---")

# Evolucion
st.markdown('<p class="section-header">📈 EVOLUCIÓN 2025 → 2026</p>', unsafe_allow_html=True)

evol_data = []
for label, c25, c26 in [
    ("1er Saque Ganado %","1er_saque_ganado_pct_2025","1er_saque_ganado_pct_2026"),
    ("2do Saque Ganado %","2do_saque_ganado_pct_2025","2do_saque_ganado_pct_2026"),
    ("BP Salvados %","bp_salvados_pct_2025","bp_salvados_pct_2026"),
    ("Juegos Saque G %","juegos_saque_g_pct_2025","juegos_saque_g_pct_2026"),
]:
    v25, v26 = player.get(c25), player.get(c26)
    if pd.notna(v25) and pd.notna(v26):
        evol_data.append({"Metrica": label, "2025": v25, "2026": v26})

if evol_data:
    df_e = pd.DataFrame(evol_data)
    fig_e = go.Figure()
    fig_e.add_trace(go.Bar(name="2025", x=df_e["Metrica"], y=df_e["2025"], marker_color="#1a472a"))
    fig_e.add_trace(go.Bar(name="2026", x=df_e["Metrica"], y=df_e["2026"], marker_color="#00ff88"))
    fig_e.update_layout(barmode="group", template="plotly_dark",
                         paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)",
                         height=300, margin=dict(l=10,r=10,t=10,b=10),
                         legend=dict(font=dict(color="white")), yaxis=dict(range=[0,100]))
    st.plotly_chart(fig_e, use_container_width=True)

st.markdown("---")
st.markdown('<p style="text-align:center;color:#333;font-size:0.8rem">US Open 2026 Analytics Platform · Capstone Project</p>', unsafe_allow_html=True)

