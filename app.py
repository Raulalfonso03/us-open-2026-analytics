import streamlit as st
import pandas as pd
import numpy as np
import plotly.graph_objects as go

st.set_page_config(
    page_title="US Open 2026 Analytics",
    page_icon="🎾",
    layout="wide",
    initial_sidebar_state="collapsed"
)

st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Bebas+Neue&family=Inter:wght@300;400;600;700;900&display=swap');

* { font-family: 'Inter', sans-serif; }
.stApp {
    background-color: #050505;
    background-image: radial-gradient(ellipse at 20% 50%, rgba(0,100,0,0.08) 0%, transparent 50%);
}
header[data-testid="stHeader"] { background: transparent; }
[data-testid="stSidebar"] { display: none; }
.block-container { padding: 0 !important; max-width: 100% !important; }

.hero {
    background:
        linear-gradient(180deg, rgba(5,5,5,0) 0%, rgba(5,5,5,0.7) 60%, rgba(5,5,5,1) 100%),
        url('https://upload.wikimedia.org/wikipedia/commons/thumb/3/3e/USTA_Billie_Jean_King_National_Tennis_Center.jpg/1280px-USTA_Billie_Jean_King_National_Tennis_Center.jpg');
    background-size: cover;
    background-position: center top;
    min-height: 85vh;
    display: flex;
    flex-direction: column;
    justify-content: flex-end;
    padding: 60px;
}

.hero-badge {
    display: inline-block;
    background: rgba(0,255,136,0.15);
    border: 1px solid #00ff88;
    color: #00ff88;
    padding: 6px 16px;
    border-radius: 20px;
    font-size: 0.75rem;
    font-weight: 700;
    letter-spacing: 3px;
    text-transform: uppercase;
    margin-bottom: 16px;
    width: fit-content;
}

.hero-title {
    font-family: 'Bebas Neue', sans-serif;
    font-size: 9rem;
    color: #ffffff;
    line-height: 0.9;
    letter-spacing: 2px;
    margin-bottom: 8px;
}

.hero-title span { color: #00ff88; }

.hero-subtitle {
    color: rgba(255,255,255,0.5);
    font-size: 1rem;
    letter-spacing: 4px;
    text-transform: uppercase;
    margin-bottom: 32px;
}

.hero-stats { display: flex; gap: 40px; margin-bottom: 40px; }

.hero-stat-value { font-size: 2rem; font-weight: 900; color: #ffffff; line-height: 1; }
.hero-stat-label { font-size: 0.7rem; color: rgba(255,255,255,0.4); letter-spacing: 2px; text-transform: uppercase; margin-top: 4px; }

.nav {
    display: flex;
    gap: 8px;
    padding: 16px 60px;
    background: rgba(5,5,5,0.95);
    border-bottom: 1px solid rgba(255,255,255,0.05);
    position: sticky;
    top: 0;
    z-index: 100;
    overflow-x: auto;
}

.nav-item {
    padding: 8px 20px;
    border-radius: 6px;
    font-size: 0.85rem;
    font-weight: 600;
    color: rgba(255,255,255,0.5);
    white-space: nowrap;
    text-decoration: none;
}

.nav-item.active { color: #00ff88; background: rgba(0,255,136,0.1); }

.section { padding: 60px; max-width: 1400px; margin: 0 auto; }

.section-label {
    font-size: 0.7rem;
    font-weight: 700;
    letter-spacing: 4px;
    text-transform: uppercase;
    color: #00ff88;
    margin-bottom: 8px;
}

.section-title {
    font-family: 'Bebas Neue', sans-serif;
    font-size: 4rem;
    color: #ffffff;
    line-height: 1;
    margin-bottom: 40px;
}

.players-grid {
    display: grid;
    grid-template-columns: repeat(auto-fill, minmax(200px, 1fr));
    gap: 16px;
    margin-bottom: 40px;
}

.player-card {
    background: rgba(255,255,255,0.03);
    border: 1px solid rgba(255,255,255,0.06);
    border-radius: 16px;
    overflow: hidden;
    position: relative;
    transition: all 0.3s;
}

.player-card:hover {
    border-color: #00ff88;
    transform: translateY(-4px);
    box-shadow: 0 20px 40px rgba(0,255,136,0.1);
}

.player-card-img {
    width: 100%;
    height: 180px;
    object-fit: cover;
    object-position: top;
    background: linear-gradient(135deg, #0d1117, #1a2a1a);
    display: block;
}

.player-card-body { padding: 16px; }
.player-card-rank { font-size: 0.65rem; font-weight: 700; letter-spacing: 2px; color: #00ff88; text-transform: uppercase; margin-bottom: 4px; }
.player-card-name { font-size: 1rem; font-weight: 700; color: #ffffff; margin-bottom: 8px; line-height: 1.2; }
.player-card-prob { font-size: 1.6rem; font-weight: 900; color: #00ff88; line-height: 1; }
.player-card-prob-label { font-size: 0.65rem; color: rgba(255,255,255,0.3); text-transform: uppercase; letter-spacing: 1px; }
.player-card-bar { height: 3px; background: rgba(255,255,255,0.06); border-radius: 2px; margin-top: 12px; overflow: hidden; }
.player-card-bar-fill { height: 100%; background: linear-gradient(90deg, #00ff88, #00bfff); border-radius: 2px; }

.injury-tag {
    position: absolute; top: 12px; right: 12px;
    background: rgba(255,68,68,0.9); color: white;
    font-size: 0.6rem; font-weight: 700; padding: 3px 8px;
    border-radius: 4px; letter-spacing: 1px;
}

.doubt-tag {
    position: absolute; top: 12px; right: 12px;
    background: rgba(255,170,0,0.9); color: black;
    font-size: 0.6rem; font-weight: 700; padding: 3px 8px;
    border-radius: 4px; letter-spacing: 1px;
}

.ranking-table { width: 100%; border-collapse: collapse; }
.ranking-table th {
    font-size: 0.65rem; font-weight: 700; letter-spacing: 2px;
    text-transform: uppercase; color: rgba(255,255,255,0.3);
    padding: 12px 16px; text-align: left;
    border-bottom: 1px solid rgba(255,255,255,0.05);
}
.ranking-table td { padding: 14px 16px; border-bottom: 1px solid rgba(255,255,255,0.03); color: rgba(255,255,255,0.8); font-size: 0.9rem; }
.ranking-table tr:hover td { background: rgba(255,255,255,0.02); }
.rank-num { font-weight: 900; color: rgba(255,255,255,0.2); font-size: 1.1rem; }
.rank-name { font-weight: 700; color: #ffffff; }
.rank-hard { font-weight: 700; color: #00ff88; }

.progress-mini { height: 4px; background: rgba(255,255,255,0.06); border-radius: 2px; width: 80px; display: inline-block; vertical-align: middle; margin-left: 8px; }
.progress-mini-fill { height: 100%; background: #00ff88; border-radius: 2px; }

.divider { height: 1px; background: linear-gradient(90deg, transparent, rgba(255,255,255,0.06), transparent); margin: 0 60px; }

.footer { padding: 40px 60px; text-align: center; color: rgba(255,255,255,0.2); font-size: 0.8rem; letter-spacing: 1px; border-top: 1px solid rgba(255,255,255,0.04); margin-top: 40px; }
</style>
""", unsafe_allow_html=True)

@st.cache_data
def load_data():
    base = "https://raw.githubusercontent.com/Raulalfonso03/us-open-2026-analytics/main/"
    df_master = pd.read_csv(base + "df_master_final.csv", sep=None, engine="python")
    df_pred   = pd.read_csv(base + "us_open_predictions.csv", sep=None, engine="python")
    return df_master, df_pred

df_master, df_pred = load_data()

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
    "Alexander Bublik":      "https://www.atptour.com/-/media/alias/player-headshot/BK92",
    "Casper Ruud":           "https://www.atptour.com/-/media/alias/player-headshot/RH16",
}

# HERO
st.markdown(f"""
<div class="hero">
    <div class="hero-badge">🎾 Grand Slam · Hard Court · New York</div>
    <div class="hero-title">US <span>OPEN</span><br>2026</div>
    <div class="hero-subtitle">Analytics & Prediction Platform · Powered by Machine Learning</div>
    <div class="hero-stats">
        <div class="hero-stat">
            <div class="hero-stat-value">{len(df_master)}</div>
            <div class="hero-stat-label">Players analyzed</div>
        </div>
        <div class="hero-stat">
            <div class="hero-stat-value">65.2%</div>
            <div class="hero-stat-label">Model accuracy</div>
        </div>
        <div class="hero-stat">
            <div class="hero-stat-value">4,581</div>
            <div class="hero-stat-label">Matches analyzed</div>
        </div>
        <div class="hero-stat">
            <div class="hero-stat-value">26 Aug</div>
            <div class="hero-stat-label">Tournament start</div>
        </div>
    </div>
</div>
""", unsafe_allow_html=True)

# NAV
st.markdown("""
<div class="nav">
    <a class="nav-item active" href="/">Home</a>
    <a class="nav-item" href="/1_Player_Profiles">Player Profiles</a>
    <a class="nav-item" href="/2_Player_Comparison">Comparison</a>
    <a class="nav-item" href="/3_Match_Prediction">Match Prediction</a>
    <a class="nav-item" href="/4_Tournament_Prediction">Tournament</a>
    <a class="nav-item" href="/5_Analytics_Dashboard">Dashboard</a>
    <a class="nav-item" href="/6_ML_Model">ML Model</a>
    <a class="nav-item" href="/7_About">About</a>
</div>
""", unsafe_allow_html=True)
    <a class="nav-item" href="/1_Player_Profiles">👤 Player Profiles</a>
    <a class="nav-item" href="/2_Player_Comparison">⚖️ Comparison</a>
    <a class="nav-item" href="/3_Match_Prediction">🔮 Match Prediction</a>
    <a class="nav-item" href="/4_Tournament_Prediction">🏆 Tournament</a>
    <a class="nav-item" href="/5_Analytics_Dashboard">📊 Dashboard</a>
    <a class="nav-item" href="/6_ML_Model">🤖 ML Model</a>
    <a class="nav-item" href="/7_About">ℹ️ About</a>
</div>
""", unsafe_allow_html=True)

# TOP CONTENDERS
st.markdown("""
<div class="section">
    <div class="section-label">2026 Predictions</div>
    <div class="section-title">Top Contenders</div>
""", unsafe_allow_html=True)

cols = st.columns(6)
for i, row in df_pred.head(12).iterrows():
    name   = row["Jugador"]
    prob   = row["Prob US Open"]
    rank   = int(row["Ranking ATP"]) if pd.notna(row.get("Ranking ATP")) else "?"
    estado = row.get("Estado", "FIT")
    foto   = fotos.get(name, "")
    
    with cols[i % 6]:
        if estado == "LESIONADO":
            badge = "🔴 INJURED"
            color = "#ff4444"
        elif estado == "DUDA":
            badge = "🟡 DOUBT"
            color = "#ffaa00"
        else:
            badge = "🟢 FIT"
            color = "#00ff88"
        
        if foto:
            st.image(foto, use_container_width=True)
        
        st.markdown(f"""
        <div style="background:rgba(255,255,255,0.03);border:1px solid rgba(255,255,255,0.08);
                    border-radius:12px;padding:12px;margin-top:8px;text-align:center">
            <div style="color:#00ff88;font-size:0.65rem;font-weight:700;letter-spacing:2px">ATP #{rank}</div>
            <div style="color:#fff;font-weight:700;font-size:0.9rem;margin:4px 0">{name}</div>
            <div style="color:{color};font-size:1.4rem;font-weight:900">{prob}%</div>
            <div style="color:rgba(255,255,255,0.3);font-size:0.6rem">win probability</div>
            <div style="color:{color};font-size:0.7rem;margin-top:6px">{badge}</div>
        </div>
        """, unsafe_allow_html=True)

st.markdown('<div class="divider"></div>', unsafe_allow_html=True)

# ATP RANKING
st.markdown("""
<div class="section">
    <div class="section-label">Current standings</div>
    <div class="section-title">ATP Ranking</div>
""", unsafe_allow_html=True)

df_rank = df_master[df_master["atp_rank_current"].notna()].sort_values("atp_rank_current").head(15).copy()

table_html = """
<table class="ranking-table">
<thead><tr>
    <th>#</th><th>Player</th><th>Points</th><th>Hard Win%</th><th>GS Win%</th><th>Status</th>
</tr></thead><tbody>
"""

for _, row in df_rank.iterrows():
    rank   = int(row["atp_rank_current"])
    name   = row["player_name"]
    pts    = f"{int(row['atp_points_current']):,}" if pd.notna(row.get("atp_points_current")) else "-"
    hard   = row.get("winpct_en_hard_52w", 0)
    gs     = row.get("winpct_grand_slams_52w", 0)
    estado = row.get("injury_status", "FIT")
    hard_pct = f"{hard*100:.1f}%" if pd.notna(hard) and hard <= 1 else "-"
    gs_pct   = f"{gs*100:.1f}%"   if pd.notna(gs)   and gs <= 1   else "-"
    hard_w   = int(hard * 100)    if pd.notna(hard)  and hard <= 1 else 0

    if estado == "LESIONADO":
        status_html = '<span style="color:#ff4444;font-size:0.75rem;font-weight:700">⚠️ INJURED</span>'
    elif estado == "DUDA":
        status_html = '<span style="color:#ffaa00;font-size:0.75rem;font-weight:700">❓ DOUBT</span>'
    else:
        status_html = '<span style="color:#00ff88;font-size:0.75rem;font-weight:700">✅ FIT</span>'

    table_html += f"""<tr>
        <td class="rank-num">{rank}</td>
        <td class="rank-name">{name}</td>
        <td style="color:rgba(255,255,255,0.4)">{pts}</td>
        <td class="rank-hard">{hard_pct}
            <span class="progress-mini"><span class="progress-mini-fill" style="width:{hard_w}%"></span></span>
        </td>
        <td style="color:rgba(255,255,255,0.6)">{gs_pct}</td>
        <td>{status_html}</td>
    </tr>"""

table_html += "</tbody></table></div>"
st.markdown(table_html, unsafe_allow_html=True)

st.markdown('<div class="divider"></div>', unsafe_allow_html=True)

# PROBABILITY CHART
st.markdown("""
<div class="section">
    <div class="section-label">Machine Learning Model</div>
    <div class="section-title">Win Probabilities</div>
""", unsafe_allow_html=True)

colors = []
for _, row in df_pred.head(15).iterrows():
    if row.get("Estado") == "LESIONADO": colors.append("#ff4444")
    elif row.get("Estado") == "DUDA": colors.append("#ffaa00")
    else: colors.append("#00ff88")

fig = go.Figure(go.Bar(
    x=df_pred.head(15)["Prob US Open"],
    y=df_pred.head(15)["Jugador"],
    orientation="h",
    marker=dict(color=colors, opacity=0.85),
    text=df_pred.head(15)["Prob US Open"].apply(lambda x: f"{x}%"),
    textposition="outside",
    textfont=dict(color="rgba(255,255,255,0.6)", size=12)
))
fig.update_layout(
    template="plotly_dark",
    paper_bgcolor="rgba(0,0,0,0)",
    plot_bgcolor="rgba(0,0,0,0)",
    height=520,
    margin=dict(l=10, r=80, t=10, b=10),
    xaxis=dict(showgrid=False, showticklabels=False, range=[0, 7]),
    yaxis=dict(autorange="reversed", tickfont=dict(size=13, color="rgba(255,255,255,0.8)"),
               gridcolor="rgba(255,255,255,0.03)"),
    showlegend=False,
    font=dict(family="Inter")
)
st.plotly_chart(fig, use_container_width=True)
st.markdown("""
<p style="color:rgba(255,255,255,0.2);font-size:0.75rem;text-align:center;margin-top:-20px">
🟢 FIT &nbsp;&nbsp; 🟡 DOUBT &nbsp;&nbsp; 🔴 INJURED · Estimated probabilities, not real results
</p>
</div>
""", unsafe_allow_html=True)

# FOOTER
st.markdown("""
<div class="footer">
    US OPEN 2026 ANALYTICS PLATFORM · DATA ANALYTICS CAPSTONE PROJECT<br>
    <span style="color:rgba(0,255,136,0.4)">Data: ATP Tour · Jeff Sackmann · Kaggle · Jul 2026</span>
</div>
""", unsafe_allow_html=True)
