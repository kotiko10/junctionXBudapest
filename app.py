import uvicorn
import subprocess
from fastapi import FastAPI, Request
import numpy as np
import csv
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from fastapi import Form

# ++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
# Dummy Data
from datetime import datetime, time, timedelta
import json
from pathlib import Path

# # Path to the JSON file relative to the project root
# json_path = Path(__file__).parent / 'static/data' / 'people.json'

# # Load the JSON data
# with open(json_path, 'r') as file:
#     people_data = json.load(file)

# ++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++

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

def get_week_dates():
    # Get the current date
    today = datetime.today()

    # Calculate the start of the week (Monday)
    start_of_week = today - timedelta(days=today.weekday())

    # Generate dates for the week
    week_dates = [start_of_week + timedelta(days=i) for i in range(7)]

    return [date.strftime("%Y-%m-%d") for date in week_dates]

def get_week_dates(offset=0):
    # Get the current date
    today = datetime.today()

    # Calculate the start of the week (Monday) with an offset
    start_of_week = today - timedelta(days=today.weekday()) + timedelta(weeks=offset)

    # Generate dates for the week
    week_dates = [start_of_week + timedelta(days=i) for i in range(7)]

    # Return the dates in mm/dd/yyyy format
    return [date.strftime("%m/%d/%Y") for date in week_dates]


@app.get("/Technologies", response_class=HTMLResponse)
async def technologies(request: Request):
    return templates.TemplateResponse("technologies.html", {"request": request})

@app.get("/Schedule", response_class=HTMLResponse)
async def floors(request: Request):
    return templates.TemplateResponse("schedule.html", {"request": request})

@app.get("/VitalBeam1", response_class=HTMLResponse)
async def vitalbeam1(request: Request, week_offset: int = 0):
    week_dates = get_week_dates(week_offset)
    with open('static/data/vital1.json', 'r') as file:
        appointments = json.load(file)
    return templates.TemplateResponse("VitalBeam1.html", {
        "request": request, 
        "appointments": appointments, 
        "week_dates": week_dates,
        "week_offset": week_offset
    })
    # return templates.TemplateResponse("VitalBeam1.html", {"request": request})

@app.get("/VitalBeam2", response_class=HTMLResponse)
async def floors(request: Request):
    return templates.TemplateResponse("VitalBeam2.html", {"request": request})

@app.get("/TrueBeam1", response_class=HTMLResponse)
# async def true_beam1(request: Request):
#     # Load people data from the JSON file in the static/data directory
#     json_path = Path(__file__).parent / 'static' / 'data' / 'people.json'
#     with open(json_path, 'r') as file:
#         people = json.load(file)

#     # Assuming your appointment slots start at 8:00 AM and are 45 minutes each
#     appointments = []
#     start_time = time(hour=8, minute=0)  # Start at 8:00 AM
#     for person in people:
#         # Calculate appointment end time
#         end_time = (datetime.combine(datetime.today(), start_time) + timedelta(minutes=45)).time()
#         appointments.append({
#             'start': start_time.strftime("%H:%M"),
#             'end': end_time.strftime("%H:%M"),
#             'name': person['name'],
#             'email': person['email'],
#             'phone': person['phone']
#         })
#         start_time = (datetime.combine(datetime.today(), end_time) + timedelta(minutes=15)).time()  # 15 minutes break between appointments

#     # Render the HTML page with the appointments data
#     return templates.TemplateResponse('TrueBeam1.html', {"request": request, "appointments": appointments})
@app.get("/TrueBeam1", response_class=HTMLResponse)
async def truebeam1(request: Request):
    # Load JSON data
    json_path = Path(__file__).parent / 'static' / 'data' / 'people.json'
    with open(json_path, 'r') as file:
        people_data = json.load(file)

    # Convert time to minutes for height calculation and filter for Monday
    appointments = []
    for person in people_data:
        start_time = datetime.strptime(person["start"], "%H:%M")
        end_time = datetime.strptime(person["end"], "%H:%M")
        duration = int((end_time - start_time).total_seconds() / 60)
        appointments.append({
            "start": person["start"],
            "end": person["end"],
            "name": person["name"],
            "duration": duration,
            "day": 0  # Assuming Monday is day 0
        })

    return templates.TemplateResponse("TrueBeam1.html", {"request": request, "appointments": appointments})
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