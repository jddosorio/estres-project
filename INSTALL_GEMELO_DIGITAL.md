# Instalación del menú y dashboard Gemelo Digital

Este paquete reemplaza `app.py` por un punto de entrada con navegación lateral
y mueve el dashboard ambiental existente a `views/1_Monitoreo_Ambiental.py`.
También incorpora el Gemelo Digital y deja preparados los accesos a Reportes y
ClickHouse.

Desde la raíz de `~/Projects/protege-project`:

```bash
unzip ~/Downloads/PROTEGE-Digital-Twin-Dashboard.zip
streamlit run app.py
```

Streamlit detectará automáticamente:

```text
app.py
views/1_Monitoreo_Ambiental.py
views/2_Gemelo_Digital.py
views/3_Reportes.py
views/4_ClickHouse.py
```

La página consulta tablas completamente calificadas bajo `protege.twin_*`,
por lo que el dashboard ambiental puede continuar utilizando la base de datos
`default` definida en `.streamlit/secrets.toml`.

Después de validar localmente:

```bash
git add app.py views/
git commit -m "Add PROTEGE dashboard navigation and Digital Twin"
git push
```
