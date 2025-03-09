import Swiper, { Navigation, Pagination } from 'swiper'; // ✅ Correct modular imports
import 'swiper/css'; // ✅ Import core Swiper CSS
import "swiper/swiper-bundle.css"; // ✅ Import Swiper bundle CSS
import 'swiper/css/effect-cube'; // ✅ Import Cube effect module CSS
import 'swiper/css/navigation'; // ✅ Import Navigation module CSS
import 'swiper/css/pagination'; // ✅ Import Pagination module CSS

// Enable Navigation and Pagination modules
Swiper.use([Navigation, Pagination]);

// =====================
// GSAP Animations (Optional)
// =====================
import gsap from 'gsap';

// =====================
// Swiper Initialization
// =====================
document.addEventListener("DOMContentLoaded", function () {
  const swiper = new Swiper(".swiper-container", {
      modules: [Navigation, Pagination],
      slidesPerView: 3,
      spaceBetween: 15,
      loop: true,
      autoplay: {
          delay: 2500,
          disableOnInteraction: false,
      },
      navigation: {
          nextEl: "#gallery-next",
          prevEl: "#gallery-prev",
      },
      pagination: {
          el: ".swiper-pagination",
          clickable: true,
      },
  });

  console.log("Swiper instance:", swiper);
});

// =====================
// GSAP animation (optional)
// =====================
if (document.querySelector(".hero-overlay")) {
  gsap.from(".hero-overlay", {
    opacity: 0,
    y: 50,
    duration: 2,
    ease: "power2.out",
  });
} // ✅ Ensure this closing bracket exists!

// -----------------------------------------------------------
// Search Functionality for Gallery Items
if (document.querySelector(".search-input")) {
  const searchInput = document.querySelector(".search-input");
  const items = document.querySelectorAll(".search-item");

  searchInput.addEventListener("input", (e) => {
    const term = e.target.value.toLowerCase();
    items.forEach(item => {
      // Examine both <h4> and <p> elements within the item
      const textElement = item.querySelector("h4, p");
      const text = textElement ? textElement.textContent.toLowerCase() : "";
      item.style.display = text.includes(term) ? "block" : "none";
    });
  });
}

// -----------------------------------------------------------
// Lazy Loading Images Using Intersection Observer API
document.addEventListener("DOMContentLoaded", () => {
  const lazyLoadImages = document.querySelectorAll("img.lazyload");
  if (lazyLoadImages.length > 0) {
    const observer = new IntersectionObserver((entries, observerInstance) => {
      entries.forEach(entry => {
        if (entry.isIntersecting) {
          const img = entry.target;
          // Set src attribute from data-src
          img.src = img.dataset.src;
          img.classList.add("fade-in");
          observerInstance.unobserve(img);
        }
      });
    });
    lazyLoadImages.forEach(img => observer.observe(img));
  }
});

// -----------------------------------------------------------
// Preloader Fade Out Animation Using GSAP
window.addEventListener("load", () => {
  const preloader = document.getElementById("preloader");
  if (preloader) {
    gsap.to(preloader, {
      opacity: 0,
      duration: 0.5,
      onComplete: () => preloader.style.display = 'none'
    });
  }
});

// -----------------------------------------------------------
// Contact Form Submission with Fade-Out Feedback
if (document.querySelector("#contactForm")) {
  const contactForm = document.querySelector("#contactForm");
  contactForm.addEventListener("submit", (e) => {
    e.preventDefault();
    gsap.to("#contactForm", { opacity: 0, duration: 0.3 });
    setTimeout(() => {
      alert("Thank you for your message! We'll get back to you shortly.");
      contactForm.reset();
      gsap.to("#contactForm", { opacity: 1, duration: 0.3 });
    }, 300);
  });
}

// -----------------------------------------------------------
// Scroll-to-Top Button with Smooth Scrolling
if (document.querySelector("#scrollToTop")) {
  const scrollToTopBtn = document.querySelector("#scrollToTop");
  window.addEventListener("scroll", () => {
    scrollToTopBtn.classList.toggle("visible", window.scrollY > 300);
  });
  scrollToTopBtn.addEventListener("click", () => {
    gsap.to(window, { scrollTo: { y: 0 }, duration: 1 });
  });
}

// -----------------------------------------------------------
// "Load More" Button to Reveal Additional Content
if (document.querySelector("#loadMore")) {
  const loadMoreBtn = document.querySelector("#loadMore");
  const hiddenItems = document.querySelectorAll(".product-item.hidden");

  loadMoreBtn.addEventListener("click", () => {
    hiddenItems.forEach((item, index) => {
      if (index < 6) item.classList.remove("hidden");
    });
    if (document.querySelectorAll(".product-item.hidden").length === 0) {
      loadMoreBtn.style.display = "none";
    }
  });
}

// -----------------------------------------------------------
// Highlight Active Navbar Link on Click
if (document.querySelectorAll(".nav-link")) {
  const navLinks = document.querySelectorAll(".nav-link");
  navLinks.forEach(link => {
    link.addEventListener("click", () => {
      navLinks.forEach(navLink => navLink.classList.remove("active"));
      link.classList.add("active");
    });
  });
}

// -----------------------------------------------------------
// Mobile Navbar Toggle with GSAP
if (document.querySelector("#navbarToggle") && document.querySelector(".navbar-menu")) {
  const navbarToggle = document.querySelector("#navbarToggle");
  const navbarMenu = document.querySelector(".navbar-menu");
  navbarToggle.addEventListener("click", () => {
    if (navbarMenu.classList.contains("active")) {
      gsap.to(navbarMenu, { opacity: 0, duration: 0.3, onComplete: () => navbarMenu.classList.remove("active") });
    } else {
      gsap.to(navbarMenu, { opacity: 1, duration: 0.3 });
      navbarMenu.classList.add("active");
    }
  });
}

// -----------------------------------------------------------
// Scroll Animations: Fade-in Effect on Sections as They Come Into View
if (document.querySelectorAll(".fade-in")) {
  const fadeInSections = document.querySelectorAll(".fade-in");
  const checkVisibility = () => {
    fadeInSections.forEach(section => {
      const rect = section.getBoundingClientRect();
      // Toggle class "visible" when section is in viewport
      section.classList.toggle("visible", rect.top <= window.innerHeight && rect.bottom >= 0);
    });
  };
  window.addEventListener("scroll", checkVisibility);
  checkVisibility();
}

// -----------------------------------------------------------
// Sticky Navbar: Add 'sticky' Class When Scrolled Past 50px
window.addEventListener("scroll", () => {
  const navbar = document.querySelector(".navbar");
  if (navbar) {
    navbar.classList.toggle("sticky", window.scrollY > 50);
  }
});

// -----------------------------------------------------------
// Parallax Scrolling: Move Background for Elements with "parallax-bg" Class
document.addEventListener("scroll", () => {
  const parallax = document.querySelector(".parallax-bg");
  if (parallax) {
    parallax.style.transform = `translateY(${window.scrollY * 0.5}px)`;
  }
});

// -----------------------------------------------------------
// Product Filter: Filter Items Based on Selected Category
if (document.querySelector("#product-filter")) {
  const filterSelect = document.querySelector("#product-filter");
  const productItems = document.querySelectorAll(".product-item");
  filterSelect.addEventListener("change", (e) => {
    const selectedCategory = e.target.value;
    productItems.forEach(item => {
      item.style.display = selectedCategory === "all" || item.dataset.category === selectedCategory ? "block" : "none";
    });
  });
}

// -----------------------------------------------------------
// Parallax Effect for Blog Images Using GSAP
document.addEventListener('scroll', () => {
  const parallaxImage = document.querySelector('.parallax img');
  if (parallaxImage) {
    gsap.to(parallaxImage, { y: window.scrollY * 0.4, duration: 0.5 });
  }
});

// -----------------------------------------------------------
// Currency Conversion: Convert Price in ZAR to Target Currency
function convertCurrency(priceZar, targetCurrency) {
  const exchangeRates = {
    "ZAR": 1,
    "USD": 0.053,  // Example rate; update as needed
    "NGN": 28.3    // Example rate; update as needed
  };
  const convertedPrice = priceZar * exchangeRates[targetCurrency];
  return convertedPrice.toFixed(2);
}

const currencySelector = document.getElementById('currency-selector');
if (currencySelector) {
  currencySelector.addEventListener('change', function() {
    const selectedCurrency = this.value;
    const pricesInZar = document.querySelectorAll('.price-zar');
    pricesInZar.forEach(priceElement => {
      const priceZar = parseFloat(priceElement.getAttribute('data-price-zar'));
      const convertedPrice = convertCurrency(priceZar, selectedCurrency);
      priceElement.textContent = `${selectedCurrency} ${convertedPrice}`;
    });
  });
}

// -----------------------------------------------------------
// Sorting Functionality: Sort Products/Services Based on Criteria
function sortItems(criteria) {
  const container = document.querySelector('.items-container');
  if (!container) return;
  const items = Array.from(container.children);
  items.sort((a, b) => {
    if (criteria === 'price-low-high') {
      return parseFloat(a.getAttribute('data-price')) - parseFloat(b.getAttribute('data-price'));
    } else if (criteria === 'price-high-low') {
      return parseFloat(b.getAttribute('data-price')) - parseFloat(a.getAttribute('data-price'));
    } else if (criteria === 'name-a-z') {
      return a.getAttribute('data-name').localeCompare(b.getAttribute('data-name'));
    } else if (criteria === 'name-z-a') {
      return b.getAttribute('data-name').localeCompare(a.getAttribute('data-name'));
    }
  });
  container.innerHTML = '';
  items.forEach(item => container.appendChild(item));
}

const sortSelector = document.getElementById('sort-selector');
if (sortSelector) {
  sortSelector.addEventListener('change', function() {
    sortItems(this.value);
  });
}

// -----------------------------------------------------------
// Checkout: Dynamic Cart Calculation with Tax Computations
document.addEventListener("DOMContentLoaded", function () {
  // Sample cart data; in production this would be dynamic
  const cartData = [
    { name: "Product 1", price: 100, quantity: 2 },
    { name: "Product 2", price: 150, quantity: 1 }
  ];
  const taxRate = 0.15; // 15%

  function updateCartSummary() {
    let subtotal = 0;
    const cartItemsContainer = document.getElementById('cart-items');
    if (cartItemsContainer) {
      cartItemsContainer.innerHTML = "";
      cartData.forEach(item => {
        const itemTotal = item.price * item.quantity;
        subtotal += itemTotal;
        const itemHTML = `
          <div class="cart-item">
            <p><strong>${item.name}</strong></p>
            <p>Price: R${item.price}</p>
            <p>Quantity: ${item.quantity}</p>
            <p>Total: R${itemTotal.toFixed(2)}</p>
          </div>
        `;
        cartItemsContainer.insertAdjacentHTML('beforeend', itemHTML);
      });
      const taxAmount = subtotal * taxRate;
      const totalAmount = subtotal + taxAmount;
      document.getElementById('subtotal').textContent = `R${subtotal.toFixed(2)}`;
      document.getElementById('tax').textContent = `R${taxAmount.toFixed(2)}`;
      document.getElementById('total').textContent = `R${totalAmount.toFixed(2)}`;
    }
  }
  updateCartSummary();
});

// -----------------------------------------------------------
// Guest Checkout: Dynamic Cart Data Handling (Identical to Checkout Logic)
document.addEventListener("DOMContentLoaded", function () {
  const guestCartData = [
    { name: "Product 1", price: 100, quantity: 2 },
    { name: "Product 2", price: 150, quantity: 1 }
  ];
  const taxRate = 0.15; // 15%

  function updateGuestCart() {
    let subtotal = 0;
    const cartItemsContainer = document.getElementById('cart-items');
    if (cartItemsContainer) {
      cartItemsContainer.innerHTML = "";
      guestCartData.forEach(item => {
        const itemTotal = item.price * item.quantity;
        subtotal += itemTotal;
        const itemHTML = `
          <div class="cart-item">
            <p><strong>${item.name}</strong></p>
            <p>Price: R${item.price}</p>
            <p>Quantity: ${item.quantity}</p>
            <p>Total: R${itemTotal.toFixed(2)}</p>
          </div>
        `;
        cartItemsContainer.insertAdjacentHTML('beforeend', itemHTML);
      });
      const taxAmount = subtotal * taxRate;
      const totalAmount = subtotal + taxAmount;
      document.getElementById('subtotal').textContent = `R${subtotal.toFixed(2)}`;
      document.getElementById('tax').textContent = `R${taxAmount.toFixed(2)}`;
      document.getElementById('total').textContent = `R${totalAmount.toFixed(2)}`;
    }
  }
  updateGuestCart();
});

