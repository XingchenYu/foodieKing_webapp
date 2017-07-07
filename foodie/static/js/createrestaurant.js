var map;
function initMap() {
    map = new google.maps.Map(document.getElementById("restaurantMap"), {
        center: {lat: 40.4435, lng: -79.9435},
        zoom: 16
    });
    var infoWindow = new google.maps.InfoWindow({map: map});
    console.log(infoWindow);
        var pos;
        if (navigator.geolocation) {
        navigator.geolocation.getCurrentPosition(function(position) {
            pos = {
                lat: position.coords.latitude,
                lng: position.coords.longitude
            };
            infoWindow.setPosition(pos);
            var content='<div class="iw_title">Locate Your Restaurant</div>';
            infoWindow.setContent(content);
            map.setCenter(pos);
        }, function () {
            handleLocationError(true, infoWindow, map.getCenter());
        });
    } else {
        // Browser doesn't support Geolocation
        handleLocationError(false, infoWindow, map.getCenter());
    }
}

/*
 * setRestaurantPos:
 * 		Set restaurant's position to where user clicks on the map.
 */
function setRestaurantPos(event) {
	var lat = event.latLng.lat();
    var lng = event.latLng.lng();
    var latInput = $("#resCoordX");
    var lngInput = $("#resCoordY");
    latInput.val(lat);
    lngInput.val(lng);
}

$(document).ready(function () {
    // Add event-handlers
	initMap();
    
    google.maps.event.addListener(map, "click", setRestaurantPos); 
    
    // CSRF set-up copied from Django docs
    function getCookie(name) {
        var cookieValue = null;
        if (document.cookie && document.cookie != '') {
            var cookies = document.cookie.split(';');
            for (var i = 0; i < cookies.length; i++) {
                var cookie = jQuery.trim(cookies[i]);
                // Does this cookie string begin with the name we want?
                if (cookie.substring(0, name.length + 1) == (name + '=')) {
                    cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                    break;
                }
            }
        }
        return cookieValue;
    }
    var csrftoken = getCookie('csrftoken');
    $.ajaxSetup({
        beforeSend: function (xhr, settings) {
            xhr.setRequestHeader("X-CSRFToken", csrftoken);
        }
    });
});

