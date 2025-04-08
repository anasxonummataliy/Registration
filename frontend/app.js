const form = document.getElementById("register-form");

form.addEventListener('submit', async (e) => {
    e.preventDefault();

    // Forma maydonlaridan ma'lumotlarni olish
    const name = document.getElementById('name').value.trim(),
        email = document.getElementById('email').value.trim(),
        password = document.getElementById('password').value;

    // Oddiy validatsiya
    if (!name || !email || !password) {
        alert("Please fill in all required fields.");
        return;
    }

    if (!/\S+@\S+\.\S+/.test(email)) {
        alert("Please enter a valid email address.");
        return;
    }

    if (password.length < 6) {
        alert("Password must be at least 6 characters long.");
        return;
    }

    if (name.length < 2) {
        alert("Name must be at least 2 characters long.");
        return;
    }

    try {
        const response = await fetch("http://localhost:8000/regis/", {
            method: "POST",
            headers: {
                "Content-Type": "application/json"
            },
            body: JSON.stringify({
                name: name,
                email: email,
                password: password
            })
        });

        const data = await response.json();
        if (response.ok) {
            console.log("Success:", data);
            alert(`Registration successful! User ID: ${data.user_id}`);
            form.reset(); // Formani tozalash
            // Agar login sahifangiz bo'lsa, bu yerga yo'naltirish qo'shishingiz mumkin
            // window.location.href = "login.html";
        } else {
            console.error("Error:", data);
            alert(`Error: ${data.detail || data.message || "Unknown error"}`);
        }
    } catch (error) {
        console.error("Fetch error:", error);
        alert("Something went wrong. Please try again later.");
    }
});