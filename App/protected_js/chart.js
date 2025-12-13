document.addEventListener("DOMContentLoaded", () => {
    try {
        const data = JSON.parse(localStorage.getItem("courses"));
        if (!data || !data.courses) throw new Error("Courses data not found in localStorage");

        const courses = data.courses;
        const tbody = document.getElementById("chart-body");
        if (!tbody) throw new Error("chart-body element not found");

        tbody.innerHTML = "";

        courses.forEach(course => {
            const tr = document.createElement("tr");

            const status = course.status?.passed || "❔";
            const prereq = course.prerequisite
                ? courses.find(x => x.id === course.prerequisite)?.name || "نامشخص"
                : "—";

            tr.innerHTML = `
                <td class="chart-status">${status}</td>
                <td>${prereq}</td>
                <td>${course.credits}</td>
                <td>${course.name}</td>
            `;
            tbody.appendChild(tr);
        });

    } catch (err) {
        console.error("Chart.js error:", err);
        alert("خطا در بارگذاری چارت: " + err.message);
    }
});
