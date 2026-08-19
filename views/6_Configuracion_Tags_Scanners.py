"""Configuration page for PROTEGE BLE tags and scanners."""

from __future__ import annotations

import streamlit as st


st.title("PROTEGE — Configuración de Tags y Scanners")
st.caption("Preparación de dispositivos para la validación de tránsito BLE")

st.info(
    "Este módulo se habilitará durante la campaña con dispositivos reales. "
    "Permitirá asociar scanners con zonas y tags BLE con trabajadores."
)

st.markdown(
    """
    **Configuración prevista:**

    - Identificación del scanner y gateway LTE.
    - Asociación del scanner con una zona del layout.
    - Asociación del tag BLE con un trabajador simulado.
    - Registro de versión de firmware y estado del dispositivo.
    - Verificación de recepción de RSSI en ClickHouse Cloud.
    """
)

