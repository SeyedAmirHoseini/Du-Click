document.addEventListener("DOMContentLoaded", function () {

    // دریافت داده‌های کاربر از تلگرام
    const tg = Telegram.WebApp;

    tg.expand();

    const user = tg.initDataUnsafe.user;
    const auth_date = tg.initDataUnsafe.auth_date;
    const hash = tg.initDataUnsafe.hash;

    // بررسی اینکه داده‌ها وجود دارند
    if (!user || !auth_date || !hash) {
    console.error("Missing user data!");
    alert("Failed to get user data.");
    }

    // ساخت شیء داده‌ها برای ارسال به سرور
    const userData = {
        init_data: JSON.stringify(tg.initData),
        auth_date: auth_date,
        first_name: user.first_name,
        telegram_id: user.id,
        last_name: user.last_name || "",
        language_code: user.language_code || "unknown",
        username: user.username || "",
        hash: hash  // هش را در آخر اضافه می‌کنیم
    };

    fetch(window.location.href, {
        method: "POST",
        headers: {
            "Content-Type": "application/json",
        },
        body: JSON.stringify(userData),
    })
    .then((response) => response.json())
    .then((data) => {
    if (!data.redirect_url) {
        alert("Something went wrong!");
        return;
    }

    if (data.status === "exists") {
        fetch('/api/user_info/', {
        method: "POST",
        headers: {
            "Content-Type": "application/json",
        },
        body: JSON.stringify({ 
            telegram_id: user.id,
            photo_url: user.photo_url
        })
        })
        .then((response) => response.json())
        .then((studentData) => {
            if (studentData.error) {
                alert("خطا در دریافت اطلاعات دانشجو: " + studentData.error);
                return;
            }
            localStorage.setItem("userInfo", JSON.stringify(studentData));
            window.location.href = data.redirect_url;
        })
        .catch(err => {
            console.error("Fetch error:", err);
            alert("خطا در دریافت اطلاعات کاربر");
        });
    } else {
        window.location.href = data.redirect_url;
    }
    })
    .catch((error) => {
        console.error("Error:", error);
        alert("خطا در ارتباط با سرور");
    });
});