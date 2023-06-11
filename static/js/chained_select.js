function chained_select() {
    console.log('chained select')

    let degree_courseSel = document.getElementById("degree_course");
    let subjectSel = document.getElementById("subject");
    let semesterSel = document.getElementById("semester");
    for (let x in subjectObject) {
        degree_courseSel.options[degree_courseSel.options.length] = new Option(x, x);
    }
    degree_courseSel.onchange = function () {
        //empty Chapters- and Topics- dropdowns
        semesterSel.length = 1;
        subjectSel.length = 1;
        //display correct values
        for (let y in subjectObject[this.value]) {
            subjectSel.options[subjectSel.options.length] = new Option(y, y);
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
}