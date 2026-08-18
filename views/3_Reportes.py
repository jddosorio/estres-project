"""Reports placeholder for the PROTEGE validation platform."""

from __future__ import annotations

import streamlit as st


st.title("PROTEGE — Reportes")
st.caption("Consolidación de evidencias y resultados del procedimiento TRL-4 → TRL-5")

st.info(
    "Este módulo se utilizará para generar reportes por período, trabajador, "
    "zona y ejecución del Gemelo Digital."
)

st.markdown(
    """
    **Contenido previsto:**

    - Resumen ejecutivo de Time on Tools.
    - Tiempo productivo y no productivo por período.
    - Permanencia por zona y trabajador.
    - Validación de jornadas y transiciones ENTER/EXIT.
    - Exportación de evidencias para el informe CORFO.
    """
)

