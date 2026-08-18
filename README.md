# PROTEGE Digital Twin — Time on Tools

Diseño de referencia para medir la permanencia de trabajadores en zonas de una
faena simulada. El proyecto separa explícitamente el **Gemelo Digital ideal**
de la futura estimación mediante tags BLE y gateways (scanners) fijos.

## Dos capas de validación

1. **Digital Twin ground truth:** genera la ubicación real conocida, eventos
   `ENTER`/`EXIT`, intervalos exactos y KPI esperados. No utiliza RSSI.
2. **Inferencia BLE:** recibe `ble_raw`, estima los mismos intervalos y luego se
   compara contra el ground truth para medir error, recall y salidas forzadas.

El Gemelo Digital es, por tanto, la referencia de validación. Los scanners son
una fuente de observaciones que se incorporará después y cuya calidad podrá
medirse objetivamente.

## Objetivo

Transformar detecciones BLE (`timestamp`, gateway, tag y RSSI) en una línea de
tiempo por trabajador y, desde ella, calcular:

- tiempo productivo en el frente de trabajo;
- tiempo de acceso y salida;
- tiempo en casa de cambio;
- tiempo asociado a instrucciones/reuniones;
- tiempo asociado al pañol o espera de herramientas;
- tiempo sin ubicación confiable;
- tiempo total de permanencia en faena.

La ubicación es una **inferencia probabilística**. La presencia en la zona de
reunión o pañol no demuestra por sí sola que hubo espera; para un KPI contractual
debe cruzarse con órdenes de trabajo, agenda de charlas o eventos del supervisor.

## Layout imaginario

```mermaid
flowchart LR
    A["Z01 Acceso"] --> B["Z02 Casa de cambio"]
    B --> C["Z03 Reunión e instrucciones"]
    C --> D["Z04 Pañol de herramientas"]
    D --> E["Z05 Frente de trabajo"]
```

| Zona | Gateway | Propósito | Clasificación inicial |
| --- | --- | --- | --- |
| Z01 Acceso | GW-ACCESS-01 | Entrada/salida y límite de turno | soporte |
| Z02 Casa de cambio | GW-CHANGE-01 | Cambio de ropa/EPP | no productivo planificado |
| Z03 Reunión | GW-BRIEF-01 | Charla, asignación e instrucciones | no productivo planificado |
| Z04 Herramientas | GW-TOOLS-01 | Retiro/devolución y espera | no productivo inferido |
| Z05 Frente de trabajo | GW-WORK-01 | Ejecución de la tarea | productivo |

El modelo ideal amplía el frente de trabajo a `Z05-A`, `Z05-B` y `Z05-C` para
representar tres casas, pisos o frentes. `Z00` representa tránsito o zona
indefinida y `Z06` representa la colación.

## Estado ideal del Gemelo Digital

Cada trabajador tiene una sola zona activa. En el ground truth todas las
entradas y salidas son conocidas exactamente:

```mermaid
stateDiagram-v2
    [*] --> Undefined
    Undefined --> ZoneA: ENTER A
    Undefined --> ZoneB: ENTER B
    Undefined --> ZoneC: ENTER C
    ZoneA --> ZoneB: EXIT A + ENTER B
    ZoneA --> ZoneC: EXIT A + ENTER C
    ZoneB --> ZoneA: EXIT B + ENTER A
    ZoneB --> ZoneC: EXIT B + ENTER C
    ZoneC --> ZoneA: EXIT C + ENTER A
    ZoneC --> ZoneB: EXIT C + ENTER B
    ZoneA --> Undefined: EXIT / fin de turno
    ZoneB --> Undefined: EXIT / fin de turno
    ZoneC --> Undefined: EXIT / fin de turno
```

La jornada base contiene nueve horas de presencia, 36 minutos de colación y
8 h 24 min de tiempo laboral por día. Cinco jornadas completas producen
exactamente 42 horas laborales y 45 horas de presencia semanal.

Para separar espacios colindantes conviene instalar un gateway por zona, lejos
de tabiques metálicos, registrar coordenadas y altura, y ejecutar una campaña de
calibración con el tag en el pecho/casco en puntos conocidos. Si una zona es
grande o tiene sombra RF, se agregan scanners adicionales con el mismo `zone_id`.

## Arquitectura

```mermaid
flowchart TD
    T["Tags BLE de trabajadores"] --> G["5 gateways fijos"]
    G --> I["Ingesta segura"]
    I --> R["ClickHouse: lecturas RSSI crudas"]
    R --> L["Motor de localización"]
    C["Catálogos de gateways, zonas y trabajadores"] --> L
    L --> V["Intervalos de permanencia"]
    V --> K["KPI por trabajador, turno y categoría"]
    K --> D["Dashboard y reporte de validación"]
```

Cada lectura debe contener `event_time`, `gateway_address`, `tag_address`,
`rssi_dbm`, contador de secuencia y estado del gateway. La identidad del
trabajador se mantiene en un catálogo separado. El dashboard no necesita exponer
la dirección BLE; puede trabajar con `worker_id` pseudonimizado.

## Lógica de ubicación RSSI

1. Normalizar direcciones BLE a mayúsculas.
2. Agrupar lecturas por trabajador en ventanas de 5 s.
3. Calcular la mediana RSSI por zona; la mediana reduce picos y multipath.
4. Elegir la zona con mejor RSSI si supera `min_rssi_dbm` (inicio: -85 dBm).
5. Mantener la zona actual mientras el candidato no sea al menos 6 dB mejor.
6. Confirmar un cambio sólo después de 3 ventanas consecutivas (15 s).
7. Si no hay lectura válida durante 30 s, cerrar el intervalo y marcar
   `UNKNOWN`; no distribuir artificialmente ese tiempo.
8. Unir huecos menores de 15 s si antes y después aparece la misma zona.

Los valores son parámetros iniciales; deben calibrarse con recorridos reales y
una matriz de confusión por zona. Para el piloto, la meta razonable es ≥90 % de
exactitud de zona y error absoluto mediano ≤30 s por permanencia.

## Definición inicial de KPI

Sea el turno observado desde la primera detección válida de entrada hasta la
última detección válida de salida:

`T_presencia = T_salida - T_entrada`

`T_productivo = suma(intervalos en Z05)`

`T_no_productivo = T_cambio + T_instrucciones + T_herramientas`

`T_no_clasificado = T_presencia - T_productivo - T_no_productivo - T_soporte`

`Time on Tools (%) = 100 × T_productivo / T_presencia`

También debe informarse cobertura:

`Cobertura (%) = 100 × (T_presencia - T_no_clasificado) / T_presencia`

No se debe presentar Time on Tools sin cobertura, porque una pérdida de señal
podría mejorar o empeorar artificialmente el indicador.

## Archivos

- `sql/001_schema.sql`: tablas de catálogos, lecturas e intervalos.
- `sql/002_seed_simulated_site.sql`: zonas, gateways y trabajadores ficticios.
- `sql/003_kpi_views.sql`: vista diaria de tiempos y porcentajes.
- `sql/004_twin_views.sql`: validación semanal, resumen de zonas y auditoría
  de transiciones del Gemelo Digital.
- `src/simulate_digital_twin.py`: genera el ground truth ideal, sin RSSI.
- `src/simulate_protege.py`: genera un recorrido BLE reproducible.
- `src/infer_zones.py`: referencia del algoritmo de permanencia.
- `tests/test_infer_zones.py`: pruebas unitarias básicas.
- `tests/test_digital_twin.py`: valida 9 h de presencia, 36 min de colación,
  continuidad de intervalos y 42 h laborales semanales.

## Ejecución local

```bash
python3 src/simulate_digital_twin.py \
  --output-dir sample_data/digital_twin \
  --start-date 2026-01-05 \
  --days 182 \
  --workers 20 \
  --seed 42

python3 src/simulate_protege.py --output sample_data/scans.csv
python3 src/infer_zones.py \
  --scans sample_data/scans.csv \
  --gateways sample_data/gateways.csv \
  --output sample_data/intervals.csv
python3 -m unittest discover -s tests -v
```

La ejecución del Gemelo Digital produce:

- `twin_manifest.json`: parámetros reproducibles y `run_id`.
- `twin_zones.csv`: catálogo de zonas ideales.
- `twin_events.csv`: eventos exactos `ENTER` y `EXIT`.
- `twin_intervals.csv`: permanencias exactas por trabajador y zona.
- `twin_daily_kpis.csv`: KPI esperados para validar ClickHouse y Streamlit.

La simulación sólo valida la lógica. Antes del despliegue se deben validar
privacidad, consentimiento, retención de datos, seguridad de transporte y reglas
laborales aplicables.

## Plan de validación

1. Marcar 10–15 puntos de prueba y medir 2 minutos por punto.
2. Hacer al menos 20 recorridos con horario anotado o video de referencia.
3. Ajustar umbral, histéresis y permanencia mínima sin usar los recorridos de
   evaluación final.
4. Comparar zona inferida contra zona real y reportar matriz de confusión.
5. Ejecutar 3–5 jornadas simuladas con varios tags y tráfico normal.
6. Congelar parámetros antes de medir los KPI del piloto.
