function switchTheme() {
    var body = document.body;
    var nav = document.getElementById("main-nav");
    if (nav.classList.contains("bg-body-tertiary")) {
        nav.classList.remove("bg-body-tertiary");
        nav.classList.add("bg-body-dark");
    }
    else {
        nav.classList.remove("bg-body-dark");
        nav.classList.add("bg-body-tertiary");
    }
    if (nav.classList.contains("navbar-expand-lg")) {
        nav.classList.remove("navbar-expand-lg");
        nav.classList.add("navbar-expand-dark");
    }
    else {
        nav.classList.remove("navbar-expand-dark");
        nav.classList.add("navbar-expand-lg");
    }
    body.classList.toggle("dark-mode-body");
}
