/* 
  This is a SAMPLE FILE to get you started.
  Please, follow the project instructions to complete the tasks.
*/

document.addEventListener('DOMContentLoaded', () => {
    const loginForm = document.getElementById('login-form');

    if (loginForm) {
        loginForm.addEventListener('submit', async (event) => {
            event.preventDefault();

            const email = document.getElementById('email').value;
            const password = document.getElementById('password').value;

            await loginUser(email, password);
        });
    }

    checkAuthentication();
    populatePriceFilter();
});

async function loginUser(email, password) {
    const response = await fetch('http://127.0.0.1:5005/api/v1/auth/login', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({ email, password })
    });

    if (response.ok) {
        const data = await response.json();
        document.cookie = `token=${data.access_token}; path=/`;
        window.location.href = 'index.html';
    } else {
        alert('Login failed: ' + response.statusText);
    }
}

function getCookie(name) {
    const cookies = document.cookie.split(';');
    for (let cookie of cookies) {
        const [key, value] = cookie.trim().split('=');
        if (key === name) {
            return value;
        }
    }
    return null;
}

function checkAuthentication() {
    const loginLink = document.getElementById('login-link');
    if (!loginLink) {
        return;
    }

    const token = getCookie('token');

    if (!token) {
        loginLink.style.display = 'block';
    } else {
        loginLink.style.display = 'none';
        fetchPlaces(token);
    }
}

async function fetchPlaces(token) {
    const placesList = document.getElementById('places-list');
    if (!placesList) {
        return;
    }

    const response = await fetch('http://127.0.0.1:5005/api/v1/places/', {
        method: 'GET',
        headers: {
            'Authorization': `Bearer ${token}`
        }
    });

    if (response.ok) {
        const places = await response.json();
        displayPlaces(places);
    }
}

function displayPlaces(places) {
    const placesList = document.getElementById('places-list');
    placesList.innerHTML = '';

    places.forEach((place) => {
        const placeCard = document.createElement('article');
        placeCard.className = 'place-card';
        placeCard.dataset.price = place.price;
        placeCard.innerHTML = `
            <h2>${place.title}</h2>
            <p>Price per night: $${place.price}</p>
            <button class="details-button">View Details</button>
        `;
        placesList.appendChild(placeCard);
    });
}

function populatePriceFilter() {
    const priceFilter = document.getElementById('price-filter');
    if (!priceFilter) {
        return;
    }

    const options = ['10', '50', '100', 'All'];
    options.forEach((value) => {
        const option = document.createElement('option');
        option.value = value;
        option.textContent = value;
        priceFilter.appendChild(option);
    });

    priceFilter.addEventListener('change', (event) => {
        const selected = event.target.value;
        const placeCards = document.querySelectorAll('.place-card');

        placeCards.forEach((card) => {
            const price = parseFloat(card.dataset.price);

            if (selected === 'All' || price <= parseFloat(selected)) {
                card.style.display = 'block';
            } else {
                card.style.display = 'none';
            }
        });
    });
}
