import streamlit as st
import pandas as pd
import numpy as np

st.set_page_config(page_title="Tournament Prediction", page_icon="🏆", layout="wide")

st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Bebas+Neue&family=Inter:wght@300;400;600;700;900&display=swap');
* { font-family: 'Inter', sans-serif; }
.stApp { background-color: #050505; }
[data-testid="stSidebar"] { background: rgba(5,5,5,0.98) !important; border-right: 1px solid rgba(0,255,136,0.15) !important; }
[data-testid="stSidebar"] * { color: rgba(255,255,255,0.6) !important; }
.section-header { font-family: 'Bebas Neue', sans-serif; font-size: 1.5rem; color: #ffffff; border-bottom: 1px solid rgba(0,255,136,0.3); padding-bottom: 8px; margin: 24px 0 16px 0; letter-spacing: 2px; }
.section-label { font-size: 0.7rem; font-weight: 700; letter-spacing: 3px; color: #00ff88; text-transform: uppercase; margin-bottom: 4px; }
[data-testid="metric-container"] { background: rgba(255,255,255,0.03); border: 1px solid rgba(255,255,255,0.08); border-radius: 12px; padding: 12px; }
[data-testid="stMetricValue"] { color: #00ff88 !important; font-weight: 900 !important; }
[data-testid="stMetricLabel"] { color: rgba(255,255,255,0.4) !important; font-size: 0.75rem !important; }
</style>
""", unsafe_allow_html=True)

@st.cache_data
def load_data():
    base = "https://raw.githubusercontent.com/Raulalfonso03/us-open-2026-analytics/main/"
    df_master = pd.read_csv(base + "df_master_final.csv", sep=None, engine="python")
    df_pred   = pd.read_csv(base + "us_open_predictions.csv", sep=None, engine="python")
    winpct_cols = [c for c in df_master.columns if 'winpct' in c]
    for col in winpct_cols:
        df_master[col] = pd.to_numeric(df_master[col], errors='coerce')
        mask = df_master[col] > 1
        df_master.loc[mask, col] = df_master.loc[mask, col] / 1000
    return df_master, df_pred

df_master, df_pred = load_data()

fotos = {
    "Jannik Sinner":                "https://www.atptour.com/-/media/alias/player-headshot/S0AG",
    "Carlos Alcaraz":               "https://www.atptour.com/-/media/alias/player-headshot/A0E2",
    "Alexander Zverev":             "https://www.atptour.com/-/media/alias/player-headshot/Z355",
    "Felix Auger-Aliassime":        "https://www.atptour.com/-/media/alias/player-headshot/AG37",
    "Ben Shelton":                  "https://www.atptour.com/-/media/alias/player-headshot/S0S1",
    "Alex de Minaur":               "https://www.atptour.com/-/media/alias/player-headshot/DH58",
    "Taylor Fritz":                 "https://www.atptour.com/-/media/alias/player-headshot/FB98",
    "Novak Djokovic":               "https://www.atptour.com/-/media/alias/player-headshot/D643",
    "Daniil Medvedev":              "https://www.atptour.com/-/media/alias/player-headshot/MM58",
    "Flavio Cobolli":               "https://www.atptour.com/-/media/alias/player-headshot/C0E9",
    "Alexander Bublik":             "https://www.atptour.com/-/media/alias/player-headshot/BK92",
    "Casper Ruud":                  "https://www.atptour.com/-/media/alias/player-headshot/RH16",
    "Andrey Rublev":                "https://www.atptour.com/-/media/alias/player-headshot/RE44",
    "Jiri Lehecka":                 "https://www.atptour.com/-/media/alias/player-headshot/L0BV",
    "Jakub Mensik":                 "https://www.atptour.com/-/media/alias/player-headshot/M0NI",
    "Learner Tien":                 "https://www.atptour.com/-/media/alias/player-headshot/T0HA",
    "Frances Tiafoe":               "https://www.atptour.com/-/media/alias/player-headshot/TD51",
    "Tommy Paul":                   "https://www.atptour.com/-/media/alias/player-headshot/PL56",
    "Lorenzo Musetti":              "https://www.atptour.com/-/media/alias/player-headshot/M0EJ",
    "Karen Khachanov":              "https://www.atptour.com/-/media/alias/player-headshot/KE29",
    "Arthur Fils":                  "https://www.atptour.com/-/media/alias/player-headshot/F0F1",
    "Ugo Humbert":                  "https://www.atptour.com/-/media/alias/player-headshot/HH26",
    # --- Añadidos: jugadores que no tenían foto ---
    "Rafael Jodar":                 "https://www.atptour.com/-/media/alias/player-headshot/J0DZ",
    "Joao Fonseca":                 "https://www.atptour.com/-/media/alias/player-headshot/F0FV",
    "Francisco Cerundolo":          "https://www.atptour.com/-/media/alias/player-headshot/C0AU",
    "Cameron Norrie":               "https://www.atptour.com/-/media/alias/player-headshot/N771",
    "Alejandro Davidovich Fokina":  "https://www.atptour.com/-/media/alias/player-headshot/DH50",
    "Arthur Rinderknech":           "https://www.atptour.com/-/media/alias/player-headshot/RC91",
    "Luciano Darderi":              "https://www.atptour.com/-/media/alias/player-headshot/D0FJ",
    "Valentin Vacherot":            "https://www.atptour.com/-/media/alias/player-headshot/VA25",
}

# Title
st.markdown("""
<div style="text-align:center;padding:40px 0 20px 0">
    <div style="font-size:0.7rem;font-weight:700;letter-spacing:4px;color:#00ff88;text-transform:uppercase;margin-bottom:8px">US Open 2026</div>
    <div style="font-family:'Bebas Neue',sans-serif;font-size:4rem;color:#ffffff;letter-spacing:3px;line-height:1">TOURNAMENT PREDICTION</div>
    <div style="flex:0 0 36px;color:rgba(255,255,255,0.2);font-weight:900;font-size:1rem;white-space:nowrap;overflow:visible">#{i+1}</div>
</div>
<hr style="border:none;border-top:1px solid rgba(255,255,255,0.06);margin:0 0 24px 0">
""", unsafe_allow_html=True)

# Tournament info
c1, c2, c3, c4 = st.columns(4)
with c1: st.metric("📅 Dates", "26 Aug - 7 Sep", "2026")
with c2: st.metric("🏟️ Venue", "Flushing Meadows", "New York")
with c3: st.metric("🎾 Surface", "Hard Court", "Outdoor")
with c4: st.metric("🏆 Defending Champion", "Carlos Alcaraz", "2025")

st.markdown("---")

# Top 3 podium
st.markdown('<div class="section-label">Top Favorites</div>', unsafe_allow_html=True)
st.markdown('<div class="section-header">PODIUM</div>', unsafe_allow_html=True)

top3 = df_pred.head(3)
medals = ["🥇", "🥈", "🥉"]
border_colors = ["#FFD700", "#C0C0C0", "#CD7F32"]

cols_podium = st.columns(3)
for i, (col, (_, row)) in enumerate(zip(cols_podium, top3.iterrows())):
    name   = row["Jugador"]
    prob   = row["Prob US Open"]
    rank   = int(row["Ranking ATP"]) if pd.notna(row.get("Ranking ATP")) else "?"
    hard   = row.get("Win% Hard", "N/A")
    gs     = row.get("Win% GS", "N/A")
    estado = row.get("Estado", "FIT")
    foto   = fotos.get(name, "")

    if estado == "LESIONADO":
        badge = '<span style="background:rgba(255,68,68,0.2);color:#ff4444;border:1px solid #ff4444;border-radius:4px;padding:2px 8px;font-size:0.65rem;font-weight:700">INJURED</span>'
    elif estado == "DUDA":
        badge = '<span style="background:rgba(255,170,0,0.2);color:#ffaa00;border:1px solid #ffaa00;border-radius:4px;padding:2px 8px;font-size:0.65rem;font-weight:700">DOUBT</span>'
    else:
        badge = '<span style="background:rgba(0,255,136,0.1);color:#00ff88;border:1px solid #00ff88;border-radius:4px;padding:2px 8px;font-size:0.65rem;font-weight:700">FIT</span>'

    img_html = f'<img src="{foto}" style="width:110px;height:110px;object-fit:cover;object-position:top;border-radius:50%;border:3px solid {border_colors[i]};margin-bottom:12px">' if foto else f'<div style="width:110px;height:110px;background:rgba(255,255,255,0.05);border-radius:50%;border:3px solid {border_colors[i]};display:flex;align-items:center;justify-content:center;font-size:3rem;margin-bottom:12px">🎾</div>'

    with col:
        st.markdown(f"""
        <div style="background:rgba(255,255,255,0.02);border:1px solid {border_colors[i]}40;
                    border-radius:16px;padding:24px;text-align:center">
            <div style="font-size:1.5rem;margin-bottom:8px">{medals[i]}</div>
            <div style="display:flex;justify-content:center">{img_html}</div>
            <div style="font-size:1.1rem;font-weight:900;color:#ffffff;margin-bottom:4px">{name}</div>
            <div style="color:rgba(255,255,255,0.4);font-size:0.8rem;margin-bottom:8px">ATP #{rank}</div>
            {badge}
            <div style="font-size:2.5rem;font-weight:900;color:{border_colors[i]};margin-top:12px;line-height:1">{prob}%</div>
            <div style="color:rgba(255,255,255,0.3);font-size:0.65rem;letter-spacing:1px;text-transform:uppercase">win probability</div>
            <div style="color:rgba(255,255,255,0.3);font-size:0.75rem;margin-top:8px">Hard: {hard} · GS: {gs}</div>
        </div>""", unsafe_allow_html=True)

st.markdown("---")

# Full ranking list
st.markdown('<div class="section-label">All Contenders</div>', unsafe_allow_html=True)
st.markdown('<div class="section-header">FULL RANKINGS</div>', unsafe_allow_html=True)

for i, row in df_pred.iterrows():
    name   = row["Jugador"]
    prob   = row["Prob US Open"]
    rank   = int(row["Ranking ATP"]) if pd.notna(row.get("Ranking ATP")) else "?"
    hard   = row.get("Win% Hard", "N/A")
    estado = row.get("Estado", "FIT")
    foto   = fotos.get(name, "")

    if estado == "LESIONADO":
        badge = '<span style="background:rgba(255,68,68,0.2);color:#ff4444;border-radius:4px;padding:2px 6px;font-size:0.6rem;font-weight:700">INJURED</span>'
        bar_color = "#ff4444"
    elif estado == "DUDA":
        badge = '<span style="background:rgba(255,170,0,0.2);color:#ffaa00;border-radius:4px;padding:2px 6px;font-size:0.6rem;font-weight:700">DOUBT</span>'
        bar_color = "#ffaa00"
    else:
        badge = '<span style="background:rgba(0,255,136,0.1);color:#00ff88;border-radius:4px;padding:2px 6px;font-size:0.6rem;font-weight:700">FIT</span>'
        bar_color = "#00ff88"

    img_html = f'<img src="{foto}" style="width:40px;height:40px;object-fit:cover;object-position:top;border-radius:50%;border:2px solid {bar_color}">' if foto else f'<div style="width:40px;height:40px;background:rgba(255,255,255,0.05);border-radius:50%;border:2px solid {bar_color};display:flex;align-items:center;justify-content:center;font-size:1.2rem">🎾</div>'

    st.markdown(f"""
    <div style="background:rgba(255,255,255,0.02);border:1px solid rgba(255,255,255,0.05);
                border-radius:10px;padding:12px 16px;margin:6px 0">
        <div style="display:flex;align-items:center;gap:12px;margin-bottom:8px">
            <div style="color:rgba(255,255,255,0.2);font-weight:900;font-size:1rem;width:24px">#{i+1}</div>
            {img_html}
            <div style="flex:1">
                <div style="color:#ffffff;font-weight:700;font-size:0.95rem">{name}</div>
                <div style="color:rgba(255,255,255,0.3);font-size:0.75rem">ATP #{rank} · Hard: {hard}</div>
            </div>
            {badge}
            <div style="color:{bar_color};font-weight:900;font-size:1.1rem">{prob}%</div>
        </div>
        <div style="background:rgba(255,255,255,0.06);border-radius:3px;height:4px;overflow:hidden">
            <div style="width:{prob*15}%;height:4px;background:{bar_color};border-radius:3px"></div>
        </div>
    </div>""", unsafe_allow_html=True)

st.markdown("---")
st.markdown("""
<p style="text-align:center;color:rgba(255,255,255,0.15);font-size:0.75rem">
US Open 2026 Analytics Platform · Capstone Project · Estimated probabilities, not real results
</p>""", unsafe_allow_html=True)
