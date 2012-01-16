$(document).ready(function() {    
    $(':input:visible:enabled:first').focus();
    //intialize the submit button
   
   
    
    
 });


function postcomment(divbox,id,commentbox,commentbuttonbox,textareabox)
/**
 * divbox box to which we need to append comment
 * id of entity to which we need to associate comment
 * Comment box to hide when we are done
 * ajax image will come and go before commentbutton box 
 ***/

{
    
   var data = {};   
   text  = $("textarea[name="+textareabox+"]").val();
   entity = ""  
   if ($.trim(text).length  <= 0)
            {
                window.alert("Please enter the comment.........");
                return ;
            }
   
   
   imageid = "image"+divbox 
   $("#"+commentbuttonbox).before("<span id="+imageid+"> &nbsp; &nbsp; <img src='/appmedia/images/alumclubajax.gif' alt='ajax image'/>  </span>") 
   $("#"+commentbuttonbox).attr("disabled", "true");   
   //Bring answer send an ajax request
   serverurl = "/askalumini/postcomment/";
  
   if (divbox.indexOf("question") >= 0)
   {
    entity = "question";
    
   }
   else{
    
    entity = "answer";
   }
   
   
 
   
   data.id =  id;
   data.entity = entity;
   data.divbox = divbox;
   data.commentbox = commentbox;
   data.text = text;
   data.commentbuttonbox = commentbuttonbox;
   data.textareabox = textareabox;
   
   //Get the answer
   $.post(serverurl,
            data,
            checkResponse,
            "json"
           );
       
    
}



function checkResponse(data)
{
    
    if ( data['error'] == "success" )
    {
        commentbox = data['commentbox'];
        divbox = data['divbox'];
        text = data['text'];
        commentbuttonbox = data['commentbuttonbox'];       
        $("#"+commentbuttonbox).removeAttr("disabled");        
        imageid = "#image"+divbox;                
        $(imageid).remove();
        textareabox = data.textareabox;
        $("textarea[name="+textareabox+"]").val("");        
        $("#"+commentbox).css("display","none");
        $("#"+divbox).append(text);
        
        
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
        $(divid).css("display","block");
        
    }
    
    
}