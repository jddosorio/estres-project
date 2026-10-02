from pathlib import Path

import pandas as pd
import streamlit as st
import pydeck as pdk
import numpy as np
import plotly.graph_objects as go
from plotly.subplots import make_subplots


# -----------------------------------------------------------------------------
# Configuración
# -----------------------------------------------------------------------------

st.set_page_config(
    page_title="GPS | ESTRES",
    page_icon="📍",
    layout="wide",
)

DATA_FILE = Path("sample_data/betoneraGPS.csv")

LAT_COL = "latitude-1 => (Aggregate=TimeAverage2)"
LON_COL = "longitude-1 => (Aggregate=TimeAverage2)"
TIME_COL = "Timestamp"


# -----------------------------------------------------------------------------
# Carga de datos
# -----------------------------------------------------------------------------

@st.cache_data
def load_data():
    df = pd.read_csv(DATA_FILE)

    df[TIME_COL] = pd.to_datetime(df[TIME_COL])

    df[LAT_COL] = pd.to_numeric(df[LAT_COL], errors="coerce")
    df[LON_COL] = pd.to_numeric(df[LON_COL], errors="coerce")

    df = df.dropna(subset=[TIME_COL, LAT_COL, LON_COL])
    df = df.sort_values(TIME_COL).reset_index(drop=True)

    return df


df = load_data()


# -----------------------------------------------------------------------------
# Cálculo de distancia GPS
# -----------------------------------------------------------------------------

def haversine_distance(lat1, lon1, lat2, lon2):
    """Distancia entre dos coordenadas GPS en km."""

    R = 6371.0

    lat1 = np.radians(lat1)
    lon1 = np.radians(lon1)
    lat2 = np.radians(lat2)
    lon2 = np.radians(lon2)

    dlat = lat2 - lat1
    dlon = lon2 - lon1

    a = (
        np.sin(dlat / 2.0) ** 2
        + np.cos(lat1)
        * np.cos(lat2)
        * np.sin(dlon / 2.0) ** 2
    )

    c = 2 * np.arctan2(np.sqrt(a), np.sqrt(1 - a))

    return R * c


df["distance_km"] = 0.0

if len(df) > 1:
    df.loc[1:, "distance_km"] = haversine_distance(
        df[LAT_COL].iloc[:-1].values,
        df[LON_COL].iloc[:-1].values,
        df[LAT_COL].iloc[1:].values,
        df[LON_COL].iloc[1:].values,
    )

total_distance = df["distance_km"].sum()

start_time = df[TIME_COL].iloc[0]
end_time = df[TIME_COL].iloc[-1]
duration = end_time - start_time


# -----------------------------------------------------------------------------
# Título
# -----------------------------------------------------------------------------

st.title("📍 Posición GPS")

st.caption(
    "Proyecto CORFO 25IRA2-308620 — "
    "Validación del seguimiento geográfico del activo móvil"
)


# -----------------------------------------------------------------------------
# Descripción
# -----------------------------------------------------------------------------

st.subheader("Prueba de seguimiento GPS")

st.markdown(
    """
Durante la campaña experimental realizada con el camión betonera,
la posición geográfica del vehículo fue registrada durante su
desplazamiento hacia el sector **La Negra, Antofagasta**.

El sistema GPS permite asociar las mediciones estructurales obtenidas
por el sistema ESTRES con la posición geográfica del activo móvil.

La información fue registrada durante el desplazamiento del vehículo,
permitiendo reconstruir posteriormente su trayectoria.
"""
)


# -----------------------------------------------------------------------------
# KPIs
# -----------------------------------------------------------------------------

st.subheader("Resumen de la adquisición")

col1, col2, col3, col4 = st.columns(4)

col1.metric(
    "Fecha",
    start_time.strftime("%d-%m-%Y"),
)

col2.metric(
    "Inicio",
    start_time.strftime("%H:%M:%S"),
)

col3.metric(
    "Fin",
    end_time.strftime("%H:%M:%S"),
)

col4.metric(
    "Distancia GPS",
    f"{total_distance:.2f} km",
)


col1, col2, col3 = st.columns(3)

col1.metric(
    "Duración",
    f"{duration.total_seconds() / 60:.0f} min",
)

col2.metric(
    "Registros GPS",
    f"{len(df):,}",
)

sample_period = df[TIME_COL].diff().dt.total_seconds().median()

col3.metric(
    "Período de adquisición",
    f"{sample_period:.0f} s",
)


# -----------------------------------------------------------------------------
# Coordenadas
# -----------------------------------------------------------------------------

st.subheader("Coordenadas registradas")

start_lat = df[LAT_COL].iloc[0]
start_lon = df[LON_COL].iloc[0]

end_lat = df[LAT_COL].iloc[-1]
end_lon = df[LON_COL].iloc[-1]

col1, col2 = st.columns(2)

with col1:
    st.markdown("**Inicio del registro: COVIEFI**")
    st.write(f"Latitud: {start_lat:.6f}")
    st.write(f"Longitud: {start_lon:.6f}")

with col2:
    st.markdown("**Fin del registro: La Negra**")
    st.write(f"Latitud: {end_lat:.6f}")
    st.write(f"Longitud: {end_lon:.6f}")


# -----------------------------------------------------------------------------
# Mapa - Trayectoria GPS
# -----------------------------------------------------------------------------

st.subheader("Trayectoria del camión")

route = df[[LAT_COL, LON_COL, TIME_COL]].copy()

route = route.rename(
    columns={
        LAT_COL: "lat",
        LON_COL: "lon",
        TIME_COL: "timestamp",
    }
)

# Eliminar coordenadas inválidas
route = route.dropna(subset=["lat", "lon"])

# -------------------------------------------------------------------------
# Crear trayectoria
# -------------------------------------------------------------------------

route_points = route[["lon", "lat"]].values.tolist()

route_data = pd.DataFrame(
    {
        "path": [route_points],
    }
)

# Línea de trayectoria
route_layer = pdk.Layer(
    "PathLayer",
    route_data,
    get_path="path",
    get_color=[0, 120, 255],
    get_width=8,
    width_min_pixels=4,
    pickable=True,
)

# -------------------------------------------------------------------------
# Punto inicial y final
# -------------------------------------------------------------------------

start_point = pd.DataFrame(
    {
        "lat": [route.iloc[0]["lat"]],
        "lon": [route.iloc[0]["lon"]],
        "label": ["Inicio"],
    }
)

end_point = pd.DataFrame(
    {
        "lat": [route.iloc[-1]["lat"]],
        "lon": [route.iloc[-1]["lon"]],
        "label": ["Fin"],
    }
)

start_layer = pdk.Layer(
    "ScatterplotLayer",
    start_point,
    get_position="[lon, lat]",
    get_fill_color=[0, 180, 0],
    get_radius=80,
    radius_min_pixels=7,
    pickable=True,
)

end_layer = pdk.Layer(
    "ScatterplotLayer",
    end_point,
    get_position="[lon, lat]",
    get_fill_color=[220, 0, 0],
    get_radius=80,
    radius_min_pixels=7,
    pickable=True,
)

# -------------------------------------------------------------------------
# Centro y zoom automático
# -------------------------------------------------------------------------

center_lat = (route["lat"].min() + route["lat"].max()) / 2
center_lon = (route["lon"].min() + route["lon"].max()) / 2

lat_range = route["lat"].max() - route["lat"].min()
lon_range = route["lon"].max() - route["lon"].min()

max_range = max(lat_range, lon_range)

if max_range < 0.01:
    zoom = 14
elif max_range < 0.03:
    zoom = 13
elif max_range < 0.06:
    zoom = 12
elif max_range < 0.12:
    zoom = 11
elif max_range < 0.25:
    zoom = 10
else:
    zoom = 9

view_state = pdk.ViewState(
    latitude=center_lat,
    longitude=center_lon,
    zoom=zoom,
    pitch=0,
)

# -------------------------------------------------------------------------
# Mapa
# -------------------------------------------------------------------------

deck = pdk.Deck(
    map_style="https://basemaps.cartocdn.com/gl/voyager-gl-style/style.json",
    initial_view_state=view_state,
    layers=[
        route_layer,
        start_layer,
        end_layer,
    ],
    tooltip={
        "text": "{label}"
    },
)

st.pydeck_chart(
    deck,
    use_container_width=True,
)


# -----------------------------------------------------------------------------
# Registro GPS en el tiempo
# -----------------------------------------------------------------------------

st.subheader("Registro GPS en el tiempo")

plot_df = df[
    [
        TIME_COL,
        LAT_COL,
        LON_COL,
    ]
].copy()

plot_df = plot_df.rename(
    columns={
        TIME_COL: "Timestamp",
        LAT_COL: "Latitude",
        LON_COL: "Longitude",
    }
)

# Gráfico con doble eje Y
fig = make_subplots(
    specs=[[{"secondary_y": True}]]
)

# Latitud - eje izquierdo
fig.add_trace(
    go.Scatter(
        x=plot_df["Timestamp"],
        y=plot_df["Latitude"],
        name="Latitud",
        mode="lines",
    ),
    secondary_y=False,
)

# Longitud - eje derecho
fig.add_trace(
    go.Scatter(
        x=plot_df["Timestamp"],
        y=plot_df["Longitude"],
        name="Longitud",
        mode="lines",
    ),
    secondary_y=True,
)

fig.update_layout(
    height=430,
    margin=dict(l=20, r=20, t=20, b=20),
    hovermode="x unified",
    legend=dict(
        orientation="h",
        yanchor="bottom",
        y=1.02,
        xanchor="left",
        x=0,
    ),
)

# Eje X
fig.update_xaxes(
    title_text="Hora",
)

# Eje Y izquierdo
fig.update_yaxes(
    title_text="Latitud [°]",
    secondary_y=False,
)

# Eje Y derecho
fig.update_yaxes(
    title_text="Longitud [°]",
    secondary_y=True,
)

st.plotly_chart(
    fig,
    use_container_width=True,
)


# -----------------------------------------------------------------------------
# Datos
# -----------------------------------------------------------------------------

with st.expander("Ver datos GPS"):
    display_df = df[
        [
            TIME_COL,
            LAT_COL,
            LON_COL,
        ]
    ].copy()

    display_df.columns = [
        "Timestamp",
        "Latitude",
        "Longitude",
    ]

    st.dataframe(
        display_df,
        use_container_width=True,
        hide_index=True,
    )


# -----------------------------------------------------------------------------
# Validación
# -----------------------------------------------------------------------------

st.subheader("Validación funcional")

st.success(
    """
Durante la prueba se registraron 601 posiciones GPS durante un período
de 50 minutos. La trayectoria reconstruida a partir de las coordenadas
representa aproximadamente 18,2 km de desplazamiento.

Esta prueba permite verificar la capacidad del sistema para registrar
la posición geográfica del activo móvil y asociar información de
localización con los datos adquiridos por el sistema de monitoreo
estructural ESTRES.
"""
)


st.info(
    """
La incorporación de información GPS permite contextualizar espacialmente
los eventos estructurales registrados por el sistema, facilitando el
análisis posterior de las solicitaciones mecánicas en función de la
ubicación y condiciones de operación del equipo.
"""
)

st.success(
    """
Durante el trayecto desde Coviefi hacia el sector La Negra se atravesaron
varios sectores con pérdida o ausencia de cobertura celular. Durante estos
intervalos, el sistema mantuvo la adquisición de datos mediante el mecanismo
Store & Forward implementado en el Edge Computer.

Los datos fueron almacenados temporalmente en forma local mientras la
comunicación LTE no estaba disponible y, una vez recuperada la conectividad,
fueron retransmitidos automáticamente hacia el historiador remoto.

Este comportamiento permitió mantener la continuidad de los datos frente
a interrupciones de la red celular, demostrando la resiliencia de la
arquitectura de comunicaciones del sistema ESTRES.
"""
)