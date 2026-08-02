import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go

st.set_page_config(page_title="Analytics Dashboard", page_icon="📊", layout="wide")

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
    url = "https://raw.githubusercontent.com/Raulalfonso03/us-open-2026-analytics/main/df_master_final.csv"
    df = pd.read_csv(url, sep=None, engine="python")
    winpct_cols = [c for c in df.columns if 'winpct' in c]
    for col in winpct_cols:
        df[col] = pd.to_numeric(df[col], errors='coerce')
        mask = df[col] > 1
        df.loc[mask, col] = df.loc[mask, col] / 1000
    return df

df = load_data()

# Title
st.markdown("""
<div style="text-align:center;padding:40px 0 20px 0">
    <div style="font-size:0.7rem;font-weight:700;letter-spacing:4px;color:#00ff88;text-transform:uppercase;margin-bottom:8px">US Open 2026</div>
    <div style="font-family:'Bebas Neue',sans-serif;font-size:4rem;color:#ffffff;letter-spacing:3px;line-height:1">ANALYTICS DASHBOARD</div>
    <div style="color:rgba(255,255,255,0.3);font-size:0.9rem;margin-top:8px;letter-spacing:2px">Interactive visualizations of the ATP circuit</div>
</div>
<hr style="border:none;border-top:1px solid rgba(255,255,255,0.06);margin:0 0 24px 0">
""", unsafe_allow_html=True)

# Sidebar filters
with st.sidebar:
    st.markdown("## 🔧 Filters")
    st.markdown("---")
    top_n = st.slider("Top N players", 10, 50, 20)
    only_fit = st.checkbox("Only FIT players", value=False)

df_filtered = df.copy()
if only_fit and "injury_status" in df.columns:
    df_filtered = df_filtered[df_filtered["injury_status"] == "FIT"]

# KPIs
c1, c2, c3, c4 = st.columns(4)
with c1:
    st.metric("👥 Players analyzed", len(df))
with c2:
    hard_vals = df[df["winpct_en_hard_52w"].notna() & (df["winpct_en_hard_52w"] <= 1)]["winpct_en_hard_52w"]
    st.metric("🎾 Avg Hard Win%", f"{hard_vals.mean()*100:.1f}%")
with c3:
    top_server = df.nlargest(1, "aces_2026")["player_name"].values[0] if "aces_2026" in df.columns else "N/A"
    st.metric("🎯 Best Server", top_server)
with c4:
    fit_count = len(df[df["injury_status"] == "FIT"]) if "injury_status" in df.columns else len(df)
    st.metric("✅ FIT Players", fit_count)

st.markdown("---")

# Top servers and returners
col1, col2 = st.columns(2)

with col1:
    st.markdown('<div class="section-label">Hard Court 2026</div>', unsafe_allow_html=True)
    st.markdown('<div class="section-header">TOP SERVERS (Aces)</div>', unsafe_allow_html=True)
    df_aces = df_filtered[df_filtered["aces_2026"].notna()].nlargest(top_n, "aces_2026")[["player_name","aces_2026"]]
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
    st.markdown('<div class="section-label">Hard Court 2026</div>', unsafe_allow_html=True)
    st.markdown('<div class="section-header">BEST RETURNERS (BP Converted)</div>', unsafe_allow_html=True)
    df_bp = df_filtered[df_filtered["bp_convertidos_pct_2026"].notna()].nlargest(top_n, "bp_convertidos_pct_2026")[["player_name","bp_convertidos_pct_2026"]]
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

# Win% Hard and GS
col1, col2 = st.columns(2)

with col1:
    st.markdown('<div class="section-label">Last 52 Weeks</div>', unsafe_allow_html=True)
    st.markdown('<div class="section-header">TOP WIN% HARD COURT</div>', unsafe_allow_html=True)
    df_hard = df_filtered[df_filtered["winpct_en_hard_52w"].notna() & (df_filtered["winpct_en_hard_52w"] <= 1)].nlargest(top_n, "winpct_en_hard_52w")[["player_name","winpct_en_hard_52w"]]
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
    st.markdown('<div class="section-label">Last 52 Weeks</div>', unsafe_allow_html=True)
    st.markdown('<div class="section-header">TOP WIN% GRAND SLAMS</div>', unsafe_allow_html=True)
    df_gs = df_filtered[df_filtered["winpct_grand_slams_52w"].notna() & (df_filtered["winpct_grand_slams_52w"] <= 1)].nlargest(top_n, "winpct_grand_slams_52w")[["player_name","winpct_grand_slams_52w"]]
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

# Distribution and correlation
col1, col2 = st.columns(2)

with col1:
    st.markdown('<div class="section-label">Distribution</div>', unsafe_allow_html=True)
    st.markdown('<div class="section-header">WIN% OVERALL DISTRIBUTION</div>', unsafe_allow_html=True)
    df_ov = df[df["winpct_overall_52w"].notna() & (df["winpct_overall_52w"] <= 1)].copy()
    df_ov["Win% Overall"] = df_ov["winpct_overall_52w"] * 100
    fig5 = px.histogram(df_ov, x="Win% Overall", nbins=20,
                        template="plotly_dark", color_discrete_sequence=["#2e8b57"],
                        labels={"Win% Overall":"Win% Overall","count":"Players"})
    fig5.add_vline(x=df_ov["Win% Overall"].mean(), line_dash="dash", line_color="#00ff88",
                   annotation_text=f"Avg: {df_ov['Win% Overall'].mean():.1f}%",
                   annotation_font_color="#00ff88")
    fig5.update_layout(paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="#0a0a0a",
                       height=350, margin=dict(l=10,r=10,t=10,b=10), showlegend=False)
    st.plotly_chart(fig5, use_container_width=True)

with col2:
    st.markdown('<div class="section-label">Correlation</div>', unsafe_allow_html=True)
    st.markdown('<div class="section-header">CORRELATION HEATMAP</div>', unsafe_allow_html=True)
    cols_corr = ["winpct_en_hard_52w","winpct_grand_slams_52w","winpct_overall_52w",
                 "winpct_masters_1000_52w","winpct_set_decisivo_52w","winpct_tiebreak_52w"]
    df_corr = df[cols_corr].dropna()
    df_corr = df_corr[df_corr < 1]
    corr = df_corr.corr()
    labels = {"winpct_en_hard_52w":"Win% Hard","winpct_grand_slams_52w":"Win% GS",
              "winpct_overall_52w":"Win% Overall","winpct_masters_1000_52w":"Win% M1000",
              "winpct_set_decisivo_52w":"Deciding Set","winpct_tiebreak_52w":"Tiebreak"}
    corr.index   = [labels.get(c,c) for c in corr.index]
    corr.columns = [labels.get(c,c) for c in corr.columns]
    fig6 = px.imshow(corr, text_auto=".2f", color_continuous_scale="RdYlGn",
                     template="plotly_dark", height=350)
    fig6.update_layout(paper_bgcolor="rgba(0,0,0,0)", margin=dict(l=10,r=10,t=10,b=10))
    st.plotly_chart(fig6, use_container_width=True)

st.markdown("---")

# Scatter
st.markdown('<div class="section-label">All Players</div>', unsafe_allow_html=True)
st.markdown('<div class="section-header">WIN% HARD COURT vs WIN% GRAND SLAMS</div>', unsafe_allow_html=True)
st.caption("Top right quadrant = best candidates for the US Open")

df_scatter = df[df["winpct_en_hard_52w"].notna() & df["winpct_grand_slams_52w"].notna() &
                (df["winpct_en_hard_52w"] <= 1) & (df["winpct_grand_slams_52w"] <= 1)].copy()
df_scatter["hard_pct"] = df_scatter["winpct_en_hard_52w"] * 100
df_scatter["gs_pct"]   = df_scatter["winpct_grand_slams_52w"] * 100

fig7 = px.scatter(df_scatter, x="hard_pct", y="gs_pct",
                  text="player_name",
                  color="injury_status" if "injury_status" in df_scatter.columns else None,
                  color_discrete_map={"FIT":"#00ff88","DUDA":"#ffaa00","LESIONADO":"#ff4444"},
                  template="plotly_dark", height=500,
                  labels={"hard_pct":"Win% Hard Court","gs_pct":"Win% Grand Slams"})
fig7.update_traces(textposition="top center", textfont=dict(size=8, color="white"), marker=dict(size=8))
fig7.update_layout(paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="#0a0a0a",
                   xaxis=dict(gridcolor="rgba(255,255,255,0.05)"),
                   yaxis=dict(gridcolor="rgba(255,255,255,0.05)"))
st.plotly_chart(fig7, use_container_width=True)

st.markdown("---")
st.markdown('<p style="text-align:center;color:rgba(255,255,255,0.15);font-size:0.8rem">US Open 2026 Analytics Platform · Capstone Project</p>', unsafe_allow_html=True)
