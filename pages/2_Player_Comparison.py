import streamlit as st
import pandas as pd
import numpy as np
import plotly.graph_objects as go

st.set_page_config(page_title="Player Comparison", page_icon="⚖️", layout="wide")

st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Bebas+Neue&family=Inter:wght@300;400;600;700;900&display=swap');
* { font-family: 'Inter', sans-serif; }
.stApp { background-color: #050505; }
[data-testid="stSidebar"] { background: rgba(5,5,5,0.98) !important; border-right: 1px solid rgba(0,255,136,0.15) !important; }
[data-testid="stSidebar"] * { color: rgba(255,255,255,0.6) !important; }
.section-header { font-family: 'Bebas Neue', sans-serif; font-size: 1.5rem; color: #ffffff; border-bottom: 1px solid rgba(0,255,136,0.3); padding-bottom: 8px; margin: 24px 0 16px 0; letter-spacing: 2px; }
.section-label { font-size: 0.7rem; font-weight: 700; letter-spacing: 3px; color: #00ff88; text-transform: uppercase; margin-bottom: 4px; }
div[data-baseweb="select"] > div { background: rgba(255,255,255,0.04) !important; border: 1px solid rgba(0,255,136,0.25) !important; border-radius: 10px !important; color: white !important; }
</style>
""", unsafe_allow_html=True)

@st.cache_data
def load_data():
    url = "https://raw.githubusercontent.com/Raulalfonso03/us-open-2026-analytics/main/df_master_final.csv"
    df = pd.read_csv(url, sep=None, engine="python")
    winpct_cols = [c for c in df.columns if 'winpct' in c]
    for col in winpct_cols:
        df[col] = pd.to_numeric(df[col], errors='coerce')
        mask = df[col] > 1
        df.loc[mask, col] = df.loc[mask, col] / 1000
    return df

df = load_data()

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
    "Hubert Hurkacz":               "https://www.atptour.com/-/media/alias/player-headshot/HB71",
    "Sebastian Korda":              "https://www.atptour.com/-/media/alias/player-headshot/K0AH",
    "Stefanos Tsitsipas":           "https://www.atptour.com/-/media/alias/player-headshot/TE51",
    "Cameron Norrie":               "https://www.atptour.com/-/media/alias/player-headshot/N771",
    "Brandon Nakashima":            "https://www.atptour.com/-/media/alias/player-headshot/N0AE",
    "Denis Shapovalov":             "https://www.atptour.com/-/media/alias/player-headshot/SU55",
    "Tomas Machac":                 "https://www.atptour.com/-/media/alias/player-headshot/M0FH",
    "Alejandro Davidovich Fokina":  "https://www.atptour.com/-/media/alias/player-headshot/DH50",
    "Francisco Cerundolo":          "https://www.atptour.com/-/media/alias/player-headshot/C0AU",
    "Nuno Borges":                  "https://www.atptour.com/-/media/alias/player-headshot/BT72",
    "Matteo Berrettini":            "https://www.atptour.com/-/media/alias/player-headshot/BE36",
    "Alex Michelsen":               "https://www.atptour.com/-/media/alias/player-headshot/M0QI",
    "Miomir Kecmanovic":            "https://www.atptour.com/-/media/alias/player-headshot/KI95",
    "Sebastian Baez":               "https://www.atptour.com/-/media/alias/player-headshot/B0BI",
    "Arthur Rinderknech":           "https://www.atptour.com/-/media/alias/player-headshot/RC91",
    "Zizou Bergs":                  "https://www.atptour.com/-/media/alias/player-headshot/BU13",
    "Stan Wawrinka":                "https://www.atptour.com/-/media/alias/player-headshot/W367",
    "Giovanni Mpetshi Perricard":   "https://www.atptour.com/-/media/alias/player-headshot/M0GZ",
}

# Title
st.markdown("""
<div style="text-align:center;padding:40px 0 20px 0">
    <div style="font-size:0.7rem;font-weight:700;letter-spacing:4px;color:#00ff88;text-transform:uppercase;margin-bottom:8px">US Open 2026</div>
    <div style="font-family:'Bebas Neue',sans-serif;font-size:4rem;color:#ffffff;letter-spacing:3px;line-height:1">PLAYER COMPARISON</div>
    <div style="color:rgba(255,255,255,0.3);font-size:0.9rem;margin-top:8px;letter-spacing:2px">Compare two players head to head</div>
</div>
<hr style="border:none;border-top:1px solid rgba(255,255,255,0.06);margin:0 0 24px 0">
""", unsafe_allow_html=True)

jugadores = sorted(df["player_name"].dropna().unique().tolist())

col1, col_vs, col2 = st.columns([2, 0.4, 2])
with col1:
    p1 = st.selectbox("Player 1", jugadores,
                       index=jugadores.index("Jannik Sinner") if "Jannik Sinner" in jugadores else 0)
with col_vs:
    st.markdown("<br><br><div style='text-align:center;font-size:1.5rem;font-weight:900;color:#00ff88'>VS</div>", unsafe_allow_html=True)
with col2:
    p2 = st.selectbox("Player 2", jugadores,
                       index=jugadores.index("Carlos Alcaraz") if "Carlos Alcaraz" in jugadores else 1)

player1 = df[df["player_name"] == p1].iloc[0]
player2 = df[df["player_name"] == p2].iloc[0]

st.markdown("---")

# Player headers with photos
col1, col2 = st.columns(2)

def get_rank(p):
    r = p.get("atp_rank_current")
    return int(r) if pd.notna(r) else "N/A"

def get_hard(p):
    h = p.get("winpct_en_hard_52w")
    return f"{h*100:.1f}%" if pd.notna(h) and h <= 1 else "N/A"

with col1:
    foto1 = fotos.get(p1, "")
    r1 = get_rank(player1)
    h1 = get_hard(player1)
    photo_html1 = f'<img src="{foto1}" style="width:120px;height:120px;object-fit:cover;object-position:top;border-radius:50%;border:3px solid #00ff88;margin-bottom:12px">' if foto1 else '<div style="width:120px;height:120px;background:rgba(255,255,255,0.05);border-radius:50%;border:3px solid #00ff88;display:flex;align-items:center;justify-content:center;font-size:3rem;margin-bottom:12px">🎾</div>'
    st.markdown(f"""
    <div style="background:linear-gradient(135deg,rgba(0,255,136,0.05),rgba(0,0,0,0));border:2px solid #00ff88;
                border-radius:16px;padding:24px;text-align:center">
        {photo_html1}
        <h2 style="color:#00ff88;margin:0;font-size:1.4rem;font-weight:900">{p1}</h2>
        <p style="color:rgba(255,255,255,0.4);margin:4px 0;font-size:0.85rem">ATP #{r1} · Hard: {h1}</p>
    </div>""", unsafe_allow_html=True)

with col2:
    foto2 = fotos.get(p2, "")
    r2 = get_rank(player2)
    h2 = get_hard(player2)
    photo_html2 = f'<img src="{foto2}" style="width:120px;height:120px;object-fit:cover;object-position:top;border-radius:50%;border:3px solid #2e8b57;margin-bottom:12px">' if foto2 else '<div style="width:120px;height:120px;background:rgba(255,255,255,0.05);border-radius:50%;border:3px solid #2e8b57;display:flex;align-items:center;justify-content:center;font-size:3rem;margin-bottom:12px">🎾</div>'
    st.markdown(f"""
    <div style="background:linear-gradient(135deg,rgba(46,139,87,0.05),rgba(0,0,0,0));border:2px solid #2e8b57;
                border-radius:16px;padding:24px;text-align:center">
        {photo_html2}
        <h2 style="color:#2e8b57;margin:0;font-size:1.4rem;font-weight:900">{p2}</h2>
        <p style="color:rgba(255,255,255,0.4);margin:4px 0;font-size:0.85rem">ATP #{r2} · Hard: {h2}</p>
    </div>""", unsafe_allow_html=True)

st.markdown("---")

# Winner prediction banner
st.markdown("---")

def calcular_score(p):
    hard = pd.to_numeric(p.get("winpct_en_hard_52w"), errors="coerce")
    gs   = pd.to_numeric(p.get("winpct_grand_slams_52w"), errors="coerce")
    ov   = pd.to_numeric(p.get("winpct_overall_52w"), errors="coerce")
    rank = pd.to_numeric(p.get("atp_rank_current"), errors="coerce")
    hard = hard if pd.notna(hard) and hard <= 1 else 0.5
    gs   = gs   if pd.notna(gs)   and gs <= 1   else 0.5
    ov   = ov   if pd.notna(ov)   and ov <= 1   else 0.5
    rank = rank if pd.notna(rank) else 50
    return hard*0.35 + gs*0.25 + ov*0.20 + (1 - rank/200)*0.20

s1 = calcular_score(player1)
s2 = calcular_score(player2)
total = s1 + s2
prob1 = round(s1/total*100, 1)
prob2 = round(s2/total*100, 1)
winner = p1 if s1 > s2 else p2
winner_prob = prob1 if s1 > s2 else prob2
loser_prob  = prob2 if s1 > s2 else prob1
loser  = p2 if s1 > s2 else p1

st.markdown(f"""
<div style="background:linear-gradient(135deg,rgba(0,255,136,0.08),rgba(0,0,0,0));
            border:1px solid rgba(0,255,136,0.4);border-radius:16px;padding:24px;
            text-align:center;margin:16px 0">
    <div style="font-size:0.7rem;font-weight:700;letter-spacing:4px;color:#00ff88;text-transform:uppercase;margin-bottom:8px">ML Prediction</div>
    <div style="font-family:'Bebas Neue',sans-serif;font-size:1rem;color:rgba(255,255,255,0.4);letter-spacing:2px;margin-bottom:4px">PREDICTED WINNER</div>
    <div style="font-family:'Bebas Neue',sans-serif;font-size:3rem;color:#00ff88;letter-spacing:2px;line-height:1">{winner}</div>
    <div style="display:flex;justify-content:center;align-items:center;gap:32px;margin-top:16px">
        <div style="text-align:center">
            <div style="font-size:2rem;font-weight:900;color:#00ff88">{winner_prob}%</div>
            <div style="font-size:0.7rem;color:rgba(255,255,255,0.3);letter-spacing:1px;text-transform:uppercase">{winner}</div>
        </div>
        <div style="color:rgba(255,255,255,0.2);font-size:1.5rem">vs</div>
        <div style="text-align:center">
            <div style="font-size:2rem;font-weight:900;color:rgba(255,255,255,0.4)">{loser_prob}%</div>
            <div style="font-size:0.7rem;color:rgba(255,255,255,0.3);letter-spacing:1px;text-transform:uppercase">{loser}</div>
        </div>
    </div>
    <div style="background:rgba(255,255,255,0.06);border-radius:4px;height:6px;margin-top:16px;overflow:hidden">
        <div style="width:{winner_prob}%;height:6px;background:linear-gradient(90deg,#1a472a,#00ff88);border-radius:4px"></div>
    </div>
</div>
""", unsafe_allow_html=True)

def compare_row(label, col, p1d, p2d, higher_better=True, is_pct=True):
    v1 = pd.to_numeric(p1d.get(col), errors="coerce")
    v2 = pd.to_numeric(p2d.get(col), errors="coerce")
    if pd.isna(v1) and pd.isna(v2): return

    def fmt(v):
        if pd.isna(v): return "N/A"
        if is_pct and v <= 1: return f"{v*100:.1f}%"
        if is_pct: return f"{v:.1f}%"
        return f"{v:.0f}"

    if pd.notna(v1) and pd.notna(v2):
        p1w = v1 > v2 if higher_better else v1 < v2
        c1 = "#00ff88" if p1w else "#ffffff"
        c2 = "#2e8b57" if not p1w else "#ffffff"
        arrow = "◀" if p1w else "▶"
    else:
        c1, c2, arrow = "#ffffff", "#ffffff", "—"

    st.markdown(f"""
    <div style="display:grid;grid-template-columns:1fr auto 1fr;align-items:center;
                padding:10px 0;border-bottom:1px solid rgba(255,255,255,0.05);gap:8px">
        <div style="text-align:right;color:{c1};font-weight:700;font-size:1rem">{fmt(v1)}</div>
        <div style="text-align:center;color:rgba(255,255,255,0.3);font-size:0.8rem;min-width:160px">{arrow} {label} {arrow}</div>
        <div style="text-align:left;color:{c2};font-weight:700;font-size:1rem">{fmt(v2)}</div>
    </div>""", unsafe_allow_html=True)

st.markdown('<div class="section-label">Last 52 Weeks</div>', unsafe_allow_html=True)
st.markdown('<div class="section-header">GENERAL STATS</div>', unsafe_allow_html=True)
compare_row("ATP Ranking", "atp_rank_current", player1, player2, higher_better=False, is_pct=False)
compare_row("Win% Overall", "winpct_overall_52w", player1, player2)
compare_row("Win% Hard Court", "winpct_en_hard_52w", player1, player2)
compare_row("Win% Grand Slams", "winpct_grand_slams_52w", player1, player2)
compare_row("Win% Masters 1000", "winpct_masters_1000_52w", player1, player2)
compare_row("Titles (52w)", "titulos_52w", player1, player2, is_pct=False)

st.markdown('<div class="section-label">Hard Court 2026</div>', unsafe_allow_html=True)
st.markdown('<div class="section-header">SERVE STATS</div>', unsafe_allow_html=True)
compare_row("1st Serve %", "1er_saque_pct_2026", player1, player2)
compare_row("1st Serve Won %", "1er_saque_ganado_pct_2026", player1, player2)
compare_row("2nd Serve Won %", "2do_saque_ganado_pct_2026", player1, player2)
compare_row("BP Saved %", "bp_salvados_pct_2026", player1, player2)
compare_row("Aces 2026", "aces_2026", player1, player2, is_pct=False)

st.markdown('<div class="section-label">Hard Court 2026</div>', unsafe_allow_html=True)
st.markdown('<div class="section-header">RETURN STATS</div>', unsafe_allow_html=True)
compare_row("1st Serve Return %", "resto_1er_pct_2026", player1, player2)
compare_row("2nd Serve Return %", "resto_2do_pct_2026", player1, player2)
compare_row("BP Converted %", "bp_convertidos_pct_2026", player1, player2)

st.markdown('<div class="section-label">Last 52 Weeks</div>', unsafe_allow_html=True)
st.markdown('<div class="section-header">PRESSURE PERFORMANCE</div>', unsafe_allow_html=True)
compare_row("After winning 1st set", "winpct_tras_ganar_set1_52w", player1, player2)
compare_row("After losing 1st set", "winpct_tras_perder_set1_52w", player1, player2)
compare_row("Deciding set", "winpct_set_decisivo_52w", player1, player2)
compare_row("Tiebreak", "winpct_tiebreak_52w", player1, player2)
compare_row("Finals", "winpct_finales_52w", player1, player2)
compare_row("vs Top 10", "winpct_vs_top10_52w", player1, player2)

st.markdown("---")
st.markdown('<div class="section-label">Visual Comparison</div>', unsafe_allow_html=True)
st.markdown('<div class="section-header">RADAR CHART</div>', unsafe_allow_html=True)

cats = ["Win%\nHard","Win%\nGS","1st Serve\nWon","BP\nSaved","Deciding\nSet","Win%\nOverall"]
cols_r = ["winpct_en_hard_52w","winpct_grand_slams_52w","1er_saque_ganado_pct_2026",
          "bp_salvados_pct_2026","winpct_set_decisivo_52w","winpct_overall_52w"]

def get_radar(player, cols):
    vals = []
    for c in cols:
        v = pd.to_numeric(player.get(c), errors="coerce")
        if pd.isna(v): vals.append(50)
        elif v <= 1: vals.append(v*100)
        else: vals.append(v)
    return vals

v1 = get_radar(player1, cols_r)
v2 = get_radar(player2, cols_r)

fig = go.Figure()
fig.add_trace(go.Scatterpolar(r=v1+[v1[0]], theta=cats+[cats[0]], fill="toself", name=p1,
                               line=dict(color="#00ff88", width=2), fillcolor="rgba(0,255,136,0.1)"))
fig.add_trace(go.Scatterpolar(r=v2+[v2[0]], theta=cats+[cats[0]], fill="toself", name=p2,
                               line=dict(color="#2e8b57", width=2), fillcolor="rgba(46,139,87,0.1)"))
fig.update_layout(polar=dict(bgcolor="#0d1117", radialaxis=dict(visible=True, range=[0,100], tickfont=dict(color="#555"))),
                  template="plotly_dark", paper_bgcolor="rgba(0,0,0,0)",
                  height=420, legend=dict(font=dict(color="white")), margin=dict(l=40,r=40,t=40,b=40))
st.plotly_chart(fig, use_container_width=True)

st.markdown("---")
st.markdown('<p style="text-align:center;color:rgba(255,255,255,0.15);font-size:0.8rem">US Open 2026 Analytics Platform · Capstone Project</p>', unsafe_allow_html=True)


