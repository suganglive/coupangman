function resetAllCheckboxes() {
  const checkboxes = document.querySelectorAll('input[type="checkbox"]');
  for (var i = 0; i < checkboxes.length; i++) {
    checkboxes[i].checked = false;
  }

  // Reset the hidden inputs as well
  document.getElementById("brandInput").value = "";
  document.getElementById("sizeInput").value = "";
  document.getElementById("panelInput").value = "";
  document.getElementById("resolutionInput").value = "";
}

function concatenateBrands() {
  const checkboxes = document.querySelectorAll(
    'input[data-name="brand"]:checked'
  );
  const selectedBrands = Array.from(checkboxes)
    .map((cb) => cb.value)
    .join("|");
  document.getElementById("brandInput").value = selectedBrands;
}

// Function to handle the "select all" functionality
function toggleSelectAllBrand(source) {
  const checkboxes = document.querySelectorAll('input[data-name="brand"]');
  checkboxes.forEach((checkbox) => {
    checkbox.checked = source.checked;
  });
  concatenateBrands(); // Update the hidden input value as well
}

function concatenateSize() {
  const checkboxes = document.querySelectorAll(
    'input[data-name="size"]:checked'
  );
  const selectedSize = Array.from(checkboxes)
    .map((cb) => cb.value)
    .join("|");
  document.getElementById("sizeInput").value = selectedSize;
}

// Function to handle the "select all" functionality
function toggleSelectAllSize(source) {
  const checkboxes = document.querySelectorAll('input[data-name="size"]');
  checkboxes.forEach((checkbox) => {
    checkbox.checked = source.checked;
  });
  concatenateSize(); // Update the hidden input value as well
}

function concatenatePanel() {
  const checkboxes = document.querySelectorAll(
    'input[data-name="panel"]:checked'
  );
  const selectedPanel = Array.from(checkboxes)
    .map((cb) => cb.value)
    .join("|");
  document.getElementById("panelInput").value = selectedPanel;
}

// Function to handle the "select all" functionality
function toggleSelectAllPanel(source) {
  const checkboxes = document.querySelectorAll('input[data-name="panel"]');
  checkboxes.forEach((checkbox) => {
    checkbox.checked = source.checked;
  });
  concatenatePanel(); // Update the hidden input value as well
}

function concatenateResolution() {
  const checkboxes = document.querySelectorAll(
    'input[data-name="resolution"]:checked'
  );
  const selectedResolution = Array.from(checkboxes)
    .map((cb) => cb.value)
    .join("|");
  document.getElementById("resolutionInput").value = selectedResolution;
}

// Function to handle the "select all" functionality
function toggleSelectAllResolution(source) {
  const checkboxes = document.querySelectorAll('input[data-name="resolution"]');
  checkboxes.forEach((checkbox) => {
    checkbox.checked = source.checked;
  });
  concatenateResolution(); // Update the hidden input value as well
}

function concatenateAll() {
  concatenateBrands();
  concatenateSize();
  concatenatePanel();
  concatenateResolution();
}

document.addEventListener("DOMContentLoaded", function () {
  function formatPrice(price) {
    return price.toString().replace(/\B(?=(\d{3})+(?!\d))/g, ",");
  }

  document.querySelectorAll(".price-details").forEach(function (element) {
    const discountedPriceElement = element.querySelector(".discounted-price");
    discountedPriceElement.textContent =
      formatPrice(discountedPriceElement.textContent.replace(/\D/g, "")) + "원";

    const originalPriceElement = element.querySelector(".original-price");
    if (originalPriceElement) {
      originalPriceElement.textContent =
        formatPrice(originalPriceElement.textContent.replace(/\D/g, "")) + "원";
    }
  });

  document.querySelectorAll(".rating-details").forEach(function (element) {
    const rating = parseFloat(element.getAttribute("data-rating"));
    const rateCountText = element.getAttribute("data-rate-count");
    const starContainer = element.querySelector(".rating-stars");
    if (
      rateCountText &&
      rateCountText.toLowerCase() !== "no review" &&
      starContainer
    ) {
      let stars = "";
      for (let i = 1; i <= 5; i++) {
        if (i <= rating) {
          stars += "🌕";
        } else if (i - 0.5 <= rating) {
          stars += "🌗";
        } else {
          stars += "🌑";
        }
      }
      starContainer.innerHTML = stars;
    }
  });

  // Sorting functionality for the Price column
  const priceHeader = document.getElementById("price-header");
  const priceSortIcon = document.getElementById("price-sort-icon");
  let priceSortDirection = 1; // 1 for ascending, -1 for descending

  priceHeader.addEventListener("click", () => {
    const tableBody = document.querySelector("tbody");
    const rows = Array.from(tableBody.querySelectorAll("tr"));

    // Sort rows based on the price
    rows.sort((a, b) => {
      const priceA = parseFloat(
        a.querySelector(".discounted-price").textContent.replace(/\D/g, "")
      );
      const priceB = parseFloat(
        b.querySelector(".discounted-price").textContent.replace(/\D/g, "")
      );
      return (priceA - priceB) * priceSortDirection;
    });

    // Append sorted rows back to the table body
    rows.forEach((row) => tableBody.appendChild(row));

    // Toggle sort direction
    priceSortDirection *= -1;
    // Update the sort icon
    if (priceSortDirection === 1) {
      priceSortIcon.className = "sort-asc";
    } else {
      priceSortIcon.className = "sort-desc";
    }
  });

  // Set initial sort icon state
  priceSortIcon.className = "sort-asc";

  // Sorting functionality for the rating count
  const ratingHeader = document.getElementById("rating-header");
  const ratingSortIcon = document.getElementById("rating-sort-icon");
  let ratingSortDirection = 1; // 1 for ascending, -1 for descending

  ratingHeader.addEventListener("click", () => {
    console.log("Rating header clicked"); // Debugging line
    const tableBody = document.querySelector("tbody");
    const rows = Array.from(tableBody.querySelectorAll("tr"));

    // Sort rows based on the rateCount
    rows.sort((a, b) => {
      const rateCountAElement = a.querySelector(".rate-count");
      const rateCountBElement = b.querySelector(".rate-count");

      const rateCountA = rateCountAElement
        ? parseInt(rateCountAElement.textContent.replace(/\D/g, ""), 10)
        : 0;
      const rateCountB = rateCountBElement
        ? parseInt(rateCountBElement.textContent.replace(/\D/g, ""), 10)
        : 0;

      return (rateCountA - rateCountB) * ratingSortDirection;
    });

    // Append sorted rows back to the table body
    rows.forEach((row) => tableBody.appendChild(row));

    // Toggle sort direction
    ratingSortDirection *= -1;
    // Update the sort icon
    if (ratingSortDirection === 1) {
      ratingSortIcon.className = "sort-asc";
    } else {
      ratingSortIcon.className = "sort-desc";
    }
    console.log("Sort direction toggled", ratingSortDirection); // Debugging line
  });

  // Set initial sort icon state
  ratingSortIcon.className = "sort-asc";
});
