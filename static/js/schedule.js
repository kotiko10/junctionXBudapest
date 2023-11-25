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
  // Calculate the top offset in pixels
// function calculateTopOffset(startTime) {
//     const [hours, minutes] = startTime.split(':').map(Number);
//     return ((hours - 8) * 60 + minutes) * 1; // 1 pixel per minute
//   }
  
  // Calculate the height of the appointment block in pixels
  function calculateHeight(duration) {
    return duration * 1; // 1 pixel per minute
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
        var topOffset = calculateTopOffset(time);
    
        var blockHeight = calculateHeight(duration);
    
        var appointmentBlock = document.createElement('div');
        appointmentBlock.className = 'appointment-block';
        appointmentBlock.style.top = topOffset + 'px';
        appointmentBlock.style.height = blockHeight + 'px';
        appointmentBlock.textContent = time + ' - ' + patientName;
    
        var selectedCell = document.querySelector(`.day-slot[data-hour="${this.dataset.hour}"][data-day="${this.dataset.day}"] .appointment-container`);
        selectedCell.appendChild(appointmentBlock);
    
        $('#addPatientModal').modal('hide');
        this.reset();
    });
  });
  