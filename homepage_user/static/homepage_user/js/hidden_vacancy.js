document.addEventListener("DOMContentLoaded", () => {
    document.querySelectorAll(".hide-icon").forEach((icon) => {
        icon.addEventListener("click", () => {
            const vacancyId = icon.getAttribute("data-id");

            fetch("/vacancy/toggle-hidden-vacancy/", {
                method: "POST",
                headers: {
                    "X-CSRFToken": getCookie("csrftoken"),
                    "X-Requested-With": "XMLHttpRequest",
                },
                body: new URLSearchParams({ vacancy_id: vacancyId }),
            })
                .then((response) => response.json())
                .then((data) => {
                    if (data.status === "hidden") {
                        const card = icon.closest(".col-12");
                        if (card) {
                            card.style.transition = "opacity 0.3s";
                            card.style.opacity = "0";
                            setTimeout(() => card.remove(), 300);
                        }
                    } else if (data.status === "removed") {
                        icon.classList.remove("bi-eye");
                        icon.classList.remove("text-danger");
                        icon.classList.add("bi-eye-slash");
                    }
                })
                .catch((error) => console.error("Ошибка:", error));
        });
    });
});

// Получение CSRF-токена
function getCookie(name) {
    let cookieValue = null;
    if (document.cookie && document.cookie !== "") {
        const cookies = document.cookie.split(";");
        for (let cookie of cookies) {
            cookie = cookie.trim();
            if (cookie.startsWith(name + "=")) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}