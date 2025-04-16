// JavaScript exists to call Python methods from passed controller object

const loginModal = new bootstrap.Modal('#loginModal');
const claimModal = new bootstrap.Modal('#claimModal');
const loginForm = document.getElementById('loginForm');
const claimForm = document.getElementById('claimForm');
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
    }, false);

    // Claim modal submit listener

    claimForm.addEventListener('submit', event => {
        // Set password field validity
        let adminPassword = $('#adminPassword').val();
        let adminPasswordConfirm = $('#adminPasswordConfirm').val();

        if (adminPassword != adminPasswordConfirm) {
            document.getElementById('adminPassword').setCustomValidity("BAD");
            document.getElementById('adminPasswordConfirm').setCustomValidity("BAD");
        } else {
            document.getElementById('adminPassword').setCustomValidity("");
            document.getElementById('adminPasswordConfirm').setCustomValidity("");
        }

        if (!claimForm.checkValidity()) {
            event.preventDefault();
            event.stopPropagation();
        }

        claimForm.classList.add('was-validated');
    }, false);

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
    // alert("Claim Server");
    loginForm.classList.add('was-validated');

    let adr = $("#address").val();
    let port = $("#port").val();

    if (adr && port) {
        let response = pywebview.api.claimServerInit(adr, port);
        response.then((value) => {

            switch (value) {
                case -1:
                    // Invalid args
                    // Works as intended with no change
                    // Form validation stops propagation
                    break;

                case 0:
                    // Server not claimed
                    // Dismiss login modal, show claim modal
                    loginModal.hide();
                    claimModal.show();
                    break;

                case 1:
                    // Claimed
                    // Show toast requiring login
                    alert("Server Claimed!");
                    break;
            }
        });
    }
}

function claimConfirm() {
    // Only arrives here if passwords match
    // Check passwords match .setCustomValidity()
    let newName = $('#newName').val();
    let adminPassword = $('#adminPassword').val();

    let response = pywebview.api.claimServerSetup(newName, adminPassword);

    // Replace with a modal so it looks nice

    response.then((value) => {
        alert(`This is your new API token. This will only be shown once: be sure to write it down!\n${value}`);
        claimModal.hide();
        loginModal.show();
    });
}

function updateSettingsDisp() {
    pywebview.api.updateSettingsDisp();
}

function showResponse(response) {
    alert(response);
}

function applyOptions() {
    alert("Apply Options");
}

function applyAGS() {
    alert("Apply AGS");
}