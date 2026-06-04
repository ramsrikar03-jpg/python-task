// Veloce Cinema - Global JS Enhancements

document.addEventListener('DOMContentLoaded', () => {
    // Auto-dismiss alert messages after 5 seconds
    const alerts = document.querySelectorAll('.flash-alert');
    alerts.forEach(alert => {
        setTimeout(() => {
            alert.style.transition = 'opacity 0.6s ease, transform 0.6s ease';
            alert.style.opacity = '0';
            alert.style.transform = 'translateY(-10px)';
            setTimeout(() => {
                alert.remove();
            }, 600);
        }, 5000);
    });

    // Add subtle visual interactions if needed
    console.log("Veloce Cinema UI Loaded successfully.");
});
