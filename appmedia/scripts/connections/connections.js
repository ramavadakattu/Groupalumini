$(document).ready(function() {    
  
  
    
});


function connectto(userid)
{
    
  var data = {};   
   $("#connectbox").before("<span id='mconnectajaximage'> &nbsp; &nbsp; <img src='/appmedia/images/alumclubajax.gif' alt='ajax image'/>  </span>")    
   //Bring answer send an ajax request
   serverurl = "/connections/add/"+userid+"/";     
   //Get the answer
   $.post(serverurl,
               data,
         sentRequest,
            "json"
           );
 
           
}


function sentRequest(data)
{
    if (data['error'] === undefined)
    {
    $("#mconnectajaximage").html("Sent invitation request.................");   
    }
    else{
        $("#mconnectajaximage").html(data['error']);           
    }
        
}


function accept(connectionid)
{
   var data = {};
   messageboxid = "#friendmessage"+connectionid
   $(messageboxid).html("&nbsp; &nbsp; <img src='/appmedia/images/alumclubajax.gif' alt='ajax image'/>  ")    
   //Bring answer send an ajax request
   serverurl = "/connections/accept/"+connectionid+"/";     
   //Get the answer
   $.post(serverurl,
               data,
         acceptDone,
            "json"
           );
   
}





function reject(connectionid)
{
   var data = {};
   messageboxid = "#friendmessage"+connectionid
   $(messageboxid).html("&nbsp; &nbsp; <img src='/appmedia/images/alumclubajax.gif' alt='ajax image'/>  ")    
   //Bring answer send an ajax request
   serverurl = "/connections/delete/"+connectionid+"/";     
   //Get the answer
   $.post(serverurl,
               data,
         deleteDone,
            "json"
           );
   
}




function acceptDone(data)
{
   
    messageboxid = "#friendmessage"+data['connectionid'];
    friendbox = "#friendbox"+data['connectionid'];
    if (data['error'] === undefined)
    {
      $(friendbox).remove();
      $("#friendmessage").html("Success Now you are friends..........")
    
    }
    else{
        $(messageboxid).html(data['error']);           
    }
        
}




function deleteDone(data)
{
   
    messageboxid = "#friendmessage"+data['connectionid'];
    friendbox = "#friendbox"+data['connectionid'];
    if (data['error'] === undefined)
    {
      $(friendbox).remove();
      $("#friendmessage").html("Successfully deleted the connection..........")
    
    }
    else{
        $(messageboxid).html(data['error']);           
    }
        
}
