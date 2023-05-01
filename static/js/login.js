let login_button = document.getElementById('login-button').addEventListener('click', login_process)
let register_btn
let login_modal

function login_process(t) {
    fetch('http://127.0.0.1:5000/login_modal')
        .then(res => res.json())
        .then(data => {

            let login_page = document.getElementById('login_page')

            login_page.innerHTML = data

            login_modal = new bootstrap.Modal(document.getElementById('login'), {});
            login_modal.show();
            document.getElementById('login-close').addEventListener('click', () => { login_modal.hide() })

            register_btn = document.getElementById('register-button').addEventListener('click', register_process)

        })



}