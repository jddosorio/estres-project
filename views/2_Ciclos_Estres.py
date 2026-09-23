"""Stress cycle analysis for the ESTRES TRL-6 validation platform."""

from __future__ import annotations

from pathlib import Path

import pandas as pd
import plotly.express as px
import streamlit as st


# ---------------------------------------------------------------------------
# Configuration
# ---------------------------------------------------------------------------

DATA_FILE = Path("sample_data/canaryBetonera-1.csv")

COLUMN_MAP = {
    "Timestamp": "timestamp",
    "stress-1 => (Aggregate=TimeAverage2)": "stress",
    "stressRate-1 => (Aggregate=TimeAverage2)": "stress_rate",
    "stressRange-1 => (Aggregate=TimeAverage2)": "stress_range",
    "stressRateRange-1 => (Aggregate=TimeAverage2)": "stress_rate_range",
    "microDamage-1 => (Aggregate=TimeAverage2)": "micro_damage",
}


# ---------------------------------------------------------------------------
# Data
# ---------------------------------------------------------------------------

@st.cache_data
def load_data() -> pd.DataFrame:
    df = pd.read_csv(DATA_FILE)

    df = df.rename(columns=COLUMN_MAP)

    required = [
        "timestamp",
        "stress",
        "stress_rate",
        "stress_range",
        "stress_rate_range",
        "micro_damage",
    ]

    missing = [column for column in required if column not in df.columns]

    if missing:
        raise ValueError(
            "Columnas requeridas no encontradas: "
            + ", ".join(missing)
        )

    df["timestamp"] = pd.to_datetime(df["timestamp"], errors="coerce")

    numeric_columns = [
        "stress",
        "stress_rate",
        "stress_range",
        "stress_rate_range",
        "micro_damage",
    ]

    for column in numeric_columns:
        df[column] = pd.to_numeric(df[column], errors="coerce")

    df = df.dropna(subset=["timestamp"])

    return df.sort_values("timestamp").reset_index(drop=True)


# ---------------------------------------------------------------------------
# Header
# ---------------------------------------------------------------------------

st.title("Ciclos de Estrés")

st.caption(
    "Proyecto CORFO 25IRA2-308620 — "
    "Análisis experimental de la respuesta estructural del camión betonera"
)


# ---------------------------------------------------------------------------
# Load CSV
# ---------------------------------------------------------------------------

if not DATA_FILE.exists():
    st.error(
        f"No se encontró el archivo de datos: {DATA_FILE}"
    )
    st.stop()

try:
    df = load_data()

except Exception as error:
    st.error("No fue posible cargar los datos experimentales.")
    st.exception(error)
    st.stop()


if df.empty:
    st.warning("El archivo de datos no contiene registros.")
    st.stop()


# ---------------------------------------------------------------------------
# Purpose
# ---------------------------------------------------------------------------

with st.container(border=True):

    st.subheader("Propósito de esta validación")

    st.markdown(
        """
        Esta página presenta las mediciones estructurales adquiridas durante
        la campaña experimental realizada sobre un **camión betonera**.

        El sensor ESR fue instalado sobre la estructura del vehículo y las
        variables fueron procesadas por el PLC y almacenadas posteriormente
        en el historiador Canary.

        Durante la prueba se operó el tambor de la betonera a diferentes
        velocidades y posteriormente se realizaron movimientos de avance y
        retroceso del vehículo.

        Debido a que esta primera campaña no dispone de marcas de tiempo
        independientes para cada maniobra, el análisis se realiza sobre la
        **respuesta dinámica global registrada durante la prueba**.
        """
    )


# ---------------------------------------------------------------------------
# Campaign information
# ---------------------------------------------------------------------------

st.subheader("Campaña experimental")

start_time = df["timestamp"].min()
end_time = df["timestamp"].max()
duration = end_time - start_time

c1, c2, c3, c4 = st.columns(4)

c1.metric(
    "Inicio",
    start_time.strftime("%H:%M:%S"),
)

c2.metric(
    "Término",
    end_time.strftime("%H:%M:%S"),
)

c3.metric(
    "Duración",
    f"{duration.total_seconds() / 60:.1f} min",
)

c4.metric(
    "Registros",
    f"{len(df):,}".replace(",", "."),
)


# ---------------------------------------------------------------------------
# Global indicators
# ---------------------------------------------------------------------------

st.subheader("Indicadores globales")

max_stress = df["stress"].max()
min_stress = df["stress"].min()
max_stress_rate = df["stress_rate"].abs().max()

events = df[
    (df["stress_range"].fillna(0).abs() > 0)
    | (df["micro_damage"].fillna(0).abs() > 0)
].copy()

k1, k2, k3, k4 = st.columns(4)

k1.metric(
    "Stress máximo",
    f"{max_stress:.2f} MPa",
)

k2.metric(
    "Stress mínimo",
    f"{min_stress:.2f} MPa",
)

k3.metric(
    "|Stress Rate| máximo",
    f"{max_stress_rate:.2f} MPa/s",
)

k4.metric(
    "Eventos detectados",
    f"{len(events):,}".replace(",", "."),
)


# ---------------------------------------------------------------------------
# Time selection
# ---------------------------------------------------------------------------

st.subheader("Intervalo de análisis")

min_ts = df["timestamp"].min().to_pydatetime()
max_ts = df["timestamp"].max().to_pydatetime()

selected_range = st.slider(
    "Seleccione el intervalo temporal",
    min_value=min_ts,
    max_value=max_ts,
    value=(min_ts, max_ts),
    format="HH:mm:ss",
)

filtered = df[
    (df["timestamp"] >= pd.Timestamp(selected_range[0]))
    & (df["timestamp"] <= pd.Timestamp(selected_range[1]))
].copy()


if filtered.empty:
    st.warning("No existen registros en el intervalo seleccionado.")
    st.stop()


# ---------------------------------------------------------------------------
# Stress
# ---------------------------------------------------------------------------

st.subheader("Stress")

stress_chart = px.line(
    filtered,
    x="timestamp",
    y="stress",
    labels={
        "timestamp": "Tiempo",
        "stress": "Stress [MPa]",
    },
)

stress_chart.update_layout(
    xaxis_title="Tiempo",
    yaxis_title="Stress [MPa]",
)

st.plotly_chart(
    stress_chart,
    use_container_width=True,
)


# ---------------------------------------------------------------------------
# Stress Rate
# ---------------------------------------------------------------------------

st.subheader("Stress Rate")

stress_rate_chart = px.line(
    filtered,
    x="timestamp",
    y="stress_rate",
    labels={
        "timestamp": "Tiempo",
        "stress_rate": "Stress Rate [MPa/s]",
    },
)

stress_rate_chart.update_layout(
    xaxis_title="Tiempo",
    yaxis_title="Stress Rate [MPa/s]",
)

st.plotly_chart(
    stress_rate_chart,
    use_container_width=True,
)


# ---------------------------------------------------------------------------
# Stress cycles
# ---------------------------------------------------------------------------

st.subheader("Ciclos de Estrés Detectados")

filtered_events = filtered[
    (filtered["stress_range"].fillna(0).abs() > 0)
    | (filtered["micro_damage"].fillna(0).abs() > 0)
].copy()


if filtered_events.empty:

    st.info(
        "No se detectaron eventos de Stress Range en "
        "el intervalo seleccionado."
    )

else:

    stress_range_chart = px.scatter(
        filtered_events,
        x="timestamp",
        y="stress_range",
        labels={
            "timestamp": "Tiempo",
            "stress_range": "Stress Range [MPa]",
        },
    )

    stress_range_chart.update_traces(
        marker={"size": 8}
    )

    stress_range_chart.update_layout(
        xaxis_title="Tiempo",
        yaxis_title="Stress Range [MPa]",
    )

    st.plotly_chart(
        stress_range_chart,
        use_container_width=True,
    )


# ---------------------------------------------------------------------------
# Interval statistics
# ---------------------------------------------------------------------------

st.subheader("Estadísticas del intervalo")

interval_events = len(filtered_events)

s1, s2, s3, s4 = st.columns(4)

s1.metric(
    "Stress máximo",
    f"{filtered['stress'].max():.2f} MPa",
)

s2.metric(
    "Stress mínimo",
    f"{filtered['stress'].min():.2f} MPa",
)

s3.metric(
    "Δ Stress",
    f"{filtered['stress'].max() - filtered['stress'].min():.2f} MPa",
)

s4.metric(
    "Eventos",
    str(interval_events),
)


s5, s6 = st.columns(2)

s5.metric(
    "Desviación estándar",
    f"{filtered['stress'].std():.2f} MPa",
)

s6.metric(
    "Stress Range máximo",
    (
        f"{filtered_events['stress_range'].abs().max():.2f} MPa"
        if not filtered_events.empty
        else "—"
    ),
)


# ---------------------------------------------------------------------------
# Event table
# ---------------------------------------------------------------------------

st.subheader("Eventos detectados")

if not filtered_events.empty:

    event_table = filtered_events[
        [
            "timestamp",
            "stress",
            "stress_rate",
            "stress_range",
            "stress_rate_range",
            "micro_damage",
        ]
    ].copy()

    event_table.columns = [
        "Timestamp",
        "Stress [MPa]",
        "Stress Rate [MPa/s]",
        "Stress Range [MPa]",
        "Stress Rate Range [MPa/s]",
        "Micro Damage",
    ]

    st.dataframe(
        event_table,
        use_container_width=True,
        hide_index=True,
    )

else:

    st.info(
        "No existen eventos en el intervalo seleccionado."
    )


# ---------------------------------------------------------------------------
# Download
# ---------------------------------------------------------------------------

st.subheader("Datos experimentales")

csv_data = filtered.to_csv(
    index=False
).encode("utf-8")

st.download_button(
    label="Descargar datos del intervalo",
    data=csv_data,
    file_name="estres_ciclos_estres.csv",
    mime="text/csv",
)


# ---------------------------------------------------------------------------
# Interpretation
# ---------------------------------------------------------------------------

st.subheader("Interpretación")

st.info(
    """
    Las mediciones muestran una respuesta estructural variable durante la
    campaña experimental y permiten identificar eventos caracterizados por
    un determinado **Stress Range**.

    Estos eventos constituyen la base para el análisis de ciclos de estrés
    y para el cálculo posterior de indicadores asociados a fatiga.

    En esta primera campaña no se asignan los peaks individuales a una
    maniobra específica debido a que no se dispone de un registro temporal
    independiente de cada operación realizada sobre el vehículo.

    Las próximas pruebas incorporarán marcas de tiempo para cada condición
    de ensayo, permitiendo correlacionar directamente las maniobras con la
    respuesta estructural registrada.
    """
)