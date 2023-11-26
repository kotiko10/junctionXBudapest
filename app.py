import uvicorn
import subprocess
from fastapi import FastAPI, Request
import subprocess
import numpy as np
import csv
import os
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
from typing import List
from fastapi import Query

app = FastAPI(debug=True)
templates = Jinja2Templates(directory='templates')


# Assuming AppointmentKey model is already defined as:
class AppointmentKey(BaseModel):
    start_time: str
    date: str
    machine_name: str

# Function to read appointments from JSON file
def read_appointments_from_file(file_path: str) -> List[dict]:
    try:
        with open(file_path, "r") as file:
            return json.load(file)
    except FileNotFoundError:
        return []

# Function to write appointments to JSON file
def write_appointments_to_file(file_path: str, appointments: List[dict]):
    with open(file_path, "w") as file:
        json.dump(appointments, file, indent=4)


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


# FastAPI endpoint to remove an appointment

@app.get("/get_appointments_for_week")
async def get_appointments_for_week(week_offset: int = Query(0)):
    # Calculate the dates for the given week
    week_dates = get_week_dates(week_offset)

    # Read the appointments from JSON file
    try:
        with open(appointments_file_path, "r") as file:
            appointments = json.load(file)
    except (FileNotFoundError, json.JSONDecodeError):
        return {"appointments": []}

    # Filter appointments for the week
    week_appointments = [appointment for appointment in appointments if appointment["date"] in week_dates]

    return {"appointments": week_appointments}


@app.delete("/remove_appointment")
async def remove_appointment(appointment_key: AppointmentKey):
    # Read existing appointments
    appointments = read_appointments_from_file(appointments_file_path)
    print(appointment_key)
    # Filter out the matching appointment
    appointments = [appt for appt in appointments if not (appt['date'] == appointment_key.date and appt['start_time'] == appointment_key.start_time)]
    #print(appointments)

    os.remove(appointments_file_path)
    

    # Write the updated list back to the file
    write_appointments_to_file(appointments_file_path, appointments)

    return {"message": "Appointment removed successfully"}

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
async def vitalbeam2(request: Request, week_offset: int = 0):
    week_dates = get_week_dates(week_offset)

    # Load appointments from file
    try:
        with open('static/data/vital2.json', 'r') as file:
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

@app.get("/TrueBeam1", response_class=HTMLResponse)
async def truebeam1(request: Request, week_offset: int = 0):
    week_dates = get_week_dates(week_offset)

    # Load appointments from file
    try:
        with open('static/data/vital2.json', 'r') as file:
            appointments = json.load(file)
    except FileNotFoundError:
        # If the file doesn't exist, initialize it as an empty list
        appointments = []
        with open('static/data/vital1.json', 'w') as file:
            json.dump(appointments, file)

    # Filter appointments for the current week
    appointments_for_week = [appointment for appointment in appointments if appointment["day"] == week_offset]

    # Return the template response
    return templates.TemplateResponse("TrueBeam1.html", {
        "request": request,
        "appointments": appointments_for_week,
        "week_dates": week_dates,
        "week_offset": week_offset
    })

@app.get("/TrueBeam2", response_class=HTMLResponse)
async def truebeam2(request: Request, week_offset: int = 0):
    week_dates = get_week_dates(week_offset)

    # Load appointments from file
    try:
        with open('static/data/vital2.json', 'r') as file:
            appointments = json.load(file)
    except FileNotFoundError:
        # If the file doesn't exist, initialize it as an empty list
        appointments = []
        with open('static/data/vital1.json', 'w') as file:
            json.dump(appointments, file)

    # Filter appointments for the current week
    appointments_for_week = [appointment for appointment in appointments if appointment["day"] == week_offset]

    # Return the template response
    return templates.TemplateResponse("TrueBeam2.html", {
        "request": request,
        "appointments": appointments_for_week,
        "week_dates": week_dates,
        "week_offset": week_offset
    })

@app.get("/Unique", response_class=HTMLResponse)
async def unique(request: Request, week_offset: int = 0):
    week_dates = get_week_dates(week_offset)

    # Load appointments from file
    try:
        with open('static/data/unique.json', 'r') as file:
            appointments = json.load(file)
    except FileNotFoundError:
        # If the file doesn't exist, initialize it as an empty list
        appointments = []
        with open('static/data/vital1.json', 'w') as file:
            json.dump(appointments, file)

    # Filter appointments for the current week
    appointments_for_week = [appointment for appointment in appointments if appointment["day"] == week_offset]

    # Return the template response
    return templates.TemplateResponse("Unique.html", {
        "request": request,
        "appointments": appointments_for_week,
        "week_dates": week_dates,
        "week_offset": week_offset
    })
#+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++

if __name__ == "__main__":
    uvicorn.run(app, host="localhost", port=8000, log_level="debug", reload=True)