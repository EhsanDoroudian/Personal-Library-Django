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

// Password Visibility Toggle
const passwordInput = document.getElementById('password');
const togglePassword = document.getElementById('togglePassword');

togglePassword.addEventListener('click', () => {
   const type = passwordInput.getAttribute('type') === 'password' ? 'text' : 'password';
   passwordInput.setAttribute('type', type);
   togglePassword.classList.toggle('bi-eye-slash');
   togglePassword.classList.toggle('bi-eye');
});

// Form Submission
const loginForm = document.getElementById('loginForm');

loginForm.addEventListener('submit', function(e) {
   e.preventDefault();

   // Basic validation
   const email = document.getElementById('email').value;
   const password = document.getElementById('password').value;

   // Validation checks
   if (!email || !password) {
       showAlert('لطفاً ایمیل و رمز عبور خود را وارد کنید.', 'danger');
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
   submitBtn.innerHTML = '<i class="spinner-border spinner-border-sm me-2"></i>در حال ورود...';
   submitBtn.disabled = true;

   // Simulate API call
   setTimeout(() => {
       submitBtn.innerHTML = originalText;
       submitBtn.disabled = false;

       // Simulate successful login
       window.location.href = "#"; // Redirect to dashboard in real scenario
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

   loginForm.insertBefore(alertDiv, loginForm.firstChild);

   // Auto hide after 5 seconds
   setTimeout(() => {
       if (alertDiv) {
           alertDiv.remove();
       }
   }, 5000);
}

// Social login hover effects
const socialButtons = document.querySelectorAll('.social-login');
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

// Password toggle functionality
document.addEventListener('DOMContentLoaded', function() {
    const togglePassword = document.getElementById('togglePassword');
    const passwordInput = document.getElementById('id_password');
    
    if (togglePassword && passwordInput) {
        togglePassword.addEventListener('click', function() {
            // Toggle password visibility
            const type = passwordInput.getAttribute('type') === 'password' ? 'text' : 'password';
            passwordInput.setAttribute('type', type);
            
            // Toggle eye icon
            this.classList.toggle('bi-eye');
            this.classList.toggle('bi-eye-slash');
        });
    }
});