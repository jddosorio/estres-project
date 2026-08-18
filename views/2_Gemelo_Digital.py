"""PROTEGE Digital Twin dashboard for Time on Tools validation."""

from __future__ import annotations

from datetime import date

import clickhouse_connect
import pandas as pd
import plotly.express as px
import streamlit as st


TWIN_DATABASE = "protege"


@st.cache_resource
def get_client():
    config = st.secrets["clickhouse"]
    return clickhouse_connect.get_client(
        host=config["host"],
        port=int(config.get("port", 8443)),
        username=config["username"],
        password=config["password"],
        database=config.get("database", "default"),
        secure=True,
    )


@st.cache_data(ttl=300, show_spinner=False)
def query_df(sql: str, parameters: dict | None = None) -> pd.DataFrame:
    return get_client().query_df(sql, parameters=parameters or {})


def format_hours(seconds: float | int) -> str:
    return f"{float(seconds) / 3600:,.1f} h"


def where_clause(worker_id: str | None, table_alias: str = "") -> tuple[str, dict]:
    prefix = f"{table_alias}." if table_alias else ""
    clause = f"""
        {prefix}run_id = toUUID({{run_id:String}})
        AND {prefix}shift_date BETWEEN toDate({{start_date:String}})
                                  AND toDate({{end_date:String}})
    """
    parameters = {
        "run_id": selected_run_id,
        "start_date": selected_dates[0].isoformat(),
        "end_date": selected_dates[1].isoformat(),
    }
    if worker_id:
        clause += f" AND {prefix}worker_id = {{worker_id:String}}"
        parameters["worker_id"] = worker_id
    return clause, parameters


st.title("PROTEGE — Gemelo Digital Time on Tools")
st.caption("Validación de la arquitectura de datos y de los KPI para la maduración TRL-4 → TRL-5")

with st.container(height=250, border=True):
    st.subheader("Propósito de esta validación")
    st.markdown(
        """
        Esta página presenta el **Gemelo Digital ideal de PROTEGE**, construido
        para validar la arquitectura de datos, las reglas de permanencia y los
        indicadores de **Time on Tools** antes de ejecutar la validación con
        scanners y tags BLE en terreno.

        El modelo simula seis meses de operación de una faena, con jornadas de
        **9 horas de permanencia**, **36 minutos de colación** y **42 horas
        laborales semanales**. Para cada trabajador se conoce exactamente la
        zona, la hora de entrada y salida y la duración de cada actividad.

        Estos datos constituyen el **ground truth** o referencia ideal. En una
        etapa posterior, los intervalos inferidos a partir del RSSI serán
        comparados con esta referencia para cuantificar exactitud, cobertura,
        error de permanencia y salidas forzadas. Por lo tanto, este dashboard
        valida el procesamiento y la visualización de KPI; no representa todavía
        mediciones BLE obtenidas en una faena real.
        """
    )

try:
    runs = query_df(
        f"""
        SELECT
            toString(run_id) AS run_id,
            model_name,
            algorithm_version,
            seed,
            start_date,
            calendar_days,
            workers,
            simulated_shifts,
            presence_minutes_per_shift,
            lunch_minutes_per_shift,
            labor_minutes_per_shift,
            timezone,
            created_at
        FROM {TWIN_DATABASE}.twin_runs FINAL
        ORDER BY created_at DESC
        """
    )
except Exception as error:
    st.error("No fue posible consultar las tablas del Gemelo Digital en ClickHouse Cloud.")
    st.exception(error)
    st.stop()

if runs.empty:
    st.warning("No existen ejecuciones cargadas en `protege.twin_runs`.")
    st.stop()

st.sidebar.header("Gemelo Digital")
run_labels = {
    row.run_id: f"{row.start_date} · {row.workers} trabajadores · {row.run_id[:8]}"
    for row in runs.itertuples()
}
selected_run_id = st.sidebar.selectbox(
    "Ejecución",
    options=runs["run_id"].tolist(),
    format_func=lambda value: run_labels[value],
)

bounds = query_df(
    f"""
    SELECT min(shift_date) AS min_date, max(shift_date) AS max_date
    FROM {TWIN_DATABASE}.twin_daily_kpis
    WHERE run_id = toUUID({{run_id:String}})
    """,
    {"run_id": selected_run_id},
).iloc[0]

min_date = pd.Timestamp(bounds["min_date"]).date()
max_date = pd.Timestamp(bounds["max_date"]).date()
selected_dates = st.sidebar.date_input(
    "Período",
    value=(min_date, max_date),
    min_value=min_date,
    max_value=max_date,
)

if not isinstance(selected_dates, (tuple, list)) or len(selected_dates) != 2:
    st.info("Selecciona una fecha inicial y una fecha final.")
    st.stop()

workers = query_df(
    f"""
    SELECT DISTINCT worker_id
    FROM {TWIN_DATABASE}.twin_daily_kpis
    WHERE run_id = toUUID({{run_id:String}})
    ORDER BY worker_id
    """,
    {"run_id": selected_run_id},
)["worker_id"].astype(str).tolist()

worker_option = st.sidebar.selectbox("Trabajador", ["Todos"] + workers)
selected_worker = None if worker_option == "Todos" else worker_option
where, params = where_clause(selected_worker)

selected_run = runs.loc[runs["run_id"] == selected_run_id].iloc[0]
st.success(
    f"Ejecución {selected_run_id[:8]} · semilla {int(selected_run['seed'])} · "
    f"{int(selected_run['workers'])} trabajadores · "
    f"{int(selected_run['simulated_shifts']):,} jornadas simuladas"
)

summary = query_df(
    f"""
    SELECT
        count() AS worker_days,
        countDistinct(worker_id) AS workers,
        sum(presence_seconds) AS presence_seconds,
        sum(labor_seconds) AS labor_seconds,
        sum(break_seconds) AS break_seconds,
        sum(productive_seconds) AS productive_seconds,
        sum(labor_seconds - productive_seconds) AS non_productive_seconds,
        sum(non_productive_planned_seconds) AS planned_seconds,
        sum(non_productive_inferred_seconds) AS inferred_seconds,
        sum(support_seconds) AS support_seconds,
        sum(undefined_seconds) AS undefined_seconds,
        round(100 * sum(productive_seconds) / nullIf(sum(labor_seconds), 0), 2)
            AS time_on_tools_labor_pct
    FROM {TWIN_DATABASE}.twin_daily_kpis
    WHERE {where}
    """,
    params,
).iloc[0]

metric_1, metric_2, metric_3, metric_4, metric_5 = st.columns(5)
metric_1.metric("Time on Tools", f"{float(summary['time_on_tools_labor_pct']):.2f} %")
metric_2.metric("Tiempo productivo", format_hours(summary["productive_seconds"]))
metric_3.metric("Tiempo no productivo", format_hours(summary["non_productive_seconds"]))
metric_4.metric("Permanencia", format_hours(summary["presence_seconds"]))
metric_5.metric("Jornadas", f"{int(summary['worker_days']):,}")

overview_tab, zones_tab, workers_tab, validation_tab = st.tabs(
    ["Resumen", "Permanencia por zona", "Trabajadores", "Validación"]
)

with overview_tab:
    daily = query_df(
        f"""
        SELECT
            shift_date,
            round(sum(productive_seconds) / 3600, 2) AS productive_hours,
            round(sum(labor_seconds - productive_seconds) / 3600, 2)
                AS non_productive_hours,
            round(100 * sum(productive_seconds) / nullIf(sum(labor_seconds), 0), 2)
                AS time_on_tools_pct
        FROM {TWIN_DATABASE}.twin_daily_kpis
        WHERE {where}
        GROUP BY shift_date
        ORDER BY shift_date
        """,
        params,
    )

    category_data = pd.DataFrame(
        {
            "Categoría": [
                "Productivo",
                "No productivo planificado",
                "Herramientas / espera inferida",
                "Soporte",
                "Indefinido",
                "Colación",
            ],
            "Horas": [
                float(summary["productive_seconds"]) / 3600,
                float(summary["planned_seconds"]) / 3600,
                float(summary["inferred_seconds"]) / 3600,
                float(summary["support_seconds"]) / 3600,
                float(summary["undefined_seconds"]) / 3600,
                float(summary["break_seconds"]) / 3600,
            ],
        }
    )

    chart_col_1, chart_col_2 = st.columns((1.6, 1))
    with chart_col_1:
        daily_long = daily.melt(
            id_vars=["shift_date", "time_on_tools_pct"],
            value_vars=["productive_hours", "non_productive_hours"],
            var_name="Tipo",
            value_name="Horas",
        )
        daily_long["Tipo"] = daily_long["Tipo"].map(
            {
                "productive_hours": "Productivo",
                "non_productive_hours": "No productivo",
            }
        )
        daily_chart = px.bar(
            daily_long,
            x="shift_date",
            y="Horas",
            color="Tipo",
            title="Horas laborales por día",
            color_discrete_map={"Productivo": "#009688", "No productivo": "#F59E0B"},
        )
        st.plotly_chart(daily_chart, use_container_width=True)

    with chart_col_2:
        category_chart = px.pie(
            category_data,
            names="Categoría",
            values="Horas",
            hole=0.48,
            title="Distribución del tiempo",
        )
        st.plotly_chart(category_chart, use_container_width=True)

    tot_chart = px.line(
        daily,
        x="shift_date",
        y="time_on_tools_pct",
        title="Evolución diaria de Time on Tools",
        labels={"shift_date": "Fecha", "time_on_tools_pct": "Time on Tools (%)"},
    )
    tot_chart.update_yaxes(range=[0, 100])
    st.plotly_chart(tot_chart, use_container_width=True)

with zones_tab:
    zone_where, zone_params = where_clause(selected_worker, table_alias="i")
    zone_data = query_df(
        f"""
        SELECT
            i.zone_id,
            any(z.zone_name) AS zone_name,
            any(i.productivity_class) AS productivity_class,
            round(sum(i.duration_seconds) / 3600, 2) AS hours,
            count() AS visits
        FROM {TWIN_DATABASE}.twin_permanence_intervals AS i
        LEFT JOIN
        (
            SELECT zone_id, argMax(zone_name, updated_at) AS zone_name
            FROM {TWIN_DATABASE}.zones
            GROUP BY zone_id
        ) AS z ON i.zone_id = z.zone_id
        WHERE {zone_where}
        GROUP BY i.zone_id
        ORDER BY hours DESC
        """,
        zone_params,
    )
    zone_data["Zona"] = zone_data["zone_id"] + " — " + zone_data["zone_name"]
    zone_chart = px.bar(
        zone_data,
        x="hours",
        y="Zona",
        color="productivity_class",
        orientation="h",
        title="Permanencia acumulada por zona",
        labels={"hours": "Horas", "productivity_class": "Clasificación"},
    )
    zone_chart.update_layout(yaxis={"categoryorder": "total ascending"})
    st.plotly_chart(zone_chart, use_container_width=True)
    st.dataframe(
        zone_data[["zone_id", "zone_name", "productivity_class", "hours", "visits"]],
        use_container_width=True,
        hide_index=True,
    )

with workers_tab:
    worker_data = query_df(
        f"""
        SELECT
            worker_id,
            count() AS simulated_days,
            round(sum(productive_seconds) / 3600, 2) AS productive_hours,
            round(sum(labor_seconds - productive_seconds) / 3600, 2)
                AS non_productive_hours,
            round(100 * sum(productive_seconds) / nullIf(sum(labor_seconds), 0), 2)
                AS time_on_tools_pct
        FROM {TWIN_DATABASE}.twin_daily_kpis
        WHERE {where}
        GROUP BY worker_id
        ORDER BY time_on_tools_pct DESC
        """,
        params,
    )
    worker_chart = px.bar(
        worker_data.sort_values("time_on_tools_pct"),
        x="time_on_tools_pct",
        y="worker_id",
        orientation="h",
        title="Time on Tools por trabajador",
        labels={"time_on_tools_pct": "Time on Tools (%)", "worker_id": "Trabajador"},
        color="time_on_tools_pct",
        color_continuous_scale="Teal",
    )
    worker_chart.update_xaxes(range=[0, 100])
    st.plotly_chart(worker_chart, use_container_width=True)
    st.dataframe(worker_data, use_container_width=True, hide_index=True)

with validation_tab:
    weekly = query_df(
        f"""
        SELECT
            toMonday(shift_date) AS week_start,
            round(sum(labor_seconds) / countDistinct(worker_id) / 3600, 2)
                AS average_labor_hours,
            round(sum(presence_seconds) / countDistinct(worker_id) / 3600, 2)
                AS average_presence_hours,
            countDistinct(worker_id) AS workers
        FROM {TWIN_DATABASE}.twin_daily_kpis
        WHERE {where}
        GROUP BY week_start
        ORDER BY week_start
        """,
        params,
    )
    audit = query_df(
        f"""
        SELECT
            countIf(event_type = 'ENTER') AS enter_events,
            countIf(event_type = 'EXIT') AS exit_events,
            enter_events - exit_events AS event_balance
        FROM {TWIN_DATABASE}.twin_zone_events
        WHERE {where}
        """,
        params,
    ).iloc[0]

    valid_days = query_df(
        f"""
        SELECT
            countIf(
                presence_seconds != 32400
                OR labor_seconds != 30240
                OR break_seconds != 2160
            ) AS invalid_worker_days
        FROM {TWIN_DATABASE}.twin_daily_kpis
        WHERE {where}
        """,
        params,
    ).iloc[0]

    check_1, check_2, check_3 = st.columns(3)
    check_1.metric("Balance ENTER − EXIT", f"{int(audit['event_balance']):,}")
    check_2.metric("Jornadas con horario inválido", f"{int(valid_days['invalid_worker_days']):,}")
    check_3.metric("Horas laborales semanales", "42.0 h")

    if int(audit["event_balance"]) == 0 and int(valid_days["invalid_worker_days"]) == 0:
        st.success("La ejecución mantiene transiciones balanceadas y jornadas consistentes.")
    else:
        st.warning("La ejecución contiene observaciones que deben revisarse.")

    weekly_chart = px.line(
        weekly,
        x="week_start",
        y="average_labor_hours",
        markers=True,
        title="Validación de 42 horas laborales semanales",
        labels={"week_start": "Semana", "average_labor_hours": "Horas por trabajador"},
    )
    weekly_chart.add_hline(
        y=42,
        line_dash="dash",
        line_color="#D97706",
        annotation_text="Objetivo: 42 h",
    )
    st.plotly_chart(weekly_chart, use_container_width=True)
    st.dataframe(weekly, use_container_width=True, hide_index=True)
