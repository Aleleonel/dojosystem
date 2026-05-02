
function toggleMenu() {
    document.getElementById("sidebar").classList.toggle("active");
}

// Fecha menu ao clicar fora
document.addEventListener('click', function (event) {
    const sidebar = document.getElementById("sidebar");
    const button = document.getElementById("menu-btn");

    if (!sidebar.contains(event.target) && !button.contains(event.target)) {
        sidebar.classList.remove("active");
    }
});