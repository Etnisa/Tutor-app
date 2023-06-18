let l = document.getElementsByClassName('enlarge')
Array.from(l).forEach(element => {
    element.addEventListener('click', enlarge)
});


function enlarge(e) {
    id = e.target.closest('a').id

    fetch(`/announcement/${id}`)
        .then(res => res.json())
        .then(data => {
            let enlarge_modal
            let enlarge = document.getElementById('annoucement')
            enlarge.innerHTML = data
                // console.log(data)
            enlarge_modal = new bootstrap.Modal(document.getElementById('enlarged'), {});
            enlarge_modal.show();

            document.getElementById('enlarged-close').addEventListener('click', () => { enlarge_modal.hide() })
        })
        .catch(error => console.log(error))

}