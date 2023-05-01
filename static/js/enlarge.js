let l = document.getElementsByClassName('enlarge')
Array.from(l).forEach(element => {
    element.addEventListener('click', enlarge)
});

let myModal

function enlarge(e) {
    id = e.target.closest('a').id

    fetch(`http://127.0.0.1:5000/announcement/${id}`)
        .then(res => res.json())
        .then(data => {
            let enlarge = document.getElementById('annoucement')
            enlarge.innerHTML = data
            console.log(data)
            myModal = new bootstrap.Modal(document.getElementById('enlarged'), {});
            myModal.show();

            document.getElementById('enlarged-close').addEventListener('click', () => { myModal.hide() })
        })
        .catch(error => console.log(error))

}