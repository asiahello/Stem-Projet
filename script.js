function mobileMenu() {
  var mobileMenuIcon = document.getElementById("mobile-menu-icon");
  var menu = document.getElementById("main-menu");

  if (mobileMenuIcon) {
    mobileMenuIcon.addEventListener("click", function() {
      menu.classList.toggle("opened");
      mobileMenuIcon.classList.toggle("opened");
    });
  }
}

mobileMenu();
