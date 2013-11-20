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
        mapTypeControlOptions: {style: google.maps.MapTypeControlStyle.DROPDOWN_MENU},
        panControlOptions: {position: google.maps.ControlPosition.RIGHT_TOP},
        zoomControlOptions: {position: google.maps.ControlPosition.RIGHT_TOP}
    },
    map: null,
    infoWindow: null,
    geocoder: null,
    markers: null,
    selectedMarker: null,
    defaultMarkerIcon: "http://chart.googleapis.com/chart?chst=d_map_pin_letter&chld=|ff776b|000000",

    init: function(mapCanvas) {
        this.map = new google.maps.Map(mapCanvas, this.mapParams);
        this.locationAutodetect();
        this.geocoder = new google.maps.Geocoder();
        this.markers = new Array();
        ui.createMapControls(this.map);
    },

    locationAutodetect: function() {
        // TODO: Do not auto-detect locations outside of Poland?
        // Reference: https://developers.google.com/maps/articles/geolocation
        if (navigator.geolocation) {
            navigator.geolocation.getCurrentPosition(function(position) {
                core.map.setCenter(
                    new google.maps.LatLng(position.coords.latitude,position.coords.longitude)
                );
                core.map.setZoom(15);
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
        if (this.selectedMarker != null) {
            this.selectedMarker.setMap(null);
            this.selectedMarker = null;
        }
    },

    clearMarkers: function() {
        // Clear selected marker if it is out of current map bounds
        if (this.selectedMarker != null
            && this.map.getBounds().contains(this.selectedMarker.getPosition()) == false) {
            this.clearSelectedMarker();
        }

        // Clear all markers but not selected one
        for (i in this.markers) {
            if (this.markers[i] != this.selectedMarker) {
                this.markers[i].setMap(null);
            }
        }

        // Reset markers array
        this.markers = new Array();
    },

    createMarker: function(latlng, icon) {
        // Reuse selected marker if possible instead of creating a new one
        // (this is mainly to preserve opened infoWindow over selected marker)
        if (this.selectedMarker != null
            && this.selectedMarker.getPosition().equals(latlng)) {
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
        for (i in locations) {
            icon = locations[i].icon != null ? locations[i].icon : this.defaultMarkerIcon;
            latlng = new google.maps.LatLng(locations[i].latitude, locations[i].longitude);
            marker = this.createMarker(latlng, icon);
            events.locationClick(marker, locations[i]);
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
                core.map.setCenter(results[0].geometry.location);
                if (results.length > 1) {
                    resultsHtml = '<ul>';
                    for (i in results) {
                        // @TODO: Use jquery .click/.live event instead of onclick
                        // Or use jQuery's .on() event? See:
                        // https://github.com/zoyalab/zoyalab.com/blob/master/js/main.js#L20
                        onclickAction = 'core.setMapCenter(' + results[i].geometry.location.lat() + ',' + results[i].geometry.location.lng() + ');';
                        resultsHtml += '<li><a href="javascript:void();" class="search-result-item" onclick="' + onclickAction + '">' + results[i].formatted_address + '</a></li>';
                    }
                    resultsHtml += '</ul>';
                    $('#control-panel-search-results').html(resultsHtml);
                    ui.activatePanel($('#control-panel-search-results'), 'Rezultat wyszukiwania');
                }
            } else {
                $('#control-panel-search-results').html(status);
            }
        });
    },

    setMapCenter: function(lat, lng) {
        latlng = new google.maps.LatLng(lat, lng);
        core.map.setCenter(latlng);
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

    infoWindowClose: function(infoWindow) {
        google.maps.event.addListener(infoWindow, 'closeclick', function() {
            core.clearInfoWindow();
            ui.resetPanel();
        });
    },

    mouseMove: function(map) {
        google.maps.event.addListener(map, 'mousemove', function(event) {
            mapStatus.updateGpsLocation(event.latLng.lat().toFixed(6), event.latLng.lng().toFixed(6));
        });
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
    }
};

/**
 * User interface elements handling
 */
var ui = {

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

        for (i in uiElementsToCheck) {
            if (null === document.getElementById(uiElementsToCheck[i])) return false;
        }
        return true;
    },

    createMapControls: function(map) {
        this.createControlPanel(map);
        this.createStatusPanel(map);
        this.createWaitingLabel(map);
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

    bindControlPanelEvents: function() {
        // Search form submission
        $('#search-form').submit(function(){
            query = $('#search-box').val();
            if (query != '') {
                core.searchLocation(query);
                return false;
            }
            return false;
        });

        // Network filter dropdown change
        $('#network-filter').change(function(){
            core.selectedMarker = null;
            google.maps.event.trigger(core.map, 'idle');
        });

        // Network standards filter
        $('.standard-filter').click(function(){
            core.selectedMarker = null;
            google.maps.event.trigger(core.map, 'idle');
        });

        // Network standards filter
        $('.band-filter').click(function(){
            core.selectedMarker = null;
            google.maps.event.trigger(core.map, 'idle');
        });

        $('.timedelta-filter').click(function(){
            core.selectedMarker = null;
            google.maps.event.trigger(core.map, 'idle');
        });

        // Data source filter
        //$('#data-source-filter').change(function(){
        $('input[name=data-source]').click(function(){
            core.selectedMarker = null;
            google.maps.event.trigger(core.map, 'idle');
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

        // $('#control-panel-header').toggleClass('control-panel-header-closed');
    }

};

var filters = {
    network: null,
    standard: [],
    band: [],
    timedelta: null,
    dataSource: 'locations',

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
        this.network = (selectedNetwork != '-1') ? selectedNetwork : null;
    },

    setStandardFilter: function() {
        this.standard = [];
        $('.standard-filter:checked').each(function(index, element){
            filters.standard.push(element.value);
        });
    },

    setBandFilter: function() {
        this.band= [];
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
        if (this.network != null) {
            url += '&network=' + this.network;
        }

        std = this.standard.join(',');
        if (std != '') {
            url += '&standard=' + std;
        }

        bnd = this.band.join(',');
        if (bnd != '') {
            url += '&band=' + bnd;
        }

        if (this.timedelta) {
            url += '&timedelta=' + this.timedelta;
        }
        return url;
    }
};

var mapStatus = {
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

    updateGpsLocation: function(lat, lng) {
        var lat2 = utils.deg2dms(lat, 'lat');
        var lng2 = utils.deg2dms(lng, 'lng');
        var latlng_info = lat + ' ' + lng + ' &hArr; ' + lat2 + ' ' + lng2;
        $('#status-gps').html(latlng_info);
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

        return d + '&ordm;' + m + '\'' + s + '\'\' ' + suffix;
    }
};
