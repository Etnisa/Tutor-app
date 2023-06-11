function slice_subject(subject, max_len){
    if (subject.length > max_len){
        subject = subject.slice(0, max_len)
        subject = subject + '...'
    }
    return subject
}

function chained_select(selected = null) {
    console.log('chained select')

    for (let x in subjectObject) {
        degree_courseSel.options[degree_courseSel.options.length] = new Option(x, x);
    }

    console.log('selected: ', selected)

    degree_courseSel.onchange = function () {
        //empty Chapters- and Topics- dropdowns
        semesterSel.length = 1;
        subjectSel.length = 1;
        //display correct values
        for (let y in subjectObject[this.value]) {
            subjectSel.options[subjectSel.options.length] = new Option(slice_subject(y, 44), y);
        }
    }
    subjectSel.onchange = function () {
        //empty Chapters dropdown
        semesterSel.length = 1;
        //display correct values
        let z = subjectObject[degree_courseSel.value][this.value];
        for (let i = 0; i < z.length; i++) {
            semesterSel.options[semesterSel.options.length] = new Option(z[i], z[i]);
        }
    }

    
    if (selected != null) {
        const event = new Event('change');
        degree_courseSel.value = selected[0]
        degree_courseSel.dispatchEvent(event)
        subjectSel.value = selected[1]
        subjectSel.dispatchEvent(event)
        semesterSel.value = selected[2].trim()
    }

}