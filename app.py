"""Main navigation for the PROTEGE Streamlit validation platform."""

from __future__ import annotations

import streamlit as st


st.set_page_config(
    page_title="PROTEGE — Plataforma de Validación",
    page_icon="🛡️",
    layout="wide",
)

st.markdown(
    """
    <style>
        .block-container {
            padding-top: 2rem;
            padding-bottom: 1rem;
        }
        h1 {
            font-size: 2.2rem !important;
            line-height: 1.15 !important;
            margin-bottom: 0.25rem !important;
        }
        [data-testid="stSidebarNav"] {
            padding-top: 0.5rem;
        }
    </style>
    """,
    unsafe_allow_html=True,
)

pages = {
    "Validación TRL-4 → TRL-5": [
        st.Page(
            "views/1_Monitoreo_Ambiental.py",
            title="Monitoreo Ambiental",
            icon="🌡️",
            default=True,
        ),
        st.Page(
            "views/2_Gemelo_Digital.py",
            title="Gemelo Digital",
            icon="🏗️",
        ),
    ],
    "Análisis y datos": [
        st.Page(
            "views/3_Reportes.py",
            title="Reportes",
            icon="📄",
        ),
        st.Page(
            "views/4_ClickHouse.py",
            title="ClickHouse",
            icon="🗄️",
        ),
    ],
}

navigation = st.navigation(pages, position="sidebar")
navigation.run()

