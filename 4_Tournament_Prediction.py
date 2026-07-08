import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go

st.set_page_config(page_title="Tournament Prediction", page_icon="🏆", layout="wide")

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
    base = "https://raw.githubusercontent.com/Raulalfonso03/us-open-2026-analytics/main/"
    df_master = pd.read_csv(base + "df_master_final.csv", sep=None, engine="python")
    df_pred   = pd.read_csv(base + "us_open_predictions.csv", sep=None, engine="python")
    return df_master, df_pred

df_master, df_pred = load_data()

with st.sidebar:
    st.markdown("## 🎾 US Open 2026")
    st.markdown("---")
    st.markdown("""
    - 🏠 Home
    - 👤 Player Profiles
    - ⚖️ Player Comparison
    - 🔮 Match Prediction
    - 🏆 **Tournament Prediction**
    - 📊 Analytics Dashboard
    - 🤖 ML Model
    - ℹ️ About
    """)

st.markdown("# 🏆 Tournament Prediction")
st.markdown("Probabilidades de ganar el US Open 2026 para cada jugador")
st.markdown("---")

# Info del torneo
c1, c2, c3, c4 = st.columns(4)
with c1:
    st.metric("📅 Fechas", "26 Aug - 7 Sep", "2026")
with c2:
    st.metric("🏟️ Sede", "Flushing Meadows", "New York")
with c3:
    st.metric("🎾 Superficie", "Hard Court", "Outdoor")
with c4:
    st.metric("🏆 Campeón Defensor", "Carlos Alcaraz", "2025")

st.markdown("---")

# Top 10 contendientes
st.markdown('<p class="section-header">🥇 TOP 10 FAVORITOS AL TÍTULO</p>', unsafe_allow_html=True)

medals = ["🥇","🥈","🥉","4️⃣","5️⃣","6️⃣","7️⃣","8️⃣","9️⃣","🔟"]

col_left, col_right = st.columns([1.2, 1])

with col_left:
    for i, row in df_pred.head(10).iterrows():
        name   = row["Jugador"]
        prob   = row["Prob US Open"]
        rank   = row.get("Ranking ATP", "?")
        hard   = row.get("Win% Hard", "N/A")
        gs     = row.get("Win% GS", "N/A")
        estado = row.get("Estado", "FIT")
        medal  = medals[i]

        if estado == "LESIONADO":
            badge = '<span style="background:#4a1a1a;color:#ff4444;border-radius:6px;padding:2px 8px;font-size:0.7rem;font-weight:700">⚠️ LESIONADO</span>'
        elif estado == "DUDA":
            badge = '<span style="background:#4a3a1a;color:#ffaa00;border-radius:6px;padding:2px 8px;font-size:0.7rem;font-weight:700">❓ DUDA</span>'
        else:
            badge = '<span style="background:#1a3a2a;color:#00ff88;border-radius:6px;padding:2px 8px;font-size:0.7rem;font-weight:700">✅ FIT</span>'

        st.markdown(f"""
        <div style="background:#0d1117;border:1px solid #1a1a2e;border-radius:12px;
                    padding:14px 18px;margin:6px 0">
            <div style="display:flex;justify-content:space-between;align-items:center;margin-bottom:6px">
                <span>
                    {medal} <b style="color:#fff;font-size:1rem">{name}</b>
                    &nbsp;<span style="color:#444;font-size:0.8rem">ATP #{rank}</span>
                    &nbsp;{badge}
                </span>
                <span style="color:#00ff88;font-weight:900;font-size:1.2rem">{prob}%</span>
            </div>
            <div style="background:#1a1a2e;border-radius:3px;height:5px;margin-bottom:6px">
                <div style="width:{prob*15}%;height:5px;border-radius:3px;
                            background:linear-gradient(90deg,#1a472a,#00ff88)"></div>
            </div>
            <span style="color:#444;font-size:0.75rem">Hard: {hard} · GS: {gs}</span>
        </div>""", unsafe_allow_html=True)

with col_right:
    colors = []
    for _, row in df_pred.head(10).iterrows():
        if row.get("Estado") == "LESIONADO": colors.append("#ff4444")
        elif row.get("Estado") == "DUDA": colors.append("#ffaa00")
        else: colors.append("#00ff88")

    fig = go.Figure(go.Bar(
        x=df_pred.head(10)["Prob US Open"],
        y=df_pred.head(10)["Jugador"],
        orientation="h",
        marker_color=colors,
        text=df_pred.head(10)["Prob US Open"].apply(lambda x: f"{x}%"),
        textposition="outside",
        textfont=dict(color="white", size=11)
    ))
    fig.update_layout(
        template="plotly_dark", paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)",
        height=400, margin=dict(l=10,r=60,t=10,b=10),
        xaxis=dict(showgrid=False, showticklabels=False, range=[0,8]),
        yaxis=dict(autorange="reversed", tickfont=dict(size=11, color="white")),
    )
    st.plotly_chart(fig, use_container_width=True)

st.markdown("---")

# Tabla completa
st.markdown('<p class="section-header">📋 RANKING COMPLETO DE CONTENDIENTES</p>', unsafe_allow_html=True)

st.dataframe(
    df_pred[["Jugador","Ranking ATP","Win% Hard","Win% GS","Estado","Prob US Open"]],
    use_container_width=True, hide_index=True,
    column_config={
        "Prob US Open": st.column_config.ProgressColumn(
            "Prob US Open", min_value=0, max_value=df_pred["Prob US Open"].max()+1, format="%.1f%%"
        ),
    }
)

st.markdown("---")

# Analisis por grupos
st.markdown('<p class="section-header">📊 ANÁLISIS POR GRUPOS</p>', unsafe_allow_html=True)

fit_players    = df_pred[df_pred["Estado"] == "FIT"]
duda_players   = df_pred[df_pred["Estado"] == "DUDA"]
lesion_players = df_pred[df_pred["Estado"] == "LESIONADO"]

c1, c2, c3 = st.columns(3)
with c1:
    st.metric("✅ Jugadores FIT", len(fit_players),
              f"Prob combinada: {fit_players['Prob US Open'].sum():.1f}%")
with c2:
    st.metric("❓ Jugadores en DUDA", len(duda_players),
              f"Prob combinada: {duda_players['Prob US Open'].sum():.1f}%")
with c3:
    st.metric("⚠️ LESIONADOS", len(lesion_players),
              f"Prob combinada: {lesion_players['Prob US Open'].sum():.1f}%")

st.markdown("---")

# Grafico scatter Win% Hard vs Win% GS
st.markdown('<p class="section-header">📈 WIN% HARD vs WIN% GRAND SLAMS</p>', unsafe_allow_html=True)
st.caption("El cuadrante superior derecho indica los jugadores más completos para el US Open")

df_plot = df_master[
    df_master["winpct_en_hard_52w"].notna() &
    df_master["winpct_grand_slams_52w"].notna() &
    (df_master["winpct_en_hard_52w"] <= 1) &
    (df_master["winpct_grand_slams_52w"] <= 1)
].copy()

df_plot["hard_pct"] = df_plot["winpct_en_hard_52w"] * 100
df_plot["gs_pct"]   = df_plot["winpct_grand_slams_52w"] * 100

fig2 = px.scatter(
    df_plot, x="hard_pct", y="gs_pct",
    text="player_name", color="injury_status",
    color_discrete_map={"FIT":"#00ff88","DUDA":"#ffaa00","LESIONADO":"#ff4444"},
    title="Win% Hard Court vs Win% Grand Slams",
    labels={"hard_pct":"Win% Hard Court","gs_pct":"Win% Grand Slams"},
    template="plotly_dark", height=500
)
fig2.update_traces(textposition="top center", textfont=dict(size=9, color="white"))
fig2.update_layout(paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="#0d1117",
                   xaxis=dict(gridcolor="#1a1a2e"), yaxis=dict(gridcolor="#1a1a2e"))
st.plotly_chart(fig2, use_container_width=True)

st.markdown("---")
st.markdown('<p style="text-align:center;color:#333;font-size:0.8rem">US Open 2026 Analytics Platform · Capstone Project · Predicciones estimadas, no resultados reales</p>', unsafe_allow_html=True)
