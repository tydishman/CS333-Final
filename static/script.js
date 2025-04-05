document.addEventListener('DOMContentLoaded', () => {
  // Sidebar logic (if sidebar exists)
  const openNav = document.getElementById("openNav");
  if (openNav) {
    openNav.addEventListener("click", () => {
      document.getElementById("main").style.marginLeft = "18%";
      const sidebar = document.getElementById("mySidebar");
      sidebar.style.width = "18%";
      sidebar.style.display = "block";
      openNav.style.display = "none";
    });
  }

  // Modal elements
  const loginBtn = document.getElementById('openLogin');
  const signupBtn = document.getElementById('openSignup');
  const loginModal = document.getElementById('loginModal');
  const signupModal = document.getElementById('signupModal');
  const closeLogin = document.getElementById('closeLogin');
  const closeSignup = document.getElementById('closeSignup');

  // Open modals
  loginBtn?.addEventListener('click', () => {
    loginModal.style.display = 'flex';
  });

  signupBtn?.addEventListener('click', () => {
    signupModal.style.display = 'flex';
  });

  // Close modals
  closeLogin?.addEventListener('click', () => {
    loginModal.style.display = 'none';
  });

  closeSignup?.addEventListener('click', () => {
    signupModal.style.display = 'none';
  });

  // Close modal when clicking outside
  window.addEventListener('click', (e) => {
    if (e.target === loginModal) loginModal.style.display = 'none';
    if (e.target === signupModal) signupModal.style.display = 'none';
  });

  // Flash messages trigger modals
  const flashMessages = document.querySelectorAll('.flash');
  flashMessages.forEach(msg => {
    const cat = msg.dataset.category;
    if (cat === 'login_error' || cat === 'signup_success') {
      loginModal.style.display = 'flex';
    } else if (cat === 'signup_error') {
      signupModal.style.display = 'flex';
    }
    alert(msg.textContent); // Replace with styled toast if desired
  });
});