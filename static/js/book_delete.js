// Dark/Light Mode Toggle
const toggleSwitch = document.querySelector('#checkbox');

function switchTheme(e) {
    if (e.target.checked) {
        document.body.classList.add('dark-mode');
        localStorage.setItem('theme', 'dark');
    } else {
        document.body.classList.remove('dark-mode');
        localStorage.setItem('theme', 'light');
    }    
}

toggleSwitch.addEventListener('change', switchTheme, false);

// Check for saved theme preference
const currentTheme = localStorage.getItem('theme');
if (currentTheme === 'dark') {
    document.body.classList.add('dark-mode');
    toggleSwitch.checked = true;
}

// Form Submission
const deleteForm = document.getElementById('deleteForm');

deleteForm.addEventListener('submit', function(e) {
    e.preventDefault();
    
    // Basic validation
    const confirmDelete = document.getElementById('confirmDelete').checked;
    
    if (!confirmDelete) {
        showAlert('لطفاً تایید کنید که می‌فهمید این عمل غیرقابل بازگشت است.', 'warning');
        return;
    }
    
    // Show loading state
    const submitBtn = this.querySelector('button[type="submit"]');
    const originalText = submitBtn.innerHTML;
    submitBtn.innerHTML = '<i class="spinner-border spinner-border-sm me-2"></i>در حال حذف...';
    submitBtn.disabled = true;
    
    // Simulate API call
    setTimeout(() => {
        submitBtn.innerHTML = originalText;
        submitBtn.disabled = false;
        
        // Show success modal
        const successModal = new bootstrap.Modal(document.getElementById('successModal'));
        successModal.show();
    }, 2000);
});

function showAlert(message, type) {
    // Remove existing alerts
    const existingAlert = document.querySelector('.alert-dismissible');
    if (existingAlert) {
        existingAlert.remove();
    }
    
    const alertDiv = document.createElement('div');
    alertDiv.className = `alert alert-${type} alert-dismissible fade show`;
    alertDiv.innerHTML = `
        <i class="bi bi-exclamation-triangle me-2"></i>
        ${message}
        <button type="button" class="btn-close" data-bs-dismiss="alert"></button>
    `;
    
    deleteForm.insertBefore(alertDiv, deleteForm.firstChild);
    
    // Auto hide after 5 seconds
    setTimeout(() => {
        if (alertDiv) {
            alertDiv.remove();
        }
    }, 5000);
}

// Cancel button functionality
const cancelBtn = document.querySelector('.btn-outline-secondary');
cancelBtn.addEventListener('click', function(e) {
    e.preventDefault();
    if (confirm('آیا از انصراف از حذف کتاب اطمینان دارید؟')) {
        window.location.href = '#'; // Redirect to books page
    }
});