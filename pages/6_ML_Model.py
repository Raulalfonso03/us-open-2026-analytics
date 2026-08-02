import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go

st.set_page_config(page_title="ML Model", page_icon="🤖", layout="wide")

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

# Title
st.markdown("""
<div style="text-align:center;padding:40px 0 20px 0">
    <div style="font-size:0.7rem;font-weight:700;letter-spacing:4px;color:#00ff88;text-transform:uppercase;margin-bottom:8px">US Open 2026</div>
    <div style="font-family:'Bebas Neue',sans-serif;font-size:4rem;color:#ffffff;letter-spacing:3px;line-height:1">MACHINE LEARNING MODEL</div>
    <div style="color:rgba(255,255,255,0.3);font-size:0.9rem;margin-top:8px;letter-spacing:2px">Methodology, results and analysis of the prediction model</div>
</div>
<hr style="border:none;border-top:1px solid rgba(255,255,255,0.06);margin:0 0 24px 0">
""", unsafe_allow_html=True)

# Model results
st.markdown('<div class="section-label">Performance</div>', unsafe_allow_html=True)
st.markdown('<div class="section-header">MODEL COMPARISON</div>', unsafe_allow_html=True)

modelos = [
    {"name": "Random Forest",       "accuracy": 58.3, "roc_auc": 0.632, "best": False},
    {"name": "Logistic Regression", "accuracy": 65.2, "roc_auc": 0.716, "best": True},
    {"name": "Decision Tree",       "accuracy": 64.1, "roc_auc": 0.698, "best": False},
]

cols = st.columns(3)
for i, (col, m) in enumerate(zip(cols, modelos)):
    with col:
        border = "#00ff88" if m["best"] else "rgba(255,255,255,0.08)"
        bg = "rgba(0,255,136,0.05)" if m["best"] else "rgba(255,255,255,0.02)"
        badge = '<div style="color:#00ff88;font-size:0.65rem;font-weight:700;letter-spacing:2px;margin-bottom:8px">🥇 BEST MODEL</div>' if m["best"] else '<div style="height:20px;margin-bottom:8px"></div>'
        acc_str = str(m["accuracy"])
        roc_str = str(round(m["roc_auc"], 3))
        st.markdown(f"""
        <div style="background:{bg};border:2px solid {border};border-radius:16px;padding:24px;text-align:center">
            {badge}
            <div style="font-size:1rem;font-weight:700;color:#ffffff;margin-bottom:16px">{m["name"]}</div>
            <div style="font-size:3rem;font-weight:900;color:#00ff88;line-height:1">{acc_str}%</div>
            <div style="color:rgba(255,255,255,0.3);font-size:0.7rem;letter-spacing:1px;text-transform:uppercase;margin-top:4px">Accuracy</div>
            <div style="color:rgba(255,255,255,0.5);font-size:0.9rem;margin-top:12px">ROC AUC: {roc_str}</div>
        </div>""", unsafe_allow_html=True)

st.markdown("---")

# Comparison chart
st.markdown('<div class="section-label">Visual Comparison</div>', unsafe_allow_html=True)
st.markdown('<div class="section-header">ACCURACY vs ROC AUC</div>', unsafe_allow_html=True)

names = [m["name"] for m in modelos]
accs  = [m["accuracy"] for m in modelos]
rocs  = [m["roc_auc"]*100 for m in modelos]

fig_comp = go.Figure()
fig_comp.add_trace(go.Bar(name="Accuracy (%)", x=names, y=accs,
                           marker_color=["#2e8b57","#00ff88","#1a472a"],
                           text=[f"{v}%" for v in accs],
                           textposition="outside", textfont=dict(color="white")))
fig_comp.add_trace(go.Bar(name="ROC AUC (%)", x=names, y=rocs,
                           marker_color=["#1a3a6a","#0066cc","#0044aa"],
                           text=[f"{v:.1f}%" for v in rocs],
                           textposition="outside", textfont=dict(color="white")))
fig_comp.update_layout(barmode="group", template="plotly_dark",
                        paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)",
                        height=350, margin=dict(l=10,r=10,t=10,b=10),
                        legend=dict(font=dict(color="white")),
                        yaxis=dict(range=[0,85]))
st.plotly_chart(fig_comp, use_container_width=True)

st.markdown("---")

# Feature importance
st.markdown('<div class="section-label">Logistic Regression</div>', unsafe_allow_html=True)
st.markdown('<div class="section-header">FEATURE IMPORTANCE</div>', unsafe_allow_html=True)

features_data = {
    "Feature": ["Hard Court Win%","Aces 2026","Grand Slam Win%","ATP Ranking",
                 "1st Serve Won%","Masters 1000 Win%","BP Converted%",
                 "After losing 1st set","Deciding Set","2nd Serve Won%",
                 "After winning 1st set","BP Saved%","Overall Win%","Tiebreak"],
    "Importance": [0.756,0.326,0.147,0.124,0.110,0.088,0.082,
                   0.074,0.073,0.059,0.031,0.026,0.016,0.007]
}
df_fi = pd.DataFrame(features_data).sort_values("Importance", ascending=True)

fig_fi = px.bar(df_fi, x="Importance", y="Feature", orientation="h",
                color="Importance", color_continuous_scale="Greens",
                template="plotly_dark")
fig_fi.update_layout(paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)",
                      height=450, coloraxis_showscale=False, showlegend=False,
                      margin=dict(l=10,r=10,t=10,b=10))
fig_fi.update_traces(text=df_fi["Importance"].apply(lambda x: f"{x:.3f}"),
                      textposition="outside", textfont=dict(color="white", size=10))
st.plotly_chart(fig_fi, use_container_width=True)

st.markdown("""
<div style="background:rgba(0,255,136,0.04);border:1px solid rgba(0,255,136,0.15);border-left:3px solid #00ff88;border-radius:8px;padding:14px 18px;margin:8px 0">
    <div style="color:#00ff88;font-size:0.7rem;font-weight:700;letter-spacing:2px;text-transform:uppercase;margin-bottom:4px">Key Finding</div>
    <div style="color:rgba(255,255,255,0.8);font-size:0.9rem">
    <b style="color:#00ff88">Hard Court Win% (0.756)</b> is by far the most important feature, confirming that past performance on hard courts is the strongest predictor for the US Open. 
    Aces (0.326) rank surprisingly second, highlighting the importance of serve dominance at Flushing Meadows.
    </div>
</div>
""", unsafe_allow_html=True)

st.markdown("---")

# Methodology
st.markdown('<div class="section-label">How it works</div>', unsafe_allow_html=True)
st.markdown('<div class="section-header">METHODOLOGY</div>', unsafe_allow_html=True)

col1, col2 = st.columns(2)
with col1:
    st.markdown("""
    *Data Sources:*
    - Master table: 185 players, 53 metrics (ATP Tour, 2025-2026)
    - Match history: 4,581 Hard Court matches (2020-2026)
    - Jeff Sackmann dataset (via Kaggle)
    - ATP Daily Update dataset (via Kaggle)

    *Features (14 variables):*
    - Difference in ATP Ranking
    - Difference in Hard Court Win%
    - Difference in Grand Slam Win%
    - Difference in Overall Win%
    - Difference in Masters 1000 Win%
    - Difference in Deciding Set Win%
    - Difference in Tiebreak Win%
    - Difference in Win% after winning/losing 1st set
    - Difference in 1st/2nd Serve Won%
    - Difference in BP Saved/Converted%
    - Difference in Aces
    """)

with col2:
    st.markdown("""
    *Training process:*
    - Dataset: 8,082 examples (match + inverted match)
    - Split: 80% training / 20% test
    - Balance: 50% winners / 50% losers

    *Models compared:*
    - Random Forest (100 trees)
    - Logistic Regression ← *BEST*
    - Decision Tree (max depth 5)

    *Best model results:*
    - Accuracy: *65.2%*
    - ROC AUC: *0.716*
    - Precision: 0.65
    - Recall: 0.65

    *Limitations:*
    - 65-70% accuracy is excellent for tennis prediction
    - Model does not include weather or court conditions
    - No direct head-to-head history between players
    - Injuries can significantly change probabilities
    """)

st.markdown("---")
st.markdown('<p style="text-align:center;color:rgba(255,255,255,0.15);font-size:0.8rem">US Open 2026 Analytics Platform · Capstone Project</p>', unsafe_allow_html=True)
