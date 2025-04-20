# 📊 Proyecto de Análisis de Demanda con FastAPI

Este proyecto permite visualizar y exportar datos de demanda en formato Excel, utilizando FastAPI como backend, está diseñado para consultar por días o por rangos de fechas

## ⚙️ Instrucciones para ejecutar el backend
## Crea y activa un entorno virtual
python -m venv venv
# En Windows
venv\Scripts\activate
# En Mac/Linux
source venv/bin/activate

## Instala las dependencias
pip install -r requirements.txt

## Ejecutar el servidor
uvicorn app.main:app --reload

