
document.getElementById('registerLink').addEventListener('click', (e) => {
  e.preventDefault();
  window.location.href = 'register.html'; 
});

if (window.location.pathname.includes('register.html')) {
  document.getElementById('registerForm').addEventListener('submit', (e) => {
    e.preventDefault();

    
    const email = document.getElementById('regEmail').value;
    const password = document.getElementById('regPassword').value;
    const confirmPassword = document.getElementById('confirmPassword').value;

    
    if (!email || !password || !confirmPassword) {
      alert('Please fill in all fields.');
      return;
    }

    if (password !== confirmPassword) {
      alert('Passwords do not match.');
      return;
    }

    
    const userData = { email, password };
    localStorage.setItem('registeredUser', JSON.stringify(userData));

    
    alert('Registration successful! Please login.');
    window.location.href = 'login.html';
  });
}


if (window.location.pathname.includes('login.html')) {
  document.getElementById('loginForm').addEventListener('submit', (e) => {
    e.preventDefault();

    
    const email = document.getElementById('email').value;
    const password = document.getElementById('password').value;

    
    const registeredUser = JSON.parse(localStorage.getItem('registeredUser'));

    
    if (registeredUser && email === registeredUser.email && password === registeredUser.password) {
      alert('Login successful! Redirecting to home page...');
      window.location.href = 'home.html'; 
    } else {
      alert('Invalid email or password. Please try again.');
    }
  });
}