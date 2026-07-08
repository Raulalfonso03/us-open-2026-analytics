import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
import requests
from PIL import Image
from io import BytesIO

st.set_page_config(
    page_title="US Open 2026 Analytics",
    page_icon="🎾",
    layout="wide",
    initial_sidebar_state="expanded"
)

st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;600;700;900&display=swap');
    
    * { font-family: 'Inter', sans-serif; }
    .stApp { background-color: #0a0a0f; }
    [data-testid="stSidebar"] { 
        background: linear-gradient(180deg, #0d1117 0%, #0a0a0f 100%);
        border-right: 1px solid #1a472a;
    }
    .main-title {
        font-size: 3.5rem; font-weight: 900;
        background: linear-gradient(90deg, #00ff88, #2e8b57, #00bfff);
        -webkit-background-clip: text; -webkit-text-fill-color: transparent;
        text-align: center; margin-bottom: 0.2rem; letter-spacing: -2px;
    }
    .subtitle {
        color: #666; text-align: center; font-size: 1rem;
        margin-bottom: 2rem; letter-spacing: 2px; text-transform: uppercase;
    }
    .player-card {
        background: linear-gradient(135deg, #0d1117 0%, #161b22 100%);
        border: 1px solid #1a472a; border-radius: 16px;
        padding: 20px; text-align: center; margin: 8px 0;
        transition: all 0.3s;
    }
    .player-card:hover { border-color: #00ff88; }
    .prob-bar-container {
        background: #0d1117; border: 1px solid #1a1a2e;
        border-radius: 12px; padding: 14px 18px; margin: 6px 0;
    }
    .prob-bar-fill {
        height: 6px; border-radius: 3px;
        background: linear-gradient(90deg, #1a472a, #00ff88);
        transition: width 0.5s ease;
    }
    .rank-badge {
        background: #1a472a; color: #00ff88;
        border-radius: 6px; padding: 2px 8px;
        font-size: 0.75rem; font-weight: 700;
    }
    .injury-badge {
        background: #4a1a1a; color: #ff4444;
        border-radius: 6px; padding: 2px 8px;
        font-size: 0.75rem; font-weight: 700;
    }
    .doubt-badge {
        background: #4a3a1a; color: #ffaa00;
        border-radius: 6px; padding: 2px 8px;
        font-size: 0.75rem; font-weight: 700;
    }
    [data-testid="metric-container"] {
        background: #0d1117; border: 1px solid #1a472a;
        border-radius: 12px; padding: 16px;
    }
    .section-header {
        font-size: 1.4rem; font-weight: 700; color: #00ff88;
        border-bottom: 2px solid #1a472a; padding-bottom: 10px;
        margin: 30px 0 20px 0; letter-spacing: 1px;
    }
</style>
""", unsafe_allow_html=True)

# ── Cargar datos ──────────────────────────────────────────────────────────
@st.cache_data
def load_data():
    base = "https://raw.githubusercontent.com/Raulalfonso03/us-open-2026-analytics/main/"
    df_master = pd.read_csv(base + "df_master_final.csv", sep=None, engine="python")
    df_pred   = pd.read_csv(base + "us_open_predictions.csv", sep=None, engine="python")
    return df_master, df_pred

df_master, df_pred = load_data()

# Fotos de jugadores (URLs de ATP Tour)
fotos = {
    "Jannik Sinner":         "https://www.atptour.com/-/media/alias/player-headshot/S0AG",
    "Carlos Alcaraz":        "https://www.atptour.com/-/media/alias/player-headshot/A0E2",
    "Alexander Zverev":      "https://www.atptour.com/-/media/alias/player-headshot/Z355",
    "Felix Auger-Aliassime": "https://www.atptour.com/-/media/alias/player-headshot/AG37",
    "Ben Shelton":           "https://www.atptour.com/-/media/alias/player-headshot/S0S1",
    "Alex de Minaur":        "https://www.atptour.com/-/media/alias/player-headshot/DH58",
    "Taylor Fritz":          "https://www.atptour.com/-/media/alias/player-headshot/FB98",
    "Novak Djokovic":        "https://www.atptour.com/-/media/alias/player-headshot/DJ17",
    "Daniil Medvedev":       "https://www.atptour.com/-/media/alias/player-headshot/MM58",
    "Flavio Cobolli":        "https://www.atptour.com/-/media/alias/player-headshot/C0E9",
}

# ── Sidebar ───────────────────────────────────────────────────────────────
with st.sidebar:
    st.markdown("## 🎾 US Open 2026")
    st.markdown("---")
    st.markdown("""
    - 🏠 **Home**
    - 👤 Player Profiles
    - ⚖️ Player Comparison
    - 🔮 Match Prediction
    - 🏆 Tournament Prediction
    - 📊 Analytics Dashboard
    - 🤖 ML Model
    - ℹ️ About
    """)
    st.markdown("---")
    st.caption("📅 Datos: Jul 2026")
    st.caption(f"👥 {len(df_master)} jugadores")
    st.caption("🎾 Superficie: Hard Court")

# ── Header ────────────────────────────────────────────────────────────────
st.markdown('<p class="main-title">US OPEN 2026</p>', unsafe_allow_html=True)
st.markdown('<p class="subtitle">Analytics & Prediction Platform · Hard Court · Flushing Meadows</p>', unsafe_allow_html=True)
st.markdown("---")

# ── KPIs ──────────────────────────────────────────────────────────────────
top1 = df_pred.iloc[0]
top2 = df_pred.iloc[1]
top3 = df_pred.iloc[2]

c1, c2, c3, c4 = st.columns(4)
with c1:
    st.metric("🥇 Gran Favorito", top1["Jugador"], f"{top1['Prob US Open']}%")
with c2:
    st.metric("🥈 2do Favorito", top2["Jugador"], f"{top2['Prob US Open']}%")
with c3:
    st.metric("🥉 3er Favorito", top3["Jugador"], f"{top3['Prob US Open']}%")
with c4:
    st.metric("🎾 US Open 2026", "26 Aug - 7 Sep", "New York")

st.markdown("---")

# ── Top 10 Contendientes ──────────────────────────────────────────────────
st.markdown('<p class="section-header">🏆 TOP 10 CONTENDIENTES</p>', unsafe_allow_html=True)
st.caption("Probabilidad estimada basada en ranking ATP, rendimiento en Hard Court, Grand Slams y forma reciente")

medals = ["🥇","🥈","🥉","4️⃣","5️⃣","6️⃣","7️⃣","8️⃣","9️⃣","🔟"]

col_left, col_right = st.columns([1.3, 1])

with col_left:
    for i, row in df_pred.head(10).iterrows():
        name   = row["Jugador"]
        prob   = row["Prob US Open"]
        rank   = int(row["Ranking ATP"]) if pd.notna(row.get("Ranking ATP")) else "?"
        hard   = row.get("Win% Hard", "N/A")
        estado = row.get("Estado", "FIT")
        medal  = medals[i]

        if estado == "LESIONADO":
            badge = '<span class="injury-badge">⚠️ LESIONADO</span>'
        elif estado == "DUDA":
            badge = '<span class="doubt-badge">❓ DUDA</span>'
        else:
            badge = '<span class="rank-badge">✅ FIT</span>'

        st.markdown(f"""
        <div class="prob-bar-container">
            <div style="display:flex;justify-content:space-between;align-items:center;margin-bottom:6px">
                <span style="font-size:1rem">
                    {medal} <b style="color:#ffffff">{name}</b>
                    &nbsp;<span style="color:#555;font-size:0.8rem">ATP #{rank}</span>
                    &nbsp;{badge}
                </span>
                <span style="color:#00ff88;font-weight:900;font-size:1.1rem">{prob}%</span>
            </div>
            <div style="background:#1a1a2e;border-radius:3px;height:6px">
                <div class="prob-bar-fill" style="width:{prob*15}%"></div>
            </div>
            <div style="color:#555;font-size:0.75rem;margin-top:4px">Hard: {hard}</div>
        </div>
        """, unsafe_allow_html=True)

with col_right:
    fig = go.Figure(go.Bar(
        x=df_pred.head(10)["Prob US Open"],
        y=df_pred.head(10)["Jugador"],
        orientation="h",
        marker=dict(
            color=df_pred.head(10)["Prob US Open"],
            colorscale=[[0,"#1a472a"],[1,"#00ff88"]],
            showscale=False
        ),
        text=df_pred.head(10)["Prob US Open"].apply(lambda x: f"{x}%"),
        textposition="outside",
        textfont=dict(color="white", size=11)
    ))
    fig.update_layout(
        template="plotly_dark",
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        height=400,
        margin=dict(l=10,r=60,t=10,b=10),
        xaxis=dict(showgrid=False, showticklabels=False, range=[0,8]),
        yaxis=dict(autorange="reversed", tickfont=dict(size=11, color="white")),
    )
    st.plotly_chart(fig, use_container_width=True)

st.markdown("---")

# ── Ranking ATP ───────────────────────────────────────────────────────────
st.markdown('<p class="section-header">📋 RANKING ATP ACTUAL</p>', unsafe_allow_html=True)

cols_rank = ["player_name","atp_rank_current","atp_points_current",
             "winpct_overall_52w","winpct_en_hard_52w","winpct_grand_slams_52w","injury_status"]
cols_exist = [c for c in cols_rank if c in df_master.columns]
df_rank = df_master[df_master["atp_rank_current"].notna()].sort_values("atp_rank_current").head(20)[cols_exist].copy()
df_rank = df_rank.rename(columns={
    "player_name":"Jugador","atp_rank_current":"Ranking",
    "atp_points_current":"Puntos","winpct_overall_52w":"Win% Overall",
    "winpct_en_hard_52w":"Win% Hard","winpct_grand_slams_52w":"Win% GS",
    "injury_status":"Estado"
})
df_rank["Ranking"] = df_rank["Ranking"].astype(int)

st.dataframe(df_rank, use_container_width=True, hide_index=True,
    column_config={
        "Win% Overall": st.column_config.ProgressColumn("Win% Overall", min_value=0, max_value=1, format="%.0%"),
        "Win% Hard":    st.column_config.ProgressColumn("Win% Hard",    min_value=0, max_value=1, format="%.0%"),
        "Win% GS":      st.column_config.ProgressColumn("Win% GS",      min_value=0, max_value=1, format="%.0%"),
    }
)

st.markdown("---")

# ── Graficos ──────────────────────────────────────────────────────────────
st.markdown('<p class="section-header">📊 ESTADÍSTICAS GENERALES</p>', unsafe_allow_html=True)

c1, c2 = st.columns(2)

with c1:
    top_srv = df_master[df_master["aces_2026"].notna()].nlargest(8,"aces_2026")[["player_name","aces_2026"]]
    fig2 = px.bar(top_srv, x="aces_2026", y="player_name", orientation="h",
                  title="🎯 Top 8 Servidores 2026 (Aces en Hard)",
                  color="aces_2026", color_continuous_scale="Greens",
                  template="plotly_dark", labels={"aces_2026":"Aces","player_name":""})
    fig2.update_layout(paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)",
                       showlegend=False, coloraxis_showscale=False,
                       yaxis=dict(autorange="reversed"), height=320,
                       margin=dict(l=10,r=10,t=40,b=10))
    st.plotly_chart(fig2, use_container_width=True)

with c2:
    df_hard = df_master[df_master["winpct_en_hard_52w"].notna()].copy()
    df_hard = df_hard[df_hard["winpct_en_hard_52w"] <= 1]
    fig3 = px.histogram(df_hard, x="winpct_en_hard_52w", nbins=20,
                        title="📈 Distribución Win% en Hard (52w)",
                        template="plotly_dark",
                        labels={"winpct_en_hard_52w":"Win% en Hard"},
                        color_discrete_sequence=["#2e8b57"])
    fig3.update_layout(paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)",
                       height=320, margin=dict(l=10,r=10,t=40,b=10), showlegend=False)
    st.plotly_chart(fig3, use_container_width=True)

st.markdown("---")
st.markdown("""
<p style="text-align:center;color:#333;font-size:0.8rem">
US Open 2026 Analytics Platform · Capstone Project · Datos: ATP Tour & Jeff Sackmann
</p>
""", unsafe_allow_html=True)
