// Calculate the top offset in pixels
function calculateTopOffset(startTime) {
  const [hours, minutes] = startTime.split(':').map(Number);
  // Calculate how many minutes past 8:00 the start time is
  const totalMinutesFromStart = minutes;
  return totalMinutesFromStart * 1; // Assuming 1 pixel per minute
}

// Calculate the height of the appointment block in pixels
function calculateHeight(duration) {
  return duration * 1; // Assuming 1 pixel per minute
}

function calculateEndTime(startTime, duration) {
  var [hour, minute] = startTime.split(':').map(Number);
  var endTime = new Date(0, 0, 0, hour, minute + duration);
  return endTime.getHours().toString().padStart(2, '0') + ':' + endTime.getMinutes().toString().padStart(2, '0');
}

function calculateAppointmentDate(dayOfWeek, weekOffset) {
  // Create a new date object for the current date
  var currentDate = new Date();

  // Calculate the number of days to add
  console.log(dayOfWeek);
  var d=(currentDate.getDay()+6)%7;
  var daysToAdd = ((weekOffset) * 7)+parseInt(dayOfWeek)-d;

  currentDate.setDate(currentDate.getDate()+daysToAdd);
  // Format the date as MM/DD/YYYY
  return  (parseInt(currentDate.getMonth())+1)+'/'+currentDate.getDate()+'/'+currentDate.getFullYear();
}

// function isTimeSlotAvailable(day, startTime, duration) {
//   const [startHours, startMinutes] = startTime.split(':').map(Number);
//   const startTotalMinutes = startHours * 60 + startMinutes;
//   const endTotalMinutes = startTotalMinutes + duration;

//   // Find all existing appointments for the selected day
//   const existingAppointments = document.querySelectorAll(`.day-slot[data-day="${day}"] .appointment-block`);
//   for (let appointment of existingAppointments) {
//     const [appStartHours, appStartMinutes] = appointment.textContent.split(' - ')[0].split(':').map(Number);
//     const appDuration = parseInt(appointment.style.height, 10);
//     const appStartTotalMinutes = appStartHours * 60 + appStartMinutes;
//     const appEndTotalMinutes = appStartTotalMinutes + appDuration;

//     // Check for overlap
//     if ((startTotalMinutes < appEndTotalMinutes) && (endTotalMinutes > appStartTotalMinutes)) {
//       return false; // Overlap found
//     }
//   }

//   return true; // No overlap, time slot is available
// }  
let loadedAppointments = []; // Global variable to store loaded appointments

function isTimeSlotAvailable(day, startTime, duration, appointments) {
    const [startHours, startMinutes] = startTime.split(':').map(Number);
    const startTotalMinutes = startHours * 60 + startMinutes;
    const endTotalMinutes = startTotalMinutes + duration;

    // Check for conflicts with existing appointment blocks in the DOM
    const existingBlocks = document.querySelectorAll(`.day-slot[data-day="${day}"] .appointment-block`);
    for (let block of existingBlocks) {
        const [blockStartHours, blockStartMinutes] = block.textContent.split(' - ')[0].split(':').map(Number);
        const blockDuration = parseInt(block.style.height, 10); // Assuming height is set in minutes
        const blockEndTotalMinutes = (blockStartHours * 60 + blockStartMinutes) + blockDuration;

        if ((startTotalMinutes < blockEndTotalMinutes) && (endTotalMinutes > blockStartHours * 60 + blockStartMinutes)) {
            return false; // Overlap found with DOM blocks
        }
    }

    // Check for conflicts with loaded appointments from JSON
    for (let appointment of appointments) {
        const appointmentDay = (new Date(appointment.date).getDay() + 6) % 7; // Convert to 0-6 (Mon-Sun)
        if (appointmentDay === day) {
            const [appStartHours, appStartMinutes] = appointment.start_time.split(':').map(Number);
            const [appEndHours, appEndMinutes] = appointment.end_time.split(':').map(Number);
            const appStartTotalMinutes = appStartHours * 60 + appStartMinutes;
            const appEndTotalMinutes = appEndHours * 60 + appEndMinutes;

            if ((startTotalMinutes < appEndTotalMinutes) && (endTotalMinutes > appStartTotalMinutes)) {
                return false; // Overlap found with JSON appointments
            }
        }
    }

    return true; // No overlap found, time slot is available
}

function getWeekOffsetFromURL() {
  // Get the week offset from the URL query parameters
  const urlParams = new URLSearchParams(window.location.search);
  return parseInt(urlParams.get('week_offset')) || 0;
}

function changeWeek(offsetChange) {
  var currentOffset = getWeekOffsetFromURL();
  var newOffset = currentOffset + offsetChange;
  window.location.search = 'week_offset=' + newOffset;
}

// function populateSchedule(appointments) {
//   // Clear current appointments from the schedule
//   document.querySelectorAll('.appointment-block').forEach(element => element.remove());

//   // Add each appointment to the schedule
//   appointments.forEach(appointment => {
//       // Convert appointment date and time to a day and hour that matches the schedule's format
//       const appointmentDate = new Date(appointment.date);
//       const dayOfWeek = appointmentDate.getDay(); // 0 (Sunday) to 6 (Saturday)
//       const [hour, minute] = appointment.start_time.split(':').map(Number);
      
//       // Assuming your schedule's day slots are marked with data attributes `data-day` and `data-hour`
//       const scheduleCell = document.querySelector(`.day-slot[data-day="${dayOfWeek}"][data-hour="${hour}"]`);

//       if (scheduleCell) {
//           const appointmentBlock = document.createElement('div');
//           appointmentBlock.className = 'appointment-block';
//           appointmentBlock.textContent = `${appointment.start_time} - ${appointment.patient_name}`;
//           scheduleCell.appendChild(appointmentBlock);
//       }
//   });
// }


// function loadAppointmentsForWeek() {
//   console.log("GAMOMIDZAXA");
//   weekOffset=getWeekOffsetFromURL();
//   fetch(`/get_appointments_for_week?week_offset=${weekOffset}`)
//       .then(response => response.json())
//       .then(data => {
//           populateSchedule(data.appointments);
//       })
//       .catch(error => console.error('Error:', error));
// }

function loadAppointmentsForWeek(weekOffset) {
  // Fetch appointments from your backend or local JSON
  fetch('/static/data/appointments.json')
      .then(response => response.json())
      .then(appointments => {
          populateSchedule(appointments, weekOffset);
      });
}

function populateSchedule(appointments, weekOffset) {
  // Clear existing appointments
  document.querySelectorAll('.appointment-block').forEach(el => el.remove());

  appointments.forEach(appointment => {
      if (isAppointmentInCurrentWeek(appointment, weekOffset)) {
          const appointmentElement = createAppointmentElement(appointment, weekOffset);
          placeAppointmentInSchedule(appointmentElement, appointment);
      }
  });
}

function isAppointmentInCurrentWeek(appointment, weekOffset) {
  const appointmentDate = new Date(appointment.date);
  const weekStart = new Date();
  weekStart.setDate(weekStart.getDate() - ((weekStart.getDay() +6)%7) + (weekOffset * 7));
  const weekEnd = new Date(weekStart);
  console.log(appointmentDate);
  weekEnd.setDate(weekEnd.getDate()+6);
  weekStart.setDate(weekStart.getDate()-1);
  return appointmentDate >= weekStart && appointmentDate <= weekEnd;
}

function createAppointmentElement(appointment, weekOffset) {
  const el = document.createElement('div');
  el.className = 'appointment-block';

  // Calculate the height of the appointment block based on duration
  const startTime = new Date('1970-01-01T' + appointment.start_time + 'Z');
  const endTime = new Date('1970-01-01T' + appointment.end_time + 'Z');
  const duration = (endTime - startTime) / (1000 * 60); // Duration in minutes
  el.style.height = calculateHeight(duration) + 'px';

  // Calculate the day of the week and format the appointment date
  const dayOfWeek = (new Date(appointment.date).getDay() + 6) % 7;
  const appointmentDate = calculateAppointmentDate(dayOfWeek, weekOffset);
  el.textContent = appointment.start_time + ' - ' + appointment.patient_name + ' - ' + appointmentDate;

  return el;
}

function placeAppointmentInSchedule(appointmentElement, appointment) {
  const dayOfWeek = (new Date(appointment.date).getDay()+6)%7; // Sunday = 0, Monday = 1, ...
  const hour = parseInt(appointment.start_time.split(':')[0]);
  const selector = `.day-slot[data-day="${dayOfWeek}"][data-hour="${hour}"] .appointment-container`;
  const cell = document.querySelector(selector);
  if (cell) {
      cell.appendChild(appointmentElement);
  }
}

document.addEventListener('DOMContentLoaded', function() {
  var weekOffset = getWeekOffsetFromURL();
  loadAppointmentsForWeek(weekOffset);
});

function calculateDurationInMinutes(startTime, endTime) {
  var start = new Date('01/01/2000 ' + startTime);
  var end = new Date('01/01/2000 ' + endTime);
  return (end - start) / 60000; // Divide by 60000 to convert milliseconds to minutes
}

document.addEventListener('DOMContentLoaded', function () {
  // Handle time slot click
  document.querySelectorAll('.day-slot').forEach(function (cell) {
      cell.addEventListener('click', function () {
        var day = this.dataset.day;
        if (day < 5) {
          var modal = document.getElementById('addPatientModal');
          var form = document.getElementById('addAppointmentForm');
          // Set the default time as the clicked time slot

          // Pre-fill the hour dropdown based on clicked time slot
          var clickedHour = this.dataset.hour.padStart(2, '0');
          form.elements['appointmentHour'].value = clickedHour;
          // var clickedTime = this.dataset.hour.padStart(2, '0') + ':00';
          // form.elements['appointmentTime'].value = clickedTime;
          form.dataset.hour = this.dataset.hour;
          form.dataset.day = day;
          $(modal).modal('show');
        }
      });
      var weekOffset = getWeekOffsetFromURL();

      document.getElementById('prevWeekButton').addEventListener('click', function() {
          changeWeek(-1); // Go to the previous week
      });
  
      document.getElementById('nextWeekButton').addEventListener('click', function() {
          changeWeek(1); // Go to the next week
      });
  
      // Load appointments for the current week
      loadAppointmentsForWeek(weekOffset);
  });
    
  // Event listener for clicking on an appointment
  document.addEventListener('click', function (event) {
      if (event.target.classList.contains('appointment-block')) {
        event.stopPropagation();  // Prevent the event from bubbling up
    
        const patientDetails = event.target.textContent;
        document.getElementById('patientDetails').textContent = patientDetails;
        const patientDetailsModal = document.getElementById('patientDetailsModal');
        $(patientDetailsModal).modal('show');
    
        // Configure the remove button
        document.getElementById('removePatientButton').onclick = function() {
          var patientDetails = event.target.closest('.appointment-block').textContent;
          var [startTime, patientName, date] = patientDetails.split(' - ');

          // console.log(startTime)
          // console.log(patientName)
          // console.log(date)

          const appointmentData = {
            start_time: startTime,
            date: date,
            machine_name: 'TrueBeam2'
        };
     
          
          fetch('/remove_appointment', {
            method: 'DELETE',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify(appointmentData)
        })
        .then(response => response.json())
        .then(data => {
            console.log('Success:', data);
            event.target.closest('.appointment-block').remove();
        })
        .catch((error) => {
            console.error('Error:', error);
        });
          
          
          event.target.remove(); // Remove the appointment block
          $(patientDetailsModal).modal('hide');
        };
      }
  });
  // Handle form submission
  document.getElementById('addAppointmentForm').addEventListener('submit', function (event) {
      event.preventDefault();

      
      var hour = this.elements['appointmentHour'].value;
      var minute = this.elements['appointmentMinute'].value;
      var time = hour + ':' + minute; // Concatenate hour and minute
      var startTime = hour + ':' + minute; // Concatenate hour and minute
      var topOffset = calculateTopOffset(startTime);

      event.preventDefault();

      var duration = parseInt(this.elements['appointmentDuration'].value, 10);
  
      var patientName = this.elements['patientName'].value;
      var patientId = parseInt(this.elements['patientId'].value, 10); // Assuming you have a field for patientId
      var endTime = calculateEndTime(startTime, duration); // You'll need to write this function
      var currentDate = new Date().toISOString().slice(0, 10); // Example current date in YYYY-MM-DD format
  
      var weekOffset = getWeekOffsetFromURL();
      var day = this.dataset.day; // Assuming you set this correctly
    

      console.log(calculateAppointmentDate(day, weekOffset));

      // PREPATING JSON DATA
      var appointmentDat = {
        patient_id: patientId,
        patient_name: patientName,
        start_time: startTime,
        end_time: endTime,
        date: calculateAppointmentDate(day, weekOffset),
        machine_name: 'TrueBeam2'
    };

      // 
      // Send this data to your FastAPI backend
      fetch('/add_appointment', {
          method: 'POST',
          headers: {
              'Content-Type': 'application/json'
          },
          body: JSON.stringify(appointmentDat)
      })
      .then(response => response.json())
      .then(data => {
          console.log('Success:', data);
          // Additional actions upon successful submission
      })
      .catch((error) => {
          console.error('Error:', error);
      });


      var patientName = this.elements['patientName'].value;
      var duration = parseInt(this.elements['appointmentDuration'].value, 10);
      var day = this.dataset.day;

      // Check if the selected time slot is available
      // if (!isTimeSlotAvailable(day, time, duration)) {
      //     alert('This time slot is already occupied. Please choose another time.');
      //     return; // Prevent adding the appointment
      // }
      if (!isTimeSlotAvailable(day, startTime, duration, loadedAppointments)) {
        alert('This time slot is already occupied. Please choose another time.');
        return; // Prevent adding the appointment
    }
      var blockHeight = calculateHeight(duration);
  
      var appointmentBlock = document.createElement('div');
      appointmentBlock.className = 'appointment-block';
      appointmentBlock.style.top = topOffset + 'px';
      appointmentBlock.style.height = blockHeight + 'px';
      appointmentBlock.textContent = time + ' - ' + patientName + ' - ' + calculateAppointmentDate(day, weekOffset);
      
      const [hours, minutes] = time.split(':').map(Number);
      var selectedCell = document.querySelector(`.day-slot[data-hour="${hours}"][data-day="${this.dataset.day}"] .appointment-container`);
      selectedCell.appendChild(appointmentBlock);
  
      $('#addPatientModal').modal('hide');
      this.reset();
  });
});