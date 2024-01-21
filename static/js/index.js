function index() {
    var element = document.getElementById("navigation-div");
    var numberOfChildren = element.getElementsByTagName('*').length

    var buttons = document.getElementsByClassName("navigation-button")

    for (let i = 0; i < buttons.length; i++)
        buttons[i].style.width = `calc(100% / ${numberOfChildren})`
}



document.addEventListener("DOMContentLoaded", () => {
  index()
});
