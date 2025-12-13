document.addEventListener('DOMContentLoaded', function () {
    const tg = Telegram.WebApp;
    const telegramId = tg.initDataUnsafe.user.id;
    const userInfo = JSON.parse(localStorage.getItem("userInfo"));

    // ============================
    //          loading
    // ============================
    const createLoadingOverlay = () => {
        if (document.getElementById("loading")) return;

        const overlay = document.createElement("div");
        overlay.id = "loading";
        overlay.className = "loading-overlay";

        const loader = document.createElement("div");
        loader.className = "loader";

        overlay.appendChild(loader);
        document.body.appendChild(overlay);
    };
    createLoadingOverlay();

    const loading = document.getElementById("loading");

    // نمایش لودینگ تا زمانی که صفحه کامل load شود
    if (loading) loading.style.display = "flex";
    window.addEventListener("load", () => {
        if (loading) loading.style.display = "none";
    });

    // نمایش لودینگ قبل از ترک صفحه
    window.addEventListener("beforeunload", () => {
        if (loading) loading.style.display = "flex";
    });

    // ============================
    //           header
    // ============================

    //نمایش پروفایل
    const profilePic = document.getElementById("profile-photo");
    const code = document.getElementById('code');

    if (profilePic && code && userInfo) {
        profilePic.src = userInfo.picture;
        code.textContent = userInfo.code;
    }

    //نمایش دروس ترم و کارکردش
    document.getElementById("term-btn").addEventListener("click", () => {
        fetch("/api/current_courses/", {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({ telegram_id: telegramId })
        })
        .then(res => res.json())
        .then(data => {
            const rows = data.map(item => `
                <tr>
                    <td>${item.course}</td>
                    <td>${item.professor}</td>
                    <td>${item.credit}</td>
                    <td>${item.prerequisite ?? "-"}</td>
                </tr>
            `).join("");

            const modal = document.createElement("div");
            modal.className = "modal-backdrop";
            modal.id = "term-modal";

            modal.innerHTML = `
                <div class="modal-box">
                    <div class="modal-header">
                        <span>دروس ترم جاری</span>
                        <span class="close-btn" id="close-modal">✖</span>
                    </div>

                    <div class="modal-table-wrapper">
                        <table class="modal-table">
                            <thead>
                                <tr>
                                    <th>درس</th>
                                    <th>استاد</th>
                                    <th>واحد</th>
                                    <th>پیش‌نیاز</th>
                                </tr>
                            </thead>
                            <tbody>${rows}</tbody>
                        </table>
                    </div>
                </div>
            `;

            document.body.appendChild(modal);

            document.getElementById("close-modal").onclick = () => modal.remove();
        })
        .catch(err => console.error("Fetch error:", err));
    });

    // ============================
    //             nav
    // ============================
    const chartBtn = document.getElementById("chart-btn");
    const shopBtn = document.getElementById("shop");
    const ertebatBtn = document.getElementById("ertebat");
    const profBtn = document.getElementById("prof");
    const middleBar = document.getElementById("middle-bar");

    const path = window.location.pathname;


    //انیمیشن دکمه ها
    // فعال شدن خودکار انیمیشن هر صفحه
    if (path !== '/home') {
        if (path.startsWith('/chart')) chartBtn.classList.add("active");
        else if (path.startsWith('/shop')) shopBtn.classList.add("active");
        else if (path.startsWith('/ertebat')) ertebatBtn.classList.add("active");
        else if (path.startsWith('/prof')) profBtn.classList.add("active");
    }

    //فعال کردنش در صورت کلیک رو آنها
    const buttons = document.querySelectorAll(".leftbar a, .rightbar a");
    buttons.forEach(btn => {
        btn.addEventListener("click", () => {
            buttons.forEach(b => b.classList.remove("active"));
            btn.classList.add("active");
        });
    });

    // رندر شدن صفحه به همراه لودینگ
    const navigateWithLoading = (url) => {
        if (loading) loading.style.display = "flex";
        setTimeout(() => window.location.href = url, 50);
    };

    middleBar.addEventListener("click", () => navigateWithLoading("/home"));

    //گرفتن داده ها از سرور و ثبت در لوکال برای استفاده در صفحه بعد
    chartBtn.addEventListener("click", async (e) => {
        e.preventDefault();
        if (!telegramId) return alert("Telegram ID not found!");

        if (loading) loading.style.display = "flex";

        try {
            const res = await fetch("/api/faculty_courses/", {
                method: "POST",
                headers: { "Content-Type": "application/json" },
                body: JSON.stringify({ telegram_id: telegramId })
            });
            const data = await res.json();
            localStorage.setItem("courses", JSON.stringify(data));
            navigateWithLoading("/chart");
        } catch (err) {
            console.error(err);
            alert("خطا در بارگذاری داده‌ها!");
            if (loading) loading.style.display = "none"; // اگر ارور خورد لودینگی که فعال شده بود رو حذف کن
        }
    });

    // ============================
    //   sending data to server 
    // ============================
    function sendDataToServer() {
        const state = window._gameState || JSON.parse(localStorage.getItem("userInfo"));
        const lastUserInfo = JSON.parse(localStorage.getItem("userInfo"));

        lastUserInfo.coin = state.coin;
        lastUserInfo.current_energy = state.current_energy;
        lastUserInfo.last_time_energy = new Date().toISOString();
        localStorage.setItem("userInfo", JSON.stringify(lastUserInfo));

        const user = tg.initDataUnsafe.user;

        const data = {
            init_data: JSON.stringify(tg.initData),
            auth_date: tg.initDataUnsafe.auth_date,
            first_name: user.first_name,
            telegram_id: user.id,
            last_name: user.last_name || "",
            language_code: user.language_code || "unknown",
            username: user.username || "",
            hash: tg.initDataUnsafe.hash,
            coin: state.coin,
            last_time_energy: new Date().toISOString(),
            current_energy: Math.floor(state.current_energy)
        };

        const blob = new Blob([JSON.stringify(data)], { type: "application/json" });
        const endpoint = `${window.location.origin}/api/update_coin/`;
        navigator.sendBeacon(endpoint, blob);
    }
cd
    //ارسال خودکار داده ها به سرور
    window.addEventListener('beforeunload', function () {
        sendDataToServer();
    });
    document.addEventListener("visibilitychange", function () {
        if (document.visibilityState === "hidden") {
            sendDataToServer();
        }
    });

});