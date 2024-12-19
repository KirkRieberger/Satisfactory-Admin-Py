const loginModal = new bootstrap.Modal('#loginModal');
const loginForm = document.getElementById('loginForm');
// Wait for Python API to be initialized
window.addEventListener('pywebviewready', function () {
    loginModal.show();

    // Login modal submit listeners

    loginForm.addEventListener('submit', event => {
        if (!loginForm.checkValidity()) {
            event.preventDefault();
            event.stopPropagation();
        }

        loginForm.classList.add('was-validated');
    }, false)

    $('#port').on({
        'focus': () => {
            $('#port').select();
        }
    });

});

function login() {
    let adr = $("#address").val();
    let key = $("#key").val();
    let port = $("#port").val();
    alert(`Address: ${adr}:${port}`);
    let response = pywebview.api.login(adr, key, port);

    response.then(value => {
        loginModal.hide();
    }).catch(error => {
        showResponse(error);
        // Clear fields
        $("#address").val("");
        $("#key").val("");
        $("#port").val("");
    });
}

function showResponse(response) {
    alert(response);
}

function showDash() {
    $('#dashboard').removeClass("d-none");
    $('#settings').addClass("d-none");
    $('#sessions').addClass("d-none");
    $('#console').addClass("d-none");

    $('#dashLink').addClass("active");
    $('#settingsLink').removeClass("active");
    $('#sessionsLink').removeClass("active");
    $('#consoleLink').removeClass("active");
}

function showSettings() {
    $('#dashboard').addClass("d-none");
    $('#settings').removeClass("d-none");
    $('#sessions').addClass("d-none");
    $('#console').addClass("d-none");

    $('#dashLink').removeClass("active");
    $('#settingsLink').addClass("active");
    $('#sessionsLink').removeClass("active");
    $('#consoleLink').removeClass("active");
}

function showSessions() {
    $('#dashboard').addClass("d-none");
    $('#settings').addClass("d-none");
    $('#sessions').removeClass("d-none");
    $('#console').addClass("d-none");

    $('#dashLink').removeClass("active");
    $('#settingsLink').removeClass("active");
    $('#sessionsLink').addClass("active");
    $('#consoleLink').removeClass("active");
}

function showConsole() {
    $('#dashboard').addClass("d-none");
    $('#settings').addClass("d-none");
    $('#sessions').addClass("d-none");
    $('#console').removeClass("d-none");

    $('#dashLink').removeClass("active");
    $('#settingsLink').removeClass("active");
    $('#sessionsLink').removeClass("active");
    $('#consoleLink').addClass("active");
}