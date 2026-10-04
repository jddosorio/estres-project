import streamlit as st


# -----------------------------------------------------------------------------
# Configuración
# -----------------------------------------------------------------------------

st.set_page_config(
    page_title="Resultados TRL-7 | ESTRES",
    page_icon="✅",
    layout="wide",
)


# -----------------------------------------------------------------------------
# Título
# -----------------------------------------------------------------------------

st.title("✅ Resultados y Validación TRL-7")

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

**Estado inicial del sistema ESTRES**

Al inicio del proyecto, los componentes principales utilizados en la
solución correspondían a **tecnologías industriales maduras,
comercialmente disponibles y con niveles de madurez equivalentes a
TRL-9 en sus respectivas aplicaciones**.

Entre ellos:

- sensor estructural HEIDENHAIN ESR;
- PLC industrial Siemens;
- gateway IBHLink UA;
- router industrial Teltonika;
- tecnologías Ethernet / PROFINET;
- OPC UA.

Por lo tanto, el nivel **TRL-4 no correspondía a la madurez individual
de estos componentes**, sino al nivel de madurez de **ESTRES como
sistema integrado**.

Al inicio del proyecto, la interconexión de estos elementos ya había
sido desarrollada a nivel de prototipo, pero aún faltaba demostrar
experimentalmente su operación conjunta sobre un activo móvil,
incluyendo procesamiento continuo, comunicaciones celulares,
almacenamiento remoto y recuperación de datos frente a pérdidas
temporales de conectividad.

En consecuencia, el punto de partida del proyecto se estableció en
**TRL-4 para el sistema ESTRES integrado**.
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
### TRL-7

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
un camión betonera como plataforma experimental, representando una
condición operacional real para un vehículo pesado.

La validación experimental demostró la operación integrada de la
cadena tecnológica extremo a extremo, incluyendo adquisición y
procesamiento de variables estructurales, comunicaciones celulares,
Edge Computing, posicionamiento GPS, historización remota y
visualización.

Adicionalmente, se validó la continuidad operacional de los datos
frente a interrupciones de comunicación mediante **Store & Forward**,
manteniendo la adquisición y almacenamiento local durante la pérdida
del enlace y recuperando automáticamente la transmisión una vez
restablecida la conectividad.

Estas evidencias permiten situar el sistema ESTRES en **TRL-7:
sistema integrado demostrado en condiciones operacionales
representativas**, habilitando su siguiente etapa de despliegue
comercial.
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

Esta funcionalidad fue además validada mediante una **interrupción controlada del enlace hacia el Historian**. Durante la pérdida de comunicación, el Edge mantuvo la adquisición y almacenó los datos localmente. Al restablecer el enlace, Store & Forward recuperó automáticamente la comunicación y transfirió al Historian los datos almacenados, sin pérdida observable de información.

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
un **prototipo de sistema demostrado en condiciones operacionales
representativas (TRL-7)** sobre un vehículo pesado de escala real.

La campaña permitió demostrar conjuntamente la adquisición de
deformaciones estructurales, procesamiento de variables asociadas a
ciclos de carga y fatiga, comunicaciones celulares, posicionamiento
GPS, almacenamiento Edge, mecanismo Store & Forward, historización
remota y visualización de la información.

En función de estas actividades y evidencias experimentales, el
proyecto presenta resultados consistentes con una maduración
tecnológica hasta **TRL-7**, sustentada por la demostración del sistema
integrado en condiciones operacionales representativas y por la
validación de la continuidad de datos mediante **Store & Forward**.

El resultado obtenido demuestra una arquitectura integrada y robusta,
capaz de mantener la adquisición de información estructural y preservar
la continuidad de los datos frente a interrupciones temporales de las
comunicaciones, habilitando la siguiente etapa de despliegue comercial.
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

st.subheader("Próxima etapa tecnológica — TRL-8")

st.info(
    """
### TRL-8 — Inicio del Despliegue Comercial

Alcanzado el nivel **TRL-7**, la siguiente etapa del sistema ESTRES
corresponde al **inicio de su despliegue comercial**, avanzando hacia
TRL-8.

Esta etapa considera iniciar implementaciones comerciales sobre
equipos mineros, configurando la solución de acuerdo con los
requerimientos operacionales de cada instalación.

La arquitectura Edge y la capacidad **Store & Forward** permiten
mantener la adquisición y continuidad de los datos durante
interrupciones temporales de las comunicaciones, facilitando el
despliegue de la solución en operaciones industriales distribuidas.

El despliegue comercial considera dos modalidades:

- **On-Premise:** suministro e instalación de la solución completa
  en la infraestructura del cliente, incluyendo sensores, Edge
  Computing, comunicaciones, Historian y herramientas de visualización.

- **Monitoring as a Service:** PULSO Tech instala y opera la
  infraestructura de monitoreo, entregando al cliente acceso a
  variables estructurales, tendencias, indicadores de fatiga y
  condición de sus activos mediante un servicio recurrente.

El objetivo de esta etapa es transformar el prototipo operacional
demostrado en **TRL-7** en una solución industrial reproducible,
calificada y comercialmente desplegable, iniciando su incorporación
en operaciones mineras.
"""
)