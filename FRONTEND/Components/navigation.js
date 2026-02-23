// Mobile navigation initialization
document.addEventListener('DOMContentLoaded', function () {
    const navToggle = document.getElementById('navToggle');
    const navMenu = document.getElementById('navMenu');
    const navOverlay = document.getElementById('navOverlay');
    const closeSidebar = document.getElementById('closeSidebar');

    if (navToggle && navMenu) {
        navToggle.addEventListener('click', function () {
            navMenu.classList.toggle('active');
            this.classList.toggle('active');
            if (navOverlay) navOverlay.classList.toggle('active');
        });

        // Close mobile menu when clicking on close button
        if (closeSidebar) {
            closeSidebar.addEventListener('click', function () {
                navMenu.classList.remove('active');
                navToggle.classList.remove('active');
                if (navOverlay) navOverlay.classList.remove('active');
            });
        }

        // Close mobile menu when clicking on overlay
        if (navOverlay) {
            navOverlay.addEventListener('click', function () {
                navMenu.classList.remove('active');
                navToggle.classList.remove('active');
                navOverlay.classList.remove('active');
            });
        }

        // Close mobile menu when clicking on a link
        const navLinks = document.querySelectorAll('.nav-link');
        navLinks.forEach(link => {
            link.addEventListener('click', () => {
                navMenu.classList.remove('active');
                navToggle.classList.remove('active');
                if (navOverlay) navOverlay.classList.remove('active');
            });
        });
    }
});