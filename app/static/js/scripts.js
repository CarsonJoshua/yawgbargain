document.addEventListener("DOMContentLoaded", function () {
    const footer = document.getElementById("footer");
    const toggleButton = document.getElementById("footer-toggle");

    // Check localStorage for footer state
    const footerState = localStorage.getItem("footerVisible");
    if (footerState === "hidden") {
        footer.style.display = "none";
        toggleButton.textContent = "▲"; // Change to "show" icon
    }

    // Toggle footer visibility
    toggleButton.addEventListener("click", function () {
        if (footer.style.display === "none") {
            footer.style.display = "block";
            localStorage.setItem("footerVisible", "shown");
            toggleButton.textContent = "▼"; // Change to "hide" icon
        } else {
            footer.style.display = "none";
            localStorage.setItem("footerVisible", "hidden");
            toggleButton.textContent = "▲"; // Change to "show" icon
        }
    });
});
