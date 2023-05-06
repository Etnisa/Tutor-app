// edit annoucement btn
let enl = document.getElementsByClassName('enlarge_acc_account')

Array.from(enl).forEach(element => {
    element.addEventListener('click', enlarge_acc_account)
});



function enlarge_acc_account(e) {
    id = e.target.closest('a').id

    fetch(`http://127.0.0.1:5000/announcement_edit/${id}`)
        .then(res => res.json())
        .then(data => {
            console.log(data)
            let enlarge_acc_account = document.getElementById('annoucement_home_page')
            enlarge_acc_account.innerHTML = data

            enlarge_acc_account_modal = new bootstrap.Modal(document.getElementById('annoucement_home_page_modal'), {});
            enlarge_acc_account_modal.show();

            document.getElementById('enlarged-close').addEventListener('click', () => { enlarge_acc_account_modal.hide() })
        })
        .catch(error => console.log(error))
}


// edit user data btn
if (edit_profil != null) edit_profil.addEventListener('click', account_edit)

function account_edit(e) {
    fetch(`http://127.0.0.1:5000/account_edit`, { 'credentials': 'include' })
        .then(res => res.json())
        .then(data => {
            console.log(data)
            let enlarge_account = document.getElementById('annoucement_home_page')
            enlarge_account.innerHTML = data

            enlarge_account_modal = new bootstrap.Modal(document.getElementById('account_edit'), {});
            enlarge_account_modal.show();

            //document.getElementById('enlarged-close').addEventListener('click', () => { enlarge_acc_account_modal.hide() })
        })
        .catch(error => console.log(error))
}

// reorder review
let div_disappear = document.getElementById('div_disappear')
let div_appear = document.getElementById('div_appear')
div_appear.style.display = 'none'
addEventListener("resize", (e) => {
    if (window.innerWidth < 991) {
        div_disappear.style.display = 'none'
        div_appear.style.display = 'block'
    } else {
        div_disappear.style.display = 'block'
        div_appear.style.display = 'none'
    }
});