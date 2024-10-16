// Simulate user login status
const isLoggedIn = true; // Change to false to simulate logged out state

// Show/hide upload section based on login status
if (isLoggedIn) {
    document.getElementById('upload-link').style.display = 'block';
    document.getElementById('upload-sidebar').style.display = 'block';
    document.getElementById('upload-section').style.display = 'block';
}

// Handle form submission for data upload
document.getElementById('upload-form').addEventListener('submit', function(event) {
    event.preventDefault();

    const uploadData = {
        country: document.getElementById('country').value,
        state: document.getElementById('state').value,
        industry: document.getElementById('industry').value,
        sub_industry: document.getElementById('sub-industry').value,
        city: document.getElementById('city').value
    };

    fetch('/api/upload', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify(uploadData)
    })
    .then(response => response.json())
    .then(data => {
        alert(data.message);
        document.getElementById('upload-form').reset();
    })
    .catch((error) => {
        console.error('Error:', error);
    });
});

/*FAQS */
document.querySelectorAll('.faq-button').forEach(button => {
    button.addEventListener('click', () => {
        const answer = button.parentElement.nextElementSibling;
        const isVisible = answer.style.display === 'block';

        // Toggle visibility of the clicked answer
        answer.style.display = isVisible ? 'none' : 'block';
    });
});

