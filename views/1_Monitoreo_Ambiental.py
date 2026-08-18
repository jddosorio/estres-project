"""Local Streamlit dashboard for PROTEGE environmental measurements."""

from __future__ import annotations

import pandas as pd
import plotly.express as px
import streamlit as st

from src.clickhouse_client import configured_database
from src.queries import (
    connection_info,
    describe_table,
    list_tables,
    preview_table,
    read_environment_data,
)


st.title("PROTEGE - Monitoreo Ambiental")
st.caption("Dashboard en la nube conectado mediante HTTPS a ClickHouse Cloud")

with st.container(height=280, border=True):
    st.subheader("Propósito de esta validación")

    st.markdown(
        """
        Esta página forma parte del procedimiento de maduración tecnológica
        de **PROTEGE desde TRL-4 a TRL-5**. Su propósito es demostrar, en un
        ambiente controlado, la capacidad de la infraestructura para adquirir
        mediciones desde un **sensor real de temperatura y humedad**, transmitirlas
        periódicamente mediante la red **NB-IoT/LTE de Entel**, almacenarlas en
        **ClickHouse Cloud** y visualizarlas remotamente mediante un dashboard
        desplegado en **Streamlit Community Cloud**.

        El sistema genera un registro aproximadamente **cada minuto**, permitiendo
        verificar la operación extremo a extremo de la cadena tecnológica:

        **Sensor ambiental → controlador LTE (gateway) → red NB-IoT/LTE →
        HTTPS/TLS → ClickHouse Cloud → dashboard Streamlit Cloud**

        **Aspectos verificados en esta prueba:**

        - Adquisición de datos desde un sensor físico.
        - Generación periódica de registros ambientales.
        - Comunicación entre el gateway LTE y la infraestructura en la nube.
        - Recepción y almacenamiento en ClickHouse Cloud.
        - Consulta remota y visualización de las mediciones.
        - Disponibilidad del dashboard para validación por terceros.

        Esta prueba valida la infraestructura de adquisición, comunicación,
        almacenamiento y visualización de PROTEGE. La estimación de
        **Time on Tools** y la permanencia por zonas se validan separadamente
        mediante el **Gemelo Digital PROTEGE** y las pruebas con scanners y
        tags BLE.
        """
    )

def find_first(columns: list[str], candidates: tuple[str, ...]) -> str | None:
    lower_to_original = {column.lower(): column for column in columns}
    for candidate in candidates:
        if candidate in lower_to_original:
            return lower_to_original[candidate]
    return None


try:
    info = connection_info().iloc[0]
    st.success(
        f"Conectado a ClickHouse {info['version']} como {info['user']} "
        f"— hora del servidor: {info['server_time']}"
    )
except Exception as error:
    st.error("No fue posible conectarse a ClickHouse Cloud.")
    st.exception(error)
    st.info(
        "Copia `.streamlit/secrets.toml.example` como "
        "`.streamlit/secrets.toml` y completa la contraseña."
    )
    st.stop()

try:
    tables = list_tables()
except Exception as error:
    st.error(f"No fue posible listar las tablas de `{configured_database()}`.")
    st.exception(error)
    st.stop()

if not tables:
    st.warning(f"La base de datos `{configured_database()}` no contiene tablas visibles.")
    st.stop()

st.sidebar.header("Datos")
default_table = "environmental_telemetry"

default_index = tables.index(default_table) if default_table in tables else 0

selected_table = st.sidebar.selectbox(
    "Tabla",
    options=tables,
    index=default_index,
)
row_limit = st.sidebar.select_slider(
    "Máximo de registros",
    options=[100, 500, 1000, 5000, 10000, 50000],
    value=5000,
)
hours = st.sidebar.selectbox(
    "Período",
    options=[1, 6, 12, 24, 72, 168, 720],
    index=3,
    format_func=lambda value: f"{value} horas",
)

schema = describe_table(selected_table)
columns = schema["name"].astype(str).tolist()

x_column = find_first(
    columns,
    ("timestamp", "event_time", "received_at", "created_at", "datetime", "ts", "time"),
)
is_time_axis = x_column is not None
if x_column is None:
    x_column = find_first(columns, ("uptime_ms", "sequence", "seq", "id"))

temperature_column = find_first(
    columns,
    ("temperature_mdeg_c", "temperature", "temperature_c", "temp_c", "temp"),
)
humidity_column = find_first(
    columns,
    ("humidity_milli_pct", "humidity", "humidity_pct", "relative_humidity", "rh"),
)

dashboard_tab, data_tab, schema_tab = st.tabs(
    ["Dashboard", "Datos", "Estructura de tabla"]
)

with dashboard_tab:
    if x_column and temperature_column and humidity_column:
        try:
            data = read_environment_data(
                table=selected_table,
                x_column=x_column,
                temperature_column=temperature_column,
                humidity_column=humidity_column,
                hours=hours,
                limit=row_limit,
                use_time_filter=is_time_axis,
            )
        except Exception as error:
            st.error("La consulta ambiental no pudo ejecutarse.")
            st.exception(error)
        else:
            if data.empty:
                st.warning("La consulta no devolvió registros para el período seleccionado.")
            else:
                latest = data.iloc[-1]
                col1, col2, col3 = st.columns(3)
                col1.metric("Temperatura", f"{latest['temperature_c']:.2f} °C")
                col2.metric("Humedad", f"{latest['humidity_pct']:.2f} %")
                col3.metric("Registros", f"{len(data):,}")

                temperature_chart = px.line(
                    data,
                    x="x_value",
                    y="temperature_c",
                    title="Temperatura",
                    labels={"x_value": x_column, "temperature_c": "Temperatura (°C)"},
                )
                humidity_chart = px.line(
                    data,
                    x="x_value",
                    y="humidity_pct",
                    title="Humedad relativa",
                    labels={"x_value": x_column, "humidity_pct": "Humedad (%)"},
                )
                st.plotly_chart(temperature_chart, use_container_width=True)
                st.plotly_chart(humidity_chart, use_container_width=True)
    else:
        missing = []
        if not x_column:
            missing.append("tiempo, uptime o secuencia")
        if not temperature_column:
            missing.append("temperatura")
        if not humidity_column:
            missing.append("humedad")
        st.info(
            "No fue posible construir automáticamente el gráfico. "
            f"Faltan columnas reconocibles de: {', '.join(missing)}."
        )
        st.write("Columnas encontradas:", columns)

with data_tab:
    try:
        preview = preview_table(selected_table, min(row_limit, 5000))
        st.dataframe(preview, use_container_width=True, hide_index=True)
        st.download_button(
            "Descargar vista como CSV",
            data=preview.to_csv(index=False).encode("utf-8"),
            file_name=f"{selected_table}_preview.csv",
            mime="text/csv",
        )
    except Exception as error:
        st.exception(error)

with schema_tab:
    st.code(f"{configured_database()}.{selected_table}")
    st.dataframe(schema, use_container_width=True, hide_index=True)
