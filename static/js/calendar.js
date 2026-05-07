document.addEventListener('DOMContentLoaded', function() {
  var calendarEl = document.getElementById('dashboard-calendar');
  if (!calendarEl) return;

  var calendar = new FullCalendar.Calendar(calendarEl, {
    initialView: 'dayGridMonth',
    timeZone: 'UTC',
    height: 'auto',
    headerToolbar: {
      left: 'prev,next today',
      center: 'title',
      right: 'dayGridMonth,timeGridWeek,timeGridDay'
    },
    events: {
      url: '/calendar/events/',
      method: 'GET'
    },
    eventClick: function(info) {
      if (info.event.url) {
        window.open(info.event.url, '_blank');
        info.jsEvent.preventDefault();
      }
    }
  });

  calendar.render();

  // Auto-refresh events every 60 seconds
  setInterval(function() {
    calendar.refetchEvents();
  }, 60000);
});
