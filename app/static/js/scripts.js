document.addEventListener("DOMContentLoaded", function () {
    const footer = document.querySelector(".footer");
    const toggleButton = document.getElementById("footer-toggle");

    // Check localStorage for footer state
    const footerState = localStorage.getItem("footerVisible");
    if (footerState === "hidden") {
        footer.style.display = "none";
        toggleButton.textContent = "▲"; // Change to "show" icon
    } else {
        footer.style.display = "block";
        toggleButton.textContent = "▼"; // Correct icon for shown state
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
