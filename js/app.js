document.addEventListener("DOMContentLoaded", () => {
    const form = document.getElementById("contact-form");
    const resultMessage = document.getElementById("result-message");

    form.addEventListener("submit", (event) => {
        event.preventDefault();

        const name = document.getElementById("name").value.trim();
        const email = document.getElementById("email").value.trim();
        const message = document.getElementById("message").value.trim();

        resultMessage.classList.remove("hidden", "success", "error");

        if (!name || !email || !message) {
            resultMessage.textContent = "Заполните все поля формы.";
            resultMessage.classList.add("error");
            return;
        }

        if (!email.includes("@")) {
            resultMessage.textContent = "Введите корректный email.";
            resultMessage.classList.add("error");
            return;
        }

        resultMessage.textContent = "Спасибо! Ваше сообщение успешно отправлено.";
        resultMessage.classList.add("success");
        form.reset();
    });
});