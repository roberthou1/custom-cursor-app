document.addEventListener('DOMContentLoaded', function() {
    // Modal functionality
    const modal = document.getElementById('privacy-modal');
    const privacyLink = document.getElementById('privacy-link');
    const closeBtn = document.getElementsByClassName('close')[0];
    
    // Open modal when privacy link is clicked
    privacyLink.addEventListener('click', function(e) {
        e.preventDefault();
        modal.style.display = 'block';
    });
    
    // Close modal when close button is clicked
    closeBtn.addEventListener('click', function() {
        modal.style.display = 'none';
    });
    
    // Close modal when clicking outside of it
    window.addEventListener('click', function(e) {
        if (e.target === modal) {
            modal.style.display = 'none';
        }
    });
    
    // Smooth scrolling for anchor links
    document.querySelectorAll('a[href^="#"]').forEach(anchor => {
        anchor.addEventListener('click', function(e) {
            if (this.getAttribute('href') === '#') return;
            
            e.preventDefault();
            
            document.querySelector(this.getAttribute('href')).scrollIntoView({
                behavior: 'smooth'
            });
        });
    });
    
    // Animate logo on hover
    const logo = document.getElementById('logo');
    if (logo) {
        logo.addEventListener('mouseover', function() {
            this.style.transform = 'rotate(10deg)';
        });
        
        logo.addEventListener('mouseout', function() {
            this.style.transform = 'rotate(0deg)';
        });
    }
});
