from pathlib import Path

import numpy as np
import pandas as pd
import streamlit as st


# -----------------------------------------------------------------------------
# Configuración
# -----------------------------------------------------------------------------
st.set_page_config(
    page_title="Pruebas Experimentales #2 | ESTRES",
    page_icon="🧪",
    layout="wide",
)

STRESS_FILE_CANDIDATES = [
    Path("sample_data/canaryBetonera-3.csv"),
    Path("canaryBetonera-3.csv"),
]
GPS_FILE_CANDIDATES = [
    Path("sample_data/betoneraGPS-2.csv"),
    Path("betoneraGPS-3.csv"),
]


def first_existing(candidates):
    return next((path for path in candidates if path.exists()), None)


def haversine_steps(lat, lon):
    """Distancia entre posiciones consecutivas, en metros."""
    lat = np.radians(np.asarray(lat, dtype=float))
    lon = np.radians(np.asarray(lon, dtype=float))
    dlat = np.diff(lat)
    dlon = np.diff(lon)
    a = (
        np.sin(dlat / 2.0) ** 2
        + np.cos(lat[:-1]) * np.cos(lat[1:]) * np.sin(dlon / 2.0) ** 2
    )
    return 6_371_000.0 * 2.0 * np.arcsin(np.sqrt(a))


def load_data(stress_path, gps_path):
    stress = pd.read_csv(stress_path)
    gps = pd.read_csv(gps_path)

    stress = stress.rename(
        columns={
            stress.columns[0]: "Timestamp",
            stress.columns[1]: "Stress",
            stress.columns[2]: "Stress Rate",
            stress.columns[3]: "Stress Range",
            stress.columns[4]: "Stress Rate Range",
            stress.columns[5]: "Micro Damage",
        }
    )
    gps = gps.rename(
        columns={
            gps.columns[0]: "Timestamp",
            gps.columns[1]: "latitude",
            gps.columns[2]: "longitude",
        }
    )

    stress["Timestamp"] = pd.to_datetime(stress["Timestamp"], errors="coerce")
    gps["Timestamp"] = pd.to_datetime(gps["Timestamp"], errors="coerce")
    stress = stress.dropna(subset=["Timestamp"]).sort_values("Timestamp")
    gps = gps.dropna(subset=["Timestamp", "latitude", "longitude"]).sort_values("Timestamp")

    # Los dos archivos están muestreados a 1 s. Se correlacionan por timestamp.
    merged = pd.merge(stress, gps, on="Timestamp", how="inner")
    return stress, gps, merged


# -----------------------------------------------------------------------------
# Título
# -----------------------------------------------------------------------------
st.title("🧪 Pruebas Experimentales #2")
st.caption(
    "Proyecto CORFO 25IRA2-308620 — Campaña con carga y correlación "
    "entre respuesta estructural y posición GPS"
)


# -----------------------------------------------------------------------------
# Objetivo y condiciones de la campaña
# -----------------------------------------------------------------------------
st.subheader("Campaña experimental — Betonera cargada en tránsito")

st.markdown(
    """
Esta segunda campaña experimental tuvo como objetivo evaluar el sistema
**ESTRES** durante el desplazamiento real de un camión betonera cargado,
correlacionando la respuesta estructural medida en el chasis con la posición
geográfica del vehículo.

El trayecto se realizó **desde el sector Huascar hasta calle Azufre**, en
Antofagasta. Durante la prueba, el camión transportó aproximadamente
**14 toneladas de concreto**. Considerando una masa aproximada de
**25 toneladas para la betonera**, la masa total movilizada durante el ensayo
fue del orden de **39 toneladas**.

El sensor ESR permaneció instalado sobre el chasis y el sistema registró en
forma simultánea las variables de estrés estructural y la posición GPS. Esto
permite identificar espacialmente los eventos de carga detectados durante el
recorrido.
"""
)

col1, col2, col3, col4 = st.columns(4)
col1.metric("Fecha", "02-10-2026")
col2.metric("Concreto transportado", "14 t")
col3.metric("Masa betonera", "25 t")
col4.metric("Masa total aprox.", "39 t")

st.info(
    "Trayecto experimental: Huascar → calle Azufre, Antofagasta. "
    "La campaña combina medición estructural ESR y posicionamiento GPS a 1 s."
)


# -----------------------------------------------------------------------------
# Configuración experimental
# -----------------------------------------------------------------------------
st.subheader("Configuración experimental")

st.markdown(
    """
La campaña se realizó utilizando la arquitectura completa del sistema **ESTRES**,
desde la medición estructural en el vehículo hasta el almacenamiento remoto de
los datos.

1. **Sensor ESR:** instalado directamente sobre el chasis del camión betonera
   para medir la respuesta estructural durante el desplazamiento.

2. **Camión betonera cargado:** el ensayo se realizó con aproximadamente
   **14 toneladas de concreto**, sobre un vehículo de aproximadamente **25
   toneladas**, alcanzando una masa total del orden de **39 toneladas**.

3. **Sistema electrónico a bordo:** la caja electrónica de adquisición,
   procesamiento y comunicaciones fue instalada en la cabina del camión
   betonera.

4. **Historiador remoto:** los datos fueron transmitidos y almacenados en un
   **Canary Historian Server**, ejecutándose remotamente en un computador
   ubicado en las oficinas de **PULSO SpA**.

5. **Recorrido experimental:** el camión realizó un trayecto desde el sector
   **Huascar hasta calle Azufre, Antofagasta**, registrándose simultáneamente
   las variables estructurales y la posición GPS durante el recorrido.
"""
)

st.info(
    "La prueba permitió validar la cadena completa de medición: "
    "Sensor ESR → adquisición y procesamiento a bordo → comunicación remota → "
    "Canary Historian Server, manteniendo además la correlación temporal con GPS."
)


# -----------------------------------------------------------------------------
# Carga de datos
# -----------------------------------------------------------------------------
st.subheader("Datos registrados")

stress_file = first_existing(STRESS_FILE_CANDIDATES)
gps_file = first_existing(GPS_FILE_CANDIDATES)

if stress_file is None or gps_file is None:
    st.warning(
        "No se encontraron los archivos de la campaña. Copie `Export.csv` y "
        "`Export-2.csv` en la carpeta `sample_data/` del proyecto (o junto a la app)."
    )
    st.stop()

stress, gps, data = load_data(stress_file, gps_file)

if data.empty:
    st.error("No existen timestamps comunes entre los datos de estrés y GPS.")
    st.stop()

steps = haversine_steps(gps["latitude"], gps["longitude"])
distance_km = steps.sum() / 1000.0
elapsed_min = (data["Timestamp"].max() - data["Timestamp"].min()).total_seconds() / 60.0

m1, m2, m3, m4, m5 = st.columns(5)
m1.metric("Muestras correlacionadas", f"{len(data):,}".replace(",", "."))
m2.metric("Intervalo común", f"{elapsed_min:.1f} min")
m3.metric("Recorrido GPS", f"{distance_km:.1f} km")
m4.metric("Stress máximo", f"{data['Stress'].max():.2f} MPa")
m5.metric("Stress Range máximo", f"{data['Stress Range'].max():.2f} MPa")

st.caption(
    f"Ventana correlacionada: {data['Timestamp'].min():%H:%M:%S} – "
    f"{data['Timestamp'].max():%H:%M:%S}. "
    "La distancia se calcula a partir de las posiciones GPS consecutivas."
)


# -----------------------------------------------------------------------------
# Respuesta estructural en el tiempo
# -----------------------------------------------------------------------------
st.subheader("Respuesta estructural durante el trayecto")

import plotly.graph_objects as go

fig = go.Figure()

fig.add_trace(
    go.Scatter(
        x=data["Timestamp"],
        y=data["Stress"],
        mode="lines",
        name="Stress",
        hovertemplate=(
            "<b>Stress</b><br>"
            "Tiempo: %{x|%H:%M:%S}<br>"
            "Valor: %{y:.2f} MPa"
            "<extra></extra>"
        ),
    )
)

fig.add_trace(
    go.Scatter(
        x=data["Timestamp"],
        y=data["Stress Range"],
        mode="lines",
        name="Stress Range",
        hovertemplate=(
            "<b>Stress Range</b><br>"
            "Tiempo: %{x|%H:%M:%S}<br>"
            "Valor: %{y:.2f} MPa"
            "<extra></extra>"
        ),
    )
)

fig.update_layout(
    height=360,
    xaxis_title="Tiempo",
    yaxis_title="Stress [MPa]",
    hovermode="x unified",
    margin=dict(l=20, r=20, t=20, b=20),
)

st.plotly_chart(
    fig,
    use_container_width=True,
    config={
        "displayModeBar": True,
        "scrollZoom": False,
        "doubleClick": False,
        "staticPlot": False,
        "modeBarButtonsToRemove": [
            "toImage",
            "select2d",
            "lasso2d",
        ],
    },
)

st.markdown(
    """
La señal **Stress** representa la respuesta estructural instantánea obtenida a
partir de la deformación medida por el ESR. La variable **Stress Range**
identifica la amplitud de los ciclos detectados por el algoritmo y permite
separar eventos estructurales relevantes de las variaciones normales de la
señal durante el desplazamiento.
"""
)


# -----------------------------------------------------------------------------
# Trayectoria GPS
# -----------------------------------------------------------------------------
st.subheader("Trayectoria GPS de la betonera")

route = data[["latitude", "longitude"]].drop_duplicates()
st.map(route, latitude="latitude", longitude="longitude", height=500)

st.caption(
    "Posiciones GPS registradas durante la ventana en que existen datos "
    "simultáneos de estrés y posición."
)


# -----------------------------------------------------------------------------
# Eventos estructurales georreferenciados
# -----------------------------------------------------------------------------
st.subheader("Eventos estructurales georreferenciados")

# Un Stress Range distinto de cero corresponde a un evento/ciclo entregado
# por el procesamiento. Se muestran los de mayor amplitud.
events = data[data["Stress Range"] > 0].copy()
events = events.sort_values("Stress Range", ascending=False)

top_n = min(20, len(events))
top_events = events.head(top_n).copy()

if not top_events.empty:
    e1, e2, e3, e4 = st.columns(4)

    e1.metric(
        "Ciclos de estrés detectados",
        f"{len(events):,}".replace(",", ".")
    )

    e2.metric(
        "Ciclos con Micro Damage > 0",
        f"{(data['Micro Damage'] > 0).sum():,}".replace(",", ".")
    )

    e3.metric(
        "Micro Damage acumulado",
        f"{data['Micro Damage'].sum():.2f} µD"
    )

    e4.metric(
        "Máx. Stress Rate Range",
        f"{data['Stress Rate Range'].max():.2f} MPa/s"
    )

    #st.markdown("#### Ubicación de los eventos de mayor Stress Range")
    #st.map(top_events[["latitude", "longitude"]], latitude="latitude", longitude="longitude", height=450)
    st.markdown("#### Ubicación de los eventos de mayor Stress Range")

    map_events = top_events.copy()

    map_events["Hora"] = map_events["Timestamp"].dt.strftime("%H:%M:%S")

    fig_events = go.Figure()

    fig_events.add_trace(
        go.Scattermap(
            lat=map_events["latitude"],
            lon=map_events["longitude"],
            mode="markers",
            marker=dict(
                size=9,
            ),
            customdata=map_events[
                [
                    "Hora",
                    "Stress",
                    "Stress Range",
                    "Stress Rate Range",
                ]
            ],
            hovertemplate=(
                "<b>Evento estructural</b><br>"
                "Hora: %{customdata[0]}<br>"
                "Stress: %{customdata[1]:.2f} MPa<br>"
                "Stress Range: %{customdata[2]:.2f} MPa<br>"
                "Stress Rate Range: %{customdata[3]:.2f} MPa/s"
                "<extra></extra>"
            ),
            name="Eventos",
        )
    )

    fig_events.update_layout(
        map=dict(
            style="carto-positron",
            center=dict(
                lat=map_events["latitude"].mean(),
                lon=map_events["longitude"].mean(),
            ),
            zoom=10,
        ),
        height=450,
        margin=dict(l=0, r=0, t=0, b=0),
        showlegend=False,
    )

    st.plotly_chart(
        fig_events,
        use_container_width=True,
        config={
            "displayModeBar": True,
            "scrollZoom": True,
        },
    )

    table = top_events[
        [
            "Timestamp",
            "Stress",
            "Stress Range",
            "Stress Rate Range",
            "Micro Damage",
            "latitude",
            "longitude",
        ]
    ].copy()
    table["Timestamp"] = table["Timestamp"].dt.strftime("%H:%M:%S")
    table = table.rename(
        columns={
            "Timestamp": "Hora",
            "latitude": "Latitud",
            "longitude": "Longitud",
        }
    )
    st.dataframe(table, use_container_width=True, hide_index=True)

    max_event = top_events.iloc[0]
    st.success(
        "Mayor evento registrado en la ventana correlacionada: "
        f"Stress Range = {max_event['Stress Range']:.2f} MPa a las "
        f"{max_event['Timestamp']:%H:%M:%S}, en "
        f"({max_event['latitude']:.6f}, {max_event['longitude']:.6f})."
    )
else:
    st.info("No se detectaron valores de Stress Range mayores que cero.")

st.caption(
    "*El valor mostrado corresponde a la suma de la variable Micro Damage "
    "registrada durante la ventana analizada; su interpretación acumulativa "
    "debe mantenerse consistente con el algoritmo ESTRES utilizado."
)


# -----------------------------------------------------------------------------
# Análisis espacial continuo
# -----------------------------------------------------------------------------
st.subheader("Correlación entre posición y solicitación estructural")

st.markdown(
    """
La incorporación de GPS permite transformar la campaña desde una prueba
puramente temporal a una prueba **espacio-temporal**. Cada muestra de estrés
puede asociarse a una posición del vehículo y, por lo tanto, los ciclos de
mayor amplitud pueden ser revisados posteriormente respecto del sector del
trayecto donde ocurrieron.

Esta información es especialmente relevante para la aplicación futura en
vehículos mineros, donde permitirá relacionar solicitaciones estructurales con
**rampas, curvas, irregularidades del camino, zonas de carga y descarga** u
otras condiciones operacionales repetitivas.
"""
)


# -----------------------------------------------------------------------------
# Resultado de la campaña
# -----------------------------------------------------------------------------
st.subheader("Resultado de la prueba")

st.success(
    """
La campaña permitió registrar simultáneamente la respuesta estructural del
chasis y la posición del camión betonera durante un desplazamiento real con
carga. El ensayo se realizó con aproximadamente **14 t de concreto**, sobre un
vehículo de aproximadamente **25 t**, representando una condición de operación
del orden de **39 t de masa total**.

Los datos demuestran que el sistema ESTRES puede adquirir y procesar las
variables estructurales durante el tránsito y asociar los eventos detectados a
coordenadas geográficas. Esta capacidad constituye un avance respecto de la
campaña experimental inicial, al incorporar una condición real con carga y la
correlación espacial de los eventos estructurales.
"""
)


# -----------------------------------------------------------------------------
# Análisis de resultados
# -----------------------------------------------------------------------------
st.subheader("Análisis de resultados")

st.markdown(
    """
El registro obtenido durante la campaña permite identificar claramente
diferentes condiciones de **demanda estructural** del camión betonera.

Durante el **trayecto con carga**, la señal de Stress presenta variaciones
asociadas a las condiciones dinámicas de circulación. Se observan eventos
transitorios de mayor demanda estructural, principalmente asociados a cambios
en la dinámica del vehículo, tales como **frenadas y otras maniobras**, los
cuales se manifiestan también como incrementos de **Stress Rate [MPa/s]**.

La condición de mayor **demanda estructural sostenida** se observa durante la
**descarga del cemento**, aproximadamente entre las **12:42 y 12:54**.
Durante este período, el Stress se mantiene en un nivel significativamente
superior al observado durante gran parte del recorrido, alcanzando un valor
medio aproximado de **35 MPa**.

Este comportamiento indica que la descarga constituye una condición operacional
estructuralmente relevante. A diferencia de los peaks transitorios observados
durante el desplazamiento, durante la descarga se presenta una demanda
estructural elevada y sostenida durante varios minutos.

En conjunto, la prueba permitió distinguir dos tipos principales de demanda:

- **demanda estructural transitoria**, asociada principalmente a la dinámica
  del vehículo durante el recorrido;
- **demanda estructural sostenida**, observada principalmente durante la
  operación de descarga del cemento.
"""
)

st.success(
    """
    **Conclusión de la prueba**

    La campaña con el camión betonera cargado permitió validar la capacidad
    del sistema ESTRES para registrar la respuesta estructural del vehículo
    durante condiciones reales de operación y diferenciar distintos niveles
    y tipos de demanda estructural.

    Los resultados muestran que la mayor **demanda estructural sostenida**
    se produjo durante la descarga del cemento, mientras que durante el
    desplazamiento se identificaron eventos transitorios asociados a la
    dinámica del vehículo.

    La medición simultánea de **Stress, Stress Range, Stress Rate y GPS**
    permite caracterizar la magnitud, duración, instante y ubicación de los
    eventos estructurales, proporcionando una base experimental para el
    análisis de fatiga y daño acumulado.
    """
)
