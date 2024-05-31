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
  checkboxes = document.querySelectorAll('input[data-name="brand"]');
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
  checkboxes = document.querySelectorAll('input[data-name="size"]');
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
  checkboxes = document.querySelectorAll('input[data-name="panel"]');
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
  checkboxes = document.querySelectorAll('input[data-name="resolution"]');
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
  let sortDirection = 1; // 1 for ascending, -1 for descending

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
      return (priceA - priceB) * sortDirection;
    });

    // Append sorted rows back to the table body
    rows.forEach((row) => tableBody.appendChild(row));

    // Toggle sort direction
    sortDirection *= -1;
    // Update the sort icon
    if (sortDirection === 1) {
      priceSortIcon.className = "sort-desc";
    } else {
      priceSortIcon.className = "sort-asc";
    }
  });

  // Set initial sort icon state
  priceSortIcon.className = "sort-asc";
});
