 // Wait for Python API to be initialized
 window.addEventListener('pywebviewready', function () {
    const loginModal = new bootstrap.Modal('#loginModal');
    loginModal.show();

    $('#loginButton').on('click', function () {
        login();
    });
    $('#address').on('keypress', (event) => {
        if (event.key === "Enter") {
            login();
        }
    });
    $('#key').on('keypress', (event) => {
        if (event.key === "Enter") {
            login();
        }
    });
 });

function login() {
    let adr = $("#address").val();
    let key = $("#key").val();
    let port = 7777;
    response = pywebview.api.login(adr, key, port);

    response.then(value => {
        loginModal.hide();
    }).catch(error => {
        showResponse(error);
        // Clear fields
        $("#address").val("");
        $("#key").val("");
    });
}

function showResponse(response) {
    alert(response);
}

function showDash() {

}

function showSettings() {

}

function showConsole() {

}