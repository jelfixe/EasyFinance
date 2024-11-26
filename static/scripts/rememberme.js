window.addEventListener('DOMContentLoaded', (event) => {
    // Check if 'Remember Me' credentials are saved
    const savedCredentials = localStorage.getItem('userCredentials');
    if (savedCredentials) {
        const { username, password } = JSON.parse(savedCredentials);
        document.getElementById('username').value = username;
        document.getElementById('password').value = password;
        document.getElementById('rememberMe').checked = true;
    }

    // Handle form submission
    const loginForm = document.getElementById('loginForm');
    loginForm.addEventListener('submit', function(event) {
        const rememberMe = document.getElementById('rememberMe').checked;
        if (rememberMe) {
            // Save credentials to localStorage
            const username = document.getElementById('username').value;
            const password = document.getElementById('password').value;
            const credentials = { username, password };
            localStorage.setItem('userCredentials', JSON.stringify(credentials));
        } else {
            // Remove credentials from localStorage
            localStorage.removeItem('userCredentials');
        }
    });
});
