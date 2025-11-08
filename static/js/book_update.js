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

// Image Preview
const bookImageInput = document.getElementById('book_image');
const imagePreview = document.getElementById('image_preview');

bookImageInput.addEventListener('input', () => {
    const url = bookImageInput.value;
    if (url) {
        imagePreview.src = url;
        imagePreview.style.display = 'block';
    } else {
        imagePreview.style.display = 'none';
        imagePreview.src = '';
    }
});