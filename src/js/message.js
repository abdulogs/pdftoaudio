function error(value = "", where = "") {
    return $(where).html(`
    <div class="alert alert-error">
        <span class="bx bx-x icon"></span>
        <h4 class="alert-heading">${value}</h4>
        <button class="close-btn bx bx-x" onclick="parentElement.remove();"></button>
    </div>
    `
    );
}

function success(value = "", where = "") {
    return $(where).html(
        `<div class="alert alert-success">
        <span class="bx bx-check-circle icon"></span>
        <h4 class="alert-heading">${value}</h4>
        <button class="close-btn bx bx-x" onclick="parentNode.parentNode.parentNode.removeChild(parentNode.parentNode);"></button>
        </div>`
    );
}

function reload() {
    setTimeout(function () {
        location.reload();
    }, 1000);
}
function redirect(location) {
    window.open(location, "_SELF");
}