import streamlit as st
import pandas as pd
import numpy as np
import pickle
import requests
import plotly.graph_objects as go

st.set_page_config(page_title="Match Prediction", page_icon="🔮", layout="wide")

st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;600;700;900&display=swap');
    * { font-family: 'Inter', sans-serif; }
    .stApp { background-color: #0a0a0f; }
    [data-testid="stSidebar"] { background: linear-gradient(180deg, #0d1117 0%, #0a0a0f 100%); border-right: 1px solid #1a472a; }
    .section-header { font-size: 1.2rem; font-weight: 700; color: #00ff88; border-bottom: 2px solid #1a472a; padding-bottom: 8px; margin: 20px 0 12px 0; }
    .winner-card {
        background: linear-gradient(135deg, #0d2818, #0d1117);
        border: 2px solid #00ff88; border-radius: 16px;
        padding: 30px; text-align: center;
    }
    .loser-card {
        background: #0d1117; border: 1px solid #1a1a2e;
        border-radius: 16px; padding: 30px; text-align: center;
    }
</style>
""", unsafe_allow_html=True)

@st.cache_data
def load_data():
    url = "https://raw.githubusercontent.com/Raulalfonso03/us-open-2026-analytics/main/df_master_final.csv"
    return pd.read_csv(url, sep=None, engine="python")

@st.cache_resource
def load_model():
    base = "https://raw.githubusercontent.com/Raulalfonso03/us-open-2026-analytics/main/"
    r_model  = requests.get(base + "modelo_lr.pkl")
    r_scaler = requests.get(base + "scaler.pkl")
    import pickle
    modelo = pickle.loads(r_model.content)
    scaler = pickle.loads(r_scaler.content)
    return modelo, scaler

df = load_data()

with st.sidebar:
    st.markdown("## 🎾 US Open 2026")
    st.markdown("---")
    st.markdown("""
    - 🏠 Home
    - 👤 Player Profiles
    - ⚖️ Player Comparison
    - 🔮 **Match Prediction**
    - 🏆 Tournament Prediction
    - 📊 Analytics Dashboard
    - 🤖 ML Model
    - ℹ️ About
    """)

st.markdown("# 🔮 Match Prediction")
st.markdown("Predice el ganador de cualquier partido del US Open 2026")
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

st.markdown("---")

if st.button("🔮 PREDECIR PARTIDO", use_container_width=True):
    
    player1 = df[df["player_name"] == p1].iloc[0]
    player2 = df[df["player_name"] == p2].iloc[0]
    
    # Verificar lesiones
    e1 = player1.get("injury_status", "FIT")
    e2 = player2.get("injury_status", "FIT")
    
    if e1 == "LESIONADO":
        st.error(f"⚠️ {p1} está LESIONADO y probablemente no juegue el US Open.")
    if e2 == "LESIONADO":
        st.error(f"⚠️ {p2} está LESIONADO y probablemente no juegue el US Open.")
    
    try:
        modelo, scaler = load_model()
        model_loaded = True
    except:
        model_loaded = False
    
    def get_diff(col, p1d, p2d):
        v1 = pd.to_numeric(p1d.get(col, np.nan), errors="coerce")
        v2 = pd.to_numeric(p2d.get(col, np.nan), errors="coerce")
        if pd.isna(v1) or pd.isna(v2): return 0
        return v1 - v2
    
    if model_loaded:
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
        prob_p1 = round(prob[1]*100, 1)
        prob_p2 = round(prob[0]*100, 1)
        ganador = p1 if prob_p1 > prob_p2 else p2
        perdedor = p2 if ganador == p1 else p1
        prob_gan = prob_p1 if ganador == p1 else prob_p2
        prob_per = prob_p2 if ganador == p1 else prob_p1
        
    else:
        # Sistema de reglas como fallback
        def score(p):
            hard = pd.to_numeric(p.get("winpct_en_hard_52w",0.5), errors="coerce")
            gs   = pd.to_numeric(p.get("winpct_grand_slams_52w",0.5), errors="coerce")
            ov   = pd.to_numeric(p.get("winpct_overall_52w",0.5), errors="coerce")
            rank = pd.to_numeric(p.get("atp_rank_current",50), errors="coerce")
            hard = hard if pd.notna(hard) and hard<=1 else 0.5
            gs   = gs   if pd.notna(gs)   and gs<=1   else 0.5
            ov   = ov   if pd.notna(ov)   and ov<=1   else 0.5
            rank = rank if pd.notna(rank) else 50
            return hard*0.4 + gs*0.3 + ov*0.2 + (1-rank/200)*0.1
        
        s1, s2 = score(player1), score(player2)
        total = s1 + s2
        prob_p1 = round(s1/total*100, 1)
        prob_p2 = round(s2/total*100, 1)
        ganador  = p1 if prob_p1 > prob_p2 else p2
        perdedor = p2 if ganador == p1 else p1
        prob_gan = prob_p1 if ganador == p1 else prob_p2
        prob_per = prob_p2 if ganador == p1 else prob_p1

    # Resultado
    st.markdown("## 🏆 RESULTADO DE LA PREDICCIÓN")
    
    col_g, col_p = st.columns(2)
    with col_g:
        st.markdown(f"""
        <div class="winner-card">
            <div style="color:#00ff88;font-size:0.85rem;letter-spacing:2px;margin-bottom:8px">GANADOR PREDICHO</div>
            <div style="color:#ffffff;font-size:1.8rem;font-weight:900">{ganador}</div>
            <div style="color:#00ff88;font-size:3rem;font-weight:900;margin:8px 0">{prob_gan}%</div>
            <div style="background:#1a472a;border-radius:4px;height:8px;margin:8px 0">
                <div style="width:{prob_gan}%;height:8px;border-radius:4px;background:#00ff88"></div>
            </div>
        </div>""", unsafe_allow_html=True)
    with col_p:
        st.markdown(f"""
        <div class="loser-card">
            <div style="color:#555;font-size:0.85rem;letter-spacing:2px;margin-bottom:8px">OPONENTE</div>
            <div style="color:#888;font-size:1.8rem;font-weight:900">{perdedor}</div>
            <div style="color:#555;font-size:3rem;font-weight:900;margin:8px 0">{prob_per}%</div>
            <div style="background:#1a1a2e;border-radius:4px;height:8px;margin:8px 0">
                <div style="width:{prob_per}%;height:8px;border-radius:4px;background:#555"></div>
            </div>
        </div>""", unsafe_allow_html=True)

    st.markdown("---")
    
    # Razones
    st.markdown('<p class="section-header">📋 ¿POR QUÉ GANA?</p>', unsafe_allow_html=True)
    
    razones = []
    gp = player1 if ganador == p1 else player2
    pp = player2 if ganador == p1 else player1
    
    def mejor_en(col, label, gp, pp, pct=True):
        vg = pd.to_numeric(gp.get(col), errors="coerce")
        vp = pd.to_numeric(pp.get(col), errors="coerce")
        if pd.notna(vg) and pd.notna(vp):
            if vg > vp:
                if pct and vg <= 1:
                    return f"✅ Mejor {label}: {vg*100:.1f}% vs {vp*100:.1f}%"
                elif pct:
                    return f"✅ Mejor {label}: {vg:.1f}% vs {vp:.1f}%"
                else:
                    return f"✅ Mejor {label}: {vg:.0f} vs {vp:.0f}"
        return None

    for r in [
        mejor_en("winpct_en_hard_52w", "Win% en Hard Court", gp, pp),
        mejor_en("winpct_grand_slams_52w", "Win% en Grand Slams", gp, pp),
        mejor_en("winpct_overall_52w", "Forma reciente (Win% Overall)", gp, pp),
        mejor_en("1er_saque_ganado_pct_2026", "1er Saque Ganado %", gp, pp, pct=True),
        mejor_en("bp_salvados_pct_2026", "Break Points Salvados %", gp, pp, pct=True),
        mejor_en("winpct_set_decisivo_52w", "Win% en Sets Decisivos", gp, pp),
        mejor_en("winpct_tras_perder_set1_52w", "Remontada tras perder 1er set", gp, pp),
    ]:
        if r:
            razones.append(r)

    rank_g = pd.to_numeric(gp.get("atp_rank_current"), errors="coerce")
    rank_p = pd.to_numeric(pp.get("atp_rank_current"), errors="coerce")
    if pd.notna(rank_g) and pd.notna(rank_p) and rank_g < rank_p:
        razones.append(f"✅ Mejor ranking ATP: #{int(rank_g)} vs #{int(rank_p)}")

    if razones:
        for r in razones[:5]:
            st.markdown(f"""
            <div style="background:#0d1117;border:1px solid #1a472a;border-radius:8px;
                        padding:12px 16px;margin:6px 0;color:#ccc">
                {r}
            </div>""", unsafe_allow_html=True)
    else:
        st.info("Ambos jugadores tienen estadísticas similares — partido muy equilibrado.")

    # Grafico
    st.markdown("---")
    fig = go.Figure(go.Bar(
        x=[prob_p1, prob_p2],
        y=[p1, p2],
        orientation="h",
        marker_color=["#00ff88" if p1==ganador else "#555",
                      "#00ff88" if p2==ganador else "#555"],
        text=[f"{prob_p1}%", f"{prob_p2}%"],
        textposition="outside",
        textfont=dict(color="white", size=14)
    ))
    fig.update_layout(
        template="plotly_dark", paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)",
        height=200, margin=dict(l=10,r=60,t=10,b=10),
        xaxis=dict(showgrid=False, showticklabels=False, range=[0,115]),
        yaxis=dict(tickfont=dict(size=14, color="white")), showlegend=False
    )
    st.plotly_chart(fig, use_container_width=True)

st.markdown("---")
st.markdown('<p style="text-align:center;color:#333;font-size:0.8rem">US Open 2026 Analytics · Modelo: Logistic Regression · Accuracy: 65.2%</p>', unsafe_allow_html=True)
