const tg = window.Telegram.WebApp;
tg.ready();

const SERVER_URL = "https://telegram-schedulebot.vercel.app/";

const form = document.getElementById("reminderForm");
const output = document.getElementById("output");
const daysInput = document.getElementById("days");

const selectedDays = new Set();

document.querySelectorAll(".day").forEach(btn => {
    btn.addEventListener("click", () => {
        const day = btn.dataset.day;

        if (selectedDays.has(day)) {
            selectedDays.delete(day);
            btn.classList.remove("active");
        } else {
            selectedDays.add(day);
            btn.classList.add("active");
        }

        daysInput.value = Array.from(selectedDays).join(",");
        tg.HapticFeedback.impactOccurred("light");
    });
});

document.getElementById("weekdays").onclick = () => {
    selectDays(["mon","tue","wed","thu","fri"]);
};

document.getElementById("alldays").onclick = () => {
    selectDays(["mon","tue","wed","thu","fri","sat","sun"]);
};

function selectDays(days) {
    selectedDays.clear();
    document.querySelectorAll(".day").forEach(b => b.classList.remove("active"));

    days.forEach(d => {
        selectedDays.add(d);
        document.querySelector(`[data-day="${d}"]`).classList.add("active");
    });

    daysInput.value = days.join(",");
}

form.addEventListener("submit", async e => {
    e.preventDefault();

    if (!daysInput.value) {
        output.innerText = "❌ Выбери дни";
        return;
    }

    const data = {
        chat_id: tg.initDataUnsafe.user.id,
        text: document.getElementById("text").value,
        time: document.getElementById("time").value,
        days: daysInput.value
    };

    const res = await fetch(SERVER_URL, {
        method: "POST",
        headers: {"Content-Type": "application/json"},
        body: JSON.stringify(data)
    });

    if (res.ok) {
        output.innerText = "✅ Напоминание создано";
        form.reset();
        selectedDays.clear();
        document.querySelectorAll(".day").forEach(b => b.classList.remove("active"));
        daysInput.value = "";
    } else {
        output.innerText = "❌ Ошибка";
    }
});