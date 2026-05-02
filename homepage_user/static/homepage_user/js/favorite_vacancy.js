document.addEventListener("DOMContentLoaded", () => {
  document.querySelectorAll(".favorite-icon").forEach(icon => {
    icon.addEventListener("click", () => {
      const vacancyId = icon.dataset.id;

      fetch(`/vacancy/toggle/${vacancyId}/`, {
        method: "POST",
        headers: {
          "X-CSRFToken": getCookie("csrftoken"),
          "X-Requested-With": "XMLHttpRequest"
        }
      })
      .then(res => res.json())
      .then(data => {
        if (data.status === "added") {
          icon.classList.remove("bi-star");
          icon.classList.add("bi-star-fill", "text-warning");
        } else if (data.status === "removed") {
          icon.classList.remove("bi-star-fill", "text-warning");
          icon.classList.add("bi-star");
        }

        const counter = document.querySelector(".favorite-counter");
        if (counter) {
          counter.textContent = data.favorite_count;
        }
      });
    });
  });

  function getCookie(name) {
    let cookieValue = null;
    if (document.cookie && document.cookie !== "") {
      const cookies = document.cookie.split(";");
      for (let i = 0; i < cookies.length; i++) {
        const cookie = cookies[i].trim();
        if (cookie.substring(0, name.length + 1) === (name + "=")) {
          cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
          break;
        }
      }
    }
    return cookieValue;
  }
});
