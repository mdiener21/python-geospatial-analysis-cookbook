        var url_base = "/api/directions/";
        var start_coord = "1587848.414,5879564.080,2";
        var end_coord =  "1588005.547,5879736.039,2";
        var sel_Val = $( "input:radio[name=typeRoute]:checked" ).val();
        var geojs_url = url_base + start_coord + "&" + end_coord + "&" + sel_Val + '/?format=json';

// uncomment this code if you want to reactivate
// the quick static demo switcher
        //$( ".radio" ).change(function() {
        //   map.getLayers().pop();
        //   var sel_Val2 = $( "input:radio[name=typeRoute]:checked" ).val();
        //   var routeUrl = '/api/directions/1587848.414,5879564.080,2&1588005.547,5879736.039,2&' + sel_Val2  + '/?format=json';
        //
        //  map.getLayers().push(new ol.layer.Vector({
        //            source: new ol.source.GeoJSON({url: routeUrl}),
        //            style:  new ol.style.Style({
        //                stroke: new ol.style.Stroke({
        //                  color: 'blue',
        //                  width: 4
        //                })
        //              }),
        //            title: "Route",
        //            name: "Route"
        //        }));
        //
        //});

        var vectorLayer = new ol.layer.Vector({
                        source: new ol.source.GeoJSON({url: geojs_url}),
                        style:  new ol.style.Style({
                            stroke: new ol.style.Stroke({
                              color: 'red',
                              width: 4
                            })
                          }),
                        title: "Route",
                        name: "Route"
                    });

        var map = new ol.Map({
          layers: [
            new ol.layer.Tile({
              source: new ol.source.OSM()
            })
              ,
            vectorLayer
          ],
          target: 'map',
          controls: ol.control.defaults({
            attributionOptions: /** @type {olx.control.AttributionOptions} */ ({
              collapsible: false
            })
          }),
          view: new ol.View({
            center: [1587927.09817072,5879650.90059265],
            zoom: 18
          })
        });

function addRoute(fromNumber, toNumber, routeType) {
    map.getLayers().pop();
    console.log("addRoute big"+ String(fromNumber));
    var baseUrl = 'http://localhost:8000/api/directions/';
    var geoJsonUrl = baseUrl + fromNumber + '&' + toNumber + '&' + routeType +'/?format=json';
    console.log("final url " + geoJsonUrl);
    map.getLayers().push(new ol.layer.Vector({
                source: new ol.source.GeoJSON({url: geoJsonUrl}),
                style:  new ol.style.Style({
                    stroke: new ol.style.Stroke({
                      color: 'purple',
                      width: 4
                    })
                  }),
                title: "Route",
                name: "Route"
            }));
    }