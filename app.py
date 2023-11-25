import uvicorn
import subprocess
from fastapi import FastAPI, Request
import numpy as np
import csv
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from fastapi import Form

app = FastAPI(debug=True)
templates = Jinja2Templates(directory='templates')

# Mounting the static directory
app.mount("/static", StaticFiles(directory="static"), name="static")

@app.get('/', response_class=HTMLResponse)
def main(request: Request):
    return templates.TemplateResponse('index.html', {'request': request})

@app.get('/Main', response_class=HTMLResponse)
def main(request: Request):
    return templates.TemplateResponse('index.html', {'request': request})

#+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++ 

@app.get("/Technologies", response_class=HTMLResponse)
async def technologies(request: Request):
    return templates.TemplateResponse("technologies.html", {"request": request})

@app.get("/Schedule", response_class=HTMLResponse)
async def floors(request: Request):
    return templates.TemplateResponse("schedule.html", {"request": request})

@app.get("/VitalBeam1", response_class=HTMLResponse)
async def floors(request: Request):
    return templates.TemplateResponse("VitalBeam1.html", {"request": request})

@app.get("/VitalBeam2", response_class=HTMLResponse)
async def floors(request: Request):
    return templates.TemplateResponse("VitalBeam2.html", {"request": request})

@app.get("/TrueBeam1", response_class=HTMLResponse)
async def floors(request: Request):
    return templates.TemplateResponse("TrueBeam1.html", {"request": request})

@app.get("/TrueBeam2", response_class=HTMLResponse)
async def floors(request: Request):
    return templates.TemplateResponse("TrueBeam2.html", {"request": request})

@app.get("/Unique", response_class=HTMLResponse)
async def floors(request: Request):
    return templates.TemplateResponse("Unique.html", {"request": request})


#+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++

@app.get('/Patients',response_class=HTMLResponse)
def main(request: Request):
    return templates.TemplateResponse('index.html', {'request': request})

@app.get('/Floor_reservation',response_class=HTMLResponse)
def main(request: Request):
    return templates.TemplateResponse('index.html', {'request': request})

@app.get('/Treatment_Reservation',response_class=HTMLResponse)
def main(request: Request):
    return templates.TemplateResponse('index.html', {'request': request})

@app.get('/Patient_Stats',response_class=HTMLResponse)
def main(request: Request):
    return templates.TemplateResponse('index.html', {'request': request})

@app.get('/Machine_Stats',response_class=HTMLResponse)
def main(request: Request):
    return templates.TemplateResponse('index.html', {'request': request})

if __name__ == "__main__":
    uvicorn.run(app, host="localhost", port=8000, log_level="debug", reload=True)