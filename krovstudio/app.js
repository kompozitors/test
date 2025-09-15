// Simple front-end login using localStorage
const loginForm = document.getElementById('loginForm');
const usernameInput = document.getElementById('username');
const userArea = document.getElementById('userArea');
const welcome = document.getElementById('welcome');
const logoutBtn = document.getElementById('logoutBtn');

function checkAuth() {
    const user = localStorage.getItem('krovstudio_user');
    if (user) {
        welcome.textContent = `Привет, ${user}!`;
        loginForm.classList.add('hidden');
        userArea.classList.remove('hidden');
    } else {
        loginForm.classList.remove('hidden');
        userArea.classList.add('hidden');
    }
}

loginForm.addEventListener('submit', (e) => {
    e.preventDefault();
    const name = usernameInput.value.trim();
    if (name) {
        localStorage.setItem('krovstudio_user', name);
        usernameInput.value = '';
        checkAuth();
    }
});

logoutBtn.addEventListener('click', () => {
    localStorage.removeItem('krovstudio_user');
    checkAuth();
});

// Roof calculator
const calcForm = document.getElementById('calcForm');
const calcResult = document.getElementById('calcResult');

calcForm.addEventListener('submit', (e) => {
    e.preventDefault();
    const length = parseFloat(document.getElementById('length').value);
    const width = parseFloat(document.getElementById('width').value);
    const slope = parseFloat(document.getElementById('slope').value);
    if (length > 0 && width > 0 && slope >= 0) {
        const area = length * width * (1 + slope / 100);
        const price = area * 500; // примерная цена
        calcResult.textContent = `Площадь: ${area.toFixed(2)} м², Стоимость: ${price.toFixed(0)} руб.`;
    }
});

// Contact form placeholder
const contactForm = document.getElementById('contactForm');
contactForm.addEventListener('submit', (e) => {
    e.preventDefault();
    alert('Сообщение отправлено!');
    contactForm.reset();
});

// Initialize
checkAuth();

// mobile nav
const menuToggle = document.getElementById('menuToggle');
const navMenu = document.getElementById('navMenu');
menuToggle.addEventListener('click', () => {
    navMenu.classList.toggle('open');
});
