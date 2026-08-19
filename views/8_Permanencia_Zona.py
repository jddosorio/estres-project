"""Zone permanence results for the PROTEGE BLE validation."""

from __future__ import annotations

import streamlit as st


st.title("PROTEGE — Permanencia por Zona")
st.caption("Resultados inferidos a partir de tags y scanners BLE")

st.info(
    "Este módulo se habilitará cuando existan intervalos de permanencia "
    "inferidos desde las mediciones RSSI reales."
)

st.markdown(
    """
    **Indicadores previstos:**

    - Tiempo de permanencia por tag, trabajador y zona.
    - Cobertura de detección durante el recorrido.
    - Error temporal de entrada y salida.
    - Cantidad de transiciones y salidas forzadas.
    - Comparación contra el ground truth del protocolo de prueba.
    """
)

