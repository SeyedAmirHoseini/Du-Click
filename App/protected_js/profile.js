document.addEventListener('DOMContentLoaded', function () {

    const userInfo = JSON.parse(localStorage.getItem("userInfo"));
    // const text = Object.entries(userInfo)
    // .map(([key, value]) => `${key} : ${value}`)
    // .join("\n");

    // alert(text);
    const smallImage = document.getElementById('smallImage');
    smallImage.src = userInfo.picture;

    const code = document.getElementById('codeprof');
    code.textContent = userInfo.code;

    const name = document.getElementById('nameprof');
    name.textContent = userInfo.name;

    const faculty = document.getElementById('facultyprof');
    faculty.textContent = Object.values(userInfo.faculty)[1];

    const name_edit = document.getElementById("name-edit");
    const code_edit = document.getElementById("code-edit");
    name_edit.value = userInfo.name;
    code_edit.placeholder = userInfo.code;
    code_edit.disabled = true;


})