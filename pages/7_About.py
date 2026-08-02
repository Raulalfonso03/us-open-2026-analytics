import streamlit as st

st.set_page_config(page_title="About", page_icon="ℹ️", layout="wide")

st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Bebas+Neue&family=Inter:wght@300;400;600;700;900&display=swap');
* { font-family: 'Inter', sans-serif; }
.stApp { background-color: #050505; }
[data-testid="stSidebar"] { background: rgba(5,5,5,0.98) !important; border-right: 1px solid rgba(0,255,136,0.15) !important; }
[data-testid="stSidebar"] * { color: rgba(255,255,255,0.6) !important; }
.section-header { font-family: 'Bebas Neue', sans-serif; font-size: 1.5rem; color: #ffffff; border-bottom: 1px solid rgba(0,255,136,0.3); padding-bottom: 8px; margin: 24px 0 16px 0; letter-spacing: 2px; }
.section-label { font-size: 0.7rem; font-weight: 700; letter-spacing: 3px; color: #00ff88; text-transform: uppercase; margin-bottom: 4px; }
</style>
""", unsafe_allow_html=True)

# Title
st.markdown("""
<div style="text-align:center;padding:40px 0 20px 0">
    <div style="font-size:0.7rem;font-weight:700;letter-spacing:4px;color:#00ff88;text-transform:uppercase;margin-bottom:8px">US Open 2026</div>
    <div style="font-family:'Bebas Neue',sans-serif;font-size:4rem;color:#ffffff;letter-spacing:3px;line-height:1">ABOUT THIS PROJECT</div>
    <div style="color:rgba(255,255,255,0.3);font-size:0.9rem;margin-top:8px;letter-spacing:2px">Project information and methodology</div>
</div>
<hr style="border:none;border-top:1px solid rgba(255,255,255,0.06);margin:0 0 24px 0">
""", unsafe_allow_html=True)

# Objective
st.markdown('<div class="section-label">Overview</div>', unsafe_allow_html=True)
st.markdown('<div class="section-header">PROJECT OBJECTIVE</div>', unsafe_allow_html=True)

st.markdown("""
<div style="background:rgba(0,255,136,0.04);border:1px solid rgba(0,255,136,0.15);border-radius:12px;padding:24px;margin-bottom:16px">
    <p style="color:rgba(255,255,255,0.85);font-size:1rem;line-height:1.8;margin:0">
    This project is a <span style="color:#00ff88;font-weight:700">Data Analytics Capstone</span> whose goal is to build a professional 
    analytics and prediction platform for the <span style="color:#00ff88;font-weight:700">US Open 2026</span>.
    </p>
    <p style="color:rgba(255,255,255,0.85);font-size:1rem;line-height:1.8;margin:16px 0 0 0">
    It combines real ATP circuit data, exploratory data analysis, feature engineering and machine learning 
    to predict the winner of the most important tournament of the American hard court season.
    </p>
</div>
""", unsafe_allow_html=True)

# Data sources
st.markdown('<div class="section-label">Data</div>', unsafe_allow_html=True)
st.markdown('<div class="section-header">DATA SOURCES</div>', unsafe_allow_html=True)

col1, col2 = st.columns(2)
with col1:
    st.markdown("""
    <div style="background:rgba(255,255,255,0.02);border:1px solid rgba(255,255,255,0.06);border-radius:12px;padding:24px;height:100%">
        <div style="color:#00ff88;font-size:1rem;font-weight:700;margin-bottom:12px">🎾 ATP Tour (atptour.com)</div>
        <p style="color:rgba(255,255,255,0.7);font-size:0.85rem;line-height:1.8">
        Serve and return statistics 2025-2026 on Hard Court, manually collected:
        </p>
        <div style="color:rgba(255,255,255,0.8);font-size:0.85rem;line-height:2;margin-top:8px">
            &#8594; 185 active players<br>
            &#8594; Aces, 1st/2nd Serve %<br>
            &#8594; Break points saved/converted<br>
            &#8594; Performance under pressure<br>
            &#8594; Current ATP Ranking (July 2026)
        </div>
    </div>
    """, unsafe_allow_html=True)

with col2:
    st.markdown("""
    <div style="background:rgba(255,255,255,0.02);border:1px solid rgba(255,255,255,0.06);border-radius:12px;padding:24px;height:100%">
        <div style="color:#00ff88;font-size:1rem;font-weight:700;margin-bottom:12px">📁 Jeff Sackmann (via Kaggle)</div>
        <p style="color:rgba(255,255,255,0.7);font-size:0.85rem;line-height:1.8">
        ATP match history 2020-2024:
        </p>
        <div style="color:rgba(255,255,255,0.8);font-size:0.85rem;line-height:2;margin-top:8px">
            &#8594; Dataset guillemservera/tennis<br>
            &#8594; Hard Court matches only<br>
            &#8594; Result, score, round
        </div>
        <div style="color:#00ff88;font-size:1rem;font-weight:700;margin:16px 0 8px 0">📁 ATP Daily Update (Kaggle)</div>
        <div style="color:rgba(255,255,255,0.8);font-size:0.85rem;line-height:2">
            &#8594; Dataset dissfya/atp-tennis<br>
            &#8594; Updated through June 2026<br>
            &#8594; 2025-2026 matches included
        </div>
    </div>
    """, unsafe_allow_html=True)

# Methodology steps
st.markdown('<div class="section-label">Process</div>', unsafe_allow_html=True)
st.markdown('<div class="section-header">METHODOLOGY</div>', unsafe_allow_html=True)

steps = [
    ("1️⃣ Phase 1 — Data Collection",
     "Loading the master table (185 players, 53 columns) and ATP match history (4,581 matches on Hard Court, 2020-2026)."),
    ("2️⃣ Phase 2 — Data Cleaning",
     "Removal of invalid matches (retirements, walkovers), correction of win% scale, filling missing values with median imputation."),
    ("3️⃣ Phase 3 — Exploratory Data Analysis",
     "Distributions, Top 10 by key metrics, correlation heatmap, pressure performance analysis across 185 players."),
    ("4️⃣ Phase 4 — Feature Engineering",
     "Creation of 14 features based on differences between players (ranking, Hard Court Win%, GS Win%, serve, pressure). 8,082 balanced examples."),
    ("5️⃣ Phase 5 — Machine Learning",
     "Comparison of Random Forest, Logistic Regression and Decision Tree. Best model: Logistic Regression with 65.2% accuracy and 0.716 ROC AUC."),
    ("6️⃣ Phase 6 — Predictions",
     "Individual match predictions and US Open 2026 win probabilities, with injury status updated to July 2026."),
]

for title, desc in steps:
    st.markdown(f"""
    <div style="background:rgba(255,255,255,0.02);border:1px solid rgba(255,255,255,0.05);
                border-left:3px solid #00ff88;border-radius:8px;padding:16px 20px;margin:8px 0">
        <div style="color:#ffffff;font-weight:700;font-size:0.95rem;margin-bottom:4px">{title}</div>
        <div style="color:rgba(255,255,255,0.6);font-size:0.85rem;line-height:1.6">{desc}</div>
    </div>""", unsafe_allow_html=True)

# Technologies
st.markdown('<div class="section-label">Stack</div>', unsafe_allow_html=True)
st.markdown('<div class="section-header">TECHNOLOGIES USED</div>', unsafe_allow_html=True)

tech = [
    ("🐍", "Python", "Main language"),
    ("🐼", "Pandas & NumPy", "Data manipulation"),
    ("📊", "Plotly", "Interactive visualizations"),
    ("🤖", "Scikit-learn", "Machine Learning"),
    ("🌐", "Streamlit", "Web Application"),
    ("☁️", "Google Colab", "Development environment"),
    ("🐙", "GitHub", "Version control"),
    ("🚀", "Streamlit Cloud", "Deployment"),
]

cols = st.columns(4)
for i, (icon, name, desc) in enumerate(tech):
    with cols[i % 4]:
        st.markdown(f"""
        <div style="background:rgba(255,255,255,0.02);border:1px solid rgba(255,255,255,0.06);
                    border-radius:12px;padding:16px;text-align:center;margin:6px 0">
            <div style="font-size:1.8rem;margin-bottom:8px">{icon}</div>
            <div style="color:#00ff88;font-weight:700;font-size:0.85rem">{name}</div>
            <div style="color:rgba(255,255,255,0.3);font-size:0.75rem;margin-top:4px">{desc}</div>
        </div>""", unsafe_allow_html=True)

# Limitations
st.markdown('<div class="section-label">Disclaimer</div>', unsafe_allow_html=True)
st.markdown('<div class="section-header">LIMITATIONS</div>', unsafe_allow_html=True)

st.markdown("""
<div style="background:rgba(255,170,0,0.04);border:1px solid rgba(255,170,0,0.2);border-radius:12px;padding:24px">
    <div style="color:rgba(255,255,255,0.8);font-size:0.85rem;line-height:2">
        &#8594; The US Open 2026 has not yet taken place — all predictions are estimates based on historical data and current form.<br>
        &#8594; The model does not include day conditions (wind, temperature, match schedule).<br>
        &#8594; No direct head-to-head history between players is included.<br>
        &#8594; Injuries can significantly change probabilities — status updated to July 2026.<br>
        &#8594; 65.2% accuracy is excellent for tennis prediction (world-class models reach 68-70%).
    </div>
</div>
""", unsafe_allow_html=True)

st.markdown("---")
st.markdown("""
<p style="text-align:center;color:rgba(255,255,255,0.2);font-size:0.85rem">
US Open 2026 Analytics Platform · Data Analytics Capstone Project<br>
<span style="color:rgba(0,255,136,0.4)">Data: ATP Tour · Jeff Sackmann · Kaggle · Jul 2026</span>
</p>""", unsafe_allow_html=True)
