"""Store & Forward and Edge Computer architecture for ESTRES."""

from __future__ import annotations

import streamlit as st


# -----------------------------------------------------------------------------
# Header
# -----------------------------------------------------------------------------

st.title("Store & Forward")

st.caption(
    "Proyecto CORFO 25IRA2-308620 — "
    "Edge Computing y continuidad de datos"
)


# -----------------------------------------------------------------------------
# Description
# -----------------------------------------------------------------------------

with st.container(border=True):

    st.subheader("Edge Computer")

    st.markdown(
        """
        El sistema ESTRES utiliza un **Siemens SIMATIC Box PC** como
        computador Edge instalado junto al sistema de adquisición.

        El equipo ejecuta **Ubuntu Server 26.04.1 LTS**, configurado como
        servidor industrial **sin interfaz gráfica (GUI)**.

        Esta configuración reduce los recursos requeridos por el sistema
        operativo y permite que la administración del equipo, Docker y los
        servicios Canary se realice de forma remota.

        El Edge Computer constituye el enlace entre la adquisición de datos
        del sistema de control y el Canary Historian remoto.
        """
    )


# -----------------------------------------------------------------------------
# Hardware / OS
# -----------------------------------------------------------------------------

st.subheader("Plataforma Edge")

col_hw, col_os = st.columns(2, gap="large")

with col_hw:

    with st.container(border=True):

        st.markdown("### 🖥️ Hardware")

        st.markdown(
            """
            **Siemens SIMATIC Box PC**

            Computador industrial utilizado como plataforma Edge del
            prototipo ESTRES.

            Sus funciones principales son:

            - adquisición de variables desde el sistema de control;
            - ejecución de servicios Canary;
            - almacenamiento temporal de datos;
            - Store & Forward;
            - comunicación con el Historian remoto;
            - administración remota.
            """
        )


with col_os:

    with st.container(border=True):

        st.markdown("### 🐧 Sistema Operativo")

        st.markdown(
            """
            **Ubuntu Server 26.04.1 LTS**

            Instalación orientada a servidor:

            - sin interfaz gráfica;
            - operación mediante línea de comandos;
            - administración remota;
            - Docker Engine;
            - Docker Compose;
            - servicios Canary ejecutados en contenedores.
            """
        )


# -----------------------------------------------------------------------------
# Docker architecture
# -----------------------------------------------------------------------------

st.subheader("Arquitectura Docker")

st.markdown(
    """
    Los componentes Canary utilizados por ESTRES se ejecutan como
    **contenedores Docker** sobre Ubuntu Server.

    Esta arquitectura permite aislar los distintos servicios, simplificar
    su administración y mantener persistencia local de los datos requeridos
    por Store & Forward.
    """
)

col1, col2 = st.columns(2, gap="large")


with col1:

    with st.container(border=True):

        st.markdown("### Canary OPC Collector")

        st.markdown(
            """
            Contenedor encargado de adquirir mediante **OPC UA** las
            variables estructurales disponibles desde el sistema de control.

            Entre las variables adquiridas se encuentran:

            - Stress
            - Stress Rate
            - Stress Range
            - Stress Rate Range
            - Micro Damage
            """
        )


    with st.container(border=True):

        st.markdown("### Canary MQTT Collector")

        st.markdown(
            """
            Servicio disponible para la adquisición de información
            publicada mediante **MQTT**.

            Permite integrar al sistema Edge fuentes de datos basadas en
            eventos o dispositivos que utilicen este protocolo.
            """
        )


    with st.container(border=True):

        st.markdown("### Canary Store & Forward")

        st.markdown(
            """
            Componente responsable de mantener la continuidad de los datos
            cuando el enlace con el Historian remoto no está disponible.

            Los datos pendientes permanecen almacenados localmente y son
            transmitidos cuando se recupera la comunicación.
            """
        )


with col2:

    with st.container(border=True):

        st.markdown("### Canary Administrator")

        st.markdown(
            """
            Servicio utilizado para la configuración y administración
            remota de los componentes Canary ejecutados en el Edge Computer.

            **Puerto:** `55273`
            """
        )


    with st.container(border=True):

        st.markdown("### Canary Identity")

        st.markdown(
            """
            Servicio de identidad utilizado por la infraestructura Canary
            para autenticación y acceso a los servicios asociados.

            **Puerto:** `55353`
            """
        )


    with st.container(border=True):

        st.markdown("### Persistencia local")

        st.markdown(
            """
            Docker mantiene un volumen persistente para los datos Canary.

            De esta forma, la información necesaria para la operación Edge
            no depende únicamente de la memoria de los contenedores.
            """
        )


# -----------------------------------------------------------------------------
# Data flow
# -----------------------------------------------------------------------------

st.subheader("Flujo de datos")

with st.container(border=True):

    st.markdown(
        """
        **PLC Siemens**

        ↓ `OPC UA`

        **IBHLink UA**

        ↓ `OPC UA`

        **Canary OPC Collector**

        ↓

        **Canary Store & Forward**

        ↓ `Ethernet`

        **Teltonika RUT200**

        ↓ `LTE`

        **Internet / RMS VPN**

        ↓

        **Canary Historian Remoto**
        """
    )


# -----------------------------------------------------------------------------
# Store & Forward principle
# -----------------------------------------------------------------------------

st.subheader("Operación Store & Forward")

st.markdown(
    """
    La conectividad celular utilizada por un equipo móvil puede presentar
    interrupciones temporales. El mecanismo **Store & Forward** evita que
    estas interrupciones impliquen necesariamente la pérdida de las
    mediciones estructurales.
    """
)

online, offline, recovery = st.columns(3, gap="large")


with online:

    with st.container(border=True):

        st.markdown("### 🟢 1. Online")

        st.markdown(
            """
            La conexión LTE/VPN se encuentra disponible.

            **Edge → Historian**

            Los datos adquiridos son enviados normalmente hacia el Canary
            Historian remoto.
            """
        )


with offline:

    with st.container(border=True):

        st.markdown("### 🔴 2. Sin comunicación")

        st.markdown(
            """
            Se interrumpe temporalmente la comunicación LTE, VPN o el acceso
            al Historian.

            **Edge → Buffer local**

            El sistema continúa adquiriendo datos y mantiene localmente la
            información pendiente de transmisión.
            """
        )


with recovery:

    with st.container(border=True):

        st.markdown("### 🔵 3. Recuperación")

        st.markdown(
            """
            Se restablece la comunicación con el servidor remoto.

            **Buffer → Historian**

            Store & Forward reanuda la transmisión y envía los datos
            almacenados durante la interrupción.
            """
        )


# -----------------------------------------------------------------------------
# Docker services
# -----------------------------------------------------------------------------

st.subheader("Servicios instalados")

st.code(
    """canary-opc-collector
canary-mqtt-collector
canary-store-and-forward
canary-administrator
canary-identity""",
    language="text",
)


# -----------------------------------------------------------------------------
# Software configuration
# -----------------------------------------------------------------------------

with st.expander("Configuración técnica del Edge Computer"):

    st.markdown(
        """
        **Sistema Operativo**

        `Ubuntu Server 26.04.1 LTS`

        **Docker Engine**

        `29.8.0`

        **Docker Compose**

        `v5.5.1`

        **Canary Administrator**

        `TCP 55273`

        **Canary Identity**

        `TCP 55353`

        **OPC UA**

        `opc.tcp://192.168.1.14:48010`
        """
    )


# -----------------------------------------------------------------------------
# Validation
# -----------------------------------------------------------------------------

st.subheader("Validación de continuidad de datos")

with st.container(border=True):

    st.markdown(
        """
        La validación de Store & Forward considera tres condiciones
        consecutivas:

        **1. Operación normal**  
        Adquisición y transmisión de datos hacia el Historian remoto.

        **2. Interrupción controlada**  
        Pérdida deliberada del enlace remoto mientras el sistema continúa
        generando y adquiriendo mediciones.

        **3. Recuperación**  
        Restablecimiento de la comunicación y verificación del reenvío de
        los datos almacenados durante la interrupción.
        """
    )


st.info(
    """
    La evidencia de validación debe incluir el registro temporal de la
    interrupción, el crecimiento del buffer local y la posterior recepción
    de los datos pendientes en el Canary Historian.
    """
)