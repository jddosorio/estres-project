"""Patente de invención del proyecto ESTRES — última resolución INAPI."""
from pathlib import Path
import streamlit as st

IMAGE_DIR = Path('images')
INAPI_GRANTED_IMAGE = IMAGE_DIR / 'inapi-patent-granted.png'

st.title('Patente de Invención')
st.caption('Proyecto CORFO 25IRA2-308620 — Protección de la propiedad intelectual')

st.subheader('Patente de invención concedida')
st.markdown('El **Instituto Nacional de Propiedad Industrial (INAPI)** concedió la patente de invención mediante la **Resolución de aceptación a registro C-2026-55098**, de **23 de octubre de 2026**.')

c1, c2, c3 = st.columns(3)
c1.metric('Solicitud', '2025-02836')
c2.metric('Fecha de solicitud', '22/09/2025')
c3.metric('Estado', 'Patente concedida')

st.markdown('### Título de la invención')
st.info('Sistema de monitoreo de deformaciones estructurales mediante sensores digitales')

st.subheader('Última resolución INAPI — 23/10/2026')
left, right = st.columns([1, 1], gap='large')
with left:
    if INAPI_GRANTED_IMAGE.exists():
        st.image(str(INAPI_GRANTED_IMAGE), caption='Resolución de aceptación a registro C-2026-55098.', use_container_width=True)
    else:
        st.info('Guardar la imagen de la resolución en `images/inapi-patent-granted.png`.')
with right:
    st.markdown('''
    La resolución **concede la patente de invención** y reconoce el cumplimiento de los requisitos de **novedad, nivel inventivo y aplicación industrial**.

    El pliego definitivo contiene **9 reivindicaciones**, presentadas el **30 de junio de 2026**.
    ''')
    st.success('Patente de invención concedida por INAPI.')

st.subheader('Relación con el proyecto ESTRES')
st.markdown('''
La invención se refiere al **monitoreo de deformaciones estructurales mediante sensores digitales**, ámbito directamente relacionado con el proyecto ESTRES y sus procesos de adquisición, tratamiento y análisis de variables estructurales.

La concesión constituye un resultado relevante de **propiedad intelectual**. Es distinta de la validación experimental del sistema y no representa por sí misma una certificación de su TRL.
''')
st.caption('Fuente: INAPI, Resolución C-2026-55098, de 23/10/2026; solicitud 2025-02836.')
