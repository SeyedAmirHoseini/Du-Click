document.addEventListener('DOMContentLoaded', function() {
    const link = document.getElementById('support-link');

    link.addEventListener('click', function(e) {
        e.preventDefault();

        // باز کردن لینک در همان WebApp
        window.location.href = "https://t.me/DuClick_bot?start=support";

        // اگر میخوای فقط WebApp پایین بیاد، نه بسته بشه:
        if (window.Telegram && Telegram.WebApp) {
            // جمع کردن WebApp به حالت collapsed
            Telegram.WebApp.expand(); // یا contract() برای جمع کردن
        }
    });
});
