// // ############################################################
// // GLOBAL INTERACTIVITY
// // ############################################################

function validateRegister() {
    const pass = document.getElementById('password').value;
    const confirm = document.getElementById('confirmPassword').value;

    if (pass !== confirm) {
        alert("❌ Error: Passwords do not match!");
        return false;
    }
    alert("✅ Registration successful! Welcome to the bookstore.");
    window.location.href = "login.html"; // Redirects to login page
    return false; // Prevent form reload for demo
}

function addToCart() {
    alert("🛒 Added to cart! (This is a frontend demo)");
}