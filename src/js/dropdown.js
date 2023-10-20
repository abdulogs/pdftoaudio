document.querySelectorAll('[data-toggle="dropdown"]').forEach((dropdown) => {
  dropdown.addEventListener("click", (event) => {
    var dropdowns, i;
    dropdowns = document.getElementsByClassName("dropdown-menu");
    if (
      dropdown.parentNode
        .querySelector("div.dropdown-menu")
        .classList.contains("dropdown-menu-show")
    ) {
      dropdown.parentNode
        .querySelector("div.dropdown-menu")
        .classList.remove("dropdown-menu-show");
      for (i = 0; i < dropdowns.length; i++) {
        var openDropdown = dropdowns[i];
        if (openDropdown.classList.contains("dropdown-menu-show")) {
          openDropdown.classList.remove("dropdown-menu-show");
        }
      }
    } else if (
      !dropdown.parentNode
        .querySelector("div.dropdown-menu")
        .classList.contains("dropdown-menu-show")
    ) {
      for (i = 0; i < dropdowns.length; i++) {
        var openDropdown = dropdowns[i];
        if (openDropdown.classList.contains("dropdown-menu-show")) {
          openDropdown.classList.remove("dropdown-menu-show");
        }
      }
      dropdown.parentNode
        .querySelector("div.dropdown-menu")
        .classList.add("dropdown-menu-show");
    }
  });
});
document.onclick = function (event) {
  event.stopPropagation();
  var dropdowns, i;
  dropdowns = document.getElementsByClassName("dropdown-menu");
  if (!event.target.closest(".dropdown")) {
    for (i = 0; i < dropdowns.length; i++) {
      var openDropdown = dropdowns[i];
      if (openDropdown.classList.contains("dropdown-menu-show")) {
        openDropdown.classList.remove("dropdown-menu-show");
      }
    }
  }
};
