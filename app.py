from pathlib import Path
import io
import pandas as pd
from fastapi import FastAPI, UploadFile, File, Form
from fastapi.responses import HTMLResponse, JSONResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from fastapi import Request

ROOT = Path(__file__).resolve().parent
app = FastAPI(title="Решись Авиа - прогноз спроса")
app.mount("/static", StaticFiles(directory=ROOT / "static"), name="static")
templates = Jinja2Templates(directory=ROOT / "templates")

@app.get("/", response_class=HTMLResponse)
async def index(request: Request):
    return templates.TemplateResponse(
    request=request, 
    name="index.html", 
    context={}
)

@app.post("/api/forecast")
async def forecast(
    forecast_file: UploadFile = File(...), routes_file: UploadFile = File(...),
    route: str = Form(...), date: str = Form(...), price: float = Form(...)
):
    try:
        fc = pd.read_csv(io.BytesIO(await forecast_file.read()))
        rt = pd.read_csv(io.BytesIO(await routes_file.read()))
        fc["date"] = pd.to_datetime(fc["date"]).dt.strftime("%Y-%m-%d")
        day = pd.to_datetime(date).strftime("%Y-%m-%d")
        row = fc[(fc.route == route) & (fc.date == day)]
        info = rt[rt.route == route]
        if row.empty or info.empty:
            return JSONResponse({"error":"Не найдена комбинация маршрута и даты или параметры маршрута."}, status_code=404)
        row, info = row.iloc[0], info.iloc[0]
        p0 = float(info["base_price"])
        sensitivity = float(info["price_sensitivity"])
        seats = int(row["seats"])
        scenarios=[]
        for q in [f"0.{i}" for i in range(1,10)]:
            demand_base=float(row[f"{q}_base_demand"])
            wanted=max(0.0, demand_base-sensitivity*(float(price)-p0))
            sold=min(float(seats), wanted)
            scenarios.append({"quantile":q,"demand":round(wanted,2),"sold":round(sold,2)})
        median=next(x for x in scenarios if x["quantile"]=="0.5")
        return {"route":route,"date":day,"price":price,"seats":seats,"base_price":p0,
                "median_demand":median["demand"],"median_sold":median["sold"],"scenarios":scenarios}
    except Exception as e:
        return JSONResponse({"error":f"Ошибка обработки файлов: {e}"}, status_code=400)
