"""Configuration page for PROTEGE BLE tags and scanners."""

from __future__ import annotations

import streamlit as st


st.title("PROTEGE — Configuración de Tags y Scanners")
st.caption("Preparación de dispositivos para la validación de tránsito BLE")

with st.container(height=245, border=True):
    st.subheader("Descripción de la solución")
    st.markdown(
        """
        PROTEGE utiliza tags BLE portados por los trabajadores y nodos fijos
        asociados a las zonas del layout. Cada tag transmite periódicamente su
        identificación mediante advertising BLE. Los nodos capturan la
        identificación, el RSSI y el instante de observación.

        Las detecciones se consolidan durante una ventana de un minuto y son
        transmitidas por el LTE Controller hacia ClickHouse Cloud mediante la
        red NB-IoT/LTE. Sobre estas observaciones se generan eventos de zona e
        intervalos de permanencia para calcular los indicadores de Time on Tools.

        PROTEGE considera una configuración básica de un nodo por zona y una
        configuración direccional con dos puntos de observación BLE.
        """
    )

st.subheader("Nomenclatura de nodos")

master_col, auxiliary_col = st.columns(2)

with master_col:
    st.markdown(
        """
        #### Master Node

        Nodo principal de la zona, compuesto por:

        - BLE Controller para detectar tags.
        - LTE Controller para comunicación NB-IoT/LTE.
        - Consolidación de observaciones por minuto.
        - Correlación de señales y generación de eventos.
        - Transmisión de datos hacia ClickHouse Cloud.
        """
    )

with auxiliary_col:
    st.markdown(
        """
        #### Auxiliary BLE Node

        Punto de observación complementario, compuesto por:

        - BLE Controller sin módem LTE.
        - Detección autónoma de advertising de tags.
        - Medición de RSSI y secuencia temporal.
        - Retransmisión BLE de observaciones al Master Node.
        - Identificación propia del punto de observación.
        """
    )

st.info(
    "Se adopta la denominación Master Node y Auxiliary BLE Node. "
    "Peer Node se reservaría para una arquitectura futura con nodos equivalentes; "
    "en la configuración actual ambos nodos tienen responsabilidades diferentes."
)

basic_tab, directional_tab, messages_tab = st.tabs(
    ["Un nodo por zona", "Detección direccional", "Datos intercambiados"]
)

with basic_tab:
    st.subheader("Configuración básica: un Master Node por zona")
    st.markdown(
        """
        **Tag BLE → Master Node → NB-IoT/LTE → ClickHouse Cloud**

        Cada zona dispone de un Master Node que detecta directamente los tags.
        Cuando un tag es detectado, la persona se asigna a esa zona. Si el mismo
        tag aparece posteriormente en otro Master Node, PROTEGE cierra el
        intervalo anterior mediante `FORCED_EXIT` y genera un nuevo `ENTER`.

        Esta configuración permite determinar la última zona conocida, pero no
        confirma por sí sola el instante exacto en que una persona abandona una
        zona si no es detectada posteriormente por otro nodo.

        **Reglas complementarias:**

        - Timeout de ausencia para pasar a `UNKNOWN` o `Z00`.
        - Cierre automático al finalizar el turno.
        - Cierre de zonas activas al detectar la salida general de la faena.
        """
    )

with directional_tab:
    st.subheader("Configuración direccional: Master Node + Auxiliary BLE Node")
    st.markdown(
        """
        El Master Node y el Auxiliary BLE Node se instalan en lados diferentes
        del acceso a una zona. Ambos detectan el mismo tag y el Master Node
        correlaciona el orden temporal y la evolución del RSSI.

        **Exterior → Auxiliary BLE Node → acceso → Master Node → Interior**

        | Secuencia de observación | Evento inferido |
        |---|---|
        | Auxiliary primero → Master después | `ENTER` |
        | Master primero → Auxiliary después | `EXIT` |
        | Solo un nodo detecta el tag | Dirección no confirmada |
        | Señales simultáneas o inestables | Evento de baja confianza |

        La dirección debe calcularse con observaciones de segundos o
        subsegundos dentro de los BLE Controllers. El envío LTE puede continuar
        realizándose cada minuto, pero debe conservar el orden de las
        observaciones para no perder la información direccional.
        """
    )

with messages_tab:
    st.subheader("Observación enviada por el Auxiliary BLE Node")
    st.code(
        """message_type: SCANNER_OBSERVATION
source_node_id: AUX-ZONE-01
tag_id: <identificador BLE>
observed_at_ms: <instante o uptime>
rssi_dbm: <RSSI observado>
sequence_no: <secuencia>
sample_count: <cantidad de muestras>""",
        language="text",
    )

    st.subheader("Evento consolidado por el Master Node")
    st.code(
        """event_time
tag_id
zone_id
event_type: ENTER | EXIT | FORCED_EXIT | UNKNOWN
event_reason
detection_mode: SINGLE_NODE | DUAL_SCANNER
confidence
master_node_id
auxiliary_node_id""",
        language="text",
    )

st.warning(
    "La ubicación física, separación y umbrales RSSI de ambos nodos deben "
    "determinarse mediante recorridos controlados durante la validación TRL-5."
)
