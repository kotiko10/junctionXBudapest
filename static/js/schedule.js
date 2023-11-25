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

function isTimeSlotAvailable(day, startTime, duration) {
  const [startHours, startMinutes] = startTime.split(':').map(Number);
  const startTotalMinutes = startHours * 60 + startMinutes;
  const endTotalMinutes = startTotalMinutes + duration;

  // Find all existing appointments for the selected day
  const existingAppointments = document.querySelectorAll(`.day-slot[data-day="${day}"] .appointment-block`);
  for (let appointment of existingAppointments) {
    const [appStartHours, appStartMinutes] = appointment.textContent.split(' - ')[0].split(':').map(Number);
    const appDuration = parseInt(appointment.style.height, 10);
    const appStartTotalMinutes = appStartHours * 60 + appStartMinutes;
    const appEndTotalMinutes = appStartTotalMinutes + appDuration;

    // Check for overlap
    if ((startTotalMinutes < appEndTotalMinutes) && (endTotalMinutes > appStartTotalMinutes)) {
      return false; // Overlap found
    }
  }

  return true; // No overlap, time slot is available
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
  
      // 
      var patientName = this.elements['patientName'].value;
      var patientId = parseInt(this.elements['patientId'].value, 10); // Assuming you have a field for patientId
      var startTime = hour + ':' + minute;
      var endTime = calculateEndTime(startTime, duration); // You'll need to write this function
      var currentDate = new Date().toISOString().slice(0, 10); // Example current date in YYYY-MM-DD format
  
      // PREPATING JSON DATA
      var appointmentDat = {
        patient_id: patientId,
        patient_name: patientName,
        start_time: startTime,
        end_time: endTime,
        date: currentDate,
        machine_name: 'VitalBeam1'
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
      if (!isTimeSlotAvailable(day, time, duration)) {
          alert('This time slot is already occupied. Please choose another time.');
          return; // Prevent adding the appointment
      }
      // var topOffset = 0;
  
      var blockHeight = calculateHeight(duration);
  
      var appointmentBlock = document.createElement('div');
      appointmentBlock.className = 'appointment-block';
      appointmentBlock.style.top = topOffset + 'px';
      appointmentBlock.style.height = blockHeight + 'px';
      appointmentBlock.textContent = time + ' - ' + patientName;
      
      const [hours, minutes] = time.split(':').map(Number);
      var selectedCell = document.querySelector(`.day-slot[data-hour="${hours}"][data-day="${this.dataset.day}"] .appointment-container`);
      selectedCell.appendChild(appointmentBlock);
  
      $('#addPatientModal').modal('hide');
      this.reset();
  });
});
