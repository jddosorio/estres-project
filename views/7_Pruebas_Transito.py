"""Controlled transit tests for the PROTEGE BLE validation."""

from __future__ import annotations

import streamlit as st


st.title("PROTEGE — Pruebas de Tránsito")
st.caption("Validación controlada del desplazamiento de tags entre zonas")

st.info(
    "Este módulo mostrará las mediciones reales de tránsito cuando comiencen "
    "las pruebas con tags portables y scanners BLE."
)

st.markdown(
    """
    **Protocolo previsto:**

    - Registrar la hora real de inicio y término de cada recorrido.
    - Trasladar el tag por una secuencia conocida de zonas.
    - Capturar RSSI por scanner durante el recorrido.
    - Identificar eventos `ENTER`, `EXIT` y `FORCED_EXIT`.
    - Comparar la trayectoria inferida con la trayectoria real anotada.
    """
)

