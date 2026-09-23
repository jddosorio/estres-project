from pathlib import Path

import streamlit as st
from PIL import Image


# -----------------------------------------------------------------------------
# Configuración
# -----------------------------------------------------------------------------

st.set_page_config(
    page_title="Pruebas Experimentales | ESTRES",
    page_icon="🧪",
    layout="wide",
)


# -----------------------------------------------------------------------------
# Archivos
# -----------------------------------------------------------------------------

IMAGE_SYSTEM = Path("images/estres-Betonera-1.jpeg")
IMAGE_SENSOR = Path("images/estres-Betonera-3.jpeg")
IMAGE_TREND = Path("images/canaryTrendBetonera.png")

VIDEO_MOVEMENT = "https://www.youtube.com/watch?v=OSTO4Nx_JSc"
VIDEO_SENSOR = "https://youtu.be/L9qCXps6sfA"


# -----------------------------------------------------------------------------
# Título
# -----------------------------------------------------------------------------

st.title("🧪 Pruebas Experimentales")

st.caption(
    "Proyecto CORFO 25IRA2-308620 — "
    "Validación experimental del sistema ESTRES"
)


# -----------------------------------------------------------------------------
# Objetivo
# -----------------------------------------------------------------------------

st.subheader("Campaña experimental — Camión betonera")

st.markdown(
    """
La campaña experimental tuvo como objetivo validar el funcionamiento
integrado del sistema **ESTRES** en un vehículo pesado de escala real,
utilizando un camión betonera como plataforma de prueba.

Un sensor de deformación estructural **ESR** fue instalado directamente
sobre el chasis del vehículo. Las deformaciones mecánicas registradas
por el sensor fueron adquiridas y procesadas por el sistema de control,
permitiendo obtener variables asociadas al comportamiento estructural
del chasis y a los ciclos de carga.

Durante la campaña se realizaron pruebas con la betonera en operación
y desplazamientos del vehículo, generando diferentes condiciones
dinámicas sobre la estructura.
"""
)


# -----------------------------------------------------------------------------
# Información de la prueba
# -----------------------------------------------------------------------------

st.subheader("Información de la prueba")

col1, col2, col3, col4 = st.columns(4)

col1.metric(
    "Fecha",
    "16-09-2026",
)

col2.metric(
    "Activo",
    "Camión betonera",
)

col3.metric(
    "Sensor",
    "ESR",
)

col4.metric(
    "Condición",
    "Dinámica",
)

st.markdown(
    """
**Condiciones consideradas durante la campaña:**

- Operación de la betonera a diferentes velocidades de rotación.
- Desplazamiento del camión hacia adelante y hacia atrás.
- Adquisición continua de la deformación estructural.
- Procesamiento de las variables de estrés y ciclos de carga.
- Registro de los datos en el historiador Canary.
"""
)


# -----------------------------------------------------------------------------
# Montaje experimental
# -----------------------------------------------------------------------------

st.subheader("Montaje experimental")

col_photo, col_text = st.columns([1, 1], gap="large")

# -------------------------------------------------------------------------
# Fotografía
# -------------------------------------------------------------------------

with col_photo:

    if IMAGE_SYSTEM.exists():

        image = Image.open(IMAGE_SYSTEM)

        # Girar 90° en sentido contrario
        image = image.rotate(-90, expand=True)

        # Imagen al ~70% del ancho de la columna
        _, img_col, _ = st.columns([0.7, 3, 0.7])

        with img_col:
            st.image(
                image,
                caption=(
                    "Sistema ESTRES instalado durante la campaña "
                    "experimental con el camión betonera."
                ),
                use_container_width=True,
            )


# -------------------------------------------------------------------------
# Descripción
# -------------------------------------------------------------------------

with col_text:

    st.markdown(
        """
El sistema electrónico de adquisición fue instalado temporalmente
junto al vehículo para realizar la campaña experimental.

La configuración utilizada permitió integrar:

- sensor de deformación estructural ESR;
- adquisición y procesamiento mediante PLC;
- comunicación industrial;
- Edge Computer;
- almacenamiento de datos;
- comunicaciones LTE;
- acceso remoto al sistema;
- registro de variables en Canary Historian.

Esta configuración permitió evaluar el sistema completo en una
condición dinámica utilizando un vehículo pesado real.
"""
    )

    st.markdown(
        """
El sistema electrónico de adquisición fue instalado temporalmente
junto al vehículo para realizar la campaña experimental.

La configuración utilizada permitió integrar:

- sensor de deformación estructural ESR;
- adquisición y procesamiento mediante PLC;
- comunicación industrial;
- Edge Computer;
- almacenamiento de datos;
- comunicaciones LTE;
- acceso remoto al sistema;
- registro de variables en Canary Historian.

Esta configuración permitió evaluar el sistema completo en una
condición dinámica utilizando un vehículo pesado real.
"""
    )


# -----------------------------------------------------------------------------
# Sensor ESR
# -----------------------------------------------------------------------------

st.subheader("Sensor ESR instalado en el chasis")

col_sensor, col_description = st.columns([1, 1], gap="large")

# -----------------------------------------------------------------------------
# Fotografía
# -----------------------------------------------------------------------------

with col_sensor:

    if IMAGE_SENSOR.exists():

        image = Image.open(IMAGE_SENSOR)

        # Girar 90° en sentido horario
        image = image.rotate(-90, expand=True)

        # Reducir el tamaño de la imagen dentro de la columna
        _, img_col, _ = st.columns([1, 3, 1])

        with img_col:
            st.image(
                image,
                caption=(
                    "Sensor ESR instalado directamente sobre "
                    "la estructura del chasis."
                ),
                use_container_width=True,
            )


# -----------------------------------------------------------------------------
# Descripción
# -----------------------------------------------------------------------------

with col_description:

    st.markdown(
        """
El sensor ESR fue instalado sobre un elemento estructural del chasis
del camión.

La instalación permite medir las pequeñas deformaciones longitudinales
producidas en la estructura como consecuencia de las solicitaciones
mecánicas experimentadas por el vehículo.

A partir de estas mediciones, el sistema ESTRES procesa las variables
utilizadas para identificar cambios de carga y eventos asociados a
ciclos de estrés.

La cadena de procesamiento utilizada durante la prueba fue:

**Deformación estructural**

→ **Stress**

→ **Stress Rate**

→ **Stress Range**

→ **Stress Rate Range**

→ **Micro Damage**
"""
    )


# -----------------------------------------------------------------------------
# Evidencia audiovisual
# -----------------------------------------------------------------------------

st.subheader("Evidencia audiovisual")

col_video1, col_video2 = st.columns(2, gap="large")

with col_video1:

    st.markdown("#### Medición con el camión en movimiento")

    st.video(VIDEO_MOVEMENT)

    st.caption(
        "Medición de deformaciones estructurales durante "
        "el movimiento del camión betonera."
    )

with col_video2:

    st.markdown("#### Sensor instalado en el chasis")

    st.video(VIDEO_SENSOR)

    st.caption(
        "Vista del sensor ESR instalado sobre el chasis "
        "del camión betonera."
    )


# -----------------------------------------------------------------------------
# Variables registradas
# -----------------------------------------------------------------------------

st.subheader("Variables registradas")

st.markdown(
    """
Durante la campaña experimental se registraron en el historiador
las principales variables generadas por el sistema de procesamiento:
"""
)

col1, col2, col3, col4, col5 = st.columns(5)

col1.metric("Stress", "MPa")
col2.metric("Stress Rate", "MPa/s")
col3.metric("Stress Range", "MPa")
col4.metric("Stress Rate Range", "MPa/s")
col5.metric("Micro Damage", "µD")


# -----------------------------------------------------------------------------
# Evidencia Canary
# -----------------------------------------------------------------------------

st.subheader("Registro de la respuesta estructural en el Historiador Canary")

if IMAGE_TREND.exists():

    st.image(
        str(IMAGE_TREND),
        caption=(
            "Registro de las variables estructurales durante "
            "la campaña experimental del 16 de septiembre de 2026."
        ),
        use_container_width=True,
    )

st.markdown(
    """
La tendencia registrada permite observar la respuesta dinámica del
chasis durante las diferentes condiciones experimentales.

Los cambios en **Stress** y **Stress Rate** representan variaciones
de la respuesta estructural medida por el sensor. El algoritmo de
procesamiento identifica variaciones de carga y genera las variables
**Stress Range** y **Stress Rate Range**.

A partir de los ciclos identificados se calcula adicionalmente la
variable **Micro Damage**, utilizada posteriormente para el análisis
de daño acumulativo por fatiga.
"""
)


# -----------------------------------------------------------------------------
# Observaciones
# -----------------------------------------------------------------------------

st.subheader("Observaciones de la campaña")

st.info(
    """
Durante esta primera campaña no se registró una marca temporal
independiente para cada maniobra realizada sobre el vehículo.

Por esta razón, los eventos observados en las tendencias permiten
demostrar la respuesta dinámica del sistema, pero no se asignan
individualmente a una velocidad específica de la betonera o a una
maniobra particular de avance o retroceso.

Las próximas campañas incorporarán un registro temporal de cada
condición experimental para permitir una correlación directa entre
la maniobra realizada y la respuesta estructural medida.
"""
)


# -----------------------------------------------------------------------------
# Validación
# -----------------------------------------------------------------------------

st.subheader("Resultado de la prueba")

st.success(
    """
La campaña permitió verificar experimentalmente la capacidad del
sistema ESTRES para adquirir deformaciones estructurales en un
vehículo pesado de escala real, procesar las mediciones y generar
variables relacionadas con estrés, ciclos de carga y micro-daño.

Asimismo, se verificó la integración entre el sensor ESR, el sistema
de adquisición y procesamiento y el historiador de datos utilizado
para registrar las variables durante la prueba.

Los resultados obtenidos constituyen evidencia experimental de la
operación integrada del prototipo en una condición dinámica relevante
para la validación TRL-6.
"""
)


# -----------------------------------------------------------------------------
# Próximas pruebas
# -----------------------------------------------------------------------------

st.subheader("Próximas pruebas experimentales")

st.markdown(
    """
Para complementar la validación se considera realizar nuevas campañas
con condiciones de operación controladas y marcas temporales para
cada ensayo:

1. **Betonera detenida** — adquisición de línea base.
2. **Rotación velocidad 1** — registro durante un intervalo definido.
3. **Rotación velocidad 2** — registro durante un intervalo definido.
4. **Rotación velocidad 3** — registro durante un intervalo definido.
5. **Desplazamiento del vehículo** — avance y retroceso controlados.
6. **Betonera cargada** — medición de la respuesta estructural con carga.
7. **Proceso de descarga** — seguimiento de la variación estructural
   durante la descarga del material.

Estas pruebas permitirán correlacionar directamente cada condición de
operación con la respuesta estructural registrada por el sistema ESTRES.
"""
)