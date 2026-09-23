import streamlit as st


# -----------------------------------------------------------------------------
# Configuración
# -----------------------------------------------------------------------------

st.set_page_config(
    page_title="Resultados TRL-6 | ESTRES",
    page_icon="✅",
    layout="wide",
)


# -----------------------------------------------------------------------------
# Título
# -----------------------------------------------------------------------------

st.title("✅ Resultados y Validación TRL-6")

st.caption(
    "Proyecto CORFO 25IRA2-308620 — "
    "Tecnologías de Industria 4.0 para el Monitoreo Estructural "
    "de Equipos Mineros de Alta Criticidad"
)


# -----------------------------------------------------------------------------
# Evolución de madurez tecnológica
# -----------------------------------------------------------------------------

st.subheader("Evolución de la madurez tecnológica")

col1, col2, col3 = st.columns([1, 0.35, 1])

with col1:
    st.markdown(
        """
### TRL-4

**Estado inicial del proyecto**

Antes de la ejecución del proyecto CORFO Innova Región,
los principales componentes utilizados en la solución correspondían
a tecnologías industriales maduras y comercialmente disponibles.

Entre ellos:

- sensor estructural HEIDENHAIN ESR;
- PLC industrial Siemens;
- gateway IBHLink UA;
- router industrial Teltonika;
- tecnologías Ethernet / PROFINET;
- OPC UA.

Sin embargo, la **solución ESTRES como sistema integrado** se
encontraba en un nivel de madurez **TRL-4**.

La integración completa de estos elementos, particularmente para
su utilización sobre un activo móvil y con comunicaciones celulares,
aún debía ser desarrollada y validada experimentalmente.
"""
    )

with col2:
    st.markdown(
        """
<br><br><br><br><br>

# ➜

<br>

### CORFO

**INNOVA REGIÓN**
""",
        unsafe_allow_html=True,
    )

with col3:
    st.markdown(
        """
### TRL-6

**Resultado del proyecto**

La ejecución del proyecto permitió implementar y validar
experimentalmente un prototipo integrado del sistema ESTRES
sobre un vehículo pesado de escala real.

La solución integra:

- medición de deformación estructural;
- procesamiento industrial;
- detección de ciclos de estrés;
- análisis de micro-daño;
- Edge Computing;
- comunicaciones LTE;
- Store & Forward;
- GPS;
- historización remota;
- visualización y acceso remoto.

La integración fue sometida a condiciones dinámicas utilizando
un camión betonera como plataforma experimental.
"""
    )


st.divider()


# -----------------------------------------------------------------------------
# Desafío tecnológico
# -----------------------------------------------------------------------------

st.subheader("Desafío tecnológico inicial")

st.markdown(
    """
El principal desafío del proyecto no correspondía al desarrollo
individual de los equipos utilizados. Los sensores, PLC, gateways y
routers corresponden a tecnologías industriales maduras.

El desafío tecnológico estaba en **integrar estos componentes en una
arquitectura capaz de operar sobre un activo móvil**, adquirir y
procesar continuamente información estructural y transmitir los datos
hacia una infraestructura remota utilizando comunicaciones celulares.

Esta condición es particularmente relevante para aplicaciones mineras,
donde la cobertura celular puede presentar interrupciones durante el
desplazamiento de los equipos.

Por esta razón, uno de los principales aspectos que debía validarse era
la capacidad de la arquitectura para mantener la continuidad de los
datos frente a pérdidas temporales de comunicación.
"""
)


# -----------------------------------------------------------------------------
# Resultados principales
# -----------------------------------------------------------------------------

st.subheader("Principales resultados alcanzados")


# Resultado 1
with st.container(border=True):

    st.markdown("### 1. Integración completa del sistema ESTRES")

    st.markdown(
        """
Se desarrolló e integró la arquitectura completa de adquisición,
procesamiento y transmisión de datos estructurales.

La solución permitió interconectar el sensor ESR, gateway EnDat/PROFINET,
PLC Siemens, gateway OPC UA, Edge Computer y sistema de comunicaciones.

Se implementó además la transmisión de información mediante una
red celular utilizando un router industrial Teltonika, permitiendo
conectar el sistema instalado en el activo móvil con la infraestructura
remota de almacenamiento y supervisión.
"""
    )


# Resultado 2
with st.container(border=True):

    st.markdown("### 2. Store & Forward para continuidad de datos")

    st.markdown(
        """
Se implementó un mecanismo **Store & Forward** en el Edge Computer
para mantener la continuidad de los datos durante interrupciones de
las comunicaciones.

Cuando la conexión celular no está disponible, los datos continúan
siendo adquiridos y son almacenados temporalmente en el sistema Edge.

Una vez recuperada la conectividad, la información pendiente es
retransmitida hacia el historiador remoto.

Esta funcionalidad es especialmente relevante para aplicaciones
mineras en la Región de Antofagasta, donde los activos móviles pueden
transitar por sectores con cobertura celular limitada o intermitente.
"""
    )


# Resultado 3
with st.container(border=True):

    st.markdown("### 3. Protección de la propiedad intelectual")

    st.markdown(
        """
Durante el desarrollo del proyecto se presentó una solicitud de
**Patente de Invención** asociada a la tecnología de monitoreo
estructural.

**Solicitud:** 2025-02836

**Título:**  
*Sistema de monitoreo de deformaciones estructurales mediante
sensores digitales*

La solicitud se encuentra actualmente en **etapa resolutiva** ante
INAPI.

Este resultado complementa el desarrollo tecnológico mediante una
estrategia formal de protección de la propiedad intelectual generada
en torno a la solución.
"""
    )


# Resultado 4
with st.container(border=True):

    st.markdown("### 4. Validación experimental en un vehículo pesado")

    st.markdown(
        """
El sistema integrado fue instalado y probado sobre el chasis de un
**camión betonera**, utilizando un sensor ESR para medir la deformación
estructural durante condiciones dinámicas.

Durante la campaña experimental se realizaron pruebas con la betonera
en operación y desplazamientos del vehículo.

El sistema adquirió y procesó las mediciones estructurales, generando
variables tales como:

- Stress;
- Stress Rate;
- Stress Range;
- Stress Rate Range;
- Micro Damage.

Las variables fueron registradas en el historiador Canary, permitiendo
verificar la operación integrada de la cadena de medición y
procesamiento.
"""
    )


# Resultado 5
with st.container(border=True):

    st.markdown("### 5. Seguimiento GPS, transmisión e historización remota")

    st.markdown(
        """
Se validó el registro de la posición GPS del activo durante su
desplazamiento, permitiendo asociar la información estructural con
la ubicación geográfica del vehículo.

Durante la prueba de desplazamiento entre el sector Coviefi y
La Negra, Antofagasta, el sistema operó utilizando comunicaciones
celulares y acceso remoto.

La arquitectura permitió integrar:

- posición GPS;
- transmisión LTE;
- acceso mediante VPN;
- Edge Computing;
- Store & Forward;
- Canary Historian;
- visualización remota.

Durante sectores con pérdida de cobertura celular, el mecanismo
Store & Forward permitió mantener localmente los datos y retransmitirlos
cuando se recuperó la conectividad.
"""
    )


# -----------------------------------------------------------------------------
# Resultado global
# -----------------------------------------------------------------------------

st.subheader("Resultado global del proyecto")

st.success(
    """
La ejecución del proyecto CORFO Innova Región permitió evolucionar
desde una solución integrada a nivel de laboratorio (TRL-4) hacia
un prototipo funcional validado experimentalmente sobre un vehículo
pesado de escala real.

La campaña permitió demostrar conjuntamente la adquisición de
deformaciones estructurales, procesamiento de variables asociadas a
ciclos de carga y fatiga, comunicaciones celulares, posicionamiento
GPS, almacenamiento Edge, mecanismo Store & Forward, historización
remota y visualización de la información.

En función de estas actividades y evidencias experimentales, el
proyecto presenta resultados consistentes con el objetivo de
maduración tecnológica hasta **TRL-6**.
"""
)


# -----------------------------------------------------------------------------
# Resumen
# -----------------------------------------------------------------------------

st.subheader("Resumen de resultados")

results = [
    {
        "Resultado": "Integración del sistema",
        "Estado": "Validado",
        "Evidencia": "Sistema ESTRES integrado",
    },
    {
        "Resultado": "Medición estructural",
        "Estado": "Validado",
        "Evidencia": "Sensor ESR en camión betonera",
    },
    {
        "Resultado": "Procesamiento de ciclos",
        "Estado": "Validado",
        "Evidencia": "Stress / Stress Range / Micro Damage",
    },
    {
        "Resultado": "Comunicación celular",
        "Estado": "Validado",
        "Evidencia": "Router industrial LTE",
    },
    {
        "Resultado": "Store & Forward",
        "Estado": "Validado",
        "Evidencia": "Recuperación ante pérdida de conectividad",
    },
    {
        "Resultado": "Posicionamiento GPS",
        "Estado": "Validado",
        "Evidencia": "Trayectoria Antofagasta - La Negra",
    },
    {
        "Resultado": "Historización remota",
        "Estado": "Validado",
        "Evidencia": "Canary Historian",
    },
    {
        "Resultado": "Propiedad intelectual",
        "Estado": "En etapa resolutiva",
        "Evidencia": "Solicitud INAPI 2025-02836",
    },
]

st.dataframe(
    results,
    use_container_width=True,
    hide_index=True,
)


# -----------------------------------------------------------------------------
# Próxima etapa
# -----------------------------------------------------------------------------

st.subheader("Próxima etapa tecnológica")

st.info(
    """
El siguiente paso en la maduración de la tecnología corresponde a
realizar una demostración del sistema ESTRES instalado sobre un
equipo minero CAEX operando en una faena minera.

Esta etapa permitirá evaluar la solución bajo las condiciones reales
de operación, carga, vibración, desplazamiento y comunicaciones
propias del ambiente minero, avanzando hacia una validación de mayor
madurez tecnológica.
"""
)