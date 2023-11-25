// Calculate the top offset in pixels
function calculateTopOffset(startTime) {
    const [hours, minutes] = startTime.split(':').map(Number);
    // Calculate how many minutes past 8:00 the start time is
    const totalMinutesFromStart = (hours - 8) * 60 + minutes;
    return totalMinutesFromStart * 1; // Assuming 1 pixel per minute
}
  
// Calculate the height of the appointment block in pixels
function calculateHeight(duration) {
    return duration * 1; // Assuming 1 pixel per minute
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
            var clickedTime = this.dataset.hour.padStart(2, '0') + ':00';
            form.elements['appointmentTime'].value = clickedTime;
            form.dataset.hour = this.dataset.hour;
            form.dataset.day = day;
            $(modal).modal('show');
          }
        });
      });
      
  
    // Handle form submission
    document.getElementById('addAppointmentForm').addEventListener('submit', function (event) {
        event.preventDefault();
        var time = this.elements['appointmentTime'].value;
        var patientName = this.elements['patientName'].value;
        var duration = parseInt(this.elements['appointmentDuration'].value, 10);
        var day = this.dataset.day;

        // Check if the selected time slot is available
        if (!isTimeSlotAvailable(day, time, duration)) {
            alert('This time slot is already occupied. Please choose another time.');
            return; // Prevent adding the appointment
        }
        var topOffset = 0;
    
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
  