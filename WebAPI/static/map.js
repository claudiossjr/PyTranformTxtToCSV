      var map;
      var markers = [];
      var polygon = null;
      var countries = [];


      function initMap(){

        map = new google.maps.Map(document.getElementById('map'), {
        zoom: 2,
        center: {lat: 40.7180628, lng: -73.9961237},
        mapTypeId: google.maps.MapTypeId.ROADMAP

        });
      

      var script = document.createElement('script');
      var url = ['https://www.googleapis.com/fusiontables/v2/query?'];
      url.push('sql=');
      var query = 'SELECT name, kml_4326 FROM 1foc3xO9DyfSIF6ofvN0kp2bxSfSeKog5FbdWdQ';
      var encodedQuery = encodeURIComponent(query);
      url.push(encodedQuery);
      url.push('&callback=drawMap');
      url.push('&key=AIzaSyDdyZKqw852jtBp9b5XUkPNgzvLNkJIkUg');
      script.src = url.join('');
      var body = document.getElementsByTagName('body')[0];
      body.appendChild(script);


    }

    function drawMap(data){

      var rows = data['rows'];

      for(var i in rows){
        if(rows[i][0] != 'Antarctica'){
          var newCoordinates = [];
          var geometries = rows[i][1]['geometries']; 
          if(geometries){
            for(var j in geometries){
              newCoordinates.push(constructNewCoordinates(geometries[j], rows[i][0]));
            }
          }else{
              newCoordinates = constructNewCoordinates(rows[i][1]['geometry'], rows[i][0]);
          }
          var country = new google.maps.Polygon({
          paths: newCoordinates,
          strokeColor: '#ff9900',
          strokeOpacity: 1,
          strokeWeight: 0.3,
          fillColor: '#ffff66',
          fillOpacity: 0,
          name: rows[i][0]
        });

          //COMEÇO DA GAMBI
          var vertices = country.getPath();
          var bounds = new google.maps.LatLngBounds();
          for(var i = 0; i < vertices.getLength(); i++){
            bounds.extend(new google.maps.LatLng(vertices.getAt(i).lat(), vertices.getAt(i).lng()));
          }

          var obj = {name: country.name,
            centerLat: bounds.getCenter().lat(),
            centerLng: bounds.getCenter().lng()
          };
          countries.push(obj);


          google.maps.event.addListener(country, 'mouseover', function() {
          this.setOptions({fillOpacity: 0.4});
        });
        google.maps.event.addListener(country, 'mouseout', function() {
          this.setOptions({fillOpacity: 0});
        });
        google.maps.event.addListener(country, 'click', function() {
          var metric = $( "#metricSelect" ).val();
          var index = $( "#indexSelect" ).val();
          var yearFrom = $("#yearFrom").val();
          var yearTo = $("#yearTo").val();

          if(!metric || !index || !yearFrom || !yearTo){
            alert("You must select all fields");
          }
          request(this.name, metric, index, yearFrom, yearTo);
        });

        country.setMap(map);

        }
      }

    }

    function constructNewCoordinates(polygon, country){
      //var bounds = new google.maps.LatLngBounds();
      var newCoordinates = [];
      var coordinates = polygon['coordinates'][0];
      for(var i in coordinates){
        var latlng = new google.maps.LatLng(coordinates[i][1], coordinates[i][0])
        newCoordinates.push(latlng);
        //bounds.extend(latlng);

      }
      /*if(country){
        console.log(country, bounds.getCenter().toString());
      }
      */
      return newCoordinates;
    }

    function generateHeatmap(){

      heatmap = new HeatmapOverlay(map, 
     {
    // radius should be small ONLY if scaleRadius is true (or small radius is intended)
      "radius": 10,
      "maxOpacity": 1, 
    // scales the radius based on map zoom
      "scaleRadius": true, 
    // if set to false the heatmap uses the global maximum for colorization
    // if activated: uses the data maximum within the current map boundaries 
    //   (there will always be a red spot with useLocalExtremas true)
      "useLocalExtrema": true,
    // which field name in your data represents the latitude - default "lat"
      latField: 'lat',    // which field name in your data represents the longitude - default "lng"
      lngField: 'lng',
    // which field name in your data represents the data value - default "value"
      valueField: 'count'
    });

    var testData = {
      max: 8,
      data: []
    };

    for(var i in countries){
      if(countries[i].name == "United States"){
        var latLng = {lat: 38.779781, lng: -102.128906, count: 4};
      }else if(countries[i].name == "Canada"){
        var latLng = {lat: 59.327585, lng: -113.027344, count: 4};
      }else if(countries[i].name == "Russia"){
        var latLng = {lat: 65.343931, lng: 97.558594, count: 4};
      }else if(countries[i].name == "China"){
        var latLng = {lat: 35.128894, lng: 101.074219, count: 4};
      }else if(countries[i].name == "Japan"){
        var latLng = {lat: countries[i].centerLat, lng: countries[i].centerLng, count: 4};
        testData.data.push(latLng);
      }
      else{
        var latLng = {lat: countries[i].centerLat, lng: countries[i].centerLng, count: 4};
      }
        
        
      
    }

    //console.log(testData);
    /*
    var testData = {
       max: 8,
       data: [{lat: 24.6408, lng:46.7728, count: 8}, {lat: 1.6408, lng:36.7728, count: 8}]
    };
    */


    heatmap.setData(testData);

      //console.log(countries);

      //console.log(map);

      /*
      for(var row in countries){
        console.log(countries[row]);
        countries[row].fillColor = "green";
        countries[row].strokeColor = "blue";
      }
      */
    }

    