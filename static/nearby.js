"use strict";

// Show recent hummingbird sightings.


function placeMarkers(sighting) {
    // Function to place markers which include pop-ups with sighting date

    // alert(sighting);

    var marker = L.marker([sighting.lat, sighting.lng]).addTo(mymap);

    marker.bindPopup("Observed on " + sighting.obsDt.slice(0, 10));
}




function addSightings(results) {
    // Success function to be called when server answers.

    // alert(results);

    results.forEach(placeMarkers);
}



function informServer(evt) {
    // Function to be called when the Form Submit Event Listener's event happens.

    // Prevents the default action that belongs to the event; request will not go straight to the server.
    evt.preventDefault();

    // alert("Inside the informServer function!");

    // Getting the id value of the html element with the location-submit class,
    // which has been set to the eBird ID needed for the eBird API call
    const button = $(".location-submit");
    const buttonID = button.attr("id");

    // alert(buttonID);

    const url = "/nearby.json";
    const formData = {
        "latitude": $("#latitude-field").val(), 
        "longitude": $("#longitude-field").val(), 
        "eBirdID": buttonID
    };

    $.get(url, formData, addSightings);
}



// Form Submit Event Listener
$('#nearby-form').on('submit', informServer);



// Map Click Event Listener
mymap.on('click', (evt) => {
        $("#latitude-field").val(evt.latlng.lat); 
        $("#longitude-field").val(evt.latlng.lng);        
});


