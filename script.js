document.addEventListener('DOMContentLoaded', function() {
    const slider = document.getElementById('temperatureSlider');
    const indicator = document.getElementById('temperatureIndicator');

    slider.addEventListener('input', function() {
        const value = slider.value;
        const max = slider.max;
        const min = slider.min;
        const percentage = (value - min) / (max - min) * 100;
        indicator.style.height = `${percentage}%`;
    });

    // Initialize the indicator height based on the initial slider value
    const initialEvent = new Event('input');
    slider.dispatchEvent(initialEvent);
});
