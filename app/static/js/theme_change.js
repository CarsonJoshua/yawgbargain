document.addEventListener('DOMContentLoaded', () => {
    const themeRadios = document.querySelectorAll('input[name="theme"]');
    const threeDCheckbox = document.getElementById('3d-mode');
    const body = document.body;

    // Load saved settings from localStorage
    const savedTheme = localStorage.getItem('theme');
    const saved3DMode = localStorage.getItem('threeDMode') === 'true';

    if (savedTheme) {
        body.classList.add(savedTheme);
        const themeRadio = document.querySelector(`input[name="theme"][value="${savedTheme}"]`);
        if (themeRadio) {
            themeRadio.checked = true;
        }
        
    }

    if (saved3DMode) {
        body.classList.add('three-d-mode');
        threeDCheckbox.checked = true;
    }

    // Update theme selection
    themeRadios.forEach(radio => {
        radio.addEventListener('change', () => {
            body.classList.remove('light-mode', 'dark-mode');
            body.classList.add(radio.value);
            localStorage.setItem('theme', radio.value);
            update3DMode();
        });
    });

    // Update 3D mode selection
    threeDCheckbox.addEventListener('change', () => {
        update3DMode();
        localStorage.setItem('threeDMode', threeDCheckbox.checked);
    });

    function update3DMode() {
        if (threeDCheckbox.checked) {
            body.classList.add('three-d-mode');
        } else {
            body.classList.remove('three-d-mode');
        }
    }
});
