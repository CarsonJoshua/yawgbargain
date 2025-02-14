document.addEventListener("DOMContentLoaded", function() {
    const footer = document.querySelector(".footer");
    const toggleButton = document.getElementById("toggle-footer");

    toggleButton.addEventListener("click", function() {
        footer.classList.toggle("hidden");
        toggleButton.innerText = footer.classList.contains("hidden") ? "▼" : "▲";
    });
});
