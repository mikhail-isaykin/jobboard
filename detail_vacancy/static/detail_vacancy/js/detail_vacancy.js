document.addEventListener("scroll", function () {
const vacancyCard = document.querySelector(".vacancy-card");
const reviewsBlock = document.querySelector("#reviews-block");
const footer = document.getElementById("vacancy-footer");

const vacancyBottom = vacancyCard.getBoundingClientRect().bottom;
const reviewsTop = reviewsBlock.getBoundingClientRect().top;

if (vacancyBottom < 0 && reviewsTop > window.innerHeight) {
  footer.classList.remove("d-none");
} else {
  footer.classList.add("d-none");
}
});



// Получаем элементы
const moreBtn = document.getElementById("more-options-btn");
const moreMenu = document.getElementById("more-options-menu");

moreBtn.addEventListener("click", function(e) {
  e.stopPropagation();
  moreMenu.classList.toggle("d-none");
});

document.addEventListener("click", function() {
  if (!moreMenu.classList.contains("d-none")) {
    moreMenu.classList.add("d-none");
  }
});

// Действия кнопок
document.getElementById("hide-this-vacancy").addEventListener("click", function() {
  document.getElementById("vacancy-card-detail").style.display = "none";
  moreMenu.classList.add("d-none");
});

document.getElementById("hide-company-vacancies-1").addEventListener("click", function() {
  const companyVacancies = document.querySelectorAll(".related-vacancies .card");
  companyVacancies.forEach(v => v.style.display = "none");
  const relatedBlock = document.querySelector(".related-vacancies");
  if (relatedBlock) relatedBlock.style.display = "none";
  moreMenu.classList.add("d-none");
});

document.getElementById("report-vacancy").addEventListener("click", function() {
  alert("Спасибо! Вакансия отправлена на модерацию.");
  moreMenu.classList.add("d-none");
});
