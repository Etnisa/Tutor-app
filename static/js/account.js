// edit annoucement btn
let enl = document.getElementsByClassName('enlarge_ann')

Array.from(enl).forEach(element => {
    element.addEventListener('click', enlarge_ann)
});


function enlarge_ann(e) {
    id = e.target.closest('a').id

    fetch(`/announcement_edit/${id}`)
        .then(res => res.json())
        .then(data => {
            // console.log(data)
            let enlarge_acc_account = document.getElementById('annoucement_home_page')
            enlarge_acc_account.innerHTML = data

            eval(document.getElementById('edit_chained_select').innerHTML) // data for chained select

            enlarge_acc_account_modal = new bootstrap.Modal(document.getElementById('annoucement_home_page_modal'), {});
            enlarge_acc_account_modal.show();

            chained_select(selected) // annoucement edit

            document.getElementById('enlarged-close').addEventListener('click', () => {
                enlarge_acc_account_modal.hide()
            })
        })
        .catch(error => console.log(error))
}


// edit user data btn
if (edit_profil != null) edit_profil.addEventListener('click', account_edit)

function account_edit(e) {
    fetch(`/account_edit`, {'credentials': 'include'})
        .then(res => res.json())
        .then(data => {
            console.log(data)
            let enlarge_account = document.getElementById('annoucement_home_page')
            enlarge_account.innerHTML = data

            enlarge_account_modal = new bootstrap.Modal(document.getElementById('account_edit'), {});
            enlarge_account_modal.show();

            document.getElementById('acc-edit-close').addEventListener('click', () => {
                enlarge_account_modal.hide()
            })
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


// edit user data process          edit-acc-btn

// let edit = document.getElementById("edit-acc-btn").addEventListener('click', edit_acc_process)

// function edit_acc_process(e) { WTF
//     console.log("Powodzenie")
// }