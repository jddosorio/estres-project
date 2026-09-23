"""System overview for the ESTRES TRL-6 validation platform."""

from __future__ import annotations

import streamlit as st


# ---------------------------------------------------------------------------
# Page
# ---------------------------------------------------------------------------

st.title("ESTRES — Informe Final del Sistema de Monitoreo Estructural")

st.caption(
    "Proyecto CORFO 25IRA2-308620 — "
    "Validación del prototipo integrado TRL-6"
)


# ---------------------------------------------------------------------------
# Objective
# ---------------------------------------------------------------------------

with st.container(border=True):
    st.subheader("Propósito de esta validación")

    st.markdown(
        """
        El proyecto desarrolla y valida una plataforma de
        **monitoreo estructural para equipos mineros de alta criticidad**.

        El sistema permite medir deformaciones estructurales mediante un
        sensor digital ESR, procesar las mediciones para obtener variables
        asociadas a ciclos de carga y fatiga, y transmitir la información
        desde un activo móvil hacia sistemas remotos de almacenamiento y
        visualización.

        La campaña experimental TRL-6 fue realizada sobre un
        **camión betonera de escala real**, utilizando el sistema integrado
        de adquisición, procesamiento Edge y comunicaciones.
        """
    )


# ---------------------------------------------------------------------------
# Architecture
# ---------------------------------------------------------------------------

st.subheader("Arquitectura del sistema")

col_arch, col_photo = st.columns([0.7, 1.3])

with col_arch:
    st.markdown(
        """
        La cadena tecnológica implementada es:

        **Sensor ESR**

        ↓ `EnDat`

        **Gateway EnDat / PROFINET**

        ↓ `PROFINET`

        **PLC Siemens**

        ↓ `OPC UA`

        **Edge Computer — Ubuntu Linux**

        ↓ `Canary Store & Forward`

        **Teltonika RUT200**

        ↓ `LTE`

        **Red Celular / VPN**

        ↓

        **Canary Historian Remoto**
        """
    )

with col_photo:

    img_col, _ = st.columns([3, 5])

    with img_col:
        st.image(
            "images/estres-electronics-box.jpeg",
            caption=(
                "Unidad de adquisición, procesamiento y comunicaciones "
                "del prototipo ESTRES."
            ),
            use_container_width=True,
        )
# ---------------------------------------------------------------------------
# Main functions
# ---------------------------------------------------------------------------

st.subheader("Funciones validadas")

col1, col2, col3 = st.columns(3)

with col1:
    with st.container(border=True):
        st.markdown("### 📈 Monitoreo estructural")
        st.markdown(
            """
            - Deformación estructural
            - Stress
            - Stress Rate
            - Stress Range
            - Ciclos de carga
            - Micro Damage
            """
        )

with col2:
    with st.container(border=True):
        st.markdown("### 📡 Comunicaciones")
        st.markdown(
            """
            - Ethernet industrial
            - OPC UA
            - LTE
            - VPN
            - GPS
            - Acceso remoto
            """
        )

with col3:
    with st.container(border=True):
        st.markdown("### 💾 Gestión de datos")
        st.markdown(
            """
            - Edge Computing
            - Store & Forward
            - Canary Historian
            - Datos históricos
            - AnyViz
            - Visualización remota
            """
        )


# ---------------------------------------------------------------------------
# Processing chain
# ---------------------------------------------------------------------------

st.subheader("Procesamiento estructural")

st.markdown(
    """
    La información adquirida por el sensor es procesada para generar
    indicadores asociados al comportamiento estructural:

    **Deformación**

    ↓

    **Stress**

    ↓

    **Stress Range**

    ↓

    **Load Cycle**

    ↓

    **Curva S-N**

    ↓

    **Micro Damage**

    ↓

    **Daño acumulado**
    """
)


# ---------------------------------------------------------------------------
# Experimental validation
# ---------------------------------------------------------------------------

st.subheader("Campaña experimental")

with st.container(border=True):
    st.markdown(
        """
        Para la validación del prototipo se instaló el sistema sobre un
        **camión betonera**.

        Durante la campaña se realizaron diferentes condiciones dinámicas:

        - operación del tambor de la betonera;
        - diferentes velocidades de rotación;
        - desplazamiento del vehículo;
        - movimientos de avance y retroceso.

        Durante estas pruebas el sistema permaneció adquiriendo las variables
        estructurales y transmitiendo información hacia la infraestructura
        remota.
        """
    )


# ---------------------------------------------------------------------------
# TRL-6 validation scope
# ---------------------------------------------------------------------------

st.subheader("Alcance de la validación TRL-6")

validation = {
    "Subsistema": [
        "Sensor estructural",
        "Adquisición industrial",
        "Procesamiento",
        "Edge Computing",
        "Comunicación celular",
        "Posicionamiento",
        "Continuidad de datos",
        "Almacenamiento remoto",
        "Visualización",
    ],
    "Tecnología": [
        "ESR / EnDat",
        "PROFINET / PLC",
        "Stress / Load Cycles / Fatigue",
        "Ubuntu Linux",
        "Teltonika RUT200 / LTE",
        "GPS",
        "Canary Store & Forward",
        "Canary Historian",
        "AnyViz",
    ],
}

st.dataframe(
    validation,
    use_container_width=True,
    hide_index=True,
)


# ---------------------------------------------------------------------------
# TRL interpretation
# ---------------------------------------------------------------------------

st.info(
    """
    Esta plataforma reúne la evidencia experimental utilizada para documentar
    la validación TRL-6 del prototipo integrado.

    Las diferentes secciones presentan los resultados de ciclos de carga,
    fatiga, comunicaciones, GPS, Store & Forward y almacenamiento remoto.
    """
)