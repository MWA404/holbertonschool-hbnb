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
    initAddReviewPage();
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

function getPlaceIdFromURL() {
    const params = new URLSearchParams(window.location.search);
    return params.get('id');
}

function checkAuthentication() {
    const loginLink = document.getElementById('login-link');
    const token = getCookie('token');

    if (loginLink) {
        loginLink.style.display = token ? 'none' : 'block';
    }

    fetchPlaces(token);

    const addReviewSection = document.getElementById('add-review');
    if (addReviewSection) {
        addReviewSection.style.display = token ? 'block' : 'none';
    }

    const placeDetailsSection = document.getElementById('place-details');
    if (placeDetailsSection) {
        const placeId = getPlaceIdFromURL();
        if (placeId) {
            fetchPlaceDetails(token, placeId);

            const addReviewLink = document.querySelector(
                '#add-review a.details-button');
            if (addReviewLink) {
                addReviewLink.href = `add_review.html?id=${placeId}`;
            }
        }
    }
}

async function fetchPlaces(token) {
    const placesList = document.getElementById('places-list');
    if (!placesList) {
        return;
    }

    const headers = {};
    if (token) {
        headers['Authorization'] = `Bearer ${token}`;
    }

    const response = await fetch('http://127.0.0.1:5005/api/v1/places/', {
        method: 'GET',
        headers: headers
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

        const detailsButton = placeCard.querySelector('.details-button');
        detailsButton.addEventListener('click', () => {
            window.location.href = `place.html?id=${place.id}`;
        });

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

async function fetchPlaceDetails(token, placeId) {
    const headers = {};
    if (token) {
        headers['Authorization'] = `Bearer ${token}`;
    }

    const response = await fetch(
        `http://127.0.0.1:5005/api/v1/places/${placeId}`,
        {
            method: 'GET',
            headers: headers
        }
    );

    if (response.ok) {
        const place = await response.json();
        displayPlaceDetails(place);
    }
}

function displayPlaceDetails(place) {
    const placeDetailsSection = document.getElementById('place-details');
    placeDetailsSection.innerHTML = '';

    const heading = document.createElement('h2');
    heading.textContent = place.title;
    placeDetailsSection.appendChild(heading);

    const info = document.createElement('div');
    info.className = 'place-info';

    const ownerName = place.owner
        ? `${place.owner.first_name} ${place.owner.last_name}`
        : 'Unknown';

    info.innerHTML = `
        <p>Host: ${ownerName}</p>
        <p>Price per night: $${place.price}</p>
        <p>Description: ${place.description || ''}</p>
        <p>Amenities:</p>
    `;

    const amenityIcons = {
        'wifi': 'images/icon_wifi.png',
        'bed': 'images/icon_bed.png',
        'bath': 'images/icon_bath.png',
        'bathroom': 'images/icon_bath.png'
    };

    place.amenities.forEach((amenity) => {
        const amenityLine = document.createElement('p');
        const key = amenity.name.toLowerCase();
        const iconSrc = amenityIcons[key];

        if (iconSrc) {
            const icon = document.createElement('img');
            icon.src = iconSrc;
            icon.alt = amenity.name + ' icon';
            amenityLine.appendChild(icon);
        }

        amenityLine.appendChild(document.createTextNode(amenity.name));
        info.appendChild(amenityLine);
    });

    placeDetailsSection.appendChild(info);

    const reviewsSection = document.getElementById('reviews');
    reviewsSection.innerHTML = '';

    place.reviews.forEach((review) => {
        const reviewCard = document.createElement('article');
        reviewCard.className = 'review-card';
        reviewCard.innerHTML = `
            <p>${review.text}</p>
            <p>${review.user_name}</p>
            <p>Rating: ${review.rating}</p>
        `;
        reviewsSection.appendChild(reviewCard);
    });
}

function initAddReviewPage() {
    const reviewForm = document.getElementById('review-form');
    if (!reviewForm) {
        return;
    }

    const token = getCookie('token');
    if (!token) {
        window.location.href = 'index.html';
        return;
    }

    const placeId = getPlaceIdFromURL();

    reviewForm.addEventListener('submit', async (event) => {
        event.preventDefault();

        const reviewText = document.getElementById('review').value;
        const rating = document.getElementById('rating').value;

        const response = await submitReview(
            token, placeId, reviewText, rating);
        await handleResponse(response, reviewForm);
    });
}

async function submitReview(token, placeId, reviewText, rating) {
    return fetch('http://127.0.0.1:5005/api/v1/reviews/', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
            'Authorization': `Bearer ${token}`
        },
        body: JSON.stringify({
            text: reviewText,
            rating: parseInt(rating, 10),
            place_id: placeId
        })
    });
}

async function handleResponse(response, reviewForm) {
    if (response.ok) {
        alert('Review submitted successfully!');
        reviewForm.reset();
    } else {
        const data = await response.json().catch(() => ({}));
        alert(data.error || 'Failed to submit review');
    }
}
