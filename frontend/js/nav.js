// frontend/js/nav.js

document.addEventListener("DOMContentLoaded", () => {
    // Highlight active page
    const navLinks = document.querySelectorAll("nav a");
    const currentPath = window.location.pathname;
  
    navLinks.forEach(link => {
      if (link.getAttribute("href") === currentPath) {
        link.classList.add("active");
      }
    });
  
    // Mobile nav toggle
    const menuToggle = document.querySelector(".menu-toggle");
    const navMenu = document.querySelector("nav ul");
  
    if (menuToggle && navMenu) {
      menuToggle.addEventListener("click", () => {
        navMenu.classList.toggle("show");
      });
    }
  
    // Logout button
    const logoutBtn = document.querySelector("#logout-btn");
    if (logoutBtn) {
      logoutBtn.addEventListener("click", () => {
        localStorage.removeItem("token");
        window.location.href = "/login.html";
      });
    }
  });
  