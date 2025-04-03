// JavaScript exists to call Python methods from passed controller object

const loginModal = new bootstrap.Modal('#loginModal');
const claimModal = new bootstrap.Modal('#claimModal');
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

    // Highlight all text on port field focus
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
    let response = pywebview.api.login(adr, key, port);

    response.then(function () {
        loginModal.hide();
    }).catch(error => {
        showResponse(error);
        // Clear fields
        $("#address").val("");
        $("#key").val("");
        $("#port").val("");
    });
}

function claimServer() {
    alert("Claim Server");
    let adr = $("#address").val();
    let port = $("#port").val();
    let response = pywebview.api.claimServerInit(adr, port);
    response.then((value) => {
        if (value == 0) {
            // Server not claimed
            // Dismiss login modal, show claim modal
            loginModal.hide();
            claimModal.show();
        } else if (value == -1) {
            // Invalid args
            // Clear form, try again
        } else if (value == 1) {
            // Claimed
            // 
        }
    });

}

function showResponse(response) {
    alert(response);
}

function applyOptions() {
    alert("Apply Options");
}
