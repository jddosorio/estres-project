"""Stress Control Unit description for the ESTRES TRL-6 platform."""

from __future__ import annotations

from pathlib import Path

import streamlit as st


# ---------------------------------------------------------------------------
# Configuration
# ---------------------------------------------------------------------------

IMAGE_FILE = Path("images/estres-electronics-box.jpeg")


# ---------------------------------------------------------------------------
# Header
# ---------------------------------------------------------------------------

st.title("Stress Control Unit")

st.caption(
    "Proyecto CORFO 25IRA2-308620 — "
    "Unidad electrónica de adquisición y procesamiento estructural"
)


# ---------------------------------------------------------------------------
# Overview
# ---------------------------------------------------------------------------

with st.container(border=True):

    st.subheader("Descripción")

    st.markdown(
        """
        La **Stress Control Unit** constituye la unidad electrónica de
        adquisición y procesamiento del sistema ESTRES.

        Su función es adquirir la medición de deformación proveniente del
        sensor ESR, transferirla al sistema de control industrial y ejecutar
        el procesamiento necesario para obtener las variables utilizadas en
        el análisis de ciclos de estrés y fatiga.

        La unidad integra en un gabinete industrial los elementos de
        adquisición, control, comunicaciones industriales, Edge Computing
        y alimentación requeridos para operar el sistema como un prototipo
        autónomo y transportable.
        """
    )


# ---------------------------------------------------------------------------
# Photo and acquisition chain
# ---------------------------------------------------------------------------

st.subheader("Unidad electrónica")

col_photo, col_chain = st.columns([1, 1.25], gap="large")


with col_photo:

    if IMAGE_FILE.exists():

        # Imagen al 60% del ancho de col_photo
        img_col, _ = st.columns([3, 2])

        with img_col:
            st.image(
                str(IMAGE_FILE),
                caption=(
                    "Stress Control Unit utilizada durante la "
                    "campaña experimental TRL-6."
                ),
                use_container_width=True,
            )

    else:

        st.warning(
            f"No se encontró la imagen: {IMAGE_FILE}"
        )


with col_chain:

    st.markdown("### Cadena de adquisición y procesamiento")

    st.markdown(
        """
        **Sensor ESR**

        ↓ `EnDat`

        **Gateway EnDat / PROFINET**

        ↓ `PROFINET`

        **PLC Siemens**

        ↓ `PROFINET / Ethernet`

        **IBHLink UA**

        ↓ `OPC UA`

        **Edge Computer — Ubuntu Linux**

        ↓ `Canary Edge`

        **Store & Forward / Historización remota**
        """
    )


# ---------------------------------------------------------------------------
# Functional architecture
# ---------------------------------------------------------------------------

st.subheader("Arquitectura funcional")

with st.container(border=True):

    st.markdown(
        """
        La Stress Control Unit separa funcionalmente el procesamiento
        determinístico de las variables estructurales y la gestión Edge
        de los datos.

        **PLC Siemens**

        Realiza la adquisición y el procesamiento en tiempo real de las
        mediciones provenientes del sensor ESR.

        **Edge Computer**

        Adquiere mediante OPC UA las variables procesadas por el PLC y
        ejecuta los servicios necesarios para almacenamiento temporal,
        Store & Forward y transferencia hacia el historiador remoto.
        """
    )


# ---------------------------------------------------------------------------
# Main components
# ---------------------------------------------------------------------------

st.subheader("Componentes principales")

col1, col2 = st.columns(2, gap="large")


with col1:

    with st.container(border=True):

        st.markdown("### Sensor ESR")

        st.markdown(
            """
            Sensor digital de deformación estructural utilizado como
            elemento primario de medición.

            La información del sensor es transmitida mediante la interfaz
            digital **EnDat** hacia el gateway de adquisición.
            """
        )


    with st.container(border=True):

        st.markdown("### Gateway EnDat / PROFINET")

        st.markdown(
            """
            Interfaz entre el sensor ESR y el sistema de control industrial.

            El gateway recibe la información digital EnDat y la incorpora
            a la red **PROFINET**, permitiendo que las mediciones sean
            adquiridas por el PLC Siemens.
            """
        )


    with st.container(border=True):

        st.markdown("### PLC Siemens")

        st.markdown(
            """
            Controlador industrial encargado de adquirir y procesar las
            variables estructurales en tiempo real.

            El procesamiento implementado permite obtener:

            - deformación estructural;
            - Stress;
            - Stress Rate;
            - Stress Range;
            - Stress Rate Range;
            - detección de ciclos de estrés;
            - Micro Damage.
            """
        )


with col2:

    with st.container(border=True):

        st.markdown("### IBHLink UA")

        st.markdown(
            """
            Gateway industrial que proporciona acceso **OPC UA** a las
            variables disponibles en el sistema de control.

            Esta interfaz desacopla el procesamiento realizado por el PLC
            de las aplicaciones Edge encargadas de adquirir y gestionar
            los datos.
            """
        )


    with st.container(border=True):

        st.markdown("### Edge Computer")

        st.markdown(
            """
            Computador industrial con **Ubuntu Linux** encargado de ejecutar
            los servicios Edge de la plataforma.

            Sus principales funciones son:

            - adquisición de variables mediante OPC UA;
            - ejecución de Canary Edge;
            - almacenamiento temporal;
            - Store & Forward;
            - transferencia de datos hacia el historiador remoto.
            """
        )


    with st.container(border=True):

        st.markdown("### Alimentación e infraestructura")

        st.markdown(
            """
            El gabinete integra las fuentes de alimentación, montaje sobre
            riel DIN, cableado y conexiones Ethernet requeridas para
            interconectar los diferentes componentes de la unidad.

            La integración en un único gabinete facilita el transporte,
            instalación y utilización del prototipo en campañas de prueba.
            """
        )


# ---------------------------------------------------------------------------
# Structural processing
# ---------------------------------------------------------------------------

st.subheader("Procesamiento estructural")

with st.container(border=True):

    st.markdown(
        """
        El procesamiento implementado transforma la medición primaria
        obtenida por el sensor ESR en variables utilizadas para detectar
        ciclos de estrés y estimar su contribución al daño por fatiga.
        """
    )

    st.markdown(
        """
        ### Cadena de procesamiento

        **Deformación estructural**

        ↓

        **Stress**

        ↓

        **Stress Rate**

        ↓

        **Stress Range**

        ↓

        **Detección del ciclo de estrés**

        ↓

        **Curva S-N**

        ↓

        **Micro Damage**
        """
    )


# ---------------------------------------------------------------------------
# Data interface
# ---------------------------------------------------------------------------

st.subheader("Interfaz con el sistema Edge")

col_plc, col_edge = st.columns(2)


with col_plc:

    with st.container(border=True):

        st.markdown("### Control industrial")

        st.markdown(
            """
            **Sensor / PLC**

            - EnDat
            - PROFINET
            - procesamiento en tiempo real
            - detección de eventos
            - cálculo de variables estructurales
            """
        )


with col_edge:

    with st.container(border=True):

        st.markdown("### Procesamiento Edge")

        st.markdown(
            """
            **PLC / Edge Computer**

            - OPC UA
            - Canary Edge
            - adquisición de tags
            - almacenamiento temporal
            - Store & Forward
            """
        )


# ---------------------------------------------------------------------------
# Experimental validation
# ---------------------------------------------------------------------------

st.subheader("Validación experimental")

st.success(
    """
    La Stress Control Unit fue utilizada durante la campaña experimental
    realizada sobre el camión betonera de escala real.

    Durante las pruebas, el sistema integrado adquirió las deformaciones
    estructurales, procesó las variables de estrés, identificó ciclos de
    estrés y generó los valores de Micro Damage posteriormente registrados
    en el historiador.
    """
)