import streamlit as st
import pandas as pd
import numpy as np
import plotly.graph_objects as go

st.set_page_config(page_title="Player Profiles", page_icon="👤", layout="wide")

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
.stat-row { display:flex; justify-content:space-between; padding:10px 0; border-bottom:1px solid rgba(255,255,255,0.05); }
.stat-label { color: rgba(255,255,255,0.5); font-size:0.9rem; }
.stat-value { color: #00ff88; font-weight:700; font-size:0.9rem; }
</style>
""", unsafe_allow_html=True)

@st.cache_data
def load_data():
    url = "https://raw.githubusercontent.com/Raulalfonso03/us-open-2026-analytics/main/df_master_final.csv"
    return pd.read_csv(url, sep=None, engine="python")

df = load_data()

winpct_cols = [c for c in df.columns if 'winpct' in c]
for col in winpct_cols:
    df[col] = pd.to_numeric(df[col], errors='coerce')
    mask = df[col] > 1
    df.loc[mask, col] = df.loc[mask, col] / 1000

fotos = {
    "Jannik Sinner":         "https://www.atptour.com/-/media/alias/player-headshot/S0AG",
    "Carlos Alcaraz":        "https://www.atptour.com/-/media/alias/player-headshot/A0E2",
    "Alexander Zverev":      "https://www.atptour.com/-/media/alias/player-headshot/Z355",
    "Felix Auger-Aliassime": "https://www.atptour.com/-/media/alias/player-headshot/AG37",
    "Ben Shelton":           "https://www.atptour.com/-/media/alias/player-headshot/S0S1",
    "Alex de Minaur":        "https://www.atptour.com/-/media/alias/player-headshot/DH58",
    "Taylor Fritz":          "https://www.atptour.com/-/media/alias/player-headshot/FB98",
    "Novak Djokovic":        "https://www.atptour.com/-/media/alias/player-headshot/D643",
    "Daniil Medvedev":       "https://www.atptour.com/-/media/alias/player-headshot/MM58",
    "Flavio Cobolli":        "https://www.atptour.com/-/media/alias/player-headshot/C0E9",
    "Alexander Bublik":      "https://www.atptour.com/-/media/alias/player-headshot/BK92",
    "Casper Ruud":           "https://www.atptour.com/-/media/alias/player-headshot/RH16",
    "Andrey Rublev":         "https://www.atptour.com/-/media/alias/player-headshot/RE44",
    "Jiri Lehecka":          "https://www.atptour.com/-/media/alias/player-headshot/L0BV",
    "Jakub Mensik":          "https://www.atptour.com/-/media/alias/player-headshot/M0NI",
    "Learner Tien":          "https://www.atptour.com/-/media/alias/player-headshot/T0HA",
    "Frances Tiafoe":        "https://www.atptour.com/-/media/alias/player-headshot/TD51",
    "Tommy Paul":            "https://www.atptour.com/-/media/alias/player-headshot/PL56",
}

st.markdown("# 👤 Player Profiles")
st.markdown("Detailed statistics for each ATP player")
st.markdown("---")

jugadores = sorted(df["player_name"].dropna().unique().tolist())
selected = st.selectbox("🔍 Select a player", jugadores,
                        index=jugadores.index("Jannik Sinner") if "Jannik Sinner" in jugadores else 0)

player = df[df["player_name"] == selected].iloc[0]

rank   = int(player["atp_rank_current"])   if pd.notna(player.get("atp_rank_current"))   else "N/A"
points = int(player["atp_points_current"]) if pd.notna(player.get("atp_points_current")) else "N/A"
record = player.get("record_overall_52w", "N/A")
titles = int(player["titulos_52w"])        if pd.notna(player.get("titulos_52w"))        else 0
estado = player.get("injury_status", "FIT")
nota   = player.get("injury_note", "")

if estado == "LESIONADO":
    estado_color = "#ff4444"; estado_icon = "⚠️ INJURED"
elif estado == "DUDA":
    estado_color = "#ffaa00"; estado_icon = "❓ DOUBT"
else:
    estado_color = "#00ff88"; estado_icon = "✅ FIT"

col_photo, col_info = st.columns([1, 3])

with col_photo:
    foto = fotos.get(selected, "")
    if foto:
        st.image(foto, width=200)
    else:
        st.markdown('<div style="width:200px;height:200px;background:rgba(255,255,255,0.05);border-radius:12px;display:flex;align-items:center;justify-content:center;font-size:4rem">🎾</div>', unsafe_allow_html=True)

with col_info:
    nota_html = f'<p style="color:rgba(255,255,255,0.4);font-size:0.8rem;margin-top:8px">⚠️ {nota}</p>' if nota and str(nota) != 'nan' else ''
    st.markdown(f"""
    <div style="padding:20px 0">
        <h1 style="color:#ffffff;margin:0;font-size:2.5rem;font-weight:900;font-family:'Bebas Neue',sans-serif;letter-spacing:2px">{selected}</h1>
        <p style="color:rgba(255,255,255,0.4);margin:4px 0;letter-spacing:3px;text-transform:uppercase;font-size:0.8rem">ATP Professional · Hard Court Specialist</p>
        <div style="margin-top:12px">
            <span style="background:{estado_color}22;color:{estado_color};border:1px solid {estado_color};border-radius:8px;padding:4px 14px;font-size:0.85rem;font-weight:700">{estado_icon}</span>
        </div>
        {nota_html}
        <div style="margin-top:16px;font-size:3rem;font-weight:900;color:#00ff88;line-height:1">#{rank}</div>
        <div style="color:rgba(255,255,255,0.3);font-size:0.75rem;letter-spacing:2px;text-transform:uppercase">ATP Ranking</div>
    </div>
    """, unsafe_allow_html=True)

st.markdown("---")

def fmt_pct(val):
    if pd.notna(val) and val <= 1:
        return f"{val*100:.1f}%"
    return "N/A"

c1, c2, c3, c4, c5 = st.columns(5)
with c1: st.metric("📊 Win% Overall", fmt_pct(player.get("winpct_overall_52w")), f"Record: {record}")
with c2: st.metric("🎾 Win% Hard", fmt_pct(player.get("winpct_en_hard_52w")))
with c3: st.metric("🏆 Win% GS", fmt_pct(player.get("winpct_grand_slams_52w")), str(player.get("record_grand_slams_52w","")))
with c4: st.metric("🏅 Titles (52w)", str(titles))
with c5: st.metric("💎 Win% M1000", fmt_pct(player.get("winpct_masters_1000_52w")))

st.markdown("---")
st.markdown('<div class="section-label">Hard Court</div>', unsafe_allow_html=True)
st.markdown('<div class="section-header">SERVE STATISTICS</div>', unsafe_allow_html=True)

col1, col2 = st.columns(2)
with col1:
    st.markdown("**Season 2025**")
    for label, col in [("1st Serve %","1er_saque_pct_2025"),("1st Serve Won %","1er_saque_ganado_pct_2025"),
                        ("2nd Serve Won %","2do_saque_ganado_pct_2025"),("Service Games Won %","juegos_saque_g_pct_2025"),("BP Saved %","bp_salvados_pct_2025")]:
        val = player.get(col)
        if pd.notna(val):
            st.markdown(f'<div class="stat-row"><span class="stat-label">{label}</span><span class="stat-value">{val:.1f}%</span></div>', unsafe_allow_html=True)

with col2:
    st.markdown("**Season 2026**")
    for label, col in [("1st Serve %","1er_saque_pct_2026"),("1st Serve Won %","1er_saque_ganado_pct_2026"),
                        ("2nd Serve Won %","2do_saque_ganado_pct_2026"),("Service Games Won %","juegos_saque_g_pct_2026"),("BP Saved %","bp_salvados_pct_2026")]:
        val = player.get(col)
        if pd.notna(val):
            st.markdown(f'<div class="stat-row"><span class="stat-label">{label}</span><span class="stat-value">{val:.1f}%</span></div>', unsafe_allow_html=True)

st.markdown("---")
st.markdown('<div class="section-label">2026 vs Tour Average</div>', unsafe_allow_html=True)
st.markdown('<div class="section-header">SERVE RADAR</div>', unsafe_allow_html=True)

cats   = ["1st Serve %","1st Serve\nWon %","2nd Serve\nWon %","Service\nGames %","BP\nSaved %"]
cols_p = ["1er_saque_pct_2026","1er_saque_ganado_pct_2026","2do_saque_ganado_pct_2026","juegos_saque_g_pct_2026","bp_salvados_pct_2026"]
vals_p = [player.get(c, np.nan) for c in cols_p]
vals_m = [df[c].median() for c in cols_p]

if any(pd.notna(v) for v in vals_p):
    fig_r = go.Figure()
    fig_r.add_trace(go.Scatterpolar(r=[v if pd.notna(v) else 0 for v in vals_p]+[vals_p[0] if pd.notna(vals_p[0]) else 0],
                                     theta=cats+[cats[0]], fill="toself", name=selected,
                                     line=dict(color="#00ff88", width=2), fillcolor="rgba(0,255,136,0.1)"))
    fig_r.add_trace(go.Scatterpolar(r=vals_m+[vals_m[0]], theta=cats+[cats[0]], fill="toself", name="Tour Average",
                                     line=dict(color="#555", width=1), fillcolor="rgba(85,85,85,0.1)"))
    fig_r.update_layout(polar=dict(bgcolor="#0d1117", radialaxis=dict(visible=True, range=[0,100], tickfont=dict(color="#555"))),
                         template="plotly_dark", paper_bgcolor="rgba(0,0,0,0)",
                         height=380, legend=dict(font=dict(color="white")), margin=dict(l=40,r=40,t=40,b=40))
    st.plotly_chart(fig_r, use_container_width=True)

st.markdown("---")
st.markdown('<div class="section-label">Hard Court</div>', unsafe_allow_html=True)
st.markdown('<div class="section-header">RETURN STATISTICS</div>', unsafe_allow_html=True)

col1, col2 = st.columns(2)
with col1:
    st.markdown("**Season 2025**")
    for label, col in [("1st Serve Return %","resto_1er_pct_2025"),("2nd Serve Return %","resto_2do_pct_2025"),
                        ("BP Converted %","bp_convertidos_pct_2025"),("Return Games Won %","juegos_resto_g_pct_2025")]:
        val = player.get(col)
        if pd.notna(val):
            st.markdown(f'<div class="stat-row"><span class="stat-label">{label}</span><span class="stat-value">{val:.1f}%</span></div>', unsafe_allow_html=True)

with col2:
    st.markdown("**Season 2026**")
    for label, col in [("1st Serve Return %","resto_1er_pct_2026"),("2nd Serve Return %","resto_2do_pct_2026"),
                        ("BP Converted %","bp_convertidos_pct_2026"),("Return Games Won %","juegos_resto_g_pct_2026")]:
        val = player.get(col)
        if pd.notna(val):
            st.markdown(f'<div class="stat-row"><span class="stat-label">{label}</span><span class="stat-value">{val:.1f}%</span></div>', unsafe_allow_html=True)

st.markdown("---")
st.markdown('<div class="section-label">Last 52 Weeks</div>', unsafe_allow_html=True)
st.markdown('<div class="section-header">PRESSURE PERFORMANCE</div>', unsafe_allow_html=True)

presion = {
    "After winning 1st set":("winpct_tras_ganar_set1_52w","record_tras_ganar_set1_52w"),
    "After losing 1st set": ("winpct_tras_perder_set1_52w","record_tras_perder_set1_52w"),
    "Deciding set":         ("winpct_set_decisivo_52w","record_set_decisivo_52w"),
    "5th set":              ("winpct_5to_set_52w","record_5to_set_52w"),
    "Tiebreak":             ("winpct_tiebreak_52w","record_tiebreak_52w"),
    "Finals":               ("winpct_finales_52w","record_finales_52w"),
    "Grand Slams":          ("winpct_grand_slams_52w","record_grand_slams_52w"),
    "Masters 1000":         ("winpct_masters_1000_52w","record_masters1000_52w"),
}

presion_validos = {k:(player.get(v[0]),player.get(v[1],"")) for k,(v) in presion.items() if pd.notna(player.get(v[0])) and player.get(v[0])<=1}

if presion_validos:
    col1, col2 = st.columns([1.5, 1])
    with col1:
        for label, (val, rec) in presion_validos.items():
            color = "#00ff88" if val>=0.6 else "#ffaa00" if val>=0.45 else "#ff4444"
            rec_str = str(rec) if rec and str(rec)!='nan' else ""
            st.markdown(f"""<div style="display:flex;justify-content:space-between;align-items:center;padding:10px 0;border-bottom:1px solid rgba(255,255,255,0.05)">
                <span style="color:rgba(255,255,255,0.6);width:200px">{label}</span>
                <div style="flex:1;background:rgba(255,255,255,0.06);border-radius:3px;height:6px;margin:0 16px">
                    <div style="width:{val*100:.0f}%;height:6px;border-radius:3px;background:{color}"></div>
                </div>
                <span style="color:{color};font-weight:700;width:45px;text-align:right">{val*100:.0f}%</span>
                <span style="color:rgba(255,255,255,0.3);font-size:0.75rem;width:55px;text-align:right">{rec_str}</span>
            </div>""", unsafe_allow_html=True)
    with col2:
        vals_b = [v[0]*100 for v in presion_validos.values()]
        colors_b = ["#00ff88" if v>=60 else "#ffaa00" if v>=45 else "#ff4444" for v in vals_b]
        fig_b = go.Figure(go.Bar(x=vals_b, y=list(presion_validos.keys()), orientation="h",
                                  marker_color=colors_b, text=[f"{v:.0f}%" for v in vals_b],
                                  textposition="outside", textfont=dict(color="white", size=10)))
        fig_b.update_layout(template="plotly_dark", paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)",
                             height=300, margin=dict(l=10,r=50,t=10,b=10),
                             xaxis=dict(showgrid=False, showticklabels=False, range=[0,120]),
                             yaxis=dict(tickfont=dict(size=10)), showlegend=False)
        st.plotly_chart(fig_b, use_container_width=True)

st.markdown("---")
st.markdown('<div class="section-label">Serve Performance</div>', unsafe_allow_html=True)
st.markdown('<div class="section-header">EVOLUTION 2025 → 2026</div>', unsafe_allow_html=True)

evol_data = []
for label, c25, c26 in [("1st Serve Won %","1er_saque_ganado_pct_2025","1er_saque_ganado_pct_2026"),
                          ("2nd Serve Won %","2do_saque_ganado_pct_2025","2do_saque_ganado_pct_2026"),
                          ("BP Saved %","bp_salvados_pct_2025","bp_salvados_pct_2026"),
                          ("Service Games Won %","juegos_saque_g_pct_2025","juegos_saque_g_pct_2026")]:
    v25, v26 = player.get(c25), player.get(c26)
    if pd.notna(v25) and pd.notna(v26):
        evol_data.append({"Metric": label, "2025": v25, "2026": v26})

if evol_data:
    df_e = pd.DataFrame(evol_data)
    fig_e = go.Figure()
    fig_e.add_trace(go.Bar(name="2025", x=df_e["Metric"], y=df_e["2025"], marker_color="#1a472a"))
    fig_e.add_trace(go.Bar(name="2026", x=df_e["Metric"], y=df_e["2026"], marker_color="#00ff88"))
    fig_e.update_layout(barmode="group", template="plotly_dark", paper_bgcolor="rgba(0,0,0,0)",
                         plot_bgcolor="rgba(0,0,0,0)", height=300, margin=dict(l=10,r=10,t=10,b=10),
                         legend=dict(font=dict(color="white")), yaxis=dict(range=[0,100]))
    st.plotly_chart(fig_e, use_container_width=True)

st.markdown("---")
st.markdown('<p style="text-align:center;color:rgba(255,255,255,0.15);font-size:0.8rem">US Open 2026 Analytics Platform · Capstone Project</p>', unsafe_allow_html=True)


