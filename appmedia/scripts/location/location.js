  
$(document).ready(function() {       
   
     
    
 });



function sendBucketMessage(url)
{
    
  
   var data = {};   
   text  = $("textarea[name=message]","#locatemessagebox").val();   
   if ($.trim(text).length  <= 0)
        {
            window.alert("Please enter the message.........");
            return ;
        }
   
   $("#sendbutton").before("<span id='mesageajaximage'> &nbsp; &nbsp; <img src='/appmedia/images/alumclubajax.gif' alt='ajax image'/>  </span>") 
   $("#sendbutton").attr("disabled", "true");   
   //Bring answer send an ajax request
   serverurl = url;
   data.text = text;   
   //Get the answer
   $.post(serverurl,
            data,
            messagePosted,
            "json"
           );     
   
}



function messagePosted(data)
{
    if (data['error']   === undefined )
    { 
      $("#bucketerrormessage").html("Successfully sent your message")
      $("textarea[name=message]","#locatemessagebox").val();   
      $("#sendbutton").removeAttr("disabled");
      $("#mesageajaximage").remove();
      $("#errormessagespan").html("");      
      unhide('locatemessagebox');        
    }
    else{        
        $("#errormessagespan").html(data['error'] +" &nbsp "+"Resubmit again");
        $("#mesageajaximage").remove();
        $("#sendbutton").removeAttr("disabled");
        
    } 
}







function unhide(divid)
{
    divid = "#"+divid
    toggle = $(divid).css("display");
    if (toggle.indexOf("block") >= 0 )
    {
        
        $(divid).css("display","none");
    }
    else
    {
        $("textarea[name=messagearea]","#messagebox").val("");        
        $(divid).css("display","block");
        $("textarea[name=messagearea]","#messagebox").focus();
        $("#errormessagespan").html("");   
        
    }
    
    
}


 