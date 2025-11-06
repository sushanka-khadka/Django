document.addEventListener('DOMContentLoaded', function() {
  let alertWrappers = document.querySelectorAll('.alert');

  alertWrappers.forEach(alertWrapper => {
    let alertClose = alertWrapper.querySelector('.alert__close');

    const closeAlert = () => {
      alertWrapper.style.display = 'none';
    }

    // Manual close on click
    if (alertClose) {
      alertClose.addEventListener('click', closeAlert);
    }

    // auto close after 3 seconds
    setTimeout(closeAlert, 3000);

  });
});

