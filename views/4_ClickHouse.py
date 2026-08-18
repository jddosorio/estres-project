"""ClickHouse data layer overview for the PROTEGE validation platform."""

from __future__ import annotations

import streamlit as st


st.title("PROTEGE — ClickHouse Cloud")
st.caption("Estado y trazabilidad de la capa de almacenamiento de datos")

st.info(
    "Este módulo se utilizará para revisar el estado de las tablas, volúmenes "
    "de registros, períodos disponibles y controles de calidad de datos."
)

st.markdown(
    """
    **Fuentes actualmente consideradas:**

    - `default.environmental_telemetry`: mediciones provenientes del sensor real.
    - `default.ble_raw`: registros RSSI recibidos desde scanners BLE.
    - `protege.twin_runs`: ejecuciones reproducibles del Gemelo Digital.
    - `protege.twin_zone_events`: eventos ideales ENTER/EXIT.
    - `protege.twin_permanence_intervals`: intervalos ideales por zona.
    - `protege.twin_daily_kpis`: indicadores diarios de Time on Tools.
    """
)

