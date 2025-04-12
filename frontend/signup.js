document.addEventListener('DOMContentLoaded', () => {
    const signupForm = document.getElementById('signup-form');
    const signupResult = document.getElementById('signup-result');
  
    signupForm.addEventListener('submit', async (e) => {
      e.preventDefault();
  
      const name = document.getElementById('signup-name').value;
      const email = document.getElementById('signup-email').value;
      const password = document.getElementById('signup-password').value;
  
      try {
        const response = await fetch('http://localhost:5001/api/auth/signup', {
          method: 'POST',
          headers: {
            'Content-Type': 'application/json'
          },
          body: JSON.stringify({ username: name, email, password })
        });
  
        const data = await response.json();
  
        if (response.ok) {
          // Save token and user_id
          localStorage.setItem('token', data.token);
          localStorage.setItem('user_id', data.user_id);
  
          // Redirect to home page
          window.location.href = 'index.html';
        } else {
          signupResult.textContent = data.message || 'Signup failed.';
        }
      } catch (error) {
        console.error('Signup error:', error);
        signupResult.textContent = 'An error occurred. Please try again.';
      }
    });
  });
  