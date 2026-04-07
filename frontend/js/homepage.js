// frontend/js/homepage.js

async function renderHomepage() {
    const root = document.getElementById('app-root');
    root.innerHTML = '<div class="loader">Loading Poseidon...</div>';

    try {

        const response = await fetch('http://localhost:8000/search/landing');
        const data = await response.json();

        root.innerHTML = `
            <div class="home-container">
                <section class="hero-banner">
                    <h1>Discover Local Flavors</h1>
                    <p>Freshly delivered from the deep blue.</p>
                </section>

                <section class="featured-section">
                    <h2>Trending Now</h2>
                    <div class="horizontal-scroll">
                        ${data.featured.map(item => `
                            <div class="item-card-mini">
                                <span class="price">$${item.price}</span>
                                <h4>${item.item_name}</h4>
                            </div>
                        `).join('')}
                    </div>
                </section>

                <section class="restaurant-list">
                    <h2>Popular Restaurants</h2>
                    <div class="res-grid">
                        ${data.restaurants.items.map(res => `
                            <div class="res-card" onclick="viewRestaurant(${res.id})">
                                <h3>${res.name}</h3>
                                <p>${res._address}</p>
                                <button class="view-btn">View Menu</button>
                            </div>
                        `).join('')}
                    </div>
                </section>
            </div>
        `;
    } catch (err) {
        root.innerHTML = `<p class="error">Error loading home: ${err.message}</p>`;
    }
}