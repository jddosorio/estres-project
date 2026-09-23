"""Arquitectura de comunicaciones del sistema ESTRES."""

from __future__ import annotations

from pathlib import Path

import streamlit as st


# -----------------------------------------------------------------------------
# Archivos
# -----------------------------------------------------------------------------

NETWORK_DIAGRAM = Path("images/Network-Full.png")


# -----------------------------------------------------------------------------
# Encabezado
# -----------------------------------------------------------------------------

st.title("Comunicaciones")

st.caption(
    "Proyecto CORFO 25IRA2-308620 — "
    "Arquitectura de comunicaciones del sistema ESTRES"
)

st.markdown(
    """
    Esta página presenta la arquitectura de comunicaciones utilizada durante
    la validación del prototipo integrado **TRL-6**.

    El sistema permite transmitir las variables estructurales desde la
    **Stress Control Unit** instalada en el activo móvil hacia los sistemas
    remotos de almacenamiento, análisis y visualización.
    """
)


# -----------------------------------------------------------------------------
# Diagrama de comunicaciones
# -----------------------------------------------------------------------------

st.subheader("Arquitectura de comunicaciones")

if NETWORK_DIAGRAM.exists():

    # Centramos el diagrama y evitamos que ocupe todo el ancho de la página
    _, col_diagram, _ = st.columns([2, 6, 2])

    with col_diagram:
        st.image(
            str(NETWORK_DIAGRAM),
            caption=(
                "Arquitectura de comunicaciones utilizada para la "
                "validación del sistema ESTRES."
            ),
            use_container_width=True,
        )

else:

    st.warning(
        f"No se encontró el diagrama: {NETWORK_DIAGRAM}"
    )


# -----------------------------------------------------------------------------
# Flujo de comunicaciones
# -----------------------------------------------------------------------------

st.subheader("Flujo de datos")

col1, col2, col3 = st.columns(3)

with col1:

    st.markdown(
        """
        ### 🎛️ Adquisición

        **Sensor ESR**

        ↓ `EnDat`

        **Gateway EnDat / PROFINET**

        ↓ `PROFINET`

        **PLC Siemens**

        ↓ `Ethernet / OPC UA`

        **IBHLink UA**
        """
    )


with col2:

    st.markdown(
        """
        ### 💾 Edge

        **Edge Computer — Ubuntu Linux**

        ↓ `OPC UA`

        **Canary Edge**

        ↓ `Store & Forward`

        **Buffer local de datos**

        ↓

        **Teltonika RUT200**
        """
    )


with col3:

    st.markdown(
        """
        ### 📡 Comunicación remota

        **Red celular LTE**

        ↓

        **Internet**

        ↓ `Teltonika RMS VPN`

        **Red remota**

        ↓

        **Canary Historian**
        """
    )


# -----------------------------------------------------------------------------
# Canal de comunicaciones
# -----------------------------------------------------------------------------

st.subheader("Canal de comunicaciones")

st.markdown(
    """
    La comunicación entre el sistema instalado en terreno y el servidor
    remoto utiliza un **router celular industrial Teltonika RUT200**.

    El RUT200 proporciona conectividad **LTE** y acceso a la infraestructura
    **Teltonika RMS**, utilizada para establecer la conectividad VPN entre
    el sistema remoto y los dispositivos instalados en terreno.

    La cadena principal de comunicaciones es:

    **Stress Control Unit → RUT200 → LTE → Internet → RMS VPN → Canary Historian**
    """
)


# -----------------------------------------------------------------------------
# Protocolos
# -----------------------------------------------------------------------------

st.subheader("Tecnologías y protocolos")

st.markdown(
    """
    **EnDat**  
    Comunicación digital entre el sensor ESR y el gateway.

    **PROFINET**  
    Comunicación industrial entre el gateway EnDat y el PLC Siemens.

    **OPC UA**  
    Intercambio de variables entre el PLC y el sistema Edge mediante
    IBHLink UA.

    **Ethernet industrial**  
    Red local de interconexión entre PLC, gateway OPC UA, Edge Computer
    y router celular.

    **LTE**  
    Canal de comunicación celular entre el activo móvil e Internet.

    **Teltonika RMS VPN**  
    Red privada utilizada para establecer conectividad remota segura
    entre el sistema instalado en terreno y la infraestructura remota.

    **Canary Store & Forward**  
    Permite almacenar temporalmente los datos en el Edge Computer cuando
    la comunicación remota no está disponible y reenviarlos después de
    restablecerse la conexión.
    """
)


# -----------------------------------------------------------------------------
# Resultado de la integración
# -----------------------------------------------------------------------------

st.subheader("Integración End-to-End")

st.success(
    """
    La arquitectura integra adquisición, procesamiento Edge, comunicación
    celular, VPN y almacenamiento remoto, permitiendo transportar las
    variables estructurales desde el sensor ESR instalado en el activo
    móvil hasta el Canary Historian remoto.
    """
)