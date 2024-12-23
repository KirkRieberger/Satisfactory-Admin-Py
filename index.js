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
    $('#dashboard').removeAttr("hidden");
    $('#dashboard').attr("aria-selected", "true");
    $('#dashboard').attr("tabindex", "0");

    $('#settings').attr("hidden", "");
    $('#settings').attr("aria-selected", "false");
    $('#settings').attr("tabindex", "-1");

    $('#sessions').attr("hidden", "");
    $('#sessions').attr("aria-selected", "false");
    $('#sessions').attr("tabindex", "-1");

    $('#console').attr("hidden", "");
    $('#console').attr("aria-selected", "false");
    $('#console').attr("tabindex", "-1");

    $('#dashLink').addClass("active");
    $('#settingsLink').removeClass("active");
    $('#sessionsLink').removeClass("active");
    $('#consoleLink').removeClass("active");
}

function showSettings() {
    $('#dashboard').attr("hidden", "");
    $('#dashboard').attr("aria-selected", "false");
    $('#dashboard').attr("tabindex", "-1");

    $('#settings').removeAttr("hidden");
    $('#settings').attr("aria-selected", "true");
    $('#settings').attr("tabindex", "0");

    $('#sessions').attr("hidden", "");
    $('#sessions').attr("aria-selected", "false");
    $('#sessions').attr("tabindex", "-1");

    $('#console').attr("hidden", "");
    $('#console').attr("aria-selected", "false");
    $('#console').attr("tabindex", "-1");

    $('#dashLink').removeClass("active");
    $('#settingsLink').addClass("active");
    $('#sessionsLink').removeClass("active");
    $('#consoleLink').removeClass("active");
}

function showSessions() {
    $('#dashboard').attr("hidden", "");
    $('#dashboard').attr("aria-selected", "false");
    $('#dashboard').attr("tabindex", "-1");

    $('#settings').attr("hidden", "");
    $('#settings').attr("aria-selected", "false");
    $('#settings').attr("tabindex", "-1");

    $('#sessions').removeAttr("hidden");
    $('#sessions').attr("aria-selected", "true");
    $('#sessions').attr("tabindex", "0");

    $('#console').attr("hidden", "");
    $('#console').attr("aria-selected", "false");
    $('#console').attr("tabindex", "-1");

    $('#dashLink').removeClass("active");
    $('#settingsLink').removeClass("active");
    $('#sessionsLink').addClass("active");
    $('#consoleLink').removeClass("active");
}

function showConsole() {
    $('#dashboard').attr("hidden", "");
    $('#dashboard').attr("aria-selected", "false");
    $('#dashboard').attr("tabindex", "-1");

    $('#settings').attr("hidden", "");
    $('#settings').attr("aria-selected", "false");
    $('#settings').attr("tabindex", "-1");

    $('#sessions').attr("hidden", "");
    $('#sessions').attr("aria-selected", "false");
    $('#sessions').attr("tabindex", "-1");

    $('#console').removeAttr("hidden");
    $('#console').attr("aria-selected", "true");
    $('#console').attr("tabindex", "0");

    $('#dashLink').removeClass("active");
    $('#settingsLink').removeClass("active");
    $('#sessionsLink').removeClass("active");
    $('#consoleLink').addClass("active");
}