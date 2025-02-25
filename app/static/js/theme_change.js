document.addEventListener('DOMContentLoaded', () => {
    const themeRadios = document.querySelectorAll('input[name="theme"]');
    const threeDCheckbox = document.getElementById('3d-mode');
    const body = document.body;

    themeRadios.forEach(radio => {
        radio.addEventListener('change', () => {
            body.classList.remove('light-mode', 'dark-mode');
            if (radio.value === 'light') {
                body.classList.add('light-mode');
            } else {
                body.classList.add('dark-mode');
            }
            update3DMode();
        });
    });

    threeDCheckbox.addEventListener('change', update3DMode);

    function update3DMode() {
        if (threeDCheckbox.checked) {
            body.classList.add('red-3d', 'blue-3d');
        } else {
            body.classList.remove('red-3d', 'blue-3d');
        }
    }
});
