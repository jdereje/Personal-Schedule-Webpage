//Jonathan Dereje
//Homework 3
//CSCI 4131

var map;
var markers = [];
var service;


function chgimg(name, txt) {
    var theimage = document.getElementById("image");
    theimage.src = name;
    theimage.alt = txt;

    var popupImageContainer = document.getElementById("image-section");
    popupImageContainer.style.display = "block";
}

//New Javascript added for Homework 3


//Initalizing the map, with the different services required

function initMap() {
    map = new google.maps.Map(document.getElementById('map'), {
        zoom: 13.8,
        center: { lat: 44.9727, lng: -93.23540000000003 }
    });

    var geocoder = new google.maps.Geocoder();

    var tableRows = document.querySelectorAll('#schedule-table tbody tr');
    var uniqueLocations = {};

    tableRows.forEach(function (row) {
        var cells = row.querySelectorAll('td');
        if (cells.length > 0) {
            var eventName = cells[1].textContent.trim();
            var eventTime = cells[2].textContent.trim();
            var location = cells[3].textContent.trim();

            geocodeAddress(geocoder, map, eventName, eventTime, location, uniqueLocations);
        }

    });
    document.getElementById('get-directions').addEventListener('click', function () {
        calculateAndDisplayRoute();
    });
    document.getElementById('search-places').addEventListener('click', function () {
        searchNearbyPlaces();
    });
    document.getElementById('keyword').addEventListener('input', function() {
        searchNearbyPlaces();
    });
    service = new google.maps.places.PlacesService(map);
    directionsService = new google.maps.DirectionsService();
    directionsDisplay = new google.maps.DirectionsRenderer();
    directionsDisplay.setMap(map);
}


//Functions used for finding directions and showing the route

function calculateAndDisplayRoute() {
    var destination = document.getElementById('destination').value;
    var travelMode = document.querySelector('input[name="travel-mode"]:checked').value;

    navigator.geolocation.getCurrentPosition(function (position) {
        var origin = {
            lat: position.coords.latitude,
            lng: position.coords.longitude
        };

        var request = {
            origin: origin,
            destination: destination,
            travelMode: travelMode
        };

        directionsService.route(request, function (result, status) {
            if (status == 'OK') {
                directionsDisplay.setDirections(result);
                showDirections(result);
            } else {
                window.alert('Directions request failed due to ' + status);
            }
        });
    }, function () {
        handleLocationError(true);
    });
}

function showDirections(response) {
    var directionsPanel = document.getElementById('directions-panel');
    directionsPanel.innerHTML = '';

    var route = response.routes[0];
    var summaryPanel = document.createElement('div');
    summaryPanel.classList.add('directions-summary');

  
    for (var i = 0; i < route.legs.length; i++) {
        var routeSegment = i + 1;
        summaryPanel.innerHTML += '<b>Route Segment: ' + routeSegment + '</b><br>';
        summaryPanel.innerHTML += route.legs[i].start_address + ' to ';
        summaryPanel.innerHTML += route.legs[i].end_address + '<br>';
        summaryPanel.innerHTML += route.legs[i].distance.text + '<br><br>';

        for (var j = 0; j < route.legs[i].steps.length; j++) {
            summaryPanel.innerHTML += route.legs[i].steps[j].instructions + '<br>';
        }
    }

    directionsPanel.appendChild(summaryPanel);
}


//Functions required to search for nearby places, within a 1500 meter radius

function searchNearbyPlaces() {
    const type = document.getElementById("category").value;
    const radius = parseInt(document.getElementById("radius").value);
    const myLocation = new google.maps.LatLng(44.9727, -93.23540000000003); 
    const request = {
        location: myLocation,
        radius: radius,
        type: [type],
    };

    service.nearbySearch(request, (results, status) => {
        if (status === google.maps.places.PlacesServiceStatus.OK) {
            clearMarkers();
            for (let i = 0; i < results.length; i++) {
                createMarker(results[i]);
            }
        } else {
            console.error("Error fetching nearby places:", status);
        }
    });
}


//Functions to create and clear the markers used

function createMarker(place) {
    var marker = new google.maps.Marker({
        map: map,
        position: place.geometry.location,
        
    });

    var infowindow = new google.maps.InfoWindow({
        content: '<strong>' + place.name + '</strong><br>' + place.vicinity
    });

    marker.addListener('click', function () {
        infowindow.open(map, marker);
    });

}

function clearMarkers() {
    for (var i = 0; i < markers.length; i++) {
        markers[i].setMap(null);
    }
    markers = [];
    
}


//Function for geocoding address, which includes the custom marker for the locations on the schedule. 

function geocodeAddress(geocoder, map, eventName, eventTime, address, uniqueLocations) {
    geocoder.geocode({ 'address': address }, function (results, status) {
        if (status === 'OK') {
            var location = results[0].geometry.location;
            var marker = new google.maps.Marker({
                map: map,
                position: location,
                title: eventName,
                icon: {
                    url: '../img/Goldy.png',
                    scaledSize: new google.maps.Size(35, 35) 
                }

            });
            clearMarkers();

            var infowindow = new google.maps.InfoWindow({
                content: '<strong>' + eventName + '</strong><br>' + eventTime + '<br>' + results[0].formatted_address
            });

            marker.addListener('click', function () {
                infowindow.open(map, marker);
            });


            if (!uniqueLocations.hasOwnProperty(location.toString())) {
                uniqueLocations[location.toString()] = true;
            } else {
                marker.setPosition(new google.maps.LatLng(location.lat() + 0.0001, location.lng() + 0.0001));
 
            }
        } else {
            console.error('Geocode was not successful for the following reason: ' + status);
        }
    });
}


