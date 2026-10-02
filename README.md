# ESTRES — Structural Monitoring System

## CORFO INNOVA REGIÓN Project

**Project:** 25IRA2-308620  
**Title:** Tecnologías de Industria 4.0 para el Monitoreo Estructural de Equipos Mineros de Alta Criticidad

ESTRES is an industrial structural monitoring system developed for monitoring
high-criticality mobile mining equipment.

The system measures structural deformation using an ESR sensor and processes
the measurements to identify stress cycles and estimate fatigue-related
variables.

The project integrates industrial sensing, PLC processing, Edge Computing,
cellular communications, Store & Forward, GPS positioning, remote
historization, and data visualization.

---

## System Architecture

The main data path is:

ESR Sensor  
↓  
EnDat Gateway  
↓  
PROFINET  
↓  
Siemens PLC  
↓  
OPC UA / IBHLink UA  
↓  
Edge Computer  
↓  
Canary Edge  
↓  
Teltonika LTE Router  
↓  
Cellular Network  
↓  
VPN  
↓  
Remote Canary Historian

The system also integrates GPS positioning and remote visualization.

---

## Main Technologies

- HEIDENHAIN ESR structural deformation sensor
- Siemens PLC
- PROFINET
- IBHLink UA
- OPC UA
- Linux Edge Computer
- Canary Edge
- Canary Historian
- Store & Forward
- Teltonika industrial LTE communications
- GPS
- Python
- Streamlit
- Plotly
- PyDeck

---

## Structural Variables

The processing chain implemented by ESTRES is:

**Structural Deformation**

→ **Stress**

→ **Stress Rate**

→ **Stress Range**

→ **Stress Rate Range**

→ **Micro Damage**

These variables are used to characterize structural load cycles and support
fatigue monitoring.

---

## Experimental Validation

An integrated experimental campaign was performed using a heavy cement mixer
truck.

The ESR sensor was installed directly on a structural element of the truck
chassis.

The tests included:

- structural deformation measurement;
- dynamic vehicle operation;
- stress-cycle processing;
- cellular data transmission;
- GPS tracking;
- Edge data acquisition;
- Store & Forward operation;
- remote data historization;
- remote visualization.

The experimental campaign provides evidence supporting the technological
maturation of the integrated ESTRES prototype toward TRL-6.

---

## Streamlit Application

The Streamlit application documents the system architecture, experimental
tests, communications, GPS tracking, Store & Forward operation, and TRL-6
results.

Main sections include:

- System
- Stress Control Unit
- Stress Cycles
- Fatigue
- Experimental Tests
- Communications
- GPS Position
- Store & Forward
- TRL-6 Results
- Patent
- Dissemination

---

## Repository Structure

Typical project structure:

    .
    ├── app.py
    ├── views/
    │   ├── 1_Sistema.py
    │   ├── 2_Ciclos_Estres.py
    │   ├── 3_Fatiga.py
    │   ├── 4_Comunicaciones.py
    │   ├── 5_GPS.py
    │   ├── 6_Store_Forward.py
    │   ├── 7_Resultados.py
    │   ├── 8_Patente_Invencion.py
    │   ├── 9_Stress_Control_Unit.py
    │   ├── 10_Pruebas_Experimentales.py
    │   └── 11_Difusion.py
    ├── images/
    ├── sample_data/
    ├── requirements.txt
    ├── README.md
    └── helpful_hints.md

---

## Running the Application

See:

    helpful_hints.md

for instructions to create the Python environment, run Streamlit locally,
update GitHub, and deploy the application using Streamlit Community Cloud.

---

## Intellectual Property

A patent application associated with the structural monitoring technology
has been submitted to INAPI.

**Application:** 2025-02836

**Title:**  
Sistema de monitoreo de deformaciones estructurales mediante sensores digitales

Current status: **Resolutive stage**.

---

## Project

Developed by **PULSO SpA / PULSO Tech**

Antofagasta, Chile

CORFO INNOVA REGIÓN  
Project 25IRA2-308620

