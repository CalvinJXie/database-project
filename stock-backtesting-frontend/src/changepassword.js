document.getElementById('confirm-change').addEventListener('click', async (e) => {
    e.preventDefault();

    const username = document.getElementById('username').value;
    const oldPassword = document.getElementById('old-password').value;
    const newPassword = document.getElementById('new-password').value;

    if (!username || !oldPassword || !newPassword) {
        alert('Please fill out all fields.');
        return;
    }

    try {
        const response = await fetch('http://localhost:5000/changepassword', {
            method: 'POST', // or PUT
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({
                username: username,
                old_password: oldPassword,
                new_password: newPassword
            })
        });

        const data = await response.json();

        if (response.ok) {
            alert('Password changed successfully!');
            window.location.href = 'login.html'; // redirect back
        } else {
            alert(`Error: ${data.message}`);
        }
    } catch (error) {
        console.error('Error:', error);
        alert('Failed to connect to the server');
    }
});
