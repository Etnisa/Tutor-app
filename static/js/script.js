document.getElementById('user-data').addEventListener('click', on_click_user_data)
document.getElementById('login').addEventListener('click', on_click_login)
document.getElementById('kursy').addEventListener('click', on_click_kursy)




function on_click_user_data() {
    fetch_user_data()
}

function on_click_login() {
    login()
}

function on_click_kursy() {
    fetch_announcements()
}

function fetch_user_data() {
    fetch('http://127.0.0.1:5000/my_account', {
            method: 'GET',
            credentials: "include"
        })
        .then(res => res.json())
        .then(data => console.log(data))
        .catch(error => console.log(error))
}

function login() {
    fetch('http://127.0.0.1:5000/login', {
            method: 'POST',
        })
        .then(res => res.json())
        .then(data => console.log(data))
        .catch(error => console.log(error))
}

function fetch_announcements() {
    fetch('http://127.0.0.1:5000/announcements')
        .then(res => res.json())
        .then(data => console.log(data))
        .catch(error => console.log(error))
}


document.getElementById('search').addEventListener('click', search)

function search() {
    console.log("test")
}