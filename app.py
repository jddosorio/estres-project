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

environmental_page = st.Page(
    "views/1_Monitoreo_Ambiental.py",
    title="Monitoreo Ambiental"
)
layout_page = st.Page("views/5_Layout.py", title="Layout", default=True)
digital_twin_page = st.Page("views/2_Gemelo_Digital.py", title="Gemelo Digital")
clickhouse_page = st.Page("views/4_ClickHouse.py", title="Arquitectura ClickHouse")
scanner_config_page = st.Page(
    "views/6_Configuracion_Tags_Scanners.py",
    title="Configuración",
)
transit_page = st.Page("views/7_Pruebas_Transito.py", title="Pruebas de Tránsito")
permanence_page = st.Page(
    "views/8_Permanencia_Zona.py",
    title="Permanencia por Zona",
)
reports_page = st.Page("views/3_Reportes.py", title="Reportes")

all_pages = [
    environmental_page,
    layout_page,
    digital_twin_page,
    clickhouse_page,
    scanner_config_page,
    transit_page,
    permanence_page,
    reports_page,
]

navigation = st.navigation(all_pages, position="hidden")

with st.sidebar:
    st.markdown(
        """
        <div style="padding: 0.25rem 0 0.5rem 0;">
            <div style="font-size: 1.05rem; font-weight: 700;">
                CORFO INNOVA REGIÓN
            </div>
            <div style="margin-top: 0.2rem; font-weight: 600;">PULSOTECH - PROTEGE</div>
            <div style="color: #667085; margin-top: 0.1rem;">
                25IRA2-308607E
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )

    st.divider()
    st.caption("VALIDACIÓN EN LÍNEA")
    st.page_link(environmental_page, label="Monitoreo Ambiental", icon="🌡️")

    st.divider()
    st.caption("VALIDACIÓN DE BASE DE DATOS")
    st.page_link(layout_page, label="Layout", icon="🗺️")
    st.page_link(digital_twin_page, label="Gemelo Digital", icon="🏗️")
    st.page_link(clickhouse_page, label="Arquitectura ClickHouse", icon="🗄️")

    st.divider()
    st.caption("VALIDACIÓN DE TAGS Y SCANNERS BLE")
    st.page_link(scanner_config_page, label="Configuración", icon="📡")
    st.page_link(transit_page, label="Pruebas de Tránsito", icon="🚶")
    st.page_link(permanence_page, label="Permanencia por Zona", icon="📍")

    st.divider()
    st.caption("RESULTADOS")
    st.page_link(reports_page, label="Reportes", icon="📄")

navigation.run()
