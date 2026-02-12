document.addEventListener("DOMContentLoaded", () => {
    try {
        const raw = JSON.parse(localStorage.getItem("courses") || "{}");
        const data = raw.courses || [];



        if (!Array.isArray(data)) {
            throw new Error("Courses is not an array");
        }

        const container = document.getElementById("coursesContainer");

        function renderCourses() {
            container.innerHTML = "";

            data.forEach(course => {
                const card = document.createElement("div");
                card.classList.add("course-card");

                card.innerHTML = `
                    <span class="course-title">${course.name}</span>
                    <button class="course-btn">انتخاب</button>
                `;


                const passed = course.status?.passed;
                const available = course.status?.available;

                if (passed === "❌") {

                    if (available === true) {
                        card.addEventListener("click", () => {
                            selectCourse(course.id);
                        });
                    } else {
                        addOverlay(card, "🔒");
                        card.classList.add("disabled");
                    }

                } else if (passed === "✅") {
                    addOverlay(card, "✅");
                    card.classList.add("disabled");

                } else if (passed === "❔") {
                    addOverlay(card, "❔");
                    card.classList.add("disabled");
                }

                container.appendChild(card);
            });
        }

        function addOverlay(card, icon) {
            const overlay = document.createElement("div");
            overlay.classList.add("status-overlay");
            overlay.innerText = icon;
            card.appendChild(overlay);
        }

        function selectCourse(courseId) {
            console.log("Selected:", courseId);
        }

        renderCourses();


    } catch (err) {
        console.error(err);
        alert(err.message);
    }
});
