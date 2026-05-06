document.addEventListener('DOMContentLoaded', function() {
    const checkbox = document.querySelector('#id_use_font_awesome');
    const iconClassField = document.querySelector('.field-icon_class');
    const customIconField = document.querySelector('.field-custom_icon');

    function toggleFields() {
        if (checkbox && iconClassField && customIconField) {
            if (checkbox.checked) {
                iconClassField.style.display = '';
                customIconField.style.display = 'none';
            } else {
                iconClassField.style.display = 'none';
                customIconField.style.display = '';
            }
        }
    }

    if (checkbox) {
        checkbox.addEventListener('change', toggleFields);
        toggleFields();  // Run on page load
    }
});
