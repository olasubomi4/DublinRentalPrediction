// Select the form and the price display element
const form = document.querySelector('form');
const priceDisplay = document.querySelector('.price-display');

// Add an event listener for form submission
form.addEventListener('submit', async (event) => {
    event.preventDefault(); // Prevent the default form submission

    // Gather form data
    const district = document.getElementById('districtSelect').value;
    const accommodates = document.getElementById('accommodates').value;
    const beds = document.getElementById('beds').value;
    const bedrooms = document.getElementById('bedrooms').value;
    const bathrooms = document.getElementById('bathrooms').value;
    const minNights = document.getElementById('minNights').value;
    const roomType = document.getElementById('roomTypeSelect').value;

    // List all available amenities
    const allAmenities = Array.from(document.querySelectorAll('.amenities-group input'))
        .map(checkbox => checkbox.value);

    // Gather selected amenities
    const selectedAmenities = Array.from(document.querySelectorAll('.amenities-group input:checked'))
        .map(checkbox => checkbox.value);

    // Create an object to store each amenity with a value of 1 if selected, otherwise 0
    const amenitiesData = allAmenities.reduce((acc, amenity) => {
        acc[amenity] = selectedAmenities.includes(amenity) ? 1 : 0;
        return acc;
    }, {});

    // Gather selected property type
    const propertyType = document.querySelector('input[name="property-type"]:checked').value;

    // Create an object to send to the API
    const data = {
        district,
        accommodates,
        beds,
        bedrooms,
        bathrooms,
        min_nights: minNights,
        room_type: roomType,
        ...amenitiesData,
        property_type: propertyType,
        model: 'randomForest'
    };

    try {
        // Send a POST request to the Flask API
        const response = await fetch('https://dublinrentalprediction.onrender.com/predict', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify(data),
        });

        if (!response.ok) {
            throw new Error('Network response was not ok');
        }

        // Parse the JSON response
        const result = await response.json();

        // Update the price display
        priceDisplay.textContent = `Estimated Price: €${result.predictions.toFixed(2)}`;
    } catch (error) {
        priceDisplay.textContent = 'Error estimating price. Please try again.';
    }
});

// Function to update the displayed count
function updateCount(input) {
    const countId = `${input.id}Count`;
    document.getElementById(countId).textContent = input.value;
}

// Set the initial count and add event listeners for real-time updates
document.querySelectorAll('.range-input').forEach(input => {
    updateCount(input); // Set the initial value
    input.addEventListener('input', () => updateCount(input)); // Update on input change
});
