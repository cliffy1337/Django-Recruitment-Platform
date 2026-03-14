// Main JavaScript file for recruitment platform

document.addEventListener('DOMContentLoaded', function() {
    // Mobile menu toggle
    const mobileMenuButton = document.getElementById('mobile-menu-button');
    const mobileMenu = document.getElementById('mobile-menu');

    if (mobileMenuButton && mobileMenu) {
        mobileMenuButton.addEventListener('click', function() {
            mobileMenu.classList.toggle('hidden');
        });
    }

    // Close mobile menu when clicking a link (optional)
    const mobileLinks = mobileMenu ? mobileMenu.querySelectorAll('a') : [];
    mobileLinks.forEach(link => {
        link.addEventListener('click', function() {
            mobileMenu.classList.add('hidden');
        });
    });

    // Smooth scroll for anchor links (if any)
    document.querySelectorAll('a[href^="#"]').forEach(anchor => {
        anchor.addEventListener('click', function (e) {
            const href = this.getAttribute('href');
            if (href === "#") return;
            const target = document.querySelector(href);
            if (target) {
                e.preventDefault();
                target.scrollIntoView({ behavior: 'smooth' });
            }
        });
    });

    // Add active class to current navigation item (based on URL)
    const currentPath = window.location.pathname;
    const navLinks = document.querySelectorAll('nav a');
    navLinks.forEach(link => {
        const linkPath = link.getAttribute('href');
        if (linkPath && currentPath.startsWith(linkPath) && linkPath !== '/') {
            link.classList.add('text-indigo-600', 'font-semibold');
        } else if (linkPath === '/' && currentPath === '/') {
            link.classList.add('text-indigo-600', 'font-semibold');
        }
    });

    // Optional: dynamic greeting based on time of day
    const greetingElement = document.querySelector('[data-greeting]');
    if (greetingElement) {
        const hour = new Date().getHours();
        let greeting = 'Good morning';
        if (hour >= 12 && hour < 18) greeting = 'Good afternoon';
        else if (hour >= 18) greeting = 'Good evening';
        greetingElement.textContent = greeting;
    }
});