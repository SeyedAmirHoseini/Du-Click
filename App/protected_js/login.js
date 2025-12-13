document.addEventListener('DOMContentLoaded', function() {
    const tg = Telegram.WebApp.initDataUnsafe;
    const telegram_id = tg.user.id;
    const photo_url = tg.user.photo_url;

    // عکس پروفایل
    fetch('/api/profile_photo/', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify({
            photo_url: photo_url,
            telegram_id: telegram_id
        })
    })
    .then(response => response.json())
    .then(data => {
        const smallImage = document.getElementById('smallImage');
        smallImage.src = data.photo_url;
    });

    const facultyLabel = document.querySelectorAll(".facultylabel");
    const defaultOption = document.querySelector(".default-option");

    facultyLabel.forEach(function(label){
        label.addEventListener("click", function(){
            defaultOption.style.visibility = "hidden";
            defaultOption.style.height = "0";
        });
    });

    $('.dropdown-el').click(function(e) {
        e.preventDefault();
        e.stopPropagation();
        $(this).toggleClass('expanded');
        $('#' + $(e.target).attr('for')).prop('checked', true);
    });
    $(document).click(function() {
        $('.dropdown-el').removeClass('expanded');
    });


    const codeInput = document.querySelector("input[name='code']");
    const facultyInputs = document.querySelectorAll("input[name='faculty']");
    const loginBtn = document.querySelector(".loginBtn");

    codeInput.addEventListener("keydown", function (event) {
        if (event.key === "Enter") {
            event.preventDefault();

            const firstFaculty = Array.from(facultyInputs).find(input => input.value !== "");
            if (firstFaculty) {
                const label = document.querySelector(`label[for="${firstFaculty.id}"]`);
                if (label) label.click();
                firstFaculty.focus();
            }
        }
    });

    facultyInputs.forEach(input => {
        input.addEventListener("keydown", function (event) {
            if (event.key === "Enter") {
                event.preventDefault();
                loginBtn.click();
            }
        });
    });

    document.querySelector(".loginBtn").addEventListener("click", async function(event) {
        event.preventDefault(); // جلوگیری از ارسال فرم پیش‌فرض
    
        const tg = Telegram.WebApp.initDataUnsafe
        const code = document.querySelector("input[name='code']").value; 
        const faculty = document.querySelector('input[name="faculty"]:checked').value; 
        const user_name = tg.user.first_name;  
        const user_id = tg.user.id; 
    
        const data = {
            name: user_name,
            telegram_id: user_id,
            code: code,
            faculty: faculty
        };
    

        if (!code.trim()) {
            alert("لطفاً شماره دانشجویی را وارد کنید.");
            return;
        }
        if (code.length !== 8 && code.length !== 9) {
            alert("شماره دانشجویی باید ۸ یا ۹ رقم باشد.");
            return;
        }
        if (!faculty || faculty === "") {
            alert("لطفاً یک دانشکده را انتخاب کنید.");
            return;
        }
        
        try {
            const response = await fetch(window.location.href, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify(data)
            });
    
            const responseData = await response.json();
            
            if (response.status === 201) {
                window.location.href = "/loading/";  
    
            } else {
                // اگر خطا دریافت شد، نمایش خطاها به کاربر
                if (responseData.errors) {
                    let errorMessages = '';
                    for (const [field, messages] of Object.entries(responseData.errors)) {
                        errorMessages += `${field}: ${messages.join(", ")}\n`;
                    }
                    alert("خطاها:\n" + errorMessages);
                } else {
                    alert("خطا در ارسال اطلاعات!");
                }
            }
    
        } catch (error) {
            console.error("خطا:", error);
            alert("مشکلی در ارسال اطلاعات پیش آمد.", error);
        }
    });
});