
form = document.getElementById("register-form");

form.addEventListener('submit', async (e) => {
    e.preventDefault();

    const name = document.getElementById('name').value,
        email = document.getElementById('email').value,
        password = document.getElementById('password').value;

    try {
        const response = await fetch("http://localhost:8000/registration", {
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
            console.log(data);
        }
        else {
            alert("Error" + data.message)
        }
    }
    catch (error) {
        console.error("Fetch error" + error);
        alert("Something went wrong");
    }

});