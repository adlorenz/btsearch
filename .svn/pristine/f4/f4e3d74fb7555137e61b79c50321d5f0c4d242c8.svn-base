(function($){
$(document).ready(function(){
	if($("#id_latitude,#id_longitude").length == 2) {
	
		var latInput = $("#id_latitude");
		var lonInput = $("#id_longitude");
        lonInput.parents(".form-row").after('<div class="form-row"><input id="updateMap" type="button" value="Update position on map" /><input type="text" id="selected_location" /><div id="lpMap"></div></div>');
		$("#updateMap").attr("disabled","disabled");
		
        var lat = 52.1673;
        var lng = 20.8109;
		var showMarker = false;
		var mapZoom = 4;
        if ((latInput.val()!='')&&(latInput.val()!='')) {
            lat = latInput.val();
            lng = lonInput.val();
			showMarker = true;
			mapZoom = 10;
        }
		var center = new google.maps.LatLng(lat,lng);

		var myOptions = {
		  zoom: mapZoom,
		  center: center,
		  streetViewControl: false,
		  mapTypeId: google.maps.MapTypeId.ROADMAP
		}
		var map = new google.maps.Map(document.getElementById("lpMap"), myOptions);

		var marker = new google.maps.Marker({
			position: center,
			draggable: true,
			map: map,
			visible: showMarker
		});

		google.maps.event.addListener(map, 'click', function(event) {
			getCordsFromMap(event.latLng);
		});
		google.maps.event.addListener(marker, 'dragend', function(event) {
			getCordsFromMap(event.latLng);
		});
		
		function getCordsFromMap(eventLocation){
			marker.setPosition(eventLocation);
			marker.setVisible(true);
			latInput.val(Math.round(eventLocation.lat()*1000000)/1000000);
			lonInput.val(Math.round(eventLocation.lng()*1000000)/1000000);
			
			geocoder = new google.maps.Geocoder();
			geocoder.geocode({'location': eventLocation }, function(results, status){
				$('#selected_location').val(results[0].formatted_address);
			});
				
			$("#updateMap").attr("disabled","disabled");		
		}
		
		$("#updateMap").click(function(){
			marker.setVisible(true);
			center = new google.maps.LatLng(latInput.val(),lonInput.val());
			marker.setPosition(center);
			map.setCenter(center);
			$("#updateMap").attr("disabled","disabled");
		});
		$("#id_latitude,#id_longitude").change(function(){
			$("#updateMap").attr("disabled",false);
		});
		
    }
});
})(django.jQuery);