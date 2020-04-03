"use strict";

// Show recent hummingbird sightings.


function placeMarkers(sighting) {
    
    // console.log(sighting);

    var marker = L.marker([sighting.lat, sighting.lng]).addTo(mymap);

    marker.bindPopup("Observed on " + sighting.obsDt.slice(0, 10));
}

    // 'locId': 'L1521686', 
    //  'locName': '2223 Kodiak Dr NE', 
    // 'obsDt': '2020-03-03 17:07', 
    // 'howMany': 1,
    // var res = str.slice(0, 3);



// Success function to be called when server answers. Sends info. on to browser.
function addSightings(results) {

    // console.log(results);

    results.forEach(placeMarkers);
}



// Function to be called when the Event Listener's event happens.
function informServer(evt) {
    // Prevents the default action that belongs to the event; request will not go straight to the server.
    evt.preventDefault();

    // alert("Inside the informServer function!");

    // console.log("In the informServer function!");


    // const button = $(evt.target);
    const button = $(".location-submit");
    const buttonID = button.attr("id");

    console.log(buttonID);

    const url = "/nearby.json";
    const formData = {
        "latitude": $("#latitude-field").val(), 
        "longitude": $("#longitude-field").val(), 
        "eBirdID": buttonID
    };

    $.get(url, formData, addSightings);
}


// Event Listener
$('#nearby-form').on('submit', informServer);