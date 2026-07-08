import streamlit as st

st.set_page_config(page_title="About", page_icon="ℹ️", layout="wide")

st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;600;700;900&display=swap');
    * { font-family: 'Inter', sans-serif; }
    .stApp { background-color: #0a0a0f; }
    [data-testid="stSidebar"] { background: linear-gradient(180deg, #0d1117 0%, #0a0a0f 100%); border-right: 1px solid #1a472a; }
    .section-header { font-size: 1.2rem; font-weight: 700; color: #00ff88; border-bottom: 2px solid #1a472a; padding-bottom: 8px; margin: 20px 0 12px 0; }
    .info-card {
        background: #0d1117; border: 1px solid #1a472a;
        border-radius: 12px; padding: 20px; margin: 8px 0;
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
    - 🤖 ML Model
    - ℹ️ **About**
    """)

st.markdown("# ℹ️ About")
st.markdown("Información sobre el proyecto y su metodología")
st.markdown("---")

st.markdown('<p class="section-header">🎯 OBJETIVO DEL PROYECTO</p>', unsafe_allow_html=True)
st.markdown("""
<div class="info-card">
    <p style="color:#ccc;line-height:1.8">
    Este proyecto es un <b style="color:#00ff88">Capstone de Data Analytics</b> cuyo objetivo es construir
    una plataforma profesional de análisis y predicción del <b style="color:#00ff88">US Open 2026</b>.
    </p>
    <p style="color:#ccc;line-height:1.8">
    Combina datos reales del circuito ATP, análisis exploratorio de datos, feature engineering
    y machine learning para predecir el ganador del torneo más importante del verano americano.
    </p>
</div>
""", unsafe_allow_html=True)

st.markdown('<p class="section-header">📊 FUENTES DE DATOS</p>', unsafe_allow_html=True)

col1, col2 = st.columns(2)
with col1:
    st.markdown("""
    <div class="info-card">
        <h4 style="color:#00ff88">🎾 ATP Tour (atptour.com)</h4>
        <p style="color:#888">Estadísticas de servicio y resto 2025-2026 en Hard Court, recopiladas manualmente:</p>
        <ul style="color:#ccc">
            <li>185 jugadores activos</li>
            <li>Aces, 1er/2do saque %</li>
            <li>Break points salvados/convertidos</li>
            <li>Rendimiento bajo presión</li>
            <li>Ranking ATP actual (julio 2026)</li>
        </ul>
    </div>""", unsafe_allow_html=True)

with col2:
    st.markdown("""
    <div class="info-card">
        <h4 style="color:#00ff88">📁 Jeff Sackmann (via Kaggle)</h4>
        <p style="color:#888">Historial de partidos ATP 2020-2024:</p>
        <ul style="color:#ccc">
            <li>Dataset guillemservera/tennis</li>
            <li>Partidos en Hard Court</li>
            <li>Resultado, score, ronda</li>
        </ul>
        <h4 style="color:#00ff88;margin-top:12px">📁 ATP Daily Update (Kaggle)</h4>
        <p style="color:#888">Partidos 2025-2026:</p>
        <ul style="color:#ccc">
            <li>Dataset dissfya/atp-tennis</li>
            <li>Actualizado hasta junio 2026</li>
        </ul>
    </div>""", unsafe_allow_html=True)

st.markdown('<p class="section-header">🔬 METODOLOGÍA</p>', unsafe_allow_html=True)

pasos = [
    ("1️⃣ Fase 1 — Recolección de datos", "Carga de la tabla maestra (185 jugadores, 53 columnas) y el historial de partidos ATP (4,581 partidos en Hard Court, 2020-2026)."),
    ("2️⃣ Fase 2 — Limpieza de datos", "Eliminación de partidos inválidos (retiros, walkovers), corrección de escala en variables de win%, relleno de faltantes con la mediana."),
    ("3️⃣ Fase 3 — EDA", "Análisis exploratorio: distribuciones, Top 10 por métricas clave, mapa de correlaciones, rendimiento bajo presión."),
    ("4️⃣ Fase 4 — Feature Engineering", "Creación de 14 features basadas en diferencias entre jugadores (ranking, win% Hard, GS, servicio, presión). 8,082 ejemplos balanceados."),
    ("5️⃣ Fase 5 — Machine Learning", "Comparación de Random Forest, Logistic Regression y Decision Tree. Mejor modelo: Logistic Regression con 65.2% accuracy y 0.716 ROC AUC."),
    ("6️⃣ Fase 6 — Predicciones", "Predicción de partidos individuales y probabilidades de ganar el US Open 2026, con estado de lesiones actualizado a julio 2026."),
]

for titulo, desc in pasos:
    st.markdown(f"""
    <div class="info-card">
        <b style="color:#00ff88">{titulo}</b>
        <p style="color:#888;margin:8px 0 0 0">{desc}</p>
    </div>""", unsafe_allow_html=True)

st.markdown('<p class="section-header">⚙️ TECNOLOGÍAS UTILIZADAS</p>', unsafe_allow_html=True)

col1, col2, col3 = st.columns(3)
with col1:
    st.markdown("""
    <div class="info-card" style="text-align:center">
        <div style="font-size:2rem">🐍</div>
        <b style="color:#00ff88">Python</b>
        <p style="color:#555;font-size:0.85rem">Lenguaje principal</p>
    </div>
    <div class="info-card" style="text-align:center">
        <div style="font-size:2rem">🐼</div>
        <b style="color:#00ff88">Pandas & NumPy</b>
        <p style="color:#555;font-size:0.85rem">Manipulación de datos</p>
    </div>""", unsafe_allow_html=True)

with col2:
    st.markdown("""
    <div class="info-card" style="text-align:center">
        <div style="font-size:2rem">📊</div>
        <b style="color:#00ff88">Plotly</b>
        <p style="color:#555;font-size:0.85rem">Visualizaciones interactivas</p>
    </div>
    <div class="info-card" style="text-align:center">
        <div style="font-size:2rem">🤖</div>
        <b style="color:#00ff88">Scikit-learn</b>
        <p style="color:#555;font-size:0.85rem">Machine Learning</p>
    </div>""", unsafe_allow_html=True)

with col3:
    st.markdown("""
    <div class="info-card" style="text-align:center">
        <div style="font-size:2rem">🌐</div>
        <b style="color:#00ff88">Streamlit</b>
        <p style="color:#555;font-size:0.85rem">Web Application</p>
    </div>
    <div class="info-card" style="text-align:center">
        <div style="font-size:2rem">☁️</div>
        <b style="color:#00ff88">Google Colab</b>
        <p style="color:#555;font-size:0.85rem">Entorno de desarrollo</p>
    </div>""", unsafe_allow_html=True)

st.markdown('<p class="section-header">⚠️ LIMITACIONES</p>', unsafe_allow_html=True)
st.markdown("""
<div class="info-card">
<ul style="color:#888;line-height:2">
    <li>El US Open 2026 aún no ha ocurrido — todas las predicciones son estimaciones basadas en datos históricos y forma actual.</li>
    <li>El modelo no incluye condiciones del día (viento, temperatura, horario de partido).</li>
    <li>No incluye historial head-to-head directo entre jugadores.</li>
    <li>Las lesiones pueden cambiar significativamente las probabilidades — estado actualizado a julio 2026.</li>
    <li>65.2% de accuracy es excelente para predicción de tenis (los mejores modelos del mundo alcanzan 68-70%).</li>
</ul>
</div>""", unsafe_allow_html=True)

st.markdown("---")
st.markdown("""
<p style="text-align:center;color:#444;font-size:0.9rem">
US Open 2026 Analytics Platform · Capstone Project · Data Analytics<br>
<span style="color:#1a472a">Datos: ATP Tour · Jeff Sackmann · Kaggle</span>
</p>""", unsafe_allow_html=True)
