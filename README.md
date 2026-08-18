# PROTEGE Dashboard

Dashboard Streamlit ejecutado localmente y conectado mediante HTTPS/TLS a
ClickHouse Cloud. La aplicación permite validar la conexión, seleccionar una
tabla, revisar su estructura, visualizar registros y generar automáticamente
gráficos de temperatura y humedad.

## Estructura

```text
protege-project/
├── app.py
├── requirements.txt
├── README.md
├── .gitignore
├── .streamlit/
│   ├── config.toml
│   └── secrets.toml.example
├── scripts/
│   └── check_connection.py
└── src/
    ├── __init__.py
    ├── clickhouse_client.py
    └── queries.py
```

## Instalación en macOS

Descomprimir o copiar el directorio en `~/Projects`:

```bash
cd ~/Projects/protege-project
python3 -m venv .venv
source .venv/bin/activate
python -m pip install --upgrade pip
pip install -r requirements.txt
```

Crear el archivo local de credenciales:

```bash
cp .streamlit/secrets.toml.example .streamlit/secrets.toml
```

Editar `.streamlit/secrets.toml` y reemplazar solamente la contraseña. El
archivo real de credenciales está excluido de Git por `.gitignore`.

## Probar ClickHouse sin abrir Streamlit

```bash
python scripts/check_connection.py
```

## Ejecutar el dashboard

```bash
streamlit run app.py
```

Abrir en el navegador:

```text
http://localhost:8501
```

## Columnas ambientales reconocidas

La aplicación inspecciona la tabla seleccionada y reconoce, entre otras, estas
columnas:

- Temperatura: `temperature_mdeg_c`, `temperature_c`, `temperature`, `temp_c`.
- Humedad: `humidity_milli_pct`, `humidity_pct`, `humidity`, `rh`.
- Eje horizontal: `timestamp`, `received_at`, `created_at`, `uptime_ms` o
  `sequence`.

Los valores `temperature_mdeg_c` y `humidity_milli_pct` se dividen por 1000
antes de ser presentados.

## Seguridad y operación

- No subir `.streamlit/secrets.toml` a GitHub.
- Usar idealmente un usuario ClickHouse de solo lectura para el dashboard.
- Las consultas se almacenan temporalmente en caché durante 60 segundos.
- El dashboard local deja de estar disponible cuando el computador se apaga o
  cuando se detiene Streamlit.
