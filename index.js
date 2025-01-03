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

function applyOptions() {
    alert("Apply Options");
}