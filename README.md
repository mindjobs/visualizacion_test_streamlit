# Visualización de emisiones de CO₂ — App Streamlit

Instrucciones para ejecutar la aplicación localmente.

Requisitos
- Python 3.8+
- `pip`

Pasos rápidos

1. (Opcional) Crear y activar un entorno virtual

```bash
python3 -m venv .venv
source .venv/bin/activate
```

2. Instalar dependencias

```bash
pip install --upgrade pip
pip install -r requirements.txt
```

3. Descargar los datos (si no existen)

La app espera el CSV en `data/owid-co2-data.csv`. Para descargarlo:

```bash
mkdir -p data
curl -L -o data/owid-co2-data.csv https://raw.githubusercontent.com/owid/co2-data/master/owid-co2-data.csv
```

4. Ejecutar la app

```bash
streamlit run app.py
```

Acceso
- Local: `http://localhost:8501`
- Si necesitas usar otro puerto: `streamlit run app.py --server.port 8502`

Ejecutar en background

```bash
nohup streamlit run app.py --server.port 8501 > streamlit.log 2>&1 &
echo $!
tail -f streamlit.log
```

Parar la app

```bash
# Si la ejecutaste en primer plano: Ctrl+C
kill <PID>
# O matar todos los procesos streamlit
pkill -f streamlit
```

Notas
- No se incluyeron datos en el repositorio: coloca `data/owid-co2-data.csv` en la raíz del proyecto dentro de la carpeta `data/`.
- Si la app informa que faltan columnas (`country`, `year`, `co2`), revisa el CSV o abre un issue aquí.
- En `app.py` se añadió manejo para mostrar instrucciones si el CSV falta y se reemplazó `use_container_width=True` por `width='stretch'`.

Contacto
- Si quieres que automatice la descarga desde la UI o agregue validaciones, dime y lo implemento.
