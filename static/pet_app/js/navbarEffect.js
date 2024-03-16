document.addEventListener('DOMContentLoaded', function () {
    const navbar = document.getElementById('navbar');
    const path = window.location.pathname;

    // Utility function to get cookie value by name
    function getCookie(name) {
        let cookieValue = null;
        if (document.cookie && document.cookie !== '') {
            const cookies = document.cookie.split(';');
            for (let i = 0; i < cookies.length; i++) {
                const cookie = cookies[i].trim();
                if (cookie.substring(0, name.length + 1) === (name + '=')) {
                    cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                    break;
                }
            }
        }
        return cookieValue;
    }

    // Function to determine if the user is logged in
    function isUserLoggedIn() {
        // Use the getCookie function to check for "loggedIn" cookie's value
        const loggedInValue = getCookie('loggedIn');
        // Compare the value to "true" (ensure to match the type and value, considering the value from cookies are strings)
        return loggedInValue === 'true';
    }

    // Conditions for when the navbar should have a background based on authentication and path
    const alwaysVisiblePaths = ['/log-in/', '/dashboard/signup/petowner/', '/dashboard/signup/vetstaff/'];
    const isHomePage = path === '/'; // Adjust if your home page path is different
    const isLoggedIn = isUserLoggedIn(); // Check if user is logged in

    // Apply different styles based on login status and page
    if (isHomePage && !isLoggedIn) {
        // Specific logic for unauthenticated users on the homepage
        window.addEventListener('scroll', function () {
            if (window.scrollY > 50) {
                navbar.classList.add('bg-blue-500', 'text-white');
            } else {
                navbar.classList.remove('bg-blue-500', 'text-white');
            }
        });

        navbar.addEventListener('mouseover', function () {
            navbar.classList.add('bg-blue-500', 'text-white');
        });

        navbar.addEventListener('mouseout', function () {
            if (window.scrollY < 50) {
                navbar.classList.remove('bg-blue-500', 'text-white');
            }
        });
    } else if (isLoggedIn || alwaysVisiblePaths.includes(path)) {
        // Logic for authenticated users or specific paths
        navbar.classList.add('bg-blue-500', 'text-white', 'bg-opacity-100');
    } else {
        // Default logic for other cases (e.g., authenticated user not on the homepage)
        navbar.classList.remove('bg-blue-500', 'text-white');
        navbar.classList.add('bg-blue-500', 'bg-opacity-100');
    }
});
