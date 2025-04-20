from fastapi import FastAPI, HTTPException, Query
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware  
from datetime import timedelta, datetime
import pandas as pd

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # middleware para aceptar peticione s
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

CSV_FILE = "demanda_sin_dia.csv"

@app.get("/")
async def root():
    return {"message": "Hello World"}

@app.get('/api/demanda')
async def get_demanda(range: int = Query(..., description="Rango de días hacia atrás (15, 30 o 60)")):
    if range not in [15, 30, 60]:
        raise HTTPException(status_code=400, detail="Rango no válido. Usa 15, 30 o 60.")

    try:
        df = pd.read_csv(CSV_FILE, parse_dates=["Date"])

        if df.empty:
            raise HTTPException(status_code=404, detail="El archivo CSV está vacío")

        ultima_fecha_disponible = df["Date"].max()
        fecha_limite = ultima_fecha_disponible - timedelta(days=range)

        df_filtrado = df[df["Date"] >= fecha_limite]
        df_filtrado = df_filtrado[["Date", "Value"]]
        df_filtrado["Date"] = df_filtrado["Date"].dt.strftime("%Y-%m-%d")

        return JSONResponse(content=df_filtrado.to_dict(orient="records"))

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error al procesar el CSV: {str(e)}")

@app.get("/api/demanda/por-fechas")
async def get_demanda_por_fechas(
    start_date: str = Query(..., description="Fecha de inicio en formato YYYY-MM-DD"),
    end_date: str = Query(..., description="Fecha de fin en formato YYYY-MM-DD")
):
    try:
        fecha_inicio = datetime.strptime(start_date, "%Y-%m-%d")
        fecha_fin = datetime.strptime(end_date, "%Y-%m-%d")

        if fecha_inicio > fecha_fin:
            raise HTTPException(status_code=400, detail="La fecha de inicio no puede ser mayor que la fecha de fin.")

        df = pd.read_csv(CSV_FILE, parse_dates=["Date"])

        if df.empty:
            raise HTTPException(status_code=404, detail="El archivo CSV está vacío.")

        df_filtrado = df[(df["Date"] >= fecha_inicio) & (df["Date"] <= fecha_fin)]

        if df_filtrado.empty:
            return JSONResponse(content={"message": "No hay datos disponibles en el rango de fechas especificado."}, status_code=200)

        df_filtrado = df_filtrado[["Date", "Value"]]
        df_filtrado["Date"] = df_filtrado["Date"].dt.strftime("%Y-%m-%d")

        return JSONResponse(content=df_filtrado.to_dict(orient="records"))

    except ValueError:
        raise HTTPException(status_code=400, detail="Las fechas deben estar en formato YYYY-MM-DD.")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error procesando el CSV: {str(e)}")
