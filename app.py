"""Main navigation for the ESTRES Streamlit TRL-6 validation platform."""

from __future__ import annotations

import streamlit as st


# ---------------------------------------------------------------------------
# Page configuration
# ---------------------------------------------------------------------------

st.set_page_config(
    page_title="ESTRES — Validación TRL-6",
    page_icon="📈",
    layout="wide",
)


# Selected sidebar page: white tab connected visually to main page
st.markdown(
    """
    <style>
    /* Active page link itself */
    section[data-testid="stSidebar"] a[aria-current="page"],
    section[data-testid="stSidebar"] a[aria-current="page"] > div,
    section[data-testid="stSidebar"] a[aria-current="page"] span {
        background-color: white !important;
    }

    /* Streamlit page-link wrapper containing the active link */
    section[data-testid="stSidebar"] div:has(> a[aria-current="page"]) {
        background-color: white !important;
    }

    /* Extend active row to sidebar's right edge */
    section[data-testid="stSidebar"] div:has(> a[aria-current="page"]) {
        margin-right: -2rem !important;
        padding-right: 2rem !important;
        border-radius: 8px 0 0 8px !important;
    }
    </style>
    """,
    unsafe_allow_html=True,
)


# ---------------------------------------------------------------------------
# Global style
# ---------------------------------------------------------------------------



# ---------------------------------------------------------------------------
# Pages
# ---------------------------------------------------------------------------

system_page = st.Page(
    "views/1_Sistema.py",
    title="Sistema",
    default=True,
)

stress_control_page = st.Page(
    "views/9_Stress_Control_Unit.py",
    title="Stress Control Unit",
)

load_cycles_page = st.Page(
    "views/2_Ciclos_Estres.py",
    title="Ciclos de Estres",
)

fatigue_page = st.Page(
    "views/3_Fatiga.py",
    title="Fatiga",
)

experimental_tests_page_1 = st.Page(
    "views/10_Pruebas_Experimentales_1.py",
    title="Pruebas Experimentales #1",
)

experimental_tests_page_2 = st.Page(
    "views/12_Pruebas_Experimentales_2.py",
    title="Pruebas Experimentales #2",
)

communications_page = st.Page(
    "views/4_Comunicaciones.py",
    title="Comunicaciones",
)

gps_page = st.Page(
    "views/5_GPS.py",
    title="Posición GPS",
)

store_forward_page = st.Page(
    "views/6_Store-Forward.py",
    title="Store & Forward",
)

results_page = st.Page(
    "views/7_Resultados.py",
    title="Resultados TRL-6",
)

patent_page = st.Page(
    "views/8_Patente_Invencion.py",
    title="Patente de Invención",
)

diffusion_page = st.Page(
    "views/11_Difusion.py",
    title="Difusión del Proyecto",
)


# ---------------------------------------------------------------------------
# Navigation
# ---------------------------------------------------------------------------

all_pages = [
    system_page,
    stress_control_page,
    load_cycles_page,
    fatigue_page,
    experimental_tests_page_1,
    experimental_tests_page_2,
    communications_page,
    gps_page,
    store_forward_page,
    results_page,
    patent_page,
    diffusion_page,
]

navigation = st.navigation(
    all_pages,
    position="hidden",
)


# ---------------------------------------------------------------------------
# Sidebar
# ---------------------------------------------------------------------------

with st.sidebar:

    st.caption("CORFO INNOVA REGIÓN")

    st.markdown("## ESTRES")

    st.markdown(
        "**Monitoreo Estructural de Equipos Mineros**"
    )

    st.caption("25IRA2-308620")

   

    # -----------------------------------------------------------------------
    # System
    # -----------------------------------------------------------------------

    st.divider()
    st.caption("SISTEMA")

    st.page_link(
        system_page,
        label="Sistema",
        icon="⚙️",
    )
    st.page_link(
        stress_control_page,
        label="Stress Control Unit",
        icon="🎛️",
    )

    # -----------------------------------------------------------------------
    # Structural monitoring
    # -----------------------------------------------------------------------

    st.divider()
    st.caption("MONITOREO ESTRUCTURAL")

    st.page_link(
        load_cycles_page,
        label="Ciclos de Estres",
        icon="📈",
    )

    st.page_link(
        fatigue_page,
        label="Fatiga",
        icon="〽️",
    )

    st.page_link(
        experimental_tests_page_1,
        label="Pruebas Experimentales #1",
        icon="🧪",
    )

    st.page_link(
        experimental_tests_page_2,
        label="Pruebas Experimentales #2",
        icon="🧪",
    )

    # -----------------------------------------------------------------------
    # Communications
    # -----------------------------------------------------------------------

    st.divider()
    st.caption("COMUNICACIONES")

    st.page_link(
        communications_page,
        label="Comunicaciones",
        icon="📡",
    )

    st.page_link(
        gps_page,
        label="Posición GPS",
        icon="📍",
    )

    st.page_link(
        store_forward_page,
        label="Store & Forward",
        icon="💾",
    )

    # -----------------------------------------------------------------------
    # Validation
    # -----------------------------------------------------------------------

    st.divider()
    st.caption("VALIDACIÓN")

    st.page_link(
        results_page,
        label="Resultados TRL-6",
        icon="✅",
    )

    # -----------------------------------------------------------------------
    # Intellectual property
    # -----------------------------------------------------------------------

    st.divider()
    st.caption("PROPIEDAD INTELECTUAL")

    st.page_link(
        patent_page,
        label="Patente de Invención",
        icon="📄",
    )

    # -----------------------------------------------------------------------
    # Difusion
    # -----------------------------------------------------------------------

    st.divider()
    st.caption("DIFUSION")

    st.page_link(
        diffusion_page,
        label="Difusión del Proyecto",
        icon="📣",
    )


# ---------------------------------------------------------------------------
# Run selected page
# ---------------------------------------------------------------------------

navigation.run()
