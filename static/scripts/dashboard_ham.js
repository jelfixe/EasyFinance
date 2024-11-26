document.addEventListener('DOMContentLoaded', function () {
    const hamburger = document.getElementById('hamburger');
    const sidebar = document.getElementById('sidebar');
    const mainContent = document.querySelector('.main-content');
    
    console.log(hamburger, sidebar, mainContent);  // Check if these are null
    
    if (hamburger && sidebar && mainContent) {
        hamburger.addEventListener('click', function() {
            sidebar.classList.toggle('active'); 
            mainContent.classList.toggle('active');  
        });
    } else {
        console.error('One or more required elements are missing!');
    }
});
