const tg = window.Telegram.WebApp;
tg.ready();
tg.expand();

const buttons = document.querySelectorAll(".nav-btn");
const pages = document.querySelectorAll(".page");

buttons.forEach(btn => {
    btn.onclick = () => {
        const pageId = btn.dataset.page;
        pages.forEach(p => p.classList.remove("active"));
        document.getElementById(pageId).classList.add("active");

        buttons.forEach(b => b.classList.remove("active"));
        btn.classList.add("active");
    }
});

// Показать первую страницу по умолчанию
pages[0].classList.add("active");
buttons[0].classList.add("active");