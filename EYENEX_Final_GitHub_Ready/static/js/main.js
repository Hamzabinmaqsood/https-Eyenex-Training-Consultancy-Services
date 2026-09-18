document.addEventListener("DOMContentLoaded", function () {
    const navbar = document.querySelector(".glass-navbar");
    if (navbar) {
        const handleNavbarShadow = function () {
            navbar.classList.toggle("navbar-scrolled", window.scrollY > 16);
        };
        handleNavbarShadow();
        window.addEventListener("scroll", handleNavbarShadow, { passive: true });
    }

    document.querySelectorAll("#mainNavbar .nav-link:not(.dropdown-toggle), #mainNavbar .dropdown-item, #mainNavbar .nav-cta").forEach(function (link) {
        link.addEventListener("click", function () {
            const menu = document.getElementById("mainNavbar");
            if (menu && window.innerWidth < 992 && menu.classList.contains("show") && window.bootstrap) {
                bootstrap.Collapse.getOrCreateInstance(menu).hide();
            }
        });
    });
});
