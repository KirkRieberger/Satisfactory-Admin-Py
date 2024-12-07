 // Wait for Python API to be initialized
 window.addEventListener('pywebviewready', function () {
    const loginModal = new bootstrap.Modal('#loginModal');
    loginModal.show();

    document.getElementById('loginButton').addEventListener('click', function () {
        let adr = $("#address").val();
        let key = $("#key").val();
        let port = 7777;
        response = pywebview.api.login(adr, key, port);

        response.then(value => {
            showResponse(value);
            loginModal.hide();
        }).catch(error => {
            showResponse(error);
        });
        // Error
        if (response == 523) {
            // Bad address

        }
    });
});

function showResponse(response) {
    alert(response);
}