// frontend/js/api.js
// Central API configuration for all frontend pages.
// Update API_BASE if the backend runs on a different host or port.
const API_BASE = "http://localhost:8000";

/**
 * Sends a review to the backend.
 * Triggered by the onsubmit event in the restaurant review form.
 */
async function submitReview(event, restaurantId, orderId) {
    event.preventDefault(); // Prevents the page from refreshing automatically
    
    // Grab the data from the form fields
    const ratingValue = document.getElementById('rev-rating').value;
    const commentValue = document.getElementById('rev-comment').value;
    
    // Get the logged-in user from localStorage
    const user = JSON.parse(localStorage.getItem("user"));
    if (!user) {
        alert("You must be logged in to leave a review!");
        return;
    }

    // Match the exact keys
    const payload = {
        rating: parseInt(ratingValue),
        comment: commentValue,
        order_id: orderId,
        restaurant_id: restaurantId,
        customer_id: user.id
    };

    try {
        const response = await fetch(`${API_BASE}/reviews`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify(payload)
        });

        if (response.ok) {
            alert("🔱 Review sent! Poseidon appreciates your feedback.");
            
            // Refresh the restaurant view to show the new review in the list
            viewRestaurant(restaurantId); 
        } else {
            const errorData = await response.json();
            alert(`Error: ${errorData.detail || "Could not submit review."}`);
        }
    } catch (error) {
        console.error("API Error:", error);
        alert("The connection to the deep-sea server failed.");
    }
}