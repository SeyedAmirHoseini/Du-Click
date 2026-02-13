document.addEventListener('DOMContentLoaded', function() {
    const link = document.getElementById('support-link');

    link.addEventListener('click', function(e) {
        e.preventDefault();

        window.location.href = "https://t.me/DuClick_bot?start=support";

        if (window.Telegram && Telegram.WebApp) {
            Telegram.WebApp.close();
        }
    });
});
