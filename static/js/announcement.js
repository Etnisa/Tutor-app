// add announcement             
let add_ann_btn = document.getElementById('add_ann_btn').addEventListener('click', add_ann_modal)

function add_ann_modal(){
    fetch('http://127.0.0.1:5000/add_ann_modal')
    .then(res => res.json())
    .then(data => {
        let ann_modal= document.getElementById('ann_modal')
        ann_modal.innerHTML = data

        ann_modal2 = new bootstrap.Modal(document.getElementById('ann_add_modal'), {});
        ann_modal2.show();

        document.getElementById('enlarged-close').addEventListener('click', () => { ann_modal2.hide() })
    })
    .catch(error => console.log(error))
    
}


// del announcement
let del_ann_btn = document.getElementsByClassName('del_ann_btn')

Array.from(del_ann_btn).forEach(element => {
    element.addEventListener('click', del_ann)
});

function del_ann(e) {
    id = e.target.closest('a').id
    console.log(id)
     fetch(`http://127.0.0.1:5000/del_ann/${id}`, {method: "POST"}).then(res=>{location.reload()})
     // temporary solution
    
}


