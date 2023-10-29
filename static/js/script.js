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

// Table Body
function updateTable(data) {
  const tbody = document.querySelector("table tbody");

  // Clear the existing tbody content
  tbody.innerHTML = "";

  if (data.length === 0) {
    // Handle the case when no data is available
    const noDataRow = document.createElement("tr");
    noDataRow.innerHTML = '<td colspan="6">No data available</td>';
    tbody.appendChild(noDataRow);
  } else {
    // Loop through the response data and create table rows
    data.forEach((item) => {
      const row = document.createElement("tr");
      row.innerHTML = `
        <td><img src="${item.image}" alt="Product Image"></td>
        <td>${item.title}</td>
        <td>${item.price}</td>
        <td>${item.sold}</td>
        <td>${item.location}</td>
        <td><a href="${item.link}" target="_blank">View Product</a></td>
      `;

      // Append the row to the tbody
      tbody.appendChild(row);
    });
  }
}

// Add Comma Every 3 Digits of Price
var priceElements = document.querySelectorAll(".price");

// Loop through each element and format the price
priceElements.forEach(function (element) {
  var rawPrice = parseFloat(element.getAttribute("data-raw-price"));
  var formattedPrice = rawPrice.toLocaleString("id-ID"); // 'id-ID' for Indonesian Rupiah formatting

  element.textContent = "Rp" + formattedPrice;
});
