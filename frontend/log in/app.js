
const login = document.getElementById("login-form");

login.addEventListener("submit", async (e) => {
    e.preventDefault();

    const email = document.getElementById("email").value.trim(),
        password = document.getElementById("password").value;

    if (!email || !password) {
        alert("Email yoki password kiritilmadi!")
        return;
    }
    if (!/\S+@\S+\.\S+/.test(email)) {
        alert("Email xato kiritdingiz!")
        return;
    }
    if (password.length < 6) {
        alert("Password uzunligi kamida 6 ga teng bo'lishi kerak!");
        return;
    }
    try {
        const login_response = await fetch("http://localhost:8000/login/",
            {
                method: "POST",
                headers:
                {
                    "Content-Type": "application/json"
                },
                body: JSON.stringify({
                    email: email,
                    password: password
                })
            }
        );
        const data = await login_response.json();
        if (login_response.ok){
            console.log("Success", data);
            window.location.href = "../user-page/index.html";
        }
        else{
        }
    }
    catch(error) {

    }
});