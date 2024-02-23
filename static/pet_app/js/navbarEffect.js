document.addEventListener('DOMContentLoaded', function () {
    const navbar = document.getElementById('navbar');
    const path = window.location.pathname;

    // Conditions for when the navbar should definitely have a background
    const alwaysVisiblePaths = ['/log-in/', '/dashboard/signup/petowner/', '/dashboard/signup/vetstaff/'];
    const isHomePage = path === '/'; // Adjust if your home page path is different

    if (isHomePage) {
        window.addEventListener('scroll', function () {
            if (window.scrollY > 50) {
                navbar.classList.add('bg-blue-500', 'bg-opacity-100');
            } else {
                navbar.classList.remove('bg-5lue-500', 'bg-opacity-100');
            }
        });

        navbar.addEventListener('mouseover', function () {
            navbar.classList.add('bg-blue-500', 'bg-opacity-100');
        });

        navbar.addEventListener('mouseout', function () {
            if (window.scrollY < 50) {
                navbar.classList.remove('bg-blue-500', 'bg-opacity-100');
            }
        });
    } else if (alwaysVisiblePaths.includes(path)) {
        // This ensures the navbar has a background on specific paths/pages
        navbar.classList.add('bg-blue-500', 'bg-opacity-100');
    }
});
