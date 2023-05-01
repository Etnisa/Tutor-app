let l = document.getElementsByClassName('enlarge')
Array.from(l).forEach(element => {
    element.addEventListener('click', enlarge)
});

function enlarge(e) {
    id = e.target.closest('a').id

    fetch(`http://127.0.0.1:5000/announcement/${id}`, { mode: 'no-cors' })
        .then(res => res.json())
        .then(data => {
            let enlarge = document.getElementById('annouucement')
            enlarge.innerHTML = data
            console.log(data)
        })
        .catch(error => console.log(error))

}