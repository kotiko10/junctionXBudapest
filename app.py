import uvicorn
import subprocess
from fastapi import FastAPI, Request
import numpy as np
import csv
from fastapi.responses import HTMLResponse, JSONResponse
from fastapi import HTTPException
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from fastapi import Form
from pydantic import BaseModel
from datetime import datetime, time, timedelta
import json
from pathlib import Path
from fastapi.middleware.cors import CORSMiddleware
from static.js.patient import read_json_file, write_json_file

app = FastAPI(debug=True)
templates = Jinja2Templates(directory='templates')

# Mounting the static directory
app.mount("/static", StaticFiles(directory="static"), name="static")
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allows all origins
    allow_credentials=True,
    allow_methods=["*"],  # Allows all methods
    allow_headers=["*"],  # Allows all headers
)

@app.get('/', response_class=HTMLResponse)
def main(request: Request):
    return templates.TemplateResponse('index.html', {'request': request})

@app.get('/Main', response_class=HTMLResponse)
def main(request: Request):
    return templates.TemplateResponse('index.html', {'request': request})

#+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++ 
# Define a Pydantic model for appointment data
class Appointment(BaseModel):
    patient_id: int
    patient_name: str
    start_time: str
    end_time: str
    date: str
    machine_name: str

# Ensure the directory and file exist for appointments
appointments_file_path = Path(__file__).parent / 'static/data/appointments.json'
appointments_file_path.parent.mkdir(exist_ok=True)
if not appointments_file_path.exists():
    appointments_file_path.write_text("[]")


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


# Endpoint to handle the appointment form submission
@app.post("/add_appointment")
async def add_appointment(request: Request):
    data = await request.json()
    
    # Add your logic to process the data and write to the JSON file
    # Example:
    appointments = read_json_file('static/data/appointments.json')
    appointments.append(data)
    write_json_file('static/data/appointments.json', appointments)

    return {"message": "Appointment added successfully"}
# You would also have to implement a similar endpoint for removing appointments.

@app.get("/Technologies", response_class=HTMLResponse)
async def technologies(request: Request):
    return templates.TemplateResponse("technologies.html", {"request": request})

@app.get("/Schedule", response_class=HTMLResponse)
async def floors(request: Request):
    return templates.TemplateResponse("schedule.html", {"request": request})

@app.post("/add_appointment")
async def add_appointment(request: Request):
    data = await request.json()
    
    # Read existing appointments
    try:
        with open(appointments_file_path, 'r') as file:
            appointments = json.load(file)
    except (FileNotFoundError, json.JSONDecodeError):
        appointments = []

    # Check if the patient_id already exists
    existing_appointment = next((item for item in appointments if item["patient_id"] == data["patient_id"]), None)
    if existing_appointment:
        # Increase appointment count
        existing_appointment["appointment_count"] = existing_appointment.get("appointment_count", 0) + 1
    else:
        # Add new patient with appointment count 1
        data["appointment_count"] = 1
        appointments.append(data)

    # Save the updated appointments back to the file
    with open(appointments_file_path, 'w') as file:
        json.dump(appointments, file, indent=4)

    return JSONResponse(content={"message": "Appointment added successfully"}, status_code=200)


# Endpoint to remove an appointment
@app.post("/VitalBeam1/remove-appointment")
async def remove_appointment(request: Request, start: str = Form(...), day: int = Form(...)):
    # Load existing appointments
    with open('static/data/vital1.json', 'r') as file:
        appointments = json.load(file)

    # Find and remove the appointment
    appointments = [appointment for appointment in appointments if not (appointment["start"] == start and appointment["day"] == day)]

    # Save the updated appointments
    with open('static/data/vital1.json', 'w') as file:
        json.dump(appointments, file)

    return {"message": "Appointment removed successfully"}

# Update the existing endpoint to read the appointments
@app.get("/VitalBeam1", response_class=HTMLResponse)
async def vitalbeam1(request: Request, week_offset: int = 0):
    week_dates = get_week_dates(week_offset)

    # Load appointments from file
    try:
        with open('static/data/vital1.json', 'r') as file:
            appointments = json.load(file)
    except FileNotFoundError:
        # If the file doesn't exist, initialize it as an empty list
        appointments = []
        with open('static/data/vital1.json', 'w') as file:
            json.dump(appointments, file)

    # Filter appointments for the current week
    appointments_for_week = [appointment for appointment in appointments if appointment["day"] == week_offset]

    # Return the template response
    return templates.TemplateResponse("VitalBeam1.html", {
        "request": request,
        "appointments": appointments_for_week,
        "week_dates": week_dates,
        "week_offset": week_offset
    })
# ++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++

@app.get("/VitalBeam2", response_class=HTMLResponse)
async def floors(request: Request):
    return templates.TemplateResponse("VitalBeam2.html", {"request": request})

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

if __name__ == "__main__":
    uvicorn.run(app, host="localhost", port=8000, log_level="debug", reload=True)