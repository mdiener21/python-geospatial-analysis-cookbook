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

var map = new ol.Map({
  layers: [raster, vector],
  target: 'map',
  view: new ol.View({
    center: [-8620772, 2677869],
    zoom: 4
  })
});