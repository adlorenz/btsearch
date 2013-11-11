/**
 * Author: Tomasz Wasiak
 */
(function($){
var markers = [];
var map;
var selectedIcon = "http://chart.googleapis.com/chart?chst=d_map_pin_letter&chld=|ff0000|000000";
var currentIcon = "http://chart.googleapis.com/chart?chst=d_map_pin_letter&chld=|00ff00|000000";
var normalIcon = "http://chart.googleapis.com/chart?chst=d_map_pin_letter&chld=|ff776b|000000";
var currentMarker;
var selectedMarker = -1;
var selectedLocation = -1;

function clearMap() {
    for (i in markers) markers[i].setMap(null)
}

function attachClickEvent(i,id,content){
	google.maps.event.addListener(markers[i], 'click', function(){
        if(currentMarker!=i) {
            if(selectedMarker>-1){
                markers[selectedMarker].setIcon(normalIcon);
            }
            selectedMarker = i;
            selectedLocation = id;
            markers[i].setIcon(selectedIcon);
            $("#id_location_selected").val(content);
            $(".location_selected").show("slow");
        }
    });
}

$(document).ready(function(){

    var locInput = $("#id_location");
    locInput.parents(".form-row").after('<div class="form-row"><div id="lsMap"></div></div>');
    $("#id_location_selected").before('<input id="updateLocation" type="button" value="Update location" />');

        var latLng = [52.1673,20.8109];
		var showMarkers = false;
		var mapZoom = 5;
        if ($("#id_location_coords").val() != ',') {
            latLng = $("#id_location_coords").val().split(",");
			showMarkers = true;
			mapZoom = 12;
        } else {
            var address = $("#id_location_info").val();
            var geocoder = new google.maps.Geocoder();
            geocoder.geocode( { 'address': address}, function(results, status) {
                if (status == google.maps.GeocoderStatus.OK) {
                    map.fitBounds(results[0].geometry.viewport);
                }
            });
        }
        var center = new google.maps.LatLng(latLng[0],latLng[1]);

    var myOptions = {
        zoom: mapZoom,
        center: center,
        streetViewControl: false,
        mapTypeId: google.maps.MapTypeId.ROADMAP
    }
    map = new google.maps.Map(document.getElementById("lsMap"), myOptions);

    google.maps.event.addListener(map, 'idle', function() {
        if(map.getZoom()>11) {
            getLocations();
        } else {
            clearMap();
        }
    });

    function getLocations() {
        $.ajax({
            url: "/map/locations/?bounds=" + map.getBounds().toUrlValue(),
            dataType: "json",
            headers: {
				Accept: "application/json"
			},
            success:function(data){
                clearMap();
                data = data.objects;
                for (i in data){
                    var icon = normalIcon;
                    if(data[i].id==locInput.val()){
                        icon = currentIcon;
                        currentMarker = i;
                    }
                    if(data[i].id==selectedLocation){
                        icon = selectedIcon;
                        selectedMarker = i;
                    }
                    markers[i] = new google.maps.Marker({
                        position: new google.maps.LatLng(data[i].latitude,data[i].longitude),
                        icon: icon,
                        map: map
                    });
                    attachClickEvent(i,data[i].id,data[i].summary);
                }
            }
        });
    }

    $("#updateLocation").click(function(){
        $("#id_location").val(selectedLocation);
        $("#id_location_info").val($("#id_location_selected").val());
        markers[currentMarker].setIcon(normalIcon);
        markers[selectedMarker].setIcon(currentIcon);
        $(".location_selected").hide("slow");
        $("#id_location_selected").val("");
    });

});
})(django.jQuery);