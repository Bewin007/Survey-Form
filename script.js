// Redirect to Registration Page
document.getElementById('registerLink').addEventListener('click', (e) => {
  e.preventDefault(); // Prevent default link behavior
  window.location.href = 'register.html'; // Redirect to registration page
});

// Handle Registration Form Submission (on register.html)
if (window.location.pathname.includes('register.html')) {
  document.getElementById('registerForm').addEventListener('submit', (e) => {
    e.preventDefault();

    // Get input values
    const email = document.getElementById('regEmail').value;
    const password = document.getElementById('regPassword').value;
    const confirmPassword = document.getElementById('confirmPassword').value;

    // Basic validation
    if (!email || !password || !confirmPassword) {
      alert('Please fill in all fields.');
      return;
    }

    if (password !== confirmPassword) {
      alert('Passwords do not match.');
      return;
    }

    // Save user data to localStorage
    const userData = { email, password };
    localStorage.setItem('registeredUser', JSON.stringify(userData));

    // Notify user and redirect back to the login page
    alert('Registration successful! Please login.');
    window.location.href = 'login.html';
  });
}

// Handle Login Form Submission (on login.html)
if (window.location.pathname.includes('login.html')) {
  document.getElementById('loginForm').addEventListener('submit', (e) => {
    e.preventDefault();

    // Get input values
    const email = document.getElementById('email').value;
    const password = document.getElementById('password').value;

    // Retrieve registered user data from localStorage
    const registeredUser = JSON.parse(localStorage.getItem('registeredUser'));

    // Validate credentials
    if (registeredUser && email === registeredUser.email && password === registeredUser.password) {
      alert('Login successful! Redirecting to home page...');
      window.location.href = 'home.html'; // Redirect to home page
    } else {
      alert('Invalid email or password. Please try again.');
    }
  });
}