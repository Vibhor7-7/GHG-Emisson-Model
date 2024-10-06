// Initialize the map
function initMap() {
    const mapOptions = {
        zoom: 2,
        center: { lat: 20, lng: 0 },  // Center the map on the equator
        styles: [/* Insert any custom map styles here if needed */]
    };

    const map = new google.maps.Map(document.getElementById("map"), mapOptions);

    // Add click event listener on map
    map.addListener("click", (event) => {
        const lat = event.latLng.lat();
        const lon = event.latLng.lng();

        // Call function to fetch GHG data and display city info
        fetchGHGData(lat, lon);
    });
}

// Function to fetch GHG data based on latitude and longitude
function fetchGHGData(lat, lon) {
    fetch(`/api/ghg?lat=${lat}&lon=${lon}`)
        .then(response => response.json())
        .then(data => {
            displayCityInfo(data);
        })
        .catch(error => {
            console.error('Error fetching GHG data:', error);
        });
}

// Function to display city and GHG information
function displayCityInfo(data) {
    const cityInfoDiv = document.getElementById("cityInfo");

    const ghgEmission = data.ghg_emission;
    const lat = data.latitude;
    const lon = data.longitude;

    // Customize the HTML content for city info
    cityInfoDiv.innerHTML = `
        <div class="city-info-container">
            <h2>City Information</h2>
            <p><strong>Latitude:</strong> ${lat}</p>
            <p><strong>Longitude:</strong> ${lon}</p>
            <p><strong>Estimated GHG Emissions:</strong> ${ghgEmission} tons/year</p>
        </div>
        <button onclick="closeCityInfo()">Close</button>
    `;

    cityInfoDiv.style.display = "block";
}

// Function to close the city info modal
function closeCityInfo() {
    const cityInfoDiv = document.getElementById("cityInfo");
    cityInfoDiv.style.display = "none";
}

// Wait for DOM to load before initializing the map
document.addEventListener("DOMContentLoaded", function () {
    initMap();
});
