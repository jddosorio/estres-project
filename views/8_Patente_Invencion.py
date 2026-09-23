"""Propiedad intelectual del proyecto ESTRES."""

from __future__ import annotations

from pathlib import Path

import streamlit as st


# -----------------------------------------------------------------------------
# Configuration
# -----------------------------------------------------------------------------

IMAGE_DIR = Path("images")

INAPI_STATUS_IMAGE = IMAGE_DIR / "inapi-patent-status.png"
INAPI_HISTORY_IMAGE = IMAGE_DIR / "inapi-patent-history.png"


# -----------------------------------------------------------------------------
# Header
# -----------------------------------------------------------------------------

st.title("Patente de Invención")

st.caption(
    "Proyecto CORFO 25IRA2-308620 — "
    "Protección de la propiedad intelectual"
)


# -----------------------------------------------------------------------------
# Patent summary
# -----------------------------------------------------------------------------

with st.container(border=True):

    st.subheader("Solicitud de patente")

    st.markdown(
        """
        Como parte de la estrategia de protección de la propiedad intelectual
        asociada a la tecnología desarrollada, se presentó ante el
        **Instituto Nacional de Propiedad Industrial (INAPI)** una solicitud
        de patente de invención relacionada con el sistema de monitoreo
        estructural.
        """
    )


col1, col2, col3 = st.columns(3)

with col1:
    st.metric(
        "Solicitud",
        "2025-02836",
    )

with col2:
    st.metric(
        "Fecha de solicitud",
        "22/09/2025",
    )

with col3:
    st.metric(
        "Estado",
        "Etapa resolutiva",
    )


st.markdown("### Título de la invención")

st.info(
    "Sistema de monitoreo de deformaciones estructurales "
    "mediante sensores digitales"
)


# -----------------------------------------------------------------------------
# Current status
# -----------------------------------------------------------------------------

st.subheader("Estado de tramitación")

col_status, col_text = st.columns([1, 1], gap="large")


with col_status:

    if INAPI_STATUS_IMAGE.exists():

        st.image(
            str(INAPI_STATUS_IMAGE),
            caption=(
                "Resolución INAPI de fecha 06/08/2026 que declara "
                "la solicitud en etapa resolutiva."
            ),
            use_container_width=True,
        )

    else:

        st.info(
            "Guardar la resolución INAPI como "
            "`images/inapi-patent-status.png`."
        )


with col_text:

    st.markdown("### Etapa resolutiva")

    st.markdown(
        """
        Con fecha **6 de agosto de 2026**, INAPI emitió la resolución
        correspondiente a la solicitud de patente de invención
        **2025-02836**.

        La resolución establece que, atendido el mérito de los
        antecedentes, la solicitud se encuentra en **etapa resolutiva**.

        Asimismo, los antecedentes fueron derivados al examinador
        designado por INAPI.

        Esta etapa forma parte del procedimiento de tramitación de la
        solicitud y **no corresponde todavía a la concesión definitiva
        de la patente**.
        """
    )

    st.success(
        "Solicitud de patente de invención actualmente "
        "en etapa resolutiva."
    )


# -----------------------------------------------------------------------------
# Relationship with ESTRES
# -----------------------------------------------------------------------------

st.subheader("Relación con el proyecto ESTRES")

with st.container(border=True):

    st.markdown(
        """
        La solicitud de patente protege desarrollos relacionados con el
        **monitoreo de deformaciones estructurales mediante sensores
        digitales**, ámbito tecnológico directamente relacionado con la
        plataforma ESTRES.

        El proyecto integra medición de deformaciones estructurales,
        procesamiento industrial de las señales y determinación de variables
        utilizadas para caracterizar el comportamiento estructural del activo.

        La protección de propiedad intelectual constituye, por lo tanto,
        un resultado complementario al proceso de desarrollo y validación
        tecnológica realizado durante el proyecto.
        """
    )


# -----------------------------------------------------------------------------
# INAPI procedure
# -----------------------------------------------------------------------------

st.subheader("Expediente INAPI")

st.markdown(
    """
    El expediente registra las distintas etapas administrativas y periciales
    de la solicitud desde su presentación en septiembre de 2025.
    """
)


events = [
    {
        "Fecha": "22/09/2025",
        "Actuación": "Expediente inicial",
    },
    {
        "Fecha": "23/09/2025",
        "Actuación": "Pago — Pago inicial C/2025/19512",
    },
    {
        "Fecha": "02/10/2025",
        "Actuación": "Resolución de aceptación a trámite 2025/50930",
    },
    {
        "Fecha": "24/12/2025",
        "Actuación": (
            "Resolución de apercibimiento de pago de arancel "
            "pericial 2025/65977"
        ),
    },
    {
        "Fecha": "24/12/2025",
        "Actuación": "Pago — Pago Peritaje C/2025/27043",
    },
    {
        "Fecha": "06/04/2026",
        "Actuación": "Resolución de nombramiento de perito 2026/15873",
    },
    {
        "Fecha": "07/04/2026",
        "Actuación": "SGP aceptación de nombramiento 2026/4594",
    },
    {
        "Fecha": "13/04/2026",
        "Actuación": (
            "Resolución de aceptación del nombramiento de perito "
            "2026/17715"
        ),
    },
    {
        "Fecha": "20/04/2026",
        "Actuación": "SGP informe pericial 2026/5320",
    },
    {
        "Fecha": "20/04/2026",
        "Actuación": "SGP informe de búsqueda 2026/5321",
    },
    {
        "Fecha": "23/04/2026",
        "Actuación": (
            "Resolución de notificación del informe pericial "
            "2026/20365"
        ),
    },
    {
        "Fecha": "13/05/2026",
        "Actuación": "Contesta — Informe pericial C/2026/10288",
    },
    {
        "Fecha": "19/05/2026",
        "Actuación": (
            "Resolución de pase al perito de las observaciones "
            "del solicitante 2026/26159"
        ),
    },
    {
        "Fecha": "03/06/2026",
        "Actuación": "SGP respuesta pericial 2026/7470",
    },
    {
        "Fecha": "03/06/2026",
        "Actuación": "SGP informe de búsqueda 2026/7471",
    },
    {
        "Fecha": "08/06/2026",
        "Actuación": (
            "Resolución de notificación de la respuesta pericial "
            "2026/29898"
        ),
    },
    {
        "Fecha": "27/06/2026",
        "Actuación": "Contesta — Respuesta del perito C/2026/14057",
    },
    {
        "Fecha": "30/06/2026",
        "Actuación": "Contesta — Respuesta del perito C/2026/14139",
    },
    {
        "Fecha": "07/07/2026",
        "Actuación": (
            "Resolución de existencia de observaciones del solicitante "
            "a la respuesta pericial 2026/35288"
        ),
    },
    {
        "Fecha": "06/08/2026",
        "Actuación": (
            "Resolución que declara solicitud en etapa resolutiva "
            "y designa examinador 2026/40657"
        ),
    },
]


st.dataframe(
    events,
    use_container_width=True,
    hide_index=True,
)


# -----------------------------------------------------------------------------
# Expedient screenshot
# -----------------------------------------------------------------------------

with st.expander("Ver registro del expediente INAPI"):

    if INAPI_HISTORY_IMAGE.exists():

        st.image(
            str(INAPI_HISTORY_IMAGE),
            caption=(
                "Registro de actuaciones del expediente de la "
                "solicitud de patente."
            ),
            use_container_width=True,
        )

    else:

        st.info(
            "Guardar la captura del expediente como "
            "`images/inapi-patent-history.png`."
        )


# -----------------------------------------------------------------------------
# TRL / IP distinction
# -----------------------------------------------------------------------------

st.subheader("Propiedad intelectual y validación tecnológica")

with st.container(border=True):

    st.markdown(
        """
        La tramitación de la patente constituye una línea de trabajo
        complementaria a la validación tecnológica del proyecto.

        **Validación tecnológica**

        Desarrollo y demostración experimental del sistema ESTRES,
        incluyendo sensores, adquisición, procesamiento, comunicaciones,
        Edge Computing, almacenamiento y análisis de variables estructurales.

        **Propiedad intelectual**

        Protección de los desarrollos asociados al sistema de monitoreo
        de deformaciones estructurales mediante sensores digitales.

        Ambas actividades aportan antecedentes diferentes: la validación
        experimental demuestra el funcionamiento de la tecnología, mientras
        que el expediente INAPI documenta el proceso de protección de la
        invención.
        """
    )


st.caption(
    "Fuente de antecedentes: expediente de solicitud de patente "
    "de invención INAPI 2025-02836."
)