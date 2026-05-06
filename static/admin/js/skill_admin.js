(function() {
    'use strict';

    document.addEventListener('DOMContentLoaded', function() {
        const checkbox = document.querySelector('#id_use_font_awesome');
        if (!checkbox) return;

        // Find the fieldsets/field containers
        const iconClassField = document.querySelector('.field-icon_class');
        const customIconField = document.querySelector('.field-custom_icon');

        function toggleFields() {
            if (checkbox.checked) {
                // Show Font Awesome field, hide custom icon
                if (iconClassField) iconClassField.style.display = '';
                if (customIconField) customIconField.style.display = 'none';
            } else {
                // Hide Font Awesome field, show custom icon
                if (iconClassField) iconClassField.style.display = 'none';
                if (customIconField) customIconField.style.display = '';
            }
        }

        // Toggle on change
        checkbox.addEventListener('change', toggleFields);

        // Initial state on page load
        toggleFields();
    });
})();
