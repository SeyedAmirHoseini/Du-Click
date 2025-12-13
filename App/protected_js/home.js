document.addEventListener('DOMContentLoaded', function () {

    const userInfo = JSON.parse(localStorage.getItem("userInfo"));

    //از متغییر گلوبال استفاده شده بخاطر ارتباط میان دو کد که همزمان در حال اجران
    window._gameState = {
        coin: userInfo.coin,
        current_energy: parseInt(userInfo.current_energy)
    };
    const state = window._gameState;

    // نمایش سکه و انرژی          
    const scoreDisplay = document.getElementById("buttonScore");
    const energyElement = document.getElementById("energyNumber");

    const term = parseInt(userInfo.term);
    const maxEnergy = term * 1000;
    const energyRate = maxEnergy / 3600;

    const updateDisplay = () => {
        scoreDisplay.textContent = state.coin;
        energyElement.textContent = `${Math.floor(state.current_energy)}/${maxEnergy}`;
    };

    updateDisplay();

    //انیمیشن دکمه ها            
    const topButton = document.querySelector(".topButton");
    const bottomButton = document.querySelector(".bottomButton");

    const animateButton = (button) => {
        button.style.transform = "translateY(10px)";
        setTimeout(() => {
            button.style.transform = "translateY(0)";
        }, 100);
    };

    // اضافه شدن سکه و کم شدن انرژی با کلیک 
    const increaseCoin = () => {
        if (state.current_energy < 1) return;
        state.coin += 1;
        state.current_energy -= 1;
        updateDisplay();
    };

    topButton.addEventListener("click", () => {
        animateButton(topButton);
        increaseCoin();
    });

    bottomButton.addEventListener("click", () => {
        animateButton(topButton);
        increaseCoin();
    });

    //اضافه شدن انرژی بر اساس زمان     
    setInterval(() => {
        state.current_energy += energyRate;
        if (state.current_energy > maxEnergy) state.current_energy = maxEnergy;
        updateDisplay();
    }, 1000);
});
