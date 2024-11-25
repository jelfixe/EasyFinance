// Toggle the sidebar visibility on hamburger menu click
const hamburgerMenu = document.getElementById('hamburgerMenu');
const sidebar = document.getElementById('sidebar');

hamburgerMenu.addEventListener('click', () => {
    sidebar.classList.toggle('active');
});

// Tab switching logic
function changeTab(tabIndex) {
    const tabs = document.querySelectorAll('.tab-button');
    const panels = document.querySelectorAll('.tab-panel');
    
    tabs.forEach((tab, index) => {
        tab.classList.remove('active');
        panels[index].classList.remove('active');
    });
    
    tabs[tabIndex].classList.add('active');
    panels[tabIndex].classList.add('active');
}
