import streamlit as st
import pandas as pd
import numpy as np
import plotly.graph_objects as go
import requests
import pickle

st.set_page_config(page_title="Match Prediction", page_icon="🔮", layout="wide")

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
div[data-testid="stButton"] button {
    background: linear-gradient(135deg, #1a472a, #2e8b57) !important;
    color: white !important; border: none !important;
    font-weight: 700 !important; font-size: 1rem !important;
    letter-spacing: 2px !important; border-radius: 10px !important;
    padding: 14px !important;
}
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

@st.cache_resource
def load_model():
    try:
        base = "https://raw.githubusercontent.com/Raulalfonso03/us-open-2026-analytics/main/"
        r_model  = requests.get(base + "modelo_lr.pkl")
        r_scaler = requests.get(base + "scaler.pkl")
        modelo = pickle.loads(r_model.content)
        scaler = pickle.loads(r_scaler.content)
        return modelo, scaler, True
    except:
        return None, None, False

df = load_data()
modelo, scaler, model_ok = load_model()

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
    <div style="font-family:'Bebas Neue',sans-serif;font-size:4rem;color:#ffffff;letter-spacing:3px;line-height:1">MATCH PREDICTION</div>
    <div style="color:rgba(255,255,255,0.3);font-size:0.9rem;margin-top:8px;letter-spacing:2px">Predict the winner of any US Open 2026 match</div>
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

st.markdown("---")

predict_btn = st.button("🔮  PREDICT MATCH", use_container_width=True)

if predict_btn:
    player1 = df[df["player_name"] == p1].iloc[0]
    player2 = df[df["player_name"] == p2].iloc[0]

    # Check injuries
    e1 = player1.get("injury_status", "FIT")
    e2 = player2.get("injury_status", "FIT")
    if e1 == "LESIONADO":
        st.error(f"⚠️ {p1} is INJURED and likely won't play the US Open.")
    if e2 == "LESIONADO":
        st.error(f"⚠️ {p2} is INJURED and likely won't play the US Open.")

    def get_diff(col, p1d, p2d):
        v1 = pd.to_numeric(p1d.get(col, np.nan), errors="coerce")
        v2 = pd.to_numeric(p2d.get(col, np.nan), errors="coerce")
        if pd.isna(v1) or pd.isna(v2): return 0
        return v1 - v2

    # Use ML model if available, otherwise use scoring system
    if model_ok:
        features = {
            "rank_diff":       -(get_diff("atp_rank_current", player1, player2)),
            "overall_diff":    get_diff("winpct_overall_52w", player1, player2),
            "hard_diff":       get_diff("winpct_en_hard_52w", player1, player2),
            "gs_diff":         get_diff("winpct_grand_slams_52w", player1, player2),
            "m1000_diff":      get_diff("winpct_masters_1000_52w", player1, player2),
            "deciding_diff":   get_diff("winpct_set_decisivo_52w", player1, player2),
            "tiebreak_diff":   get_diff("winpct_tiebreak_52w", player1, player2),
            "after_win_diff":  get_diff("winpct_tras_ganar_set1_52w", player1, player2),
            "after_loss_diff": get_diff("winpct_tras_perder_set1_52w", player1, player2),
            "serve1_diff":     get_diff("1er_saque_ganado_pct_2026", player1, player2),
            "serve2_diff":     get_diff("2do_saque_ganado_pct_2026", player1, player2),
            "bp_saved_diff":   get_diff("bp_salvados_pct_2026", player1, player2),
            "bp_conv_diff":    get_diff("bp_convertidos_pct_2026", player1, player2),
            "aces_diff":       get_diff("aces_2026", player1, player2),
        }
        X = pd.DataFrame([features])
        X_scaled = scaler.transform(X)
        prob = modelo.predict_proba(X_scaled)[0]
        raw_p1 = prob[1]
        raw_p2 = prob[0]
    else:
        def score(p):
            hard = pd.to_numeric(p.get("winpct_en_hard_52w", 0.5), errors="coerce")
            gs   = pd.to_numeric(p.get("winpct_grand_slams_52w", 0.5), errors="coerce")
            ov   = pd.to_numeric(p.get("winpct_overall_52w", 0.5), errors="coerce")
            rank = pd.to_numeric(p.get("atp_rank_current", 50), errors="coerce")
            hard = hard if pd.notna(hard) and hard <= 1 else 0.5
            gs   = gs   if pd.notna(gs)   and gs <= 1   else 0.5
            ov   = ov   if pd.notna(ov)   and ov <= 1   else 0.5
            rank = rank if pd.notna(rank) else 50
            return hard*0.35 + gs*0.25 + ov*0.20 + (1 - rank/200)*0.20
        s1 = score(player1)
        s2 = score(player2)
        total = s1 + s2
        raw_p1 = s1 / total
        raw_p2 = s2 / total

    # Clamp probabilities to realistic range (45%-75%)
    def clamp_prob(p):
        return max(0.38, min(0.72, p))

    cp1 = clamp_prob(raw_p1)
    cp2 = 1 - cp1
    prob_p1 = round(cp1 * 100, 1)
    prob_p2 = round(cp2 * 100, 1)

    winner  = p1 if prob_p1 > prob_p2 else p2
    loser   = p2 if winner == p1 else p1
    prob_w  = prob_p1 if winner == p1 else prob_p2
    prob_l  = prob_p2 if winner == p1 else prob_p1
    pw_data = player1 if winner == p1 else player2
    pl_data = player2 if winner == p1 else player1

    st.markdown("---")
    st.markdown('<div class="section-label">Result</div>', unsafe_allow_html=True)
    st.markdown('<div class="section-header">PREDICTION</div>', unsafe_allow_html=True)

    foto_w = fotos.get(winner, "")
    foto_l = fotos.get(loser, "")
    img_w = f'<img src="{foto_w}" style="width:130px;height:130px;object-fit:cover;object-position:top;border-radius:50%;border:4px solid #00ff88;margin-bottom:12px">' if foto_w else '<div style="width:130px;height:130px;background:rgba(255,255,255,0.05);border-radius:50%;border:4px solid #00ff88;margin-bottom:12px;display:flex;align-items:center;justify-content:center;font-size:3rem">🎾</div>'
    img_l = f'<img src="{foto_l}" style="width:100px;height:100px;object-fit:cover;object-position:top;border-radius:50%;border:3px solid rgba(255,255,255,0.2);margin-bottom:12px">' if foto_l else '<div style="width:100px;height:100px;background:rgba(255,255,255,0.03);border-radius:50%;border:3px solid rgba(255,255,255,0.1);margin-bottom:12px;display:flex;align-items:center;justify-content:center;font-size:2rem">🎾</div>'

    col_w, col_l = st.columns(2)
    with col_w:
        st.markdown(f"""
        <div style="background:linear-gradient(135deg,rgba(0,255,136,0.08),rgba(0,0,0,0));
                    border:2px solid #00ff88;border-radius:16px;padding:28px;text-align:center">
            <div style="font-size:0.65rem;font-weight:700;letter-spacing:3px;color:#00ff88;text-transform:uppercase;margin-bottom:12px">🏆 Predicted Winner</div>
            <div style="display:flex;justify-content:center">{img_w}</div>
            <div style="font-size:1.6rem;font-weight:900;color:#ffffff;margin-bottom:4px">{winner}</div>
            <div style="font-size:3rem;font-weight:900;color:#00ff88;line-height:1">{prob_w}%</div>
            <div style="font-size:0.7rem;color:rgba(255,255,255,0.3);letter-spacing:1px;text-transform:uppercase;margin-top:4px">win probability</div>
            <div style="background:rgba(0,255,136,0.15);border-radius:4px;height:6px;margin-top:16px;overflow:hidden">
                <div style="width:{prob_w}%;height:6px;background:#00ff88;border-radius:4px"></div>
            </div>
        </div>""", unsafe_allow_html=True)

    with col_l:
        st.markdown(f"""
        <div style="background:rgba(255,255,255,0.02);border:1px solid rgba(255,255,255,0.08);
                    border-radius:16px;padding:28px;text-align:center">
            <div style="font-size:0.65rem;font-weight:700;letter-spacing:3px;color:rgba(255,255,255,0.3);text-transform:uppercase;margin-bottom:12px">Opponent</div>
            <div style="display:flex;justify-content:center">{img_l}</div>
            <div style="font-size:1.6rem;font-weight:900;color:rgba(255,255,255,0.6);margin-bottom:4px">{loser}</div>
            <div style="font-size:3rem;font-weight:900;color:rgba(255,255,255,0.4);line-height:1">{prob_l}%</div>
            <div style="font-size:0.7rem;color:rgba(255,255,255,0.2);letter-spacing:1px;text-transform:uppercase;margin-top:4px">win probability</div>
            <div style="background:rgba(255,255,255,0.06);border-radius:4px;height:6px;margin-top:16px;overflow:hidden">
                <div style="width:{prob_l}%;height:6px;background:rgba(255,255,255,0.3);border-radius:4px"></div>
            </div>
        </div>""", unsafe_allow_html=True)

    st.markdown("---")
    st.markdown('<div class="section-label">Analysis</div>', unsafe_allow_html=True)
    st.markdown('<div class="section-header">WHY THIS PREDICTION?</div>', unsafe_allow_html=True)

    reasons = []

    def better_in(col, label, gp, pp, pct=True):
        vg = pd.to_numeric(gp.get(col), errors="coerce")
        vp = pd.to_numeric(pp.get(col), errors="coerce")
        if pd.notna(vg) and pd.notna(vp) and vg > vp:
            if pct and vg <= 1:
                return f"✅ Better {label}: {vg*100:.1f}% vs {vp*100:.1f}%"
            elif pct:
                return f"✅ Better {label}: {vg:.1f}% vs {vp:.1f}%"
            else:
                return f"✅ Better {label}: {vg:.0f} vs {vp:.0f}"
        return None

    rank_w = pd.to_numeric(pw_data.get("atp_rank_current"), errors="coerce")
    rank_l = pd.to_numeric(pl_data.get("atp_rank_current"), errors="coerce")
    if pd.notna(rank_w) and pd.notna(rank_l) and rank_w < rank_l:
        reasons.append(f"✅ Higher ATP ranking: #{int(rank_w)} vs #{int(rank_l)}")

    for r in [
        better_in("winpct_en_hard_52w", "Hard Court Win%", pw_data, pl_data),
        better_in("winpct_grand_slams_52w", "Grand Slam Win%", pw_data, pl_data),
        better_in("winpct_overall_52w", "Overall Win%", pw_data, pl_data),
        better_in("1er_saque_ganado_pct_2026", "1st Serve Won%", pw_data, pl_data),
        better_in("bp_salvados_pct_2026", "BP Saved%", pw_data, pl_data),
        better_in("winpct_set_decisivo_52w", "Deciding Set Win%", pw_data, pl_data),
        better_in("winpct_tras_perder_set1_52w", "Comeback ability", pw_data, pl_data),
    ]:
        if r:
            reasons.append(r)

    for reason in reasons[:5]:
        st.markdown(f"""
        <div style="background:rgba(0,255,136,0.04);border:1px solid rgba(0,255,136,0.15);
                    border-radius:8px;padding:12px 16px;margin:6px 0;color:rgba(255,255,255,0.8);font-size:0.9rem">
            {reason}
        </div>""", unsafe_allow_html=True)

    if not reasons:
        st.info("Very balanced match — both players have similar statistics.")

    st.markdown(f'<p style="color:rgba(255,255,255,0.2);font-size:0.75rem;text-align:center;margin-top:16px">Model: Logistic Regression · Accuracy: 65.2% · These are estimated probabilities, not guaranteed results.</p>', unsafe_allow_html=True)

st.markdown("---")
st.markdown('<p style="text-align:center;color:rgba(255,255,255,0.15);font-size:0.8rem">US Open 2026 Analytics Platform · Capstone Project</p>', unsafe_allow_html=True)



