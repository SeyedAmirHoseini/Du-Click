document.addEventListener('DOMContentLoaded', function () {


    const userInfo = JSON.parse(localStorage.getItem("userInfo"));

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
    

    const submitBtn = document.querySelector(".submitBtn");

    submitBtn.addEventListener("click", function () {

        const newName = name_edit.value;

        if (!newName) {
            alert("نام را وارد کنید");
            return;
        }

        const tg = Telegram.WebApp;
        const telegramId = tg.initDataUnsafe.user.id;

        fetch("/update/profile", {
            method: "POST",
            headers: {
                "Content-Type": "application/json",
            },
            body: JSON.stringify({
                telegram_id: telegramId,
                name: newName
            })
        })
        .then(response => response.json())
        .then(data => {
            if (data.success) {

                userInfo.name = newName;
                localStorage.setItem("userInfo", JSON.stringify(userInfo));

                location.reload();
            } else {
                alert(data.error);
            }
        })
        .catch(error => {
            console.error("Error:", error);
        });

    });

});
