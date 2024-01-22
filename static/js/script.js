// Call the initialization function when the page loads
initializeInputFields();

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

function showLoadingSpinner(cancelCallback) {
  const loadingSpinner = document.getElementById("loading-spinner");
  const overlay = document.createElement("div");
  overlay.id = "loading-overlay";
  overlay.style.position = "fixed";
  overlay.style.top = "0";
  overlay.style.left = "0";
  overlay.style.width = "100%";
  overlay.style.height = "100%";
  overlay.style.backgroundColor = "rgba(0, 0, 0, 0.5)";
  overlay.style.zIndex = "9999";
  overlay.style.display = "flex";
  overlay.style.flexDirection = "column";
  overlay.style.justifyContent = "center";
  overlay.style.alignItems = "center";

  const textElement = document.createElement("div");
  textElement.style.color = "#fff";
  textElement.style.fontWeight = "bold";
  textElement.textContent =
    "Mohon Tunggu Selama 1 - 3 Menit Hingga Proses Selesai";
  textElement.style.marginTop = "250px";
  overlay.appendChild(textElement);

  const cancelButton = document.createElement("button");
  cancelButton.textContent = "Cancel";
  cancelButton.style.marginTop = "20px"; // Menambahkan margin ke atas
  cancelButton.style.padding = "5px";
  cancelButton.style.cursor = "pointer";
  cancelButton.addEventListener("click", () => {
    // Panggil callback batal jika ada
    if (typeof cancelCallback === "function") {
      cancelCallback();
    }
    // Sembunyikan loading spinner
    hideLoadingSpinner();
  });
  overlay.appendChild(cancelButton);

  document.body.appendChild(overlay);

  loadingSpinner.style.display = "block";
}

function hideLoadingSpinner() {
  const loadingSpinner = document.getElementById("loading-spinner");
  const overlay = document.getElementById("loading-overlay");
  if (overlay) {
    document.body.removeChild(overlay);
  }

  loadingSpinner.style.display = "none";
}

function submitForm() {
  showLoadingSpinner(() => {
    fetch("/home/cancel_scraping", {
      method: "POST",
    })
      .then((response) => response.json())
      .then((data) => {
        alert(data.message);
        window.location.reload();
      })
      .catch((error) => {
        console.error("Error", error);
      });
  });

  const keyword = document.getElementById("search-bar").value.trim();
  const page = document.getElementById("page").value;

  // Remove "Rp" from min_price and max_price
  const min_price = document
    .getElementById("minPrice")
    .value.replace(/Rp/g, "")
    .replace(/,/g, "");
  const max_price = document
    .getElementById("maxPrice")
    .value.replace(/Rp/g, "")
    .replace(/,/g, "");

  // Check if the keyword input is empty
  if (!keyword) {
    alert("Silahkan Masukkan Nama Produk yang ingin Dicari");
    return;
  }

  // Ensure that "page" is a valid number and not starting with "0"
  if (!/^[1-9]\d*$/.test(page)) {
    alert("Halaman yang Dituju harus lebih dari 0");
    return;
  }

  // Construct the URL with parameters based on input values
  const params = [`keyword=${keyword}`, `page=${page}`];
  if (min_price) {
    params.push(`min_price=${min_price}`);
  }
  if (max_price) {
    params.push(`max_price=${max_price}`);
  }

  const url = `/home?${params.join("&")}`;

  fetch(url, {
    method: "POST",
  })
    .then((response) => response.json())
    .then((data) => {
      alert(data.message);
      if (data.message === "Search Product success") {
        hideLoadingSpinner();

        // Refresh Page
        window.location.reload();
      } else {
        // Lakukan sesuatu jika pencarian tidak berhasil
        console.log("Search Product failed");
        hideLoadingSpinner();

        // Refresh Page
        window.location.reload();
      }
    })
    .catch((error) => {
      console.error("Error:", error);
      hideLoadingSpinner();

      // Refresh Page
      window.location.reload();
    });
}

function submitFilter() {
  const keyword = document.getElementById("search-bar").value;
  const page = document.getElementById("page").value;

  let url = `/home?keyword=${keyword}&page=${page}`;
  const sort_by = document.getElementById("filterPrice").value;
  const sold_by = document.getElementById("filterSold").value;

  // Remove "Rp" from min_price and max_price, and also remove dots and commas
  const min_price = document
    .getElementById("minPrice")
    .value.replace(/[Rp,.]/g, "");

  const max_price = document
    .getElementById("maxPrice")
    .value.replace(/[Rp,.]/g, "");

  // Add min_price and max_price to the URL if they are not empty and max_price is not greater than min_price
  if (min_price) {
    url += `&min_price=${min_price}`;
  }

  if (max_price) {
    if (!min_price || parseFloat(max_price) <= parseFloat(min_price)) {
      // Max price should not be greater than min price
      alert("Harga Maksimum harus lebih tinggi dari Harga Minimum");
      return;
    }
    url += `&max_price=${max_price}`;
  }

  if (sort_by) {
    url += `&sort_by=${sort_by}`;
  }

  if (sold_by) {
    url += `&sold_by=${sold_by}`;
  }

  // Redirect to the new URL
  window.location.href = url;
}

// Add Comma Every 3 Digits of Price
var priceElements = document.querySelectorAll(".price");

// Loop through each element and format the price
priceElements.forEach(function (element) {
  var rawPrice = parseFloat(element.getAttribute("data-raw-price"));
  var formattedPrice = rawPrice.toLocaleString("id-ID"); // 'id-ID' for Indonesian Rupiah formatting

  element.textContent = "Rp" + formattedPrice;
});

function formatPriceInput(input) {
  let value = input.value.replace(/[^0-9]/g, "");

  // Remove leading zeros and dots
  value = value.replace(/^0+/, "").replace(/^\,+/, "");

  // Split the value by the decimal point
  const parts = value.split(".");
  const integerPart = parts[0];

  // Add a comma (or other separator) as a thousands separator
  const formattedIntegerPart = integerPart.replace(
    /\B(?=(\d{3})+(?!\d))/g,
    "."
  );

  // Reconstruct the formatted value with the decimal part
  if (parts.length > 1) {
    value = formattedIntegerPart + "." + parts[1];
  } else {
    value = formattedIntegerPart;
  }

  // Check if the input field is empty
  if (input.value.trim() === "") {
    input.value = ""; // Set to an empty string if empty
  } else if (input.value === "Rp") {
    input.value = ""; // Set to an empty string if it only contains "RP"
  } else {
    input.value = "Rp" + value;
  }
}

// Function to get URL parameters by name
function getParameterByName(name, url) {
  if (!url) url = window.location.href;
  name = name.replace(/[\[\]]/g, "\\$&");
  var regex = new RegExp("[?&]" + name + "(=([^&#]*)|&|#|$)"),
    results = regex.exec(url);
  if (!results) return null;
  if (!results[2]) return "";
  return decodeURIComponent(results[2].replace(/\+/g, " "));
}

// Function to initialize the input fields and select dropdowns from URL parameters
function initializeInputFields() {
  const keyword = getParameterByName("keyword");
  const minPrice = getParameterByName("min_price");
  const maxPrice = getParameterByName("max_price");
  const page = getParameterByName("page");
  const filterPrice = getParameterByName("sort_by");
  const filterSold = getParameterByName("sold_by");

  document.getElementById("search-bar").value = keyword || "";
  document.getElementById("minPrice").value = minPrice ? "Rp" + minPrice : "";
  document.getElementById("maxPrice").value = maxPrice ? "Rp" + maxPrice : "";
  document.getElementById("page").value = page || "1";

  const filterPriceSelect = document.getElementById("filterPrice");
  if (filterPrice) {
    filterPriceSelect.value = filterPrice;
  }

  const filterSoldSelect = document.getElementById("filterSold");
  if (filterSold) {
    filterSoldSelect.value = filterSold;
  }
}
