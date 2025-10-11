// Dark/Light Mode Toggle
const toggleSwitch = document.querySelector('#checkbox');

function switchTheme(e) {
    if (e.target.checked) {
        document.body.classList.add('dark-mode');
    } else {
        document.body.classList.remove('dark-mode');
    }    
}

toggleSwitch.addEventListener('change', switchTheme, false);

// Password Strength Checker
const passwordInput = document.getElementById('password');
const strengthBar = document.getElementById('strengthBar');
const strengthText = document.getElementById('strengthText');

passwordInput.addEventListener('input', function() {
    const password = this.value;
    const strength = checkPasswordStrength(password);
    
    strengthBar.className = 'password-strength-bar';
    
    if (password.length === 0) {
        strengthBar.style.width = '0%';
        strengthText.textContent = 'رمز عبور حداقل ۸ کاراکتر باشد';
        strengthText.className = 'text-muted';
    } else if (strength < 3) {
        strengthBar.classList.add('strength-weak');
        strengthText.textContent = 'رمز عبور ضعیف';
        strengthText.className = 'text-danger';
    } else if (strength < 5) {
        strengthBar.classList.add('strength-medium');
        strengthText.textContent = 'رمز عبور متوسط';
        strengthText.className = 'text-warning';
    } else {
        strengthBar.classList.add('strength-strong');
        strengthText.textContent = 'رمز عبور قوی';
        strengthText.className = 'text-success';
    }
});

function checkPasswordStrength(password) {
    let strength = 0;
    
    if (password.length >= 8) strength++;
    if (password.match(/[a-z]/)) strength++;
    if (password.match(/[A-Z]/)) strength++;
    if (password.match(/[0-9]/)) strength++;
    if (password.match(/[^a-zA-Z0-9]/)) strength++;
    
    return strength;
}

// Confirm Password Validation
const confirmPasswordInput = document.getElementById('confirmPassword');

confirmPasswordInput.addEventListener('input', function() {
    const password = passwordInput.value;
    const confirmPassword = this.value;
    
    if (confirmPassword && password !== confirmPassword) {
        this.setCustomValidity('رمز عبور و تکرار آن باید یکسان باشند');
        this.classList.add('is-invalid');
    } else {
        this.setCustomValidity('');
        this.classList.remove('is-invalid');
        if (confirmPassword) {
            this.classList.add('is-valid');
        }
    }
});

// Form Submission
const signupForm = document.getElementById('signupForm');

signupForm.addEventListener('submit', function(e) {
    e.preventDefault();
    
    // Basic validation
    const firstName = document.getElementById('firstName').value;
    const lastName = document.getElementById('lastName').value;
    const email = document.getElementById('email').value;
    const password = document.getElementById('password').value;
    const confirmPassword = document.getElementById('confirmPassword').value;
    const terms = document.getElementById('terms').checked;
    
    // Validation checks
    if (!firstName || !lastName || !email || !password || !confirmPassword) {
        showAlert('لطفاً تمام فیلدهای ضروری را پر کنید.', 'danger');
        return;
    }
    
    if (password !== confirmPassword) {
        showAlert('رمز عبور و تکرار آن باید یکسان باشند.', 'danger');
        return;
    }
    
    if (password.length < 8) {
        showAlert('رمز عبور باید حداقل ۸ کاراکتر باشد.', 'danger');
        return;
    }
    
    if (!terms) {
        showAlert('برای ثبت نام باید شرایط و قوانین را بپذیرید.', 'warning');
        return;
    }
    
    // Email validation
    const emailPattern = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
    if (!emailPattern.test(email)) {
        showAlert('لطفاً آدرس ایمیل معتبری وارد کنید.', 'danger');
        return;
    }
    
    // Show loading state
    const submitBtn = this.querySelector('button[type="submit"]');
    const originalText = submitBtn.innerHTML;
    submitBtn.innerHTML = '<i class="spinner-border spinner-border-sm me-2"></i>در حال ثبت نام...';
    submitBtn.disabled = true;
    
    // Simulate API call
    setTimeout(() => {
        submitBtn.innerHTML = originalText;
        submitBtn.disabled = false;
        
        // Show success modal
        const successModal = new bootstrap.Modal(document.getElementById('successModal'));
        successModal.show();
        
        // Clear form
        this.reset();
        document.getElementById('strengthBar').style.width = '0%';
        strengthText.textContent = 'رمز عبور حداقل ۸ کاراکتر باشد';
        strengthText.className = 'text-muted';
    }, 2000);
});

function showAlert(message, type) {
    // Remove existing alerts
    const existingAlert = document.querySelector('.alert');
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
    
    signupForm.insertBefore(alertDiv, signupForm.firstChild);
    
    // Auto hide after 5 seconds
    setTimeout(() => {
        if (alertDiv) {
            alertDiv.remove();
        }
    }, 5000);
}

// Feature item hover effects
const featureItems = document.querySelectorAll('.feature-item');
featureItems.forEach(item => {
    item.addEventListener('mouseenter', () => {
        item.style.transform = 'translateY(-5px)';
    });
    
    item.addEventListener('mouseleave', () => {
        item.style.transform = 'translateY(0)';
    });
});

// Social login hover effects
const socialButtons = document.querySelectorAll('.social-signup');
socialButtons.forEach(button => {
    button.addEventListener('mouseenter', () => {
        button.style.borderColor = 'var(--primary-color)';
        button.style.transform = 'translateY(-2px)';
    });

    button.addEventListener('mouseleave', () => {
        button.style.borderColor = '#e0e0e0';
        button.style.transform = 'translateY(0)';
    });
});