// Optional: Use JS for confirmation before submitting the purchase form
document.querySelectorAll('form').forEach(function(form) {
    form.addEventListener('submit', function(e) {
        if (!confirm("Are you sure you want to purchase this PDF?")) {
            e.preventDefault();  // Prevent form submission if user cancels
        }
    });
});
