function initMap() {
    const location = { lat: 38.8951, lng: -77.0364 }; // Example coordinates
    const map = new google.maps.Map(document.getElementById("map"), {
        zoom: 10,
        center: location,
    });
    new google.maps.Marker({
        position: location,
        map: map,
    });
}

// Load the Google Maps API asynchronously
function loadMap() {
    const script = document.createElement('script');
    script.src = `https://www.google.com/maps/place/Connaught+Place,+New+Delhi,+Delhi+110001,+India" target="_blank`;
    script.async = true;
    document.head.appendChild(script);
}

// Call loadMap when the page loads
window.onload = loadMap;
