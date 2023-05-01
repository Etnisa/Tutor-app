let register_modal
let login_button2

function register_process(e) {
    fetch('http://127.0.0.1:5000/register_modal')
        .then(res => res.json())
        .then(data => {

            let login_page = document.getElementById('login_page')
            console.log(data)
            login_page.innerHTML = data


            register_modal = new bootstrap.Modal(document.getElementById('register'), {});
            register_modal.show();

            document.getElementById('register-close').addEventListener('click', () => { register_modal.hide() })
            login_modal.hide()

            login_button2 = document.getElementById('login-button2').addEventListener('click', () => {
                register_modal.hide();
                login_modal.show()
            })

        })



}