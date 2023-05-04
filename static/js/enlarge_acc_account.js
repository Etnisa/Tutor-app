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