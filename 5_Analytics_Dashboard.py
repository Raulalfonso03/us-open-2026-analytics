import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go

st.set_page_config(page_title="Analytics Dashboard", page_icon="📊", layout="wide")

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
    - ⚖️ Player Comparison
    - 🔮 Match Prediction
    - 🏆 Tournament Prediction
    - 📊 **Analytics Dashboard**
    - 🤖 ML Model
    - ℹ️ About
    """)
    st.markdown("---")
    st.markdown("### 🔧 Filtros")
    top_n = st.slider("Top N jugadores", 10, 50, 20)
    solo_fit = st.checkbox("Solo jugadores FIT", value=False)

df_filtered = df.copy()
if solo_fit and "injury_status" in df.columns:
    df_filtered = df_filtered[df_filtered["injury_status"] == "FIT"]

st.markdown("# 📊 Analytics Dashboard")
st.markdown("Visualizaciones interactivas del circuito ATP")
st.markdown("---")

# KPIs
c1, c2, c3, c4 = st.columns(4)
with c1:
    st.metric("👥 Jugadores analizados", len(df))
with c2:
    hard_mean = df[df["winpct_en_hard_52w"]<=1]["winpct_en_hard_52w"].mean()
    st.metric("🎾 Win% Hard medio", f"{hard_mean*100:.1f}%")
with c3:
    top_server = df.nlargest(1,"aces_2026")["player_name"].values[0] if "aces_2026" in df.columns else "N/A"
    st.metric("🎯 Mejor servidor", top_server)
with c4:
    fit_count = len(df[df.get("injury_status","FIT") == "FIT"]) if "injury_status" in df.columns else len(df)
    st.metric("✅ Jugadores FIT", fit_count)

st.markdown("---")

# Top servidores y retadores
col1, col2 = st.columns(2)

with col1:
    st.markdown('<p class="section-header">🎯 TOP SERVIDORES (Aces 2026)</p>', unsafe_allow_html=True)
    df_aces = df_filtered[df_filtered["aces_2026"].notna()].nlargest(top_n,"aces_2026")[["player_name","aces_2026"]]
    fig1 = px.bar(df_aces, x="aces_2026", y="player_name", orientation="h",
                  color="aces_2026", color_continuous_scale="Greens",
                  template="plotly_dark", labels={"aces_2026":"Aces","player_name":""},
                  text="aces_2026")
    fig1.update_layout(paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)",
                       height=400, coloraxis_showscale=False, showlegend=False,
                       yaxis=dict(autorange="reversed"), margin=dict(l=10,r=10,t=10,b=10))
    fig1.update_traces(textposition="outside", textfont=dict(color="white", size=9))
    st.plotly_chart(fig1, use_container_width=True)

with col2:
    st.markdown('<p class="section-header">🏓 MEJORES EN RESTO (BP Convertidos 2026)</p>', unsafe_allow_html=True)
    df_bp = df_filtered[df_filtered["bp_convertidos_pct_2026"].notna()].nlargest(top_n,"bp_convertidos_pct_2026")[["player_name","bp_convertidos_pct_2026"]]
    fig2 = px.bar(df_bp, x="bp_convertidos_pct_2026", y="player_name", orientation="h",
                  color="bp_convertidos_pct_2026", color_continuous_scale="Blues",
                  template="plotly_dark", labels={"bp_convertidos_pct_2026":"BP Conv %","player_name":""},
                  text=df_bp["bp_convertidos_pct_2026"].apply(lambda x: f"{x:.1f}%"))
    fig2.update_layout(paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)",
                       height=400, coloraxis_showscale=False, showlegend=False,
                       yaxis=dict(autorange="reversed"), margin=dict(l=10,r=10,t=10,b=10))
    fig2.update_traces(textposition="outside", textfont=dict(color="white", size=9))
    st.plotly_chart(fig2, use_container_width=True)

st.markdown("---")

# Win% Hard y GS
col1, col2 = st.columns(2)

with col1:
    st.markdown('<p class="section-header">🎾 TOP WIN% EN HARD COURT</p>', unsafe_allow_html=True)
    df_hard = df_filtered[df_filtered["winpct_en_hard_52w"].notna() & (df_filtered["winpct_en_hard_52w"]<=1)].nlargest(top_n,"winpct_en_hard_52w")[["player_name","winpct_en_hard_52w"]]
    fig3 = px.bar(df_hard, x="winpct_en_hard_52w", y="player_name", orientation="h",
                  color="winpct_en_hard_52w", color_continuous_scale="Greens",
                  template="plotly_dark", labels={"winpct_en_hard_52w":"Win% Hard","player_name":""},
                  text=df_hard["winpct_en_hard_52w"].apply(lambda x: f"{x*100:.1f}%"))
    fig3.update_layout(paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)",
                       height=400, coloraxis_showscale=False, showlegend=False,
                       yaxis=dict(autorange="reversed"), margin=dict(l=10,r=10,t=10,b=10))
    fig3.update_traces(textposition="outside", textfont=dict(color="white", size=9))
    st.plotly_chart(fig3, use_container_width=True)

with col2:
    st.markdown('<p class="section-header">🏆 TOP WIN% EN GRAND SLAMS</p>', unsafe_allow_html=True)
    df_gs = df_filtered[df_filtered["winpct_grand_slams_52w"].notna() & (df_filtered["winpct_grand_slams_52w"]<=1)].nlargest(top_n,"winpct_grand_slams_52w")[["player_name","winpct_grand_slams_52w"]]
    fig4 = px.bar(df_gs, x="winpct_grand_slams_52w", y="player_name", orientation="h",
                  color="winpct_grand_slams_52w", color_continuous_scale="Purples",
                  template="plotly_dark", labels={"winpct_grand_slams_52w":"Win% GS","player_name":""},
                  text=df_gs["winpct_grand_slams_52w"].apply(lambda x: f"{x*100:.1f}%"))
    fig4.update_layout(paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)",
                       height=400, coloraxis_showscale=False, showlegend=False,
                       yaxis=dict(autorange="reversed"), margin=dict(l=10,r=10,t=10,b=10))
    fig4.update_traces(textposition="outside", textfont=dict(color="white", size=9))
    st.plotly_chart(fig4, use_container_width=True)

st.markdown("---")

# Correlacion y distribucion
col1, col2 = st.columns(2)

with col1:
    st.markdown('<p class="section-header">📈 DISTRIBUCIÓN WIN% OVERALL</p>', unsafe_allow_html=True)
    df_ov = df[df["winpct_overall_52w"].notna() & (df["winpct_overall_52w"]<=1)].copy()
    df_ov["Win% Overall"] = df_ov["winpct_overall_52w"] * 100
    fig5 = px.histogram(df_ov, x="Win% Overall", nbins=20,
                        template="plotly_dark", color_discrete_sequence=["#2e8b57"])
    fig5.add_vline(x=df_ov["Win% Overall"].mean(), line_dash="dash", line_color="#00ff88",
                   annotation_text=f"Media: {df_ov['Win% Overall'].mean():.1f}%",
                   annotation_font_color="#00ff88")
    fig5.update_layout(paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="#0d1117",
                       height=350, margin=dict(l=10,r=10,t=10,b=10), showlegend=False)
    st.plotly_chart(fig5, use_container_width=True)

with col2:
    st.markdown('<p class="section-header">🔥 MAPA DE CORRELACIÓN</p>', unsafe_allow_html=True)
    cols_corr = ["winpct_en_hard_52w","winpct_grand_slams_52w","winpct_overall_52w",
                 "winpct_masters_1000_52w","winpct_set_decisivo_52w","winpct_tiebreak_52w"]
    df_corr = df[cols_corr].dropna()
    df_corr = df_corr[df_corr < 1]
    corr = df_corr.corr()
    labels = {"winpct_en_hard_52w":"Win% Hard","winpct_grand_slams_52w":"Win% GS",
              "winpct_overall_52w":"Win% Overall","winpct_masters_1000_52w":"Win% M1000",
              "winpct_set_decisivo_52w":"Set Decisivo","winpct_tiebreak_52w":"Tiebreak"}
    corr.index   = [labels.get(c,c) for c in corr.index]
    corr.columns = [labels.get(c,c) for c in corr.columns]
    fig6 = px.imshow(corr, text_auto=".2f", color_continuous_scale="RdYlGn",
                     template="plotly_dark", height=350)
    fig6.update_layout(paper_bgcolor="rgba(0,0,0,0)", margin=dict(l=10,r=10,t=10,b=10))
    st.plotly_chart(fig6, use_container_width=True)

st.markdown("---")

# Scatter
st.markdown('<p class="section-header">📊 WIN% HARD vs WIN% GRAND SLAMS — TODOS LOS JUGADORES</p>', unsafe_allow_html=True)

df_scatter = df[
    df["winpct_en_hard_52w"].notna() & df["winpct_grand_slams_52w"].notna() &
    (df["winpct_en_hard_52w"]<=1) & (df["winpct_grand_slams_52w"]<=1)
].copy()
df_scatter["hard_pct"] = df_scatter["winpct_en_hard_52w"] * 100
df_scatter["gs_pct"]   = df_scatter["winpct_grand_slams_52w"] * 100

fig7 = px.scatter(df_scatter, x="hard_pct", y="gs_pct",
                  text="player_name",
                  color="injury_status" if "injury_status" in df_scatter.columns else None,
                  color_discrete_map={"FIT":"#00ff88","DUDA":"#ffaa00","LESIONADO":"#ff4444"},
                  template="plotly_dark", height=500,
                  labels={"hard_pct":"Win% Hard Court","gs_pct":"Win% Grand Slams"})
fig7.update_traces(textposition="top center", textfont=dict(size=8, color="white"), marker=dict(size=8))
fig7.update_layout(paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="#0d1117",
                   xaxis=dict(gridcolor="#1a1a2e"), yaxis=dict(gridcolor="#1a1a2e"))
st.plotly_chart(fig7, use_container_width=True)

st.markdown("---")
st.markdown('<p style="text-align:center;color:#333;font-size:0.8rem">US Open 2026 Analytics Platform · Capstone Project</p>', unsafe_allow_html=True)
