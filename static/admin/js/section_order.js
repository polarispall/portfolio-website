(function() {
    'use strict';

    const DEFAULT_SECTIONS = [
        {id: 'about', name: 'About Me', visible: true, numbered: true},
        {id: 'skills', name: 'Skills & Technologies', visible: true, numbered: true},
        {id: 'experience', name: 'Experience', visible: true, numbered: true},
        {id: 'education', name: 'Education', visible: true, numbered: true},
        {id: 'projects', name: 'Featured Projects', visible: true, numbered: true},
        {id: 'schedule', name: 'Book Time With Me', visible: true, numbered: true},
        {id: 'contact', name: 'Get In Touch', visible: true, numbered: true},
    ];

    function initSectionOrder() {
        const list = document.getElementById('section-order-list');
        const hiddenInput = document.getElementById('id_section_order');
        const resetBtn = document.getElementById('reset-sections');

        if (!list || !hiddenInput) return;

        // Initialize SortableJS
        new Sortable(list, {
            animation: 150,
            handle: '.drag-handle',
            ghostClass: 'sortable-ghost',
            chosenClass: 'sortable-chosen',
            onEnd: function() {
                updateNumbers();
                saveState();
            }
        });

        // Update section numbers
        function updateNumbers() {
            const items = list.querySelectorAll('.section-item');
            let visibleIndex = 1;

            items.forEach(function(item) {
                const numberEl = item.querySelector('.section-number');
                const isVisible = item.dataset.visible === 'true';
                const isNumbered = item.dataset.numbered === 'true';

                if (isVisible && isNumbered) {
                    numberEl.textContent = String(visibleIndex).padStart(2, '0') + '.';
                    visibleIndex++;
                } else if (isVisible && !isNumbered) {
                    numberEl.textContent = '';
                } else {
                    numberEl.textContent = '--';
                }
            });
        }

        // Save current state to hidden input
        function saveState() {
            const items = list.querySelectorAll('.section-item');
            const sections = [];

            items.forEach(function(item) {
                sections.push({
                    id: item.dataset.id,
                    name: item.querySelector('.section-name-input').value,
                    visible: item.dataset.visible === 'true',
                    numbered: item.dataset.numbered === 'true'
                });
            });

            hiddenInput.value = JSON.stringify(sections);
        }

        // Toggle visibility - use event delegation with proper handling
        list.addEventListener('click', function(e) {
            // Find the button, whether we clicked on it or its child SVG
            const toggle = e.target.closest('.visibility-toggle');
            if (!toggle) return;

            e.preventDefault();
            e.stopPropagation();

            const item = toggle.closest('.section-item');
            if (!item) return;

            // Toggle the visibility
            const currentlyVisible = item.dataset.visible === 'true';
            const newVisible = !currentlyVisible;

            // Update data attribute
            item.dataset.visible = newVisible.toString();

            // Update classes
            if (newVisible) {
                item.classList.add('visible');
                item.classList.remove('hidden');
            } else {
                item.classList.remove('visible');
                item.classList.add('hidden');
            }

            updateNumbers();
            saveState();
        });

        // Update name on input change
        list.addEventListener('input', function(e) {
            if (e.target.classList.contains('section-name-input')) {
                saveState();
            }
        });

        // Reset to defaults
        if (resetBtn) {
            resetBtn.addEventListener('click', function(e) {
                e.preventDefault();

                if (confirm('Reset all sections to default order and names?')) {
                    // Clear and rebuild list
                    list.innerHTML = '';

                    DEFAULT_SECTIONS.forEach(function(section) {
                        const li = document.createElement('li');
                        li.className = 'section-item visible';
                        li.dataset.id = section.id;
                        li.dataset.visible = 'true';
                        li.dataset.numbered = 'true';

                        li.innerHTML = `
                            <span class="drag-handle">
                                <svg width="16" height="16" viewBox="0 0 16 16" fill="currentColor">
                                    <circle cx="4" cy="4" r="1.5"/>
                                    <circle cx="4" cy="8" r="1.5"/>
                                    <circle cx="4" cy="12" r="1.5"/>
                                    <circle cx="10" cy="4" r="1.5"/>
                                    <circle cx="10" cy="8" r="1.5"/>
                                    <circle cx="10" cy="12" r="1.5"/>
                                </svg>
                            </span>
                            <span class="section-number"></span>
                            <input type="text" class="section-name-input" value="${section.name}" data-original="${section.name}">
                            <button type="button" class="visibility-toggle" title="Toggle visibility">
                                <svg class="eye-open" width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                                    <path d="M1 12s4-8 11-8 11 8 11 8-4 8-11 8-11-8-11-8z"/>
                                    <circle cx="12" cy="12" r="3"/>
                                </svg>
                                <svg class="eye-closed" width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                                    <path d="M17.94 17.94A10.07 10.07 0 0 1 12 20c-7 0-11-8-11-8a18.45 18.45 0 0 1 5.06-5.94M9.9 4.24A9.12 9.12 0 0 1 12 4c7 0 11 8 11 8a18.5 18.5 0 0 1-2.16 3.19m-6.72-1.07a3 3 0 1 1-4.24-4.24"/>
                                    <line x1="1" y1="1" x2="23" y2="23"/>
                                </svg>
                            </button>
                        `;

                        list.appendChild(li);
                    });

                    updateNumbers();
                    saveState();
                }
            });
        }

        // Initial number update
        updateNumbers();
    }

    // Initialize when DOM is ready
    if (document.readyState === 'loading') {
        document.addEventListener('DOMContentLoaded', initSectionOrder);
    } else {
        initSectionOrder();
    }
})();
