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

  loginBtn?.addEventListener('click', () => loginModal.style.display = 'flex');
  signupBtn?.addEventListener('click', () => signupModal.style.display = 'flex');
  closeLogin?.addEventListener('click', () => loginModal.style.display = 'none');
  closeSignup?.addEventListener('click', () => signupModal.style.display = 'none');

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
    document.getElementById("recurrenceOptions").style.display = "none";
    document.getElementById("customDaysInput").style.display = "none";
  });

  // --- Category toggle ---
  const categorySelect = document.getElementById("categorySelect");
  const newCategoryInput = document.getElementById("newCategoryInput");

  categorySelect?.addEventListener("change", () => {
    const isNew = categorySelect.value === "__new__";
    newCategoryInput.style.display = isNew ? "block" : "none";
    newCategoryInput.querySelector("input").required = isNew;
  });

  // --- Recurring toggle ---
  const recurringCheckbox = document.getElementById('recurringCheckbox');
  const recurrenceOptions = document.getElementById('recurrenceOptions');
  const recurrenceTypeSelect = document.getElementById('recurrence_type');
  const customDaysInput = document.getElementById('customDaysInput');

  recurringCheckbox?.addEventListener('change', () => {
    recurrenceOptions.style.display = recurringCheckbox.checked ? 'block' : 'none';
  });

  recurrenceTypeSelect?.addEventListener('change', () => {
    customDaysInput.style.display = recurrenceTypeSelect.value === 'custom_days' ? 'block' : 'none';
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
    alert(msg.textContent); // Can be upgraded to toast
  });


  // --- Form Button Enable/Disable ---
  function toggleButtonState(form, button) {
    const requiredFields = form.querySelectorAll("[required]");
    const allFilled = Array.from(requiredFields).every(f => f.value.trim());
    button.disabled = !allFilled;
    button.classList.toggle("active-submit", allFilled);
  }

  const loginForm = document.querySelector('#loginModal form');
  const loginButton = loginForm?.querySelector('button[type="submit"]');
  loginForm?.addEventListener('input', () => toggleButtonState(loginForm, loginButton));
  toggleButtonState(loginForm, loginButton);

  const signupForm = document.querySelector('#signupModal form');
  const signupButton = signupForm?.querySelector('button[type="submit"]');
  signupForm?.addEventListener('input', () => toggleButtonState(signupForm, signupButton));
  toggleButtonState(signupForm, signupButton);

  const eventForm = document.getElementById("eventForm");

  eventForm?.addEventListener("submit", async (e) => {
    e.preventDefault(); // prevent normal form submit
  
    const formData = new FormData(eventForm);
  
    const response = await fetch(eventForm.action, {
      method: "POST",
      body: formData
    });
  
    if (response.ok) {
      // Close modal and reset
      document.getElementById("eventModal").style.display = "none";
      eventForm.reset();
      document.getElementById("newCategoryInput").style.display = "none";
      // Optionally show a success toast or flash
    } else {
      alert("Error adding event!");
    }
  });
});