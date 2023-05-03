let login_page = document.getElementById('login_page')

let login_button = document.getElementById('login-button').addEventListener('click', login_process)
let login_modal

let register_btn
let register_modal

let login_button2 // btn to swich from register modal to login modal

function login_process(e, err = '') {
    fetch('http://127.0.0.1:5000/login_modal')
        .then(res => res.json())
        .then(data => {

            // show login modal

            login_page.innerHTML = data
            login_modal = new bootstrap.Modal(document.getElementById('login'), {});
            login_modal.show();

            if (err == 'login_err') {
                let login_alert = document.getElementById('login_alert')
                login_alert.style.display = 'block'

            }

            // close btn    
            document.getElementById('login-close').addEventListener('click', () => { login_modal.hide() })

            // switch from login modal to register modal
            register_btn = document.getElementById('register-button').addEventListener('click', register_process)
        })
}

function register_process() {
    fetch('http://127.0.0.1:5000/register_modal')
        .then(res => res.json())
        .then(data => {

            // show login modal
            login_page.innerHTML = data
            register_modal = new bootstrap.Modal(document.getElementById('register'), {});
            register_modal.show();

            //close btn
            document.getElementById('register-close').addEventListener('click', () => { register_modal.hide() })
            login_modal.hide()

            // switch from register to login modal
            login_button2 = document.getElementById('login-button2').addEventListener('click', () => {
                register_modal.hide();
                login_modal.show()
            })

        })
}

// login error
if (Cookies.get('login_err') == '1') {
    Cookies.remove('login_err')
    login_process(null, 'login_err')

}