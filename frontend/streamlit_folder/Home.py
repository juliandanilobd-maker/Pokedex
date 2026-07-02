from __future__ import annotations

import streamlit as st

st.set_page_config(
    page_title="Pokedex Analítica - Home",
    page_icon="🔺",
    layout="wide",
    initial_sidebar_state="expanded",
)

st.markdown(
    """
    <style>
    .main-title {
        font-size: 42px;
        font-weight: 800;
        background: linear gradient(90deg, #ff4b4b, #ff7676);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        margin-bottom: 5px;
    }
    .subtitle {
        font-size: 18px;
        opacity: 0.8;
        margin-bottom: 30px;
    }
    .feature-card {
        background-color: rgba(255, 255, 255, 0.04);
        padding: 20px;
        border-radius: 10px;
        border-left: 4px solid #ff4b4b;
        margin-bottom: 15px;
    }
    .feature-title {
        font-size: 16px;
        font-weight: bold;
        margin-bottom: 8px;
        color: #ff4b4b;
    }
    </style>
    """,
    unsafe_allow_html=True,
)

st.markdown(
    """
    <h1 class="
        main-title"
    >Pokedex</h1>
    """,
    unsafe_allow_html=True,
)
st.markdown(
    """
    <p class="
        subtitle
    ">Bienvenido, Entrenador.
    Aquí es donde la ciencia Pokemon se convierte en tu mayor ventaja competitiva
    </p>
    """,
    unsafe_allow_html=True,
)
st.info(
    "👈 **Guía de Navegación:** Utiliza el panel de la barra lateral izquierda para "
    "desplazarte entre las diferentes herramientas de rastreo y análisis de tu Pokedex"
)

st.write("")

col_info, col_visual = st.columns([1.2, 1], gap="large")

with col_info:
    st.markdown("### ⚔️ Prepara tu próxima batalla")
    st.markdown(
        "Esta no es una Pokedex ordinaria. Ha sido diseñada como tu terminal "
        "táctico avanzado, para que analices a fondo las capacidades de cualquier "
        "especie antes de saltar a la arena de combate"
    )
    st.markdown("Explora las secciones del menú lateral")

    st.markdown(
        """
        <div class="
            feature-card
        ">
            <div class="
                feature-title"
            >🔍 Búsqueda Individual Táctica
            </div>
            <div>
            Busca cualquier Pokemon por su nombre o ID. Descubirás sus datos físicos,
            su gráfico de rendimiento de estadísticas (HP, Ataque, Defensa, Velocidad)
            y su matriz de debilidades y resistencias elementales para saber cuando
            combatir. Además podrás revisar cadenas evolutivas y requisitos de nivel.
        </div>
        """,
        unsafe_allow_html=True,
    )

    st.markdown(
        """
        <div class="
            feature-card
        ">
            <div class="
                feature-title
            ">🎛️ Buscador Avanzado por Estadísticas (Filtros)
            </div>
            <div>
            ¿Necesitas un Pokemon de tipo Fuego de la segunda generación que sea
            extremadamente rápido?
            Esta herramienta te permite combinar filtros para encontrar tu
            compañero Pokemon ideal, que encaje con tu estrategia de combate
            en una galería interactiva.
            <div>
        </div>
        """,
        unsafe_allow_html=True,
    )

with col_visual:
    st.markdown("### 🎚️ Estado del Dispositivo")

    st.success("Conexión con la Base de Datos Pokemon: **ONLINE**")

    st.markdown(
        """
        <div style="
            background-color: #111;
            padding: 20px;
            border-radius: 8px;
            border: 1px solid #333;
            font-family: monospace;
            font-size: 13px;
        ">
            <span style="
                color: #00ff00;
            ">● SISTEMA OPERATIVO POKEDEX</span><br>
            <span style="
                color: #aaa;
            ">[OK] Datos de efectividad de combate cargados.</span><br>
            <span style="
                color: #aaa;
            ">[OK] Sensor de compatibilidad evolutiva activo.</span><br>
            <span style="
                color: #aaa;
            ">[OK] Registro biológico de Kanto, Johto y más...</span><br>
            <span style="
                color: #ff4b4b;
            ">[READY] Esperando ID o Nombre del espécimen...</span><br>
        </div>
        """,
        unsafe_allow_html=True,
    )

    st.write("")
    st.caption("Herramienta homologada para análisis competitivo de la Liga Pokemon.")
