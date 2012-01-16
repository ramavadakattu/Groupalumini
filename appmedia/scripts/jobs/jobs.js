$(document).ready(function() {    
  
 
    
 });









function postComment(jobid)
{
   var data = {};   
   text  = $("textarea[name=commentarea]","#commentbox").val();   
   if ($.trim(text).length  <= 0)
        {
            window.alert("Please enter the Comment.........");
            return ;
        }
   
   $("#sendbutton").before("<span id='mesageajaximage'> &nbsp; &nbsp; <img src='/appmedia/images/alumclubajax.gif' alt='ajax image'/>  </span>") 
   $("#sendbutton").attr("disabled", "true");   
   //Bring answer send an ajax request
   serverurl = "/jobs/postjobcomment/"+jobid+"/";
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
      $("#jobcomments").append("<div class='jcomment'>"+data['text']+"</div>");
      $("#sendbutton").removeAttr("disabled");
      $("#mesageajaximage").remove();
      $("#errormessagespan").html("");      
      unhide('commentbox');        
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
        $("textarea[name=commentarea]","#commentbox").val("");        
        $(divid).css("display","block");
        $("textarea[name=commentarea]","#commentbox").focus();
        $("#errormessagespan").html("");   
        
    }
    
    
}