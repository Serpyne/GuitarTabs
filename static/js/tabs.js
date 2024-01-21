function index() {
    var element = document.getElementById("navigation-div");
    var numberOfChildren = element.getElementsByTagName('*').length;

    var buttons = document.getElementsByClassName("navigation-button");

    for (let i = 0; i < buttons.length; i++)
        buttons[i].style.width = `calc(100% / ${numberOfChildren})`;
}

function setTabsElements(tabs) {
    let container = document.getElementById("tabs-div");

    for (let item in tabs) {
        let element = document.createElement("a");
        element.classList.add("tab-item");
        element.href = tabs[item];
        element.target = "_blank";
        element.innerHTML += item;
        container.appendChild(element);
    }
}

function setTabs(tabs) {
    document.addEventListener("DOMContentLoaded", () => {
        setTabsElements(tabs);
    });
}


document.addEventListener("DOMContentLoaded", () => {
  index();
});
