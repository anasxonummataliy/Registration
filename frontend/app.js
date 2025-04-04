document.getElementById("submitBtn").addEventListener("click", function (e) {
        e.preventDefault();

        const form = document.getElementById("registerForm");
        const formData = new FormData(form);

        fetch("http://localhost:8000/register", {
            method: "POST",
            body: formData,
        })
        .then(response => response.json())
        .then(data => {
            console.log("Serverdan javob:", data);
            alert("Account yaratildi!");
        })
        .catch(error => {
            console.error("Xatolik:", error);
            alert("Xatolik yuz berdi.");
        });
    });
