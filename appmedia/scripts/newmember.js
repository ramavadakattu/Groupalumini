$(document).ready(function() {    
    
    $(':input:visible:enabled:first').focus();
    
    
   if ($("#studentbox").length > 0)
    {    
            hideAnotherForm();
            modifyForm();
            $("input[name='accounttype']").change(hideAnotherForm);        
    }
    
   
    if ($("select[name='whatiamdoing']").length > 0)
    {      
            
            $("select[name='whatiamdoing']").change(modifyForm);
            modifyForm();
    }
    
    
    if ($("input[name='locationflag']").length > 0)
    {    
        $("input[name='locationflag']").click(displayMap);        
   
     if ($("form[name=efacultyform]").length >  0 )
     {
        
        
     }
     else
     {
        
         $("form").submit(loadLatLng);
     }    
    intializeMaps();
    
    }
 });


function loadLatLng()
{ 

    whichbox = "";  
    
    
    //changelocationbox
    if ($("#studentbox").length > 0)
    {
    
    if ($("#studentbox").css("display") == "none")
    {
        whichbox = "#facultybox";
    }
    else{
        whichbox = "#studentbox";
    }}
    else{
       whichbox = "#changelocationbox"
    }
    
   
   
    lng = $("input[name='longitude']",whichbox).val();
    lat =  $("input[name='latitude']",whichbox).val();
    
    if ( lng == 0 || lat == 0  || (whichbox == "#changelocationbox"))
    {
        //Let us fetch the lat and lng from the address
        city =  $("input[name='city']",whichbox).val();
        state = $("input[name='state']",whichbox).val();
        address = $("input[name='address']",whichbox).val();
        country = $("select[name='country'] option:selected",whichbox).text();
       
       
      
        mainaddress = ""
        
        if ($.trim(address).length > 0 )
        {
         mainaddress = address;               
        }
         if ($.trim(city).length > 0 )
        {
            if ($.trim(mainaddress).length == 0)
            {
                mainaddress = city;         
            }
            else{
                mainaddress = mainaddress +","+city;
            }
            
        }
         if ($.trim(state).length > 0 )
        {
            var alNumRegex = /^([a-zA-Z]+)$/;
            if(alNumRegex.test(state)) {

            }
            else
            {
                // window.alert("State should contain only alphabets....");
                // return false;
                
            }           
            
            if ($.trim(mainaddress).length == 0)
            {
                mainaddress = state;         
            }
            else{
                mainaddress = mainaddress +","+state;
            }
            
        }
        else{
            window.alert("please enter the state");
            return false;
        }
        
         if ($.trim(country).length > 0 )        
        {
            if ($.trim(mainaddress).length == 0)
            {
                mainaddress = country;         
            }
            else{
                mainaddress = mainaddress +","+country;
            }
            
        }
       
       $("input[type='submit']",whichbox).attr("disabled", "true");   
        $("input[type='submit']",whichbox).before("<span id='submiterrormessage'> &nbsp; &nbsp; <img src='/appmedia/images/alumclubajax.gif' alt='ajax image'/>  Calculating location related information........ </span>") 
           
          
        
        if ( mainaddress.length > 0 ){
            
            //put down ajax say that we are calculating some location related info
            var geo = new GClientGeocoder();                      
            geo.getLocations(mainaddress, mapAddress)
        
        } //end of len(mainaddress)       
        
        return false;
        
    }
    else{
    
      
        return true;
    }
    
}



function mapAddress(response)
{
        $("#submiterrormessage").html("submitting..........");
        // $("input[type='submit']",whichbox).removeAttr("disabled"); 
        
        
             if (!response || response.Status.code != 200) {
                   
   
                 }
                 else{
                    var place = response.Placemark[0];
                    lat = place.Point.coordinates[1];
                    lng = place.Point.coordinates[0];                    
                    $("input[name='longitude']",whichbox).val(lng);
                    $("input[name='latitude']",whichbox).val(lat);
                    
             }             
   
    if ($("#studentbox").length > 0)
    {   
        if ($("#studentbox").css("display") == "none")
        {
           document.nfacultyform.submit();
        }
        else{
           document.nstudentform.submit();
           }          
    }    
    else{        
        document.locationform.submit();
        
    }
   
}


function hideAnotherForm()
{
    
    if ( $("input[name='accounttype']").length > 0 )
    {
    var svalue = $("input[name='accounttype']:checked").val();
    svalue = svalue.toLowerCase();   
    
    if (svalue == "faculty"){
        //hide student box
        $("#studentbox").css("display","none");
        $("#facultybox").css("display","block");
        $("input[name='whichform']","#facultybox").val('faculty');
            
    }
    else if (svalue == "student")
    {
        //hide faculty box
        $("#studentbox").css("display","block");
        $("#facultybox").css("display","none");
        $("input[name='whichform']","#studentbox").val('student');
             
    }
    }
}

function modifyForm()
/** Modify the form to reflect the current state of based on the profession **/ 
{
    
   
   if ($("select[name='whatiamdoing']").length > 0 )
   {
    //user has selected some option other than None
    svalue = $("select[name='whatiamdoing']").val().toLowerCase();   
    if (svalue == "student" )
    {
     //remove the rest of options
     $("#companybody").hide();
     $("#titlebody").hide();
     $("#industrybody").hide();
      $("#marketbody").hide();
        
    }
    else if (svalue == "owner" )
    {
        //remove title
        $("#companybody").show();     
     $("#industrybody").show();
     $("#marketbody").show();
     $("#titlebody").hide();
        
        
    }
    else if (svalue == "employee" )
    {
        //remove title
        $("#companybody").show();     
     $("#industrybody").show();
     $("#titlebody").show();
     $("#marketbody").show();
        
        
    }    
    else if (svalue == "lwork" )
    {        
        //looking for work remove comapny title
        
           //remove title
        $("#companybody").hide();     
     $("#industrybody").show();
     $("#marketbody").show();
     $("#titlebody").hide();
        
        
    }
    else if (svalue == "freelance" )
    {
         //freelancer remove company and title
        $("#companybody").hide();     
        $("#industrybody").show();
        $("#marketbody").show();
        $("#titlebody").hide();
        
    }
    
   }
   
}


function getForm()
{
    svalue=""
    if ( $("input[name='accounttype']").length > 0 )
    {
            var svalue = $("input[name='accounttype']:checked").val();
            svalue = svalue.toLowerCase();
    }
    else{
        
        return "faculty";
    }
    return svalue;
    
  
}


function getMap()
{
    
    svalue = getForm();
   
    var div = ""
    if (svalue == "faculty")
    {
        div = "gmap1";        
    }
    else{
        div = "gmap2"
    }       
    return new google.maps.Map2(document.getElementById(div));   
}

function displayMap()
{
   
    locationflag = $(this).val();
    if (locationflag == "map")
    {
       $("div.mapwrapper").css("display","block");
       intializeMaps();
        
    }
    else{
        $("div.mapwrapper").css("display","none");
       
        
    }
    
    
}




function intializeMaps()
{
   
    var gmap = getMap();    
    gmap.setCenter(new google.maps.LatLng(9.97335, -15.8203),2);
    gmap.addControl(new google.maps.LargeMapControl());
    gmap.addControl(new google.maps.MapTypeControl());
    google.maps.Event.addListener(gmap, "move",captureLocation)  
    
}



function captureLocation()
{    
    center = this.getCenter();
    lat = center.lat();
    lng = center.lng();
    
    geocoder = new GClientGeocoder();
    geocoder.getLocations(center,captureAddress);

    //gettting the location 
    
}

function captureAddress(response)
{
    if (!response || response.Status.code != 200) {
        
      } else {
         place = response.Placemark[0];
         point = new GLatLng(place.Point.coordinates[1],place.Point.coordinates[0]);
         
         var countryname =  place.AddressDetails.Country.CountryName;
         
         var state = ""
         var city = ""
          var locality = "";
          
         
         if (place.AddressDetails.Country.AdministrativeArea != undefined)
         {
            var state = place.AddressDetails.Country.AdministrativeArea.AdministrativeAreaName;
            
             if (place.AddressDetails.Country.AdministrativeArea.SubAdministrativeArea != undefined)
              {
                 city = place.AddressDetails.Country.AdministrativeArea.SubAdministrativeArea.SubAdministrativeAreaName;
                 
                 
                 if (place.AddressDetails.Country.AdministrativeArea.SubAdministrativeArea.Locality != undefined)
                 {
                    locality = place.AddressDetails.Country.AdministrativeArea.SubAdministrativeArea.Locality.LocalityName;
                    
                    if (place.AddressDetails.Country.AdministrativeArea.SubAdministrativeArea.Locality.Thoroughfare != undefined)
                    {
                        locality = locality +","+ place.AddressDetails.Country.AdministrativeArea.SubAdministrativeArea.Locality.Thoroughfare.ThoroughfareName;
                        
                    }
                    
                 }
         
         
                 
               }
         }
        
         svalue = getForm();
         
       
         
         if (svalue == "faculty")
         {            
            //$("select[name='country']","#facultybox").val(countryname);
            $("#country2 option").each(function () {
                  if ($(this).text().toLowerCase().indexOf(countryname.toLowerCase()) >= 0)
                  {
                     $("#country2").val($(this).val());
                  }
                  
                  if(countryname.toLowerCase() == "usa" )
                  {
                     $("#country2").val("United States");
                    
                  }
                
            })
            
            if ($("#facultybox").length > 0)
            {
            $("input[name='city']","#facultybox").val(city);
            $("input[name='state']","#facultybox").val(state);
            $("input[name='address']","#facultybox").val(locality);
            $("input[name='longitude']","#facultybox").val(place.Point.coordinates[0]);
            $("input[name='latitude']","#facultybox").val(place.Point.coordinates[1]);
            }            
            else{
                
                    $("input[name='city']").val(city);
            $("input[name='state']").val(state);
            $("input[name='address']").val(locality);
            $("input[name='longitude']").val(place.Point.coordinates[0]);
            $("input[name='latitude']").val(place.Point.coordinates[1]); 
           
            }
            
            
            $("#locationtable2").css("backgroundColor","yellow");
            setTimeout ( "clearColor()", 1000 );
            setTimeout ( "clearColor2()", 1500 );
                 
         }
         else{
            //$("input[name='country']","#studentbox").val(countryname);
            //$("#country1").val(countryname).attr("selected","selected")
            
            $("#country1 option").each(function () {
                  if ($(this).text().toLowerCase().indexOf(countryname.toLowerCase()) >= 0)
                  {
                     $("#country1").val($(this).val());
                  }
                  
                  if(countryname.toLowerCase() == "usa" )
                  {
                     $("#country1").val("United States");
                    
                  }                  
                
            })
            
            
            $("input[name='city']","#studentbox").val(city);
            $("input[name='state']","#studentbox").val(state);
            $("input[name='address']","#studentbox").val(locality);
            $("input[name='longitude']","#studentbox").val(place.Point.coordinates[0]);
            $("input[name='latitude']","#studentbox").val(place.Point.coordinates[1]);
         
            
            $("#locationtable1").css("backgroundColor","yellow");
            setTimeout ( "clearColor()", 1000 );
            setTimeout ( "clearColor2()", 1500 );

         }
         
         
       
      }

}


function clearColor()
{
    $("#locationtable1").css("backgroundColor"," #F8F9AC");
      $("#locationtable2").css("backgroundColor"," #F8F9AC");
     
    
}


function clearColor2()
{
     
    $("#locationtable1").css("backgroundColor","white");
      $("#locationtable2").css("backgroundColor","white");
    
    
   
}  


