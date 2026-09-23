"""Difusión y participación del proyecto ESTRES."""

from __future__ import annotations

import streamlit as st


st.title("Difusión del Proyecto")

st.caption(
    "Proyecto CORFO 25IRA2-308620 — "
    "Actividades de difusión, exhibición y material audiovisual"
)


# -----------------------------------------------------------------------------
# Objetivo
# -----------------------------------------------------------------------------

with st.container(border=True):

    st.subheader("Difusión de resultados")

    st.markdown(
        """
        Durante la ejecución del proyecto ESTRES se han desarrollado
        actividades orientadas a la difusión de la tecnología, presentación
        del proyecto ante actores del ecosistema de innovación y exhibición
        de la solución para aplicaciones de monitoreo estructural en equipos
        mineros.

        Esta sección consolida las principales actividades de difusión,
        participación en eventos y material audiovisual generado durante
        el proyecto.
        """
    )


# -----------------------------------------------------------------------------
# Actividades destacadas
# -----------------------------------------------------------------------------

st.subheader("Actividades destacadas")

col1, col2 = st.columns(2, gap="large")


with col1:

    with st.container(border=True):

        st.markdown("### 🚀 Lanza tu Innovación")

        st.markdown(
            """
            El proyecto fue **seleccionado para participar en
            Lanza tu Innovación**, instancia orientada a visibilizar
            soluciones tecnológicas e innovaciones aplicables a la
            industria.

            **Evidencia a incorporar:**

            - selección del proyecto;
            - material de presentación;
            - fotografías;
            - publicaciones;
            - video de presentación.
            """
        )


with col2:

    with st.container(border=True):

        st.markdown("### ⛏️ EXPONOR 2026")

        st.markdown(
            """
            ESTRES fue presentado en el contexto de **EXPONOR 2026**,
            permitiendo mostrar la tecnología y su aplicación para
            monitoreo estructural de equipos de alta criticidad.

            **Evidencia a incorporar:**

            - participación en EXPONOR 2026;
            - fotografías de la exhibición;
            - material gráfico;
            - publicaciones;
            - videos relacionados con el proyecto.
            """
        )


# -----------------------------------------------------------------------------
# Material audiovisual
# -----------------------------------------------------------------------------

st.subheader("Material audiovisual")

st.markdown(
    """
    Como parte de las actividades de difusión del proyecto se desarrollaron
    contenidos audiovisuales orientados a presentar la tecnología ESTRES,
    su aplicación en monitoreo estructural y su participación en actividades
    de innovación y difusión tecnológica.
    """
)


col1, col2 = st.columns(2, gap="large")

with col1:

    with st.container(border=True):

        st.markdown("### ⛏️ Invitación a EXPONOR")

        st.markdown(
            """
            Video desarrollado por **PULSO Tech** para difusión de su
            participación en EXPONOR.
            """
        )

        st.video(
            "https://www.youtube.com/watch?v=UJz-BScaTA0"
        )


with col2:

    with st.container(border=True):

        st.markdown("### 🚀 Lanza tu Innovación")

        st.markdown(
            """
            Video desarrollado por **PULSO Tech** en el contexto de
            **Lanza tu Innovación**.
            """
        )

        st.video(
            "https://www.youtube.com/watch?v=Dk-kl4A3jD4"
        )


with st.container(border=True):

    st.markdown("### 📈 Monitoreo de Estrés Estructural")

    st.markdown(
        """
        Video promocional desarrollado para presentar la solución de
        **monitoreo de estrés estructural** y su aplicación en equipos
        industriales y mineros.
        """
    )

    st.video(
        "https://www.youtube.com/watch?v=BturUroqeaY"
    )

# -----------------------------------------------------------------------------
# Registro
# -----------------------------------------------------------------------------

st.subheader("Registro de actividades")

st.markdown(
    """
    Las actividades de difusión serán documentadas indicando la fecha,
    actividad, institución o evento, descripción de la participación y
    evidencia asociada.
    """
)

st.dataframe(
    {
        "Actividad": [
            "Lanza tu Innovación",
            "EXPONOR 2026",
        ],
        "Tipo": [
            "Selección / presentación",
            "Exhibición tecnológica",
        ],
        "Evidencia": [
            "Pendiente de incorporar",
            "Pendiente de incorporar",
        ],
    },
    use_container_width=True,
    hide_index=True,
)


# -----------------------------------------------------------------------------
# Resultado
# -----------------------------------------------------------------------------

st.info(
    """
    Esta sección será actualizada progresivamente con fotografías,
    publicaciones, enlaces y videos generados durante la ejecución
    del proyecto ESTRES.
    """
)