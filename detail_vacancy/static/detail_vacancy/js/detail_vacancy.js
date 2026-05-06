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
        // Находим все иконки с этим vacancyId
        document.querySelectorAll(`.favorite-icon[data-id="${vacancyId}"]`).forEach(el => {
          if (data.status === "added") {
            el.classList.remove("bi-star");
            el.classList.add("bi-star-fill", "text-warning");
          } else if (data.status === "removed") {
            el.classList.remove("bi-star-fill", "text-warning");
            el.classList.add("bi-star");
          }
        });
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
