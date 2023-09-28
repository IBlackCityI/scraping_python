// Toggle class active

const navbarNav = document.querySelector(".navbar-nav");
// ketika hamburger menu di klik
document.querySelector("#hamburger-menu").onclick = () => {
  navbarNav.classList.toggle("active");
};

// Klik di luar sidebar untuk menghilangkan nav
const hamburger = document.querySelector("#hamburger-menu");

document.addEventListener("click", function (e) {
  if (!hamburger.contains(e.target) && !navbarNav.contains(e.target)) {
    navbarNav.classList.remove("active");
  }
});

function submitForm() {
  const keyword = document.getElementById("search-bar").value;
  const page = document.getElementById("page").value;
  const url = `/home?keyword=${keyword}&page=${page}`;

  fetch(url, {
    method: "POST",
  })
    .then((response) => response.text())
    .then((result) => {
      alert(result); // Tampilkan hasil dari server
    })
    .catch((error) => {
      console.error("Error:", error);
    });
}
