# backend/main.py

# Importamos FastAPI, que es el framework con el que construiremos la API.
from fastapi import FastAPI

# Creamos una instancia de la aplicación FastAPI.
# El título es opcional, se verá en la documentación automática.
app = FastAPI(title="Triage Digital - API base")

# Definimos una ruta HTTP GET en la URL raíz "/".
# Cada vez que alguien entre a http://127.0.0.1:8000/ se ejecuta esta función.
@app.get("/")
def root():
    """
    Este endpoint es el más simple posible.
    Retorna un mensaje en formato JSON para confirmar que la API está corriendo.
    """
    return {"message": "API de Triage Digital funcionando 🚑"}
