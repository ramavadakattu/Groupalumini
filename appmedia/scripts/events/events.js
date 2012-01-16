$(document).ready(function() {    
  
 
 
    
 });


function notedown(eventid,attendingflag)
{
   var data = {};         
   $("#attendingbox").prepend("<span id='mesageajaximage'> &nbsp; &nbsp; <img src='/appmedia/images/alumclubajax.gif' alt='ajax image'/>  </span>")    
   //Bring answer send an ajax request
   serverurl = "/events/attending/"+eventid+"/"+attendingflag+"/";   
   //Get the answer
   $.post(serverurl,
            data,
            afterNotingDown,
            "json"
           );
    
}

function afterNotingDown(data)
{
    $("#mesageajaximage").remove();
    
    if (data['error'] == "success")
    {
        $("#totalattendancecount").html(data['totalcount']);
        if (data['attending'] > 0 )
        {
            //change to unattending box
            tempstr = "<a href=\"javascript:void(0)\" onclick=\"notedown( "+data['eventid']+",0)\"> Iam not attending the event </a>"           
            $("#attendingbox").html(tempstr);            
            $("#userattendingbox").append(data['spancontent']);
                
        }
        else{
            //change to attending box
            tempstr = "<a href=\"javascript:void(0)\" onclick=\"notedown( "+data['eventid']+",1)\"> Iam  attending the event </a>";            
            $("#attendingbox").html(tempstr);            
            
            
        }
        
    }
    
    
    
}