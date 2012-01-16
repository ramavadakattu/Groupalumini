var totalcharacters  = 0

$(document).ready(function() {    
  
    $(':input:visible:enabled:first').focus();   
    $("#id_messagearea").keyup(calculateCharacters);   
    totalcharacters = parseInt($("#totalcharacters").text())
    
 });




function postMessage(touserid)
{
   var data = {};   
   text  = $("textarea[name=messagearea]","#messagebox").val();   
   if ($.trim(text).length  <= 0)
        {
            window.alert("Please enter the message.........");
            return ;
        }
   
   $("#sendbutton").before("<span id='mesageajaximage'> &nbsp; &nbsp; <img src='/appmedia/images/alumclubajax.gif' alt='ajax image'/>  </span>") 
   $("#sendbutton").attr("disabled", "true");   
   //Bring answer send an ajax request
   serverurl = "/profile/sendmessage/"+touserid+"/";
   data.text = text;   
   //Get the answer
   $.post(serverurl,
            data,
            messagePosted,
            "json"
           );
    
}

function calculateCharacters()
{
   
    text  = $("textarea[name=messagearea]","#messagebox").val();   
    textlength =  text.length;       
    if (textlength > totalcharacters) {
        
       $("textarea[name=messagearea]","#messagebox").val(text.substr(0,300));
       
        //$("textarea[name=messagearea]","#messagebox").val("asdfsadf asdfsf");
       text  = $("textarea[name=messagearea]","#messagebox").val();       
       //$("textarea[name=messagearea]").scrollTop = $("textarea[name=messagearea]").scrollHeight;
       var $t = $("textarea[name=messagearea]","#messagebox");//whatever the selector you use.       
       textlength =  text.length; 
       
    }
    
    remaining =  totalcharacters - textlength;    
    $("#totalcharacters").html(remaining);    
    

    
}








function messagePosted(data)
{
    if (data['error']   === undefined )
    {
      $("#usermessages").prepend("<div class='profilemessage'>"+data['text']+"</div>");
      $("#sendbutton").removeAttr("disabled");
      $("#mesageajaximage").remove();
      $("#errormessagespan").html("");      
      unhide('messageform');        
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