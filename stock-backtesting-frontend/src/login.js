// import './styles/index.css';

document.getElementById('confirm-button').addEventListener('click', () => {
    const username = document.getElementById('username').value;
    const password = document.getElementById('password').value;

    console.log("click")



    // Simple validation (you can replace this with actual authentication logic)
    if (username && password) {
        // Redirect to their portfolio page
        window.location.href = 'portfolio.html';
    } else {
        alert('Please enter both username and password.');
    }
});
