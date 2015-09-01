var raster = new ol.layer.Tile({
  source: new ol.source.OSM()
});

var format = new ol.format.WKT();
var feature = format.readFeature(ply_data);

feature.getGeometry().transform('EPSG:4326', 'EPSG:3857');

var style_golf = new ol.style.Style({
    stroke: new ol.style.Stroke({
        color: 'blue',
        width: 3
    }),
    fill: new ol.style.Fill({
        color : 'green'

    })

});

var vector = new ol.layer.Vector({
  source: new ol.source.Vector({
    features: [feature]
  }),
    style: style_golf
});


/**
 * Elements that make up the popup.
 */
var container = document.getElementById('popup');
var content = document.getElementById('popup-content');
var closer = document.getElementById('popup-closer');

/**
 * Create an overlay to anchor the popup to the map.
 */
var overlay = new ol.Overlay(/** @type {olx.OverlayOptions} */ ({
  element: container,
  autoPan: true,
  autoPanAnimation: {
    duration: 250
  }
}));

/**
 * Add a click handler to hide the popup.
 * @return {boolean} Don't follow the href.
 */
closer.onclick = function() {
  overlay.setPosition(undefined);
  closer.blur();
  return false;
};



var map = new ol.Map({
  layers: [raster, vector],
  target: 'map',
  overlays: [overlay],
  view: new ol.View({
    center: [-9100186, 3293034],
    zoom: 6
  })
});

map.on('singleclick', function(evt) {
  var coordinate = evt.coordinate;
  var hdms = ol.coordinate.toStringHDMS(ol.proj.transform(
      coordinate, 'EPSG:3857', 'EPSG:4326'));
  var coord_3857 = ol.coordinate.toStringXY(coordinate);

  content.innerHTML = '<p>You clicked epsg:4326</p><code>' + hdms +
      '</code></br></br> ' + '<p> and in epsg:3857 </p><code>' + coord_3857 + '</code>';
  overlay.setPosition(coordinate);
});

