/**
 * btsearch.map.js
 *
 * @author Dawid Lorenz, dawid@lorenz.co
 */

/**
 * Core object to manipulate a map
 */
var core = {

    mapParams: {
        // Init zoom/center to be overriden via URL/cookie
        zoom: 9,
        center: new google.maps.LatLng(52.069245, 19.480193),
        streetViewControl: false,
        scaleControl: true,
        mapTypeId: google.maps.MapTypeId.ROADMAP,
        mapTypeControlOptions: {
            style: google.maps.MapTypeControlStyle.DROPDOWN_MENU,
            position: google.maps.ControlPosition.TOP_RIGHT
        },
        panControlOptions: {
            position: google.maps.ControlPosition.RIGHT_TOP
        },
        zoomControlOptions: {
            position: google.maps.ControlPosition.RIGHT_TOP
        }
    },
    initParams: null,
    map: null,
    infoWindow: null,
    geocoder: null,
    markers: null,
    selectedMarker: null,
    defaultMarkerIcon: "http://chart.googleapis.com/chart?chst=d_map_pin_letter&chld=|ff776b|000000",
    searchResultIcon: "http://maps.google.com/mapfiles/kml/pal3/icon52.png",

    init: function(mapCanvas, initParams) {
        this.map = new google.maps.Map(mapCanvas, this.mapParams);
        this.geocoder = new google.maps.Geocoder();
        this.markers = [];
        this.initParams = initParams;
        this.initMapBounds();
        ui.createMapControls(this.map);
    },

    initMapBounds: function() {
        if (this.initParams.zoom && (this.initParams.bounds || this.initParams.center)) {
            if (this.initParams.center) {
                var centerCoords = this.initParams.center.split(',');
                this.map.setCenter(
                    new google.maps.LatLng(centerCoords[0],centerCoords[1])
                );
            } else if (this.initParams.bounds) {
                var boundsCoords = this.initParams.bounds.split(',');
                this.map.panToBounds(new google.maps.LatLngBounds(
                    new google.maps.LatLng(boundsCoords[0],boundsCoords[1]),
                    new google.maps.LatLng(boundsCoords[2],boundsCoords[3])
                ));
            }
            this.map.setZoom(this.initParams.zoom);
        } else {
            this.userLocationAutodetect();
        }
    },

    userLocationAutodetect: function() {
        // Reference: https://developers.google.com/maps/articles/geolocation
        if (navigator.geolocation) {
            navigator.geolocation.getCurrentPosition(function(position) {
                var detectedLatLng = new google.maps.LatLng(
                    position.coords.latitude,
                    position.coords.longitude
                );
                var boundsOfPoland = new google.maps.LatLngBounds(
                    new google.maps.LatLng(49.253465,13.710938),
                    new google.maps.LatLng(55.065787,24.268799)
                );
                // Only pan to auto-detected location when it is within Poland
                if (boundsOfPoland.contains(detectedLatLng)) {
                    core.map.setCenter(detectedLatLng);
                    core.map.setZoom(15);
                } else {
                    console.log('Autodetected user location outside of Poland');
                }
            }, function() {
                console.log('Error autodetecting location');
            });
        }
    },

    bindMapEvents: function() {
        events.mapIdle(this.map);
        events.mapClick(this.map);
        events.mouseMove(this.map);
    },

    clearAllOverlays: function() {
        this.clearInfoWindow();
        this.clearSelectedMarker();
        this.clearMarkers();
    },

    clearInfoWindow: function() {
        if (this.infoWindow) {
            this.infoWindow.setMap(null);
        }
    },

    clearSelectedMarker: function() {
        if (this.selectedMarker !== null) {
            this.selectedMarker.setMap(null);
            this.selectedMarker = null;
        }
    },

    clearMarkers: function() {
        // Clear selected marker if it is out of current map bounds
        if (this.selectedMarker !== null &&
            this.map.getBounds().contains(this.selectedMarker.getPosition()) === false) {
            this.clearSelectedMarker();
        }

        // Clear all markers but not selected one
        for (var i in this.markers) {
            if (this.markers[i] != this.selectedMarker) {
                this.markers[i].setMap(null);
            }
        }

        // Reset markers array
        this.markers = [];
    },

    createMarker: function(latlng, icon) {
        // Reuse selected marker if possible instead of creating a new one
        // (this is mainly to preserve opened infoWindow over selected marker)
        if (this.selectedMarker !== null &&
            this.selectedMarker.getPosition().equals(latlng)) {
            this.markers.push(this.selectedMarker);
            return this.selectedMarker;
        }

        // Create new marker
        marker = new google.maps.Marker({
            position: latlng,
            icon: icon,
            map: this.map
        });
        this.markers.push(marker);
        return marker;
    },

    /**
     * Wrapper function around remote request to load locations for given
     * map bounds and filters.
     */
    loadLocations: function() {
        mapStatus.wait();
        if (this.map.getZoom() >= 11) {
            mapStatus.clearZoomWarning();
            requests.getLocations(this.map.getBounds(), filters.get());
        } else {
            this.clearAllOverlays();
            ui.resetPanel();
            mapStatus.waitDone();
            mapStatus.displayZoomWarning();
        }
        mapStatus.updateAll();
    },

    /**
     * Method executed on map panning/zooming, can be overriden
     *
     * Parameter 'locations' is json object containing a list
     * where each record should have following fields:
     * id, latitude, longitude, icon
     *
     * @param locations
     */
    displayLocations: function(data) {
        this.clearMarkers();
        locations = data.objects;
        for (var i in locations) {
            icon = locations[i].icon !== null ? locations[i].icon : this.defaultMarkerIcon;
            latlng = new google.maps.LatLng(locations[i].latitude, locations[i].longitude);
            marker = this.createMarker(latlng, icon);
            events.locationClick(marker, locations[i]);
            events.locationRightClick(marker);
        }
        mapStatus.updateLocationsCount();
        mapStatus.waitDone();
    },

    /**
     * Method displaying clicked location details, can be overriden
     *
     * Parameter 'locationData' is json object containing
     * just 'html' field with pre-rendered info window content.
     *
     * @param locationData
     * @param marker
     */
    displayLocationInfo: function(locationData, marker) {
        this.clearInfoWindow();
        // this.clearSelectedMarker(); -- don't make the marker disappear
        this.infoWindow = new google.maps.InfoWindow({
            content: locationData.info
        });
        this.infoWindow.open(core.map, marker);
        this.selectedMarker = marker;
        events.infoWindowClose(this.infoWindow);
    },

    // @TODO: request.searchLocation -> callback: ui.displaySearchResult (?)
    searchLocation: function(query) {
        $('#control-panel-search-results').html('');
        params = {
            'address': query,
            'region': 'pl'
        };
        this.geocoder.geocode(params, function(results, status) {
            if (status == google.maps.GeocoderStatus.OK) {
                core.displaySearchResult(results[0].geometry.location.lat(), results[0].geometry.location.lng());
                if (results.length > 1) {
                    // Generate results list
                    var resultsHtml = '<ul>';
                    for (var i in results) {
                        resultsHtml += '<li><a href="javascript:void(0);" class="search-result-item" data-latitude="' + results[i].geometry.location.lat() + '" data-longitude="' + results[i].geometry.location.lng() + '">' + results[i].formatted_address + '</a></li>';
                    }
                    resultsHtml += '</ul>';
                    $('#control-panel-search-results').html(resultsHtml);

                    // Display search results panel
                    ui.activatePanel($('#control-panel-search-results'), 'Rezultat wyszukiwania');

                    // Attach event to search results
                    $('.search-result-item').on('click', function(){
                        core.displaySearchResult($(this).data('latitude'), $(this).data('longitude'));
                    });
                }
            } else {
                $('#control-panel-search-results').html(status);
            }
        });
    },

    displaySearchResult: function(lat, lng) {
        latlng = new google.maps.LatLng(lat, lng);
        core.map.setCenter(latlng);
        core.map.setZoom(15);
        this.selectedMarker = core.createMarker(latlng, core.searchResultIcon);
    }

};


/**
 * Object to handle map events
 */
var events = {
    mapIdle: function(map) {
        google.maps.event.addListener(map, 'idle', function() {
            core.loadLocations();
        });
    },

    mapClick: function(map) {
        google.maps.event.addListener(map, 'click', function() {
            core.clearInfoWindow();
            ui.resetPanel();
        });
    },

    locationClick: function(marker, location) {
        google.maps.event.addListener(marker, 'click', function() {
            if (core.selectedMarker == marker) {
                core.clearInfoWindow();
                ui.resetPanel();
                core.selectedMarker = null;
            } else {
                requests.getLocationInfo(marker, location.id, filters.get());
            }
        });
    },

    locationRightClick: function(marker) {
        google.maps.event.addListener(marker, 'rightclick', function(){
            distanceService.toggle(marker.getPosition());
        });
        google.maps.event.addListener(marker, 'mouseover', function() {
            if (!distanceService.startPoint) {
                $('#status-panel-distance-info').show();
            }
        });
    },

    infoWindowClose: function(infoWindow) {
        google.maps.event.addListener(infoWindow, 'closeclick', function() {
            core.clearInfoWindow();
            ui.resetPanel();
        });
    },

    mouseMove: function(map) {
        google.maps.event.addListener(map, 'mousemove', function(event) {
            distanceService.draw(event.latLng);
            mapStatus.updateDistance();
            mapStatus.updateGpsLocation(event.latLng);
            $('#status-panel-distance-info').hide();
        });
    },

    distanceCancel: function(polyline) {
        google.maps.event.addListener(polyline, 'rightclick', function(event) {
            distanceService.reset();
        });
    }
};

var distanceService = {
    startPoint: null,
    polyline: null,
    distance: 0,
    heading: null,

    reset: function() {
        this.startPoint = null;
        if (this.polyline) {
            this.polyline.setMap(null);
        }
        this.polyline = null;
        this.distance = 0;
    },

    toggle: function(startPoint) {
        if (this.startPoint) {
            this.reset();
        } else {
            this.startPoint = startPoint;
            this.polyline = new google.maps.Polyline({
                strokeColor: '#FF0000',
                strokeOpacity: 0.2,
                strokeWeight: 3,
                geodesic: true
            });
            events.distanceCancel(this.polyline);
        }
    },

    draw: function(endPoint) {
        if (this.polyline) {
            path = [
                this.startPoint,
                endPoint
            ];
            this.polyline.setPath(path);
            this.polyline.setMap(core.map);
            this.distance = google.maps.geometry.spherical.computeLength(path);
            this.heading = google.maps.geometry.spherical.computeHeading(path[0], path[1]);
            // this.heading = utils.calculateHeading(path[0], path[1]);
        }
    }
};

/**
 * Object to handle XMLHttpRequest requests to web server
 */
var requests = {
    getLocations: function(mapBounds, filters) {
        $.ajax({
            url: "/map/" + filters.dataSource + "/?bounds=" + mapBounds.toUrlValue() + filters.toUrlValue(),
            dataType: "json",
            headers: {
                Accept: "application/json"
            },
            success: function(data) {
                core.displayLocations(data);
                ui.updateUrl();
            }
        });
    },

    getLocationInfo: function(marker, locationId, filters) {
        $.ajax({
            url: "/map/" + filters.dataSource + "/" + locationId + "/?" + filters.toUrlValue(),
            dataType: "json",
            headers: {
                Accept: "application/json"
            },
            success: function(data) {
                core.displayLocationInfo(data, marker);
                $('a.location-info').fancybox({
                    'type': 'ajax'
                });
            }
        });
    },

    /* Instead of loading location info in panel, open it in fancybox
    getBaseStationInfo: function(baseStationId) {
        $.ajax({
            url: "/get_base_station_info/" + baseStationId + "/",
            success: function(data) {
                $('#control-panel-location-info').html(data);
                ui.activatePanel($('#control-panel-location-info'), 'Szczegóły lokalizacji');
            }
        });
    },

    getUkeLocationInfo: function(ukeLocationId, networkCode) {
        $.ajax({
            url: "/get_uke_location_info/" + ukeLocationId + "," + networkCode + "/",
            success: function(data) {
                $('#control-panel-location-info').html(data);
                ui.activatePanel($('#control-panel-location-info'), 'Szczegóły lokalizacji');
            }
        });
    },
    */

    setControlPanelContent: function(panel) {
        $.ajax({
            url: "/map/ui/control_panel/",
            success: function(data) {
                panel.innerHTML = data;

                // Wait for panel elements to attach to DOM properly
                // before attaching events to them
                // Try jQuery's .on event? See:
                // https://github.com/zoyalab/zoyalab.com/blob/master/js/main.js#L20
                //
                // TODO: Using setInterval certainly smells shit. Fix it.
                inv = setInterval(function(){
                    if (ui.ready()) {
                        core.bindMapEvents();
                        ui.bindControlPanelEvents();
                        filters.init(core.initParams);
                        core.loadLocations();
                        clearInterval(inv);
                    }
                }, 1500);
            }
        });
    },

    setStatusPanelContent: function(panel) {
        $.ajax({
            url: "/map/ui/status_panel/",
            success: function(data) {
                panel.innerHTML = data;
            }
        });
    },

    setAdPanelContent: function(panel) {
        $.ajax({
            url: "/map/ui/ad_panel/",
            success: function(data) {
                panel.innerHTML = data;
            }
        });
    }
};

/**
 * User interface elements handling
 */
var ui = {

    pushStateSupport: function(){
        return (typeof(window.onpopstate) != 'undefined');
    },

    /**
     * Check if dynamically created elements are properly rendered
     *
     * @returns {Boolean}
     */
    ready: function() {
        uiElementsToCheck = ['control-panel-container',
                             'status-panel-container',
                             'search-form',
                             'network-filter'];

        for (var i in uiElementsToCheck) {
            if (null === document.getElementById(uiElementsToCheck[i])) return false;
        }
        return true;
    },

    createMapControls: function(map) {
        this.createControlPanel(map);
        this.createStatusPanel(map);
        this.createWaitingLabel(map);
        this.createAdPanel(map);
    },

    createControlPanel: function(map) {
        var panel = document.createElement('DIV');
        panel.id = 'control-panel-container';
        map.controls[google.maps.ControlPosition.TOP_LEFT].push(panel);

        requests.setControlPanelContent(panel);
    },

    createStatusPanel: function(map) {
        var panel = document.createElement('DIV');
        panel.id = 'status-panel-container';
        map.controls[google.maps.ControlPosition.TOP_LEFT].push(panel);

        requests.setStatusPanelContent(panel);
    },

    createWaitingLabel: function(map) {
        var label = document.createElement('DIV');
        label.id = 'waiting-label-container';
        label.className = 'label label-important';
        label.innerHTML = 'Trwa ładowanie...';
        map.controls[google.maps.ControlPosition.TOP_RIGHT].push(label);
    },

    createAdPanel: function(map) {
        // Reference: https://developers.google.com/maps/documentation/javascript/advertising
        var adUnitDiv = document.createElement('div');
        adUnitDiv.id = 'googlead-panel-container';
        var adUnitOptions = {
            format: google.maps.adsense.AdFormat.HALF_BANNER,
            position: google.maps.ControlPosition.RIGHT_BOTTOM,
            map: core.map,
            visible: true,
            publisherId: 'ca-pub-0983719504949481'
        };
        new google.maps.adsense.AdUnit(adUnitDiv, adUnitOptions);
    },

    bindControlPanelEvents: function() {
        // Search form submission
        $('#search-form').submit(function(){
            query = $('#search-box').val();
            if (query !== '') {
                core.searchLocation(query);
                return false;
            }
            return false;
        });

        // Network filter dropdown change
        $('#network-filter').change(function(){
            ui.resetMap();
        });

        // Network standards filter
        $('.standard-filter').click(function(){
            ui.resetMap();
        });

        // Network standards filter
        $('.band-filter').click(function(){
            ui.resetMap();
        });

        $('.timedelta-filter').click(function(){
            ui.resetMap();
        });

        // Data source filter
        $('input[name=data-source]').change(function(){
            ui.resetMap();
            if ($(this).val() == 'locations') {
                $('#bts-last-update-date').show();
                $('#uke-last-update-date').hide();
            } else {
                $('#bts-last-update-date').hide();
                $('#uke-last-update-date').show();
            }
        });

        $('#control-panel-header-icon').click(function(){
            ui.toggleControlPanel();
        });

        $('a#data-source-help-icon').fancybox();

        // Search box autocomplete
        searchBox = document.getElementById('search-box');
        autocomplete = new google.maps.places.Autocomplete(searchBox);
        autocomplete.bindTo('bounds', core.map);
    },

    activatePanel: function(panelObject, panelTitle) {
        $('#control-panel-filters').hide();
        $('#control-panel-search-results').hide();
        $('#control-panel-location-info').hide();
        $('#control-panel-header-title').html(panelTitle);
        panelObject.show();
    },

    resetPanel: function() {
        mainPanelObject = $('#control-panel-filters');
        if (!mainPanelObject.is(':visible')) {
            this.activatePanel(mainPanelObject, 'Filtr lokalizacji');
        }
    },

    resetMap: function() {
        core.selectedMarker = null;
        google.maps.event.trigger(core.map, 'idle');
    },

    toggleControlPanel: function() {
        $('#control-panel-body').toggle({
            complete: function() {
                // This little hack is needed to maintain scrollability of the
                // control panel when the viewport's height is too low
                var visible = $(this).is(':visible');
                if (!visible && $('#control-panel-container').css('bottom') == '0px') {
                    $('#control-panel-container').css('bottom', 'auto');
                } else {
                    $('#control-panel-container').css('bottom', '0px');
                }
            }
        });
    },

    updateUrl: function() {
        if (!this.pushStateSupport) return;
        stateObject = {
            dataSource: filters.dataSource,
            network: filters.network.join(','),
            standards: filters.standard.join(','),
            bands: filters.band.join(','),
            center: core.map.getCenter().toUrlValue(6),
            zoom: core.map.getZoom()
        };
        var query_path = '?' + $.param(stateObject);
        history.replaceState(stateObject, '', query_path);
    }

};

var filters = {
    network: [],
    standard: [],
    band: [],
    timedelta: null,
    dataSource: 'locations',

    init: function(params) {
        if (params.network) {
            $('#network-filter').val(params.network);
        }
        if (params.dataSource) {
            $('input[name=data-source][value='+params.dataSource+']').prop('checked', true);
        }
        if (params.standards) {
            var standards = params.standards.split(',');
            for (var i in standards) {
                $('#standard-filter-'+standards[i]).prop('checked', true);
            }
        }
        if (params.bands) {
            var bands = params.bands.split(',');
            for (var j in bands) {
                $('#band-filter-'+bands[j]).prop('checked', true);
            }
        }
    },

    get: function() {
        this.setNetworkFilter();
        this.setStandardFilter();
        this.setBandFilter();
        this.setDataSourceFilter();
        this.setTimedeltaFilter();
        return this;
    },

    setNetworkFilter: function() {
        var selectedNetwork = $('#network-filter').val();
        this.network = (selectedNetwork != '-1') ? selectedNetwork.split(',') : [];
    },

    setStandardFilter: function() {
        this.standard = [];
        $('.standard-filter:checked').each(function(index, element){
            filters.standard.push(element.value);
        });
    },

    setBandFilter: function() {
        this.band = [];
        $('.band-filter:checked').each(function(index, element){
            filters.band.push(element.value);
        });
    },

    setDataSourceFilter: function() {
        //this.dataSource = $('#data-source-filter').val();
        this.dataSource = $('input[name=data-source]:checked').val();
    },

    setTimedeltaFilter: function() {
        this.timedelta = null;
        this.timedelta = $('#timedelta-filter:checked').val();
    },

    toUrlValue: function() {
        var url = '';
        for (var n in this.network) {
            url += '&network=' + this.network[n];
        }

        for (var s in this.standard) {
            url += '&standard=' + this.standard[s];
        }

        for (var b in this.band) {
            url += '&band=' + this.band[b];
        }

        if (this.timedelta) {
            url += '&timedelta=' + this.timedelta;
        }
        return url;
    }
};

var mapStatus = {

    getLatLngExtendedInfo: function(point) {
        var lat = point.lat().toFixed(6);
        var lng = point.lng().toFixed(6);
        var lat2 = utils.deg2dms(lat, 'lat');
        var lng2 = utils.deg2dms(lng, 'lng');
        return lat + '&nbsp;' + lng + '&nbsp;&hArr;&nbsp;' + lat2 + '&nbsp;' + lng2;
    },

    updateAll: function() {
        this.updateZoom();
        this.updateLocationsCount();
        this.updateDataSource();
    },

    updateZoom: function() {
        $('#status-zoom').html(core.map.getZoom());
    },

    updateLocationsCount: function() {
        var locationsCount = core.markers.length;
        $('#status-locations-count').html(locationsCount);
        if (locationsCount >= 500) {
            this.displayLocationCountWarning();
        } else {
            this.clearLocationCountWarning();
        }
    },

    updateDataSource: function() {
        source = filters.dataSource == 'locations' ? 'BTSearch' : 'UKE';
        $('#status-data-source').html(source);
    },

    updateGpsLocation: function(point) {
        $('#status-gps').html(this.getLatLngExtendedInfo(point));
    },

    updateDistance: function() {
        var distance = distanceService.distance.toFixed(0);
        if (distance > 0) {
            $('#status-panel-distance').show();
            var heading = distanceService.heading.toFixed(2);
            if (heading < 0) {
                heading = (+heading + 360).toFixed(2);
            }
            var distance_km = (distance / 1000).toFixed(2);
            var distance_ta = Math.floor(distance / 550);
            if (distance_ta > 63) distance_ta = 'max';
            $('#status-distance').html(distance_km);
            $('#status-ta').html(distance_ta);
            $('#status-heading').html(heading + '&deg;');
            $('#status-gps-marker').html(this.getLatLngExtendedInfo(distanceService.startPoint));
        } else {
            $('#status-panel-distance').hide();
        }
    },

    wait: function() {
        $('#waiting-label-container').show();
        $('#map-search-submit').attr('disabled', true);
        $('#network-filter').attr('disabled', true);
        $('#data-source-filter').attr('disabled', true);
        $('.standard-filter').attr('disabled', true);
        $('.band-filter').attr('disabled', true);
        $('.timedelta-filter').attr('disabled', true);
    },

    waitDone: function() {
        $('#map-search-submit').removeAttr('disabled');
        $('#network-filter').removeAttr('disabled');
        $('#data-source-filter').removeAttr('disabled');
        $('.standard-filter').removeAttr('disabled');
        $('.band-filter').removeAttr('disabled');
        $('.timedelta-filter').removeAttr('disabled');
        $('#waiting-label-container').hide();
    },

    displayZoomWarning: function() {
        $('#status-zoom').css('color', 'red');
        $('#status-zoom').css('font-weight', 'bold');
        $('#status-zoom').attr('title', 'Lokalizacje są wyświetlane od poziomu zbliżenia 11 wzwyż');
    },

    clearZoomWarning: function() {
        $('#status-zoom').css('color', 'black');
        $('#status-zoom').css('font-weight', 'normal');
        $('#status-zoom').attr('title', '');
    },

    displayLocationCountWarning: function() {
        $('#status-locations-count').css('color', 'red');
        $('#status-locations-count').css('font-weight', 'bold');
        $('#status-locations-count').attr('title', 'Liczba wyświetlonych lokalizacji ograniczona');
    },

    clearLocationCountWarning: function() {
        $('#status-locations-count').css('color', 'black');
        $('#status-locations-count').css('font-weight', 'normal');
        $('#status-locations-count').attr('title', '');
    }
};

var utils = {
    // Credits: Krzysiek Niemczyk ;)
    deg2dms: function(coordinate, latlng) {
        // jeśli nie określono argumentu to nie wykonujemy funkcji
        if (latlng != 'lat' && latlng != 'lng') return;

        coordinate = Math.abs(coordinate);

        var d = Math.floor(coordinate);
        var s = ((coordinate - Math.floor(coordinate)) * 3600);
        var m = Math.floor(s / 60);

        s = (s - m * 60).toFixed(2);

        if (s < 10)
            s = '0' + s;
        if (m < 10)
            m = '0' + m;

        var suffix = latlng == 'lat' ? coordinate > 0 ? 'N' : 'S' : coordinate > 0 ? 'E' : 'W';

        return d + '&ordm;' + m + '\'' + s + '\'\'&nbsp;' + suffix;
    }

    /*calculateHeading: function(point1, point2) {
        var lat1 = point1.lat(); var lon1 = point1.lng();
        var lat2 = point2.lat(); var lon2 = point2.lng();

        var lat1 = lat1 * Math.PI / 180;
        var lat2 = lat2 * Math.PI / 180;
        var dLon = (lon2 - lon1) * Math.PI / 180;

        var y = Math.sin(dLon) * Math.cos(lat2);
        var x = Math.cos(lat1) * Math.sin(lat2) -
        Math.sin(lat1) * Math.cos(lat2) * Math.cos(dLon);

        var brng = Math.atan2(y, x);

        return (((brng * 180 / Math.PI) + 360) % 360);
    }*/
};

$(document).bind('keypress', 'g', function(){
    $('#standard-filter-gsm').prop('checked', !$('#standard-filter-gsm').prop('checked'));
    ui.resetMap();
});

$(document).bind('keypress', 'u', function(){
    $('#standard-filter-umts').prop('checked', !$('#standard-filter-umts').prop('checked'));
    ui.resetMap();
});

$(document).bind('keypress', 'l', function(){
    $('#standard-filter-lte').prop('checked', !$('#standard-filter-lte').prop('checked'));
    ui.resetMap();
});

$(document).bind('keypress', 'c', function(){
    $('#standard-filter-cdma').prop('checked', !$('#standard-filter-cdma').prop('checked'));
    ui.resetMap();
});

$(document).bind('keypress', '5', function(){
    $('#standard-filter-5g').prop('checked', !$('#standard-filter-5g').prop('checked'));
    ui.resetMap();
});

$(document).bind('keypress', 'i', function(){
    $('#standard-filter-iot').prop('checked', !$('#standard-filter-iot').prop('checked'));
    ui.resetMap();
});

$(document).bind('keypress', '9', function(){
    $('#band-filter-900').prop('checked', !$('#band-filter-900').prop('checked'));
    ui.resetMap();
});

$(document).bind('keypress', '1', function(){
    $('#band-filter-1800').prop('checked', !$('#band-filter-1800').prop('checked'));
    ui.resetMap();
});

$(document).bind('keypress', '2', function(){
    $('#band-filter-2100').prop('checked', !$('#band-filter-2100').prop('checked'));
    ui.resetMap();
});

$(document).bind('keypress', '8', function(){
    $('#band-filter-800').prop('checked', !$('#band-filter-800').prop('checked'));
    ui.resetMap();
});
