// Function to handle form submission
function submitForm(event) {
    event.preventDefault(); // Prevent the default form submission
  
    // Get the email address entered by the user
    const email = document.querySelector('input[name="email"]').value;
  
    // Validate the email address
    if (!email || !email.includes('@')) {
      alert('Please enter a valid email address.');
      return;
    }
  
    // Send a request to the backend to subscribe to email notifications
    fetch('/subscribe', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json'
      },
      body: JSON.stringify({ email })
    })
      .then(response => response.json())
      .then(data => {
        if (data.success) {
          alert('Successfully subscribed to email notifications!');
        } else {
          alert('Failed to subscribe to email notifications. Please try again later.');
        }
      })
      .catch(error => {
        console.error('Error:', error);
        alert('An error occurred while subscribing to email notifications. Please try again later.');
      });
  }
  
  // Add a form submit event listener
  document.querySelector('form').addEventListener('submit', submitForm);
  