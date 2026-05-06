document.addEventListener('DOMContentLoaded', function() {
    const checkbox = document.querySelector('#id_is_current');
    const endDateField = document.querySelector('.field-end_date');

    function toggleEndDate() {
        if (checkbox && endDateField) {
            if (checkbox.checked) {
                endDateField.style.display = 'none';
            } else {
                endDateField.style.display = '';
            }
        }
    }

    if (checkbox) {
        checkbox.addEventListener('change', toggleEndDate);
        toggleEndDate();  // Run on page load
    }
});
