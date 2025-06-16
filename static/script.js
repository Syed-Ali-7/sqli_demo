document.getElementById('loginForm').addEventListener('submit', function (e) {
  e.preventDefault();

  const username = document.getElementById('username').value;
  const password = document.getElementById('password').value;

  fetch('/login', {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
    },
    body: JSON.stringify({ username, password }),
  })
    .then((response) => response.json())
    .then((data) => {
      const messageDiv = document.getElementById('message');
      const studentDataDiv = document.getElementById('studentData');

      if (data.error) {
        messageDiv.textContent = data.error;
        messageDiv.className = 'message error';
        studentDataDiv.innerHTML = '';
      } else {
        messageDiv.textContent = 'Login successful!';
        messageDiv.className = 'message success';

        let html = '<h3>Student Information</h3>';
        for (const [key, value] of Object.entries(data.student)) {
          html += `<p><strong>${key}:</strong> ${value}</p>`;
        }
        studentDataDiv.innerHTML = html;
      }
    })
    .catch((error) => {
      console.error('Error:', error);
      const message = document.getElementById('message');
      message.textContent = 'An error occurred';
      message.className = 'message error';
    });
});

// Password visibility toggle
document.getElementById('togglePassword').addEventListener('click', function () {
  const passwordInput = document.getElementById('password');
  const type = passwordInput.getAttribute('type');

  if (type === 'password') {
    passwordInput.setAttribute('type', 'text');
    this.textContent = '🙈'; 
  } else {
    passwordInput.setAttribute('type', 'password');
    this.textContent = '👁'; 
  }
});
