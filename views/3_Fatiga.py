"""Fatigue analysis for the ESTRES TRL-6 validation platform."""

from __future__ import annotations

from pathlib import Path

import pandas as pd
import plotly.graph_objects as go
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
# PLC S-N curve
# ---------------------------------------------------------------------------

SN_STRESS = [100, 150, 200, 250, 300]

SN_CYCLES = [
    10_000_000,
    1_000_000,
    100_000,
    10_000,
    1_000,
]


# ---------------------------------------------------------------------------
# Load experimental data
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

    missing = [
        column
        for column in required
        if column not in df.columns
    ]

    if missing:
        raise ValueError(
            "Columnas requeridas no encontradas: "
            + ", ".join(missing)
        )

    df["timestamp"] = pd.to_datetime(
        df["timestamp"],
        errors="coerce",
    )

    numeric_columns = [
        "stress",
        "stress_rate",
        "stress_range",
        "stress_rate_range",
        "micro_damage",
    ]

    for column in numeric_columns:
        df[column] = pd.to_numeric(
            df[column],
            errors="coerce",
        )

    df = df.dropna(subset=["timestamp"])

    return df.sort_values("timestamp").reset_index(drop=True)


# ---------------------------------------------------------------------------
# Header
# ---------------------------------------------------------------------------

st.title("Fatiga por Ciclos de Estrés")

st.caption(
    "Proyecto CORFO 25IRA2-308620 — "
    "Evaluación experimental del daño por fatiga"
)


# ---------------------------------------------------------------------------
# Load data
# ---------------------------------------------------------------------------

if not DATA_FILE.exists():
    st.error(
        f"No se encontró el archivo de datos: {DATA_FILE}"
    )
    st.stop()

try:
    df = load_data()

except Exception as error:
    st.error(
        "No fue posible cargar los datos experimentales."
    )
    st.exception(error)
    st.stop()


if df.empty:
    st.warning(
        "El archivo de datos no contiene registros."
    )
    st.stop()


# ---------------------------------------------------------------------------
# Purpose
# ---------------------------------------------------------------------------

with st.container(border=True):

    st.subheader("Propósito de esta página")

    st.markdown(
        """
        Esta página presenta la **curva S-N configurada en el PLC**
        para el procesamiento de los ciclos de estrés y el cálculo
        de **Micro Damage**.

        Cada ciclo detectado por el algoritmo proporciona un
        **Stress Range**. A partir de este valor, el PLC determina
        el número de ciclos correspondiente mediante la curva S-N
        y calcula la contribución de micro daño del evento.

        Para esta campaña experimental, de corta duración, el
        Micro Damage se agrupa **por minuto** para observar su
        evolución temporal.
        """
    )

    st.info(
        """
        En una aplicación industrial real, el indicador de daño
        acumulado se evaluará sobre períodos operacionales más
        largos, particularmente **por turno de operación**.
        """
    )


# ---------------------------------------------------------------------------
# S-N curve
# ---------------------------------------------------------------------------

st.subheader("Curva S-N configurada en el PLC")

col_chart, col_table = st.columns([2.2, 1])


with col_chart:

    fig_sn = go.Figure()

    fig_sn.add_trace(
        go.Scatter(
            x=SN_CYCLES,
            y=SN_STRESS,
            mode="lines+markers",
            name="Curva S-N PLC",
            marker=dict(size=9),
        )
    )

    fig_sn.update_layout(
        xaxis=dict(
            title="Número de ciclos N",
            type="log",
        ),
        yaxis=dict(
            title="Stress Range [MPa]",
        ),
        margin=dict(
            l=20,
            r=20,
            t=20,
            b=20,
        ),
        height=430,
    )

    st.plotly_chart(
        fig_sn,
        use_container_width=True,
    )


with col_table:

    st.markdown("#### Puntos configurados")

    sn_table = pd.DataFrame(
        {
            "Stress Range [MPa]": SN_STRESS,
            "Ciclos N": SN_CYCLES,
        }
    )

    st.dataframe(
        sn_table,
        use_container_width=True,
        hide_index=True,
    )

    st.markdown(
        """
        **Límites utilizados por el PLC**

        `Stress Range < 100 MPa`

        → **100.000.000 ciclos**

        `Stress Range > 300 MPa`

        → cálculo limitado a **300 MPa**
        """
    )


# ---------------------------------------------------------------------------
# Calculation principle
# ---------------------------------------------------------------------------

st.subheader("Cálculo de daño")

with st.container(border=True):

    st.markdown(
        """
        Para cada ciclo de estrés detectado:

        **Stress Range → Curva S-N → Número de ciclos N → Micro Damage**

        La contribución de daño implementada en el PLC se basa en:
        """
    )

    st.latex(
        r"D_{\mathrm{micro}} = \frac{1}{N} \times 10^{6}"
    )

    st.markdown(
        """
        donde **N** corresponde al número de ciclos determinado mediante
        la curva S-N para el **Stress Range** del evento.

        De esta forma, los eventos de mayor **Stress Range** generan una
        contribución de daño significativamente mayor.
        """
    )


# ---------------------------------------------------------------------------
# Experimental interval
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
    st.warning(
        "No existen registros en el intervalo seleccionado."
    )
    st.stop()


# ---------------------------------------------------------------------------
# Detected fatigue events
# ---------------------------------------------------------------------------

events = filtered[
    filtered["micro_damage"].fillna(0) > 0
].copy()


# ---------------------------------------------------------------------------
# Micro damage per minute
# ---------------------------------------------------------------------------

st.subheader("Micro daño acumulado por minuto")

st.markdown(
    """
    Para visualizar la evolución del daño durante esta campaña,
    las contribuciones individuales de **Micro Damage** se agrupan
    en intervalos de un minuto.
    """
)


if events.empty:

    st.info(
        "No existen eventos de Micro Damage en "
        "el intervalo seleccionado."
    )

else:

    damage_per_minute = (
        events
        .set_index("timestamp")["micro_damage"]
        .resample("1min")
        .sum()
        .fillna(0)
        .reset_index()
    )

    fig_damage = go.Figure()

    fig_damage.add_trace(
        go.Bar(
            x=damage_per_minute["timestamp"],
            y=damage_per_minute["micro_damage"],
            name="Micro Damage / min",
        )
    )

    fig_damage.update_layout(
        xaxis_title="Tiempo",
        yaxis_title="Micro Damage acumulado [µD]",
        margin=dict(
            l=20,
            r=20,
            t=20,
            b=20,
        ),
        height=430,
    )

    st.plotly_chart(
        fig_damage,
        use_container_width=True,
    )


# ---------------------------------------------------------------------------
# Summary
# ---------------------------------------------------------------------------

st.subheader("Resumen del intervalo")

if events.empty:

    total_damage = 0.0
    max_minute_damage = 0.0
    max_minute_time = None

else:

    total_damage = events["micro_damage"].sum()

    max_row = damage_per_minute.loc[
        damage_per_minute["micro_damage"].idxmax()
    ]

    max_minute_damage = max_row["micro_damage"]
    max_minute_time = max_row["timestamp"]


c1, c2, c3, c4 = st.columns(4)

c1.metric(
    "Eventos con daño",
    f"{len(events)}",
)

c2.metric(
    "Micro daño acumulado",
    f"{total_damage:.2f} µD",
)

c3.metric(
    "Máximo por minuto",
    f"{max_minute_damage:.2f} µD",
)

c4.metric(
    "Minuto de máximo",
    (
        max_minute_time.strftime("%H:%M")
        if max_minute_time is not None
        else "—"
    ),
)


# ---------------------------------------------------------------------------
# Stress Range vs Micro Damage
# ---------------------------------------------------------------------------

st.subheader("Stress Range y Micro Damage")

st.markdown(
    """
    La siguiente visualización permite observar la relación entre
    la magnitud de los ciclos detectados y la contribución de daño
    calculada por el PLC.
    """
)


if not events.empty:

    fig_relation = go.Figure()

    fig_relation.add_trace(
        go.Scatter(
            x=events["stress_range"],
            y=events["micro_damage"],
            mode="markers",
            name="Eventos",
            customdata=events["timestamp"],
            hovertemplate=(
                "Stress Range: %{x:.2f} MPa<br>"
                "Micro Damage: %{y:.4f} µD<br>"
                "Tiempo: %{customdata}<extra></extra>"
            ),
        )
    )

    fig_relation.update_layout(
        xaxis_title="Stress Range [MPa]",
        yaxis_title="Micro Damage [µD]",
        margin=dict(
            l=20,
            r=20,
            t=20,
            b=20,
        ),
        height=420,
    )

    st.plotly_chart(
        fig_relation,
        use_container_width=True,
    )


# ---------------------------------------------------------------------------
# Operational interpretation
# ---------------------------------------------------------------------------

st.subheader("Interpretación operacional")

with st.container(border=True):

    st.markdown(
        """
        La curva S-N transforma la magnitud de cada ciclo de estrés
        en una estimación de su contribución relativa al daño por
        fatiga.

        En consecuencia, no todos los ciclos tienen la misma
        importancia: un ciclo de mayor **Stress Range** puede
        producir una contribución de daño considerablemente mayor
        que múltiples ciclos de menor amplitud.

        Para esta prueba de corta duración, la agrupación por minuto
        permite identificar los períodos donde se concentra el daño.

        En la aplicación sobre equipos mineros, el mismo principio
        permitirá obtener indicadores como:

        - daño acumulado durante el turno;
        - daño por hora de operación;
        - comparación entre turnos;
        - identificación de períodos de alta solicitación;
        - evolución del daño acumulado del activo.
        """
    )


# ---------------------------------------------------------------------------
# TRL-6 evidence
# ---------------------------------------------------------------------------

st.subheader("Evidencia de validación")

st.success(
    """
    Los datos experimentales permiten verificar la cadena funcional:

    **Medición estructural → Stress → Stress Range → Ciclo de estrés
    → Curva S-N → Micro Damage**

    La presencia de eventos de Micro Damage en los registros del
    historiador demuestra que el procesamiento de fatiga se ejecutó
    durante la campaña experimental sobre el camión betonera.
    """
)