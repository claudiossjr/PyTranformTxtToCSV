      var map;
      var markers = [];
      var polygon = null;


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
              newCoordinates.push(constructNewCoordinates(geometries[j]));
            }
          }else{
              newCoordinates = constructNewCoordinates(rows[i][1]['geometry']);
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
          google.maps.event.addListener(country, 'mouseover', function() {
          this.setOptions({fillOpacity: 0.4});
        });
        google.maps.event.addListener(country, 'mouseout', function() {
          this.setOptions({fillOpacity: 0});
        });
        google.maps.event.addListener(country, 'click', function() {
          var metric = $( "#metricSelect" ).val();
          var index = $( "#indexSelect" ).val();
          if(!metric || !index){
            alert("You must select a metric and a index");
          }
          request(this.name, metric, index);
        });

        country.setMap(map);

        }
      }
    }
    function constructNewCoordinates(polygon){
      var newCoordinates = [];
      var coordinates = polygon['coordinates'][0];
      for(var i in coordinates){
        newCoordinates.push(new google.maps.LatLng(coordinates[i][1], coordinates[i][0]));
      }
      return newCoordinates;
    }

    