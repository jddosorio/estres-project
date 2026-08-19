"""Conceptual site layout for the PROTEGE Digital Twin."""

from __future__ import annotations

from textwrap import dedent

import pandas as pd
import streamlit as st


st.title("PROTEGE — Layout de la Faena Simulada")
st.caption("Distribución conceptual de zonas para la validación del Gemelo Digital")

with st.container(height=220, border=True):
    st.subheader("Descripción del layout")
    st.markdown(
        """
        Este layout representa un **ambiente controlado e imaginario de faena**
        utilizado para validar la arquitectura de datos y los indicadores de
        **Time on Tools** durante la maduración de PROTEGE desde TRL-4 a TRL-5.

        Las instalaciones de apoyo se ubican junto al acceso y siguen la
        secuencia operacional **Acceso → Casa de cambio → Instrucciones →
        Herramientas → Frentes de trabajo**. La zona `Z00` representa circulación
        o tránsito entre instalaciones. Los frentes `Z05-A`, `Z05-B` y `Z05-C`
        representan tres casas, pisos o áreas productivas independientes. La
        colación se modela separadamente como `Z06`.

        En el Gemelo Digital cada trabajador mantiene una sola zona activa. Al
        ingresar a una nueva zona se cierra el intervalo anterior y se inicia un
        nuevo intervalo de permanencia.
        """
    )

st.html(
    dedent(
        """
    <style>
        .protege-site-plan {
            display: grid;
            gap: 0.65rem;
            margin: 1rem 0 1.25rem 0;
        }
        .protege-work-row,
        .protege-support-row {
            display: grid;
            gap: 0.65rem;
        }
        .protege-work-row {
            grid-template-columns: repeat(3, minmax(0, 1fr));
        }
        .protege-support-row {
            grid-template-columns: repeat(5, minmax(0, 1fr));
        }
        .protege-zone {
            border: 1px solid rgba(49, 51, 63, 0.25);
            border-radius: 0.55rem;
            min-height: 6rem;
            padding: 0.85rem;
        }
        .protege-zone strong,
        .protege-zone span {
            display: block;
        }
        .protege-zone-id {
            color: rgba(49, 51, 63, 0.66);
            margin-bottom: 0.3rem;
        }
        .protege-zone-meta {
            color: rgba(49, 51, 63, 0.68);
            margin-top: 0.35rem;
        }
        .protege-productive { background: rgba(0, 150, 136, 0.14); }
        .protege-planned { background: rgba(255, 75, 75, 0.12); }
        .protege-inferred { background: rgba(255, 164, 33, 0.16); }
        .protege-support { background: rgba(28, 131, 225, 0.13); }
        .protege-break { background: rgba(100, 181, 246, 0.16); }
        .protege-transit {
            align-items: center;
            background: rgba(128, 128, 128, 0.10);
            display: flex;
            justify-content: center;
            min-height: 4.25rem;
            text-align: center;
        }
        .protege-entry {
            color: rgba(49, 51, 63, 0.72);
            padding-left: 0.5rem;
        }
        @media (max-width: 800px) {
            .protege-work-row,
            .protege-support-row {
                grid-template-columns: 1fr;
            }
        }
    </style>

    <div class="protege-site-plan" aria-label="Layout conceptual de zonas PROTEGE">
        <div class="protege-work-row">
            <div class="protege-zone protege-productive">
                <span class="protege-zone-id">Z05-A</span>
                <strong>Frente de trabajo A</strong>
                <span class="protege-zone-meta">Productivo · WORK_FACE</span>
            </div>
            <div class="protege-zone protege-productive">
                <span class="protege-zone-id">Z05-B</span>
                <strong>Frente de trabajo B</strong>
                <span class="protege-zone-meta">Productivo · WORK_FACE</span>
            </div>
            <div class="protege-zone protege-productive">
                <span class="protege-zone-id">Z05-C</span>
                <strong>Frente de trabajo C</strong>
                <span class="protege-zone-meta">Productivo · WORK_FACE</span>
            </div>
        </div>

        <div class="protege-zone protege-transit">
            <span><strong>Z00 · Circulación y tránsito</strong><br>
            Acceso → Cambio → Instrucciones → Herramientas → Frentes de trabajo</span>
        </div>

        <div class="protege-support-row">
            <div class="protege-zone protege-support">
                <span class="protege-zone-id">Z01</span>
                <strong>Acceso y control</strong>
                <span class="protege-zone-meta">Entrada / salida</span>
            </div>
            <div class="protege-zone protege-planned">
                <span class="protege-zone-id">Z02</span>
                <strong>Casa de cambio</strong>
                <span class="protege-zone-meta">Preparación / EPP</span>
            </div>
            <div class="protege-zone protege-planned">
                <span class="protege-zone-id">Z03</span>
                <strong>Instrucciones</strong>
                <span class="protege-zone-meta">Reunión / coordinación</span>
            </div>
            <div class="protege-zone protege-inferred">
                <span class="protege-zone-id">Z04</span>
                <strong>Herramientas</strong>
                <span class="protege-zone-meta">Pañol / espera</span>
            </div>
            <div class="protege-zone protege-break">
                <span class="protege-zone-id">Z06</span>
                <strong>Colación</strong>
                <span class="protege-zone-meta">36 minutos</span>
            </div>
        </div>

        <div class="protege-entry">↕ Ingreso / salida de la faena</div>
    </div>
        """
    )
)

zones = pd.DataFrame(
    [
        ("Z01", "Acceso y control", "Soporte", "Ingreso, salida y límite del turno"),
        ("Z02", "Casa de cambio", "No productivo planificado", "Preparación y cambio de EPP"),
        ("Z03", "Instrucciones", "No productivo planificado", "Reunión y asignación de actividades"),
        ("Z04", "Herramientas", "No productivo inferido", "Retiro, devolución o espera de herramientas"),
        ("Z05-A", "Frente de trabajo A", "Productivo", "Ejecución directa de actividades"),
        ("Z05-B", "Frente de trabajo B", "Productivo", "Ejecución directa de actividades"),
        ("Z05-C", "Frente de trabajo C", "Productivo", "Ejecución directa de actividades"),
        ("Z06", "Colación", "Descanso", "Colación planificada de 36 minutos"),
        ("Z00", "Circulación y tránsito", "Indefinido", "Transición entre zonas controladas"),
    ],
    columns=["Zona", "Nombre", "Clasificación", "Propósito"],
)

st.subheader("Definición de zonas")
st.dataframe(zones, use_container_width=True, hide_index=True)

st.info(
    "El layout es una representación conceptual para la validación controlada. "
    "La ubicación definitiva de scanners, distancias y áreas de cobertura se "
    "determinará durante la campaña de validación BLE en terreno."
)
