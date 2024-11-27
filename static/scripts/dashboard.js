document.addEventListener('DOMContentLoaded', function () {
    const menuItems = document.querySelectorAll('.menu-item');
    const iframe = document.getElementById('content-frame');
    
    menuItems.forEach(item => {
        item.addEventListener('click', function (e) {
            // Check if the clicked item is not the logout link
            if (!item.href.includes('/logout')) {
                e.preventDefault();  // Prevent the default action (following the link)
                const target = item.getAttribute('data-target');
                iframe.src = target;  // Update the iframe src to load the new page
            }
        });
    });
});
