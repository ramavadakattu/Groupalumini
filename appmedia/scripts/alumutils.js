$(document).ready(function() {    
    //$(':input:visible:enabled:first').focus();
    //intialize the submit button
       
    if ($("#iregistrationform").length > 0)
    {
      $("#iregistrationform").submit(pushAjax);          
    }
    
    //Intialize constants
    window.CHART_ENTRIES=5;
    
    
 });


function pushAjax()
{    
   //disable submit button
   $('input[type=submit]', this).attr("disabled", "true");
   // introduce ajax image
    $('input[type=submit]', this)  
   //return true  
   return true;
   
   
   
}



function getMarkerOpts() {
    var greenIcon = new google.maps.Icon(google.maps.DEFAULT_ICON);
    greenIcon.image = "http://djangopeople.net/static/img/green-bubble.png";
    greenIcon.iconSize = new google.maps.Size(32,32);
    greenIcon.shadowSize = new google.maps.Size(56,32);
    greenIcon.iconAnchor = new google.maps.Point(16,32);
    greenIcon.infoWindowAnchor = new google.maps.Point(16,0); 
    markerOpts = { icon: greenIcon };
    return markerOpts;
}



function makeWindow(name,profile,batch,type,photo,address,url,lat,lon) {
    var html =  '' + 
        '<p>' + 
        '<img src="' + photo + '" alt="' + name + '" class="main">' + 
        '<span><a href="' + url + '">' + name + '</a></span> <p>';
       
     
     if( profile.length > 0 )
     {
        html +=  ' <span>'+profile+'</span> <br/>';
        
     }
     
        
     if (type == "student")
     {
        html += '<span> Batch: '+batch+'</span> <br/>';
     }
     else{
        
     }        
    
      html += '<span>'+address+'</span> </p>'+        
              '<span class="meta"><a href="#" onclick="zoomOn(' + lat + ', ' + lon + '); return false;">Zoom to point</a></span>'
              '</p>';
   
    
    return html;
}



function zoomOn(lat, lon) {
    //gmap.closeInfoWindow();
    gmap.setCenter(new google.maps.LatLng(lat, lon), 12);
}



function zoomToLocation(address) {        
        
        var geo = new GClientGeocoder();
        geo.getLocations(address, function (result){

              // ===== Look for the bounding box of the first result =====
              var N = result.Placemark[0].ExtendedData.LatLonBox.north;
              var S = result.Placemark[0].ExtendedData.LatLonBox.south;
              var E = result.Placemark[0].ExtendedData.LatLonBox.east;
              var W = result.Placemark[0].ExtendedData.LatLonBox.west;
              var bounds = new GLatLngBounds(new GLatLng(S,W), new
GLatLng(N,E));
              // Choose a zoom level that fits
              var zoom = gmap.getBoundsZoomLevel(bounds);
              gmap.setCenter(bounds.getCenter(),zoom);
         }
      );
   

} 


