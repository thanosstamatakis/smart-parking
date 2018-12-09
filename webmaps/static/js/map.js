

var bounds = null;


var map_c69f8540565a476887a0a3ab633e71e1 = L.map(
    'map_c69f8540565a476887a0a3ab633e71e1', {
    center: [38.246269, 21.7339247],
    zoom: 17,
    maxBounds: bounds,
    layers: [],
    worldCopyJump: false,
    crs: L.CRS.EPSG3857,
    zoomControl: false,
});

    
    
var tile_layer_1c1507a935ac402fac767e266a534f70 = L.tileLayer(
    'https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png',
    {
    "attribution": null,
    "detectRetina": false,
    "maxNativeZoom": 18,
    "maxZoom": 18,
    "minZoom": 0,
    "noWrap": false,
    "opacity": 1,
    "subdomains": "abc",
    "tms": false
}).addTo(map_c69f8540565a476887a0a3ab633e71e1);



$(document).ready(function () {
    $('.fixed-action-btn').floatingActionButton();
});



function zoomOutToggle() {
    map_c69f8540565a476887a0a3ab633e71e1.zoomOut();
}



function zoomInToggle() {
    map_c69f8540565a476887a0a3ab633e71e1.zoomIn();
}