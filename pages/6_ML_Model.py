import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go

st.set_page_config(page_title="ML Model", page_icon="🤖", layout="wide")

st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;600;700;900&display=swap');
    * { font-family: 'Inter', sans-serif; }
    .stApp { background-color: #0a0a0f; }
    [data-testid="stSidebar"] { background: linear-gradient(180deg, #0d1117 0%, #0a0a0f 100%); border-right: 1px solid #1a472a; }
    .section-header { font-size: 1.2rem; font-weight: 700; color: #00ff88; border-bottom: 2px solid #1a472a; padding-bottom: 8px; margin: 20px 0 12px 0; }
    [data-testid="metric-container"] { background: #0d1117; border: 1px solid #1a472a; border-radius: 12px; padding: 12px; }
    .model-card {
        background: #0d1117; border: 1px solid #1a472a;
        border-radius: 12px; padding: 20px; text-align: center; margin: 8px 0;
    }
    .best-model {
        background: linear-gradient(135deg, #0d2818, #0d1117);
        border: 2px solid #00ff88; border-radius: 12px;
        padding: 20px; text-align: center; margin: 8px 0;
    }
</style>
""", unsafe_allow_html=True)

with st.sidebar:
    st.markdown("## 🎾 US Open 2026")
    st.markdown("---")
    st.markdown("""
    - 🏠 Home
    - 👤 Player Profiles
    - ⚖️ Player Comparison
    - 🔮 Match Prediction
    - 🏆 Tournament Prediction
    - 📊 Analytics Dashboard
    - 🤖 **ML Model**
    - ℹ️ About
    """)

st.markdown("# 🤖 Machine Learning Model")
st.markdown("Metodología, resultados y análisis del modelo de predicción")
st.markdown("---")

# Resultados de los modelos
st.markdown('<p class="section-header">📊 COMPARACIÓN DE MODELOS</p>', unsafe_allow_html=True)

modelos_data = {
    "Modelo":    ["Random Forest", "Logistic Regression", "Decision Tree"],
    "Accuracy":  [0.583, 0.652, 0.641],
    "ROC AUC":   [0.632, 0.716, 0.698],
    "Precision": [0.58, 0.65, 0.64],
    "Recall":    [0.58, 0.65, 0.64],
}
df_modelos = pd.DataFrame(modelos_data)

col1, col2, col3 = st.columns(3)
for i, (col, row) in enumerate(zip([col1,col2,col3], df_modelos.itertuples())):
    with col:
        is_best = row.Modelo == "Logistic Regression"
        card_class = "best-model" if is_best else "model-card"
        badge = "🥇 MEJOR MODELO" if is_best else ""
        st.markdown(f"""
        <div class="{card_class}">
            <div style="color:#00ff88;font-size:0.75rem;margin-bottom:4px">{badge}</div>
            <div style="color:#fff;font-size:1.1rem;font-weight:700">{row.Modelo}</div>
            <div style="color:#00ff88;font-size:2rem;font-weight:900;margin:8px 0">{row.Accuracy*100:.1f}%</div>
            <div style="color:#555;font-size:0.85rem">Accuracy</div>
            <div style="color:#888;font-size:0.9rem;margin-top:8px">ROC AUC: {row._4:.3f}</div>
        </div>""", unsafe_allow_html=True)

st.markdown("---")

# Grafico comparativo
fig_comp = go.Figure()
fig_comp.add_trace(go.Bar(name="Accuracy", x=df_modelos["Modelo"], y=df_modelos["Accuracy"]*100,
                           marker_color=["#2e8b57","#00ff88","#1a472a"],
                           text=[f"{v*100:.1f}%" for v in df_modelos["Accuracy"]],
                           textposition="outside", textfont=dict(color="white")))
fig_comp.add_trace(go.Bar(name="ROC AUC", x=df_modelos["Modelo"], y=df_modelos["ROC AUC"]*100,
                           marker_color=["#1a3a6a","#0066cc","#0044aa"],
                           text=[f"{v*100:.1f}%" for v in df_modelos["ROC AUC"]],
                           textposition="outside", textfont=dict(color="white")))
fig_comp.update_layout(barmode="group", template="plotly_dark",
                        paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)",
                        height=350, margin=dict(l=10,r=10,t=10,b=10),
                        legend=dict(font=dict(color="white")),
                        yaxis=dict(range=[0,90]))
st.plotly_chart(fig_comp, use_container_width=True)

st.markdown("---")

# Feature Importance
st.markdown('<p class="section-header">🎯 FEATURE IMPORTANCE — LOGISTIC REGRESSION</p>', unsafe_allow_html=True)

features_data = {
    "Feature": ["Win% Hard Court","Aces 2026","Win% Grand Slams","Ranking ATP",
                 "1er Saque Ganado %","Win% Masters 1000","BP Convertidos %",
                 "Tras perder 1er set","Set Decisivo","2do Saque Ganado %",
                 "Tras ganar 1er set","BP Salvados %","Win% Overall","Tiebreak"],
    "Importancia": [0.756,0.326,0.147,0.124,0.110,0.088,0.082,
                    0.074,0.073,0.059,0.031,0.026,0.016,0.007]
}
df_fi = pd.DataFrame(features_data).sort_values("Importancia", ascending=True)

fig_fi = px.bar(df_fi, x="Importancia", y="Feature", orientation="h",
                color="Importancia", color_continuous_scale="Greens",
                template="plotly_dark", labels={"Importancia":"Importancia","Feature":""})
fig_fi.update_layout(paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)",
                      height=450, coloraxis_showscale=False, showlegend=False,
                      margin=dict(l=10,r=10,t=10,b=10))
fig_fi.update_traces(text=df_fi["Importancia"].apply(lambda x: f"{x:.3f}"),
                      textposition="outside", textfont=dict(color="white", size=10))
st.plotly_chart(fig_fi, use_container_width=True)

st.markdown("---")

# Metodologia
st.markdown('<p class="section-header">📋 METODOLOGÍA</p>', unsafe_allow_html=True)

col1, col2 = st.columns(2)
with col1:
    st.markdown("""
    **Fuentes de datos:**
    - Tabla maestra: 185 jugadores, 53 métricas (ATP Tour, 2025-2026)
    - Historial de partidos: 4,581 partidos en Hard Court (2020-2026)
    - Dataset Jeff Sackmann (via Kaggle)
    - Dataset ATP Daily Update (via Kaggle)

    **Features del modelo (14 variables):**
    - Diferencia de ranking ATP
    - Diferencia de Win% en Hard Court
    - Diferencia de Win% en Grand Slams
    - Diferencia de Win% Overall
    - Diferencia de Win% Masters 1000
    - Diferencia de Win% Set Decisivo
    - Diferencia de Win% Tiebreak
    - Diferencia de Win% tras ganar/perder 1er set
    - Diferencia de 1er/2do Saque Ganado %
    - Diferencia de BP Salvados/Convertidos %
    - Diferencia de Aces
    """)

with col2:
    st.markdown("""
    **Proceso de entrenamiento:**
    - Dataset: 8,082 ejemplos (partido + partido invertido)
    - Split: 80% entrenamiento / 20% test
    - Balance: 50% ganadores / 50% perdedores
    
    **Modelos comparados:**
    - Random Forest (100 árboles)
    - Logistic Regression ← **MEJOR**
    - Decision Tree (profundidad máx. 5)

    **Resultados del mejor modelo:**
    - Accuracy: **65.2%**
    - ROC AUC: **0.716**
    - Precision: 0.65
    - Recall: 0.65
    
    **Limitaciones:**
    - Predecir tenis es inherentemente difícil (65-70% es excelente)
    - No incluye condiciones del día (viento, temperatura)
    - No incluye historial head-to-head directo
    - Las lesiones reducen la fiabilidad de la predicción
    """)

st.markdown("---")
st.markdown('<p style="text-align:center;color:#333;font-size:0.8rem">US Open 2026 Analytics Platform · Capstone Project</p>', unsafe_allow_html=True)
