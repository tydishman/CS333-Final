document.addEventListener('DOMContentLoaded', () => {
  // --- Sidebar toggle ---
  const openNav = document.getElementById("openNav");
  const mySidebar = document.getElementById("mySidebar");
  if (openNav) {
    openNav.addEventListener("click", () => {
      document.getElementById("main").style.marginLeft = "18%";
      mySidebar.style.width = "18%";
      mySidebar.style.display = "block";
      openNav.style.display = "none";
    });
  }

  window.w3_close = () => {
    document.getElementById("main").style.marginLeft = "0";
    mySidebar.style.display = "none";
    openNav.style.display = "inline-block";
  };

  // --- Auth modals ---
  const loginBtn = document.getElementById('openLogin');
  const signupBtn = document.getElementById('openSignup');
  const loginModal = document.getElementById('loginModal');
  const signupModal = document.getElementById('signupModal');
  const closeLogin = document.getElementById('closeLogin');
  const closeSignup = document.getElementById('closeSignup');

  loginBtn?.addEventListener('click', () => {
    loginModal.style.display = 'flex';
  });

  signupBtn?.addEventListener('click', () => {
    signupModal.style.display = 'flex';
  });

  closeLogin?.addEventListener('click', () => {
    loginModal.style.display = 'none';
  });

  closeSignup?.addEventListener('click', () => {
    signupModal.style.display = 'none';
  });

  // --- FAB Event Modal ---
  const openEventBtn = document.getElementById('openEventModal');
  const eventModal = document.getElementById('eventModal');
  const closeEventBtn = document.getElementById('closeEventModal');

  openEventBtn?.addEventListener('click', () => {
    eventModal.style.display = 'flex';
  });

  closeEventBtn?.addEventListener('click', () => {
    eventModal.style.display = 'none';
    eventModal.querySelector('form')?.reset();
    document.getElementById("newCategoryInput").style.display = "none";
  });

  // --- Category toggle ---
  const categorySelect = document.getElementById("categorySelect");
  const newCategoryInput = document.getElementById("newCategoryInput");

  categorySelect?.addEventListener("change", () => {
    if (categorySelect.value === "__new__") {
      newCategoryInput.style.display = "block";
      newCategoryInput.querySelector("input").required = true;
    } else {
      newCategoryInput.style.display = "none";
      newCategoryInput.querySelector("input").required = false;
    }
  });

  // --- Flash messages ---
  const flashMessages = document.querySelectorAll('.flash');
  flashMessages.forEach(msg => {
    const cat = msg.dataset.category;
    if (cat === 'login_error' || cat === 'signup_success') {
      loginModal.style.display = 'flex';
    } else if (cat === 'signup_error') {
      signupModal.style.display = 'flex';
    }
    alert(msg.textContent); // TODO: replace with toast
  });

  // --- Wishlist Modal ---
  const openWishlistBtn = document.getElementById("openWishlistModal");
  const closeWishlistBtn = document.getElementById("closeWishlistModal");
  const wishlistModal = document.getElementById("wishlistModal");

  openWishlistBtn?.addEventListener("click", () => {
    wishlistModal.style.display = "flex";
  });

  closeWishlistBtn?.addEventListener("click", () => {
    wishlistModal.style.display = "none";
  });

  window.addEventListener("click", (e) => {
    if (e.target === loginModal) loginModal.style.display = 'none';
    if (e.target === signupModal) signupModal.style.display = 'none';
    if (e.target === eventModal) eventModal.style.display = 'none';
    if (e.target === wishlistModal) wishlistModal.style.display = 'none';
  });
});