document.getElementById('login-form').addEventListener('submit', async (e) => {
    e.preventDefault(); // Prevent form from refreshing the page
  
    const email = document.getElementById('login-email').value;
    const password = document.getElementById('login-password').value;
  
    try {
      const response = await fetch('http://localhost:5001/api/auth/login', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json'
        },
        body: JSON.stringify({ email, password })
      });
  
      const data = await response.json();
  
      if (response.ok) {
        // Save token and user ID to localStorage
        localStorage.setItem('token', data.token);
        localStorage.setItem('user_id', data.user.id);
        
        // Redirect to homepage
        window.location.href = 'index.html';
      } else {
        document.getElementById('login-result').textContent = data.message || 'Login failed.';
      }
    } catch (err) {
      console.error('Login Error:', err);
      document.getElementById('login-result').textContent = 'Something went wrong!';
    }
  });
  