$(document).ready(function() {
   
  
  if ($("form[name=entryform]").length > 0)
  {
         $("form[name=entryform]").submit(specifyWhichButton);
         $("input[name=whichbutton]").val("save"); 
  }
  
  if ($("form[name=commentform]").length > 0)
  {   
         $("textarea[name=commentarea]","#commentbox").val("Type your comment here");
         $("textarea[name=commentarea]","#commentbox").focus(removeDefaultText);
         $("textarea[name=commentarea]","#commentbox").blur(addDefaultText);        
       if ($("input[name=username]").length > 0 )
       {
         $("input[name=username]","#commentbox").val("Name");
         $("input[name=username]","#commentbox").focus(removeDefaultText);
         $("input[name=username]","#commentbox").blur(addDefaultText);        
         $("input[name=webaddress]","#commentbox").val("Website (Optional)");
         $("input[name=webaddress]","#commentbox").focus(removeDefaultText);
         $("input[name=webaddress]","#commentbox").blur(addDefaultText);        
       }   
  }
  
    
 });


function removeDefaultText()
{
   name =  $(this).attr('name');
   value = $(this).val();
   if (name =="commentarea")
   {
     
      if (value == "Type your comment here")
      {
        $("textarea[name=commentarea]","#commentbox").val("");    
         
      }      
   }
   else if (name == "username")
   {
       if (value == "Name")
      {
       $("input[name=username]","#commentbox").val("");
      }
   }
   else if (name == "webaddress")
   {
      if (value == "Website (Optional)")
      {
             $("input[name=webaddress]","#commentbox").val("");
      }
      
   }
   
}


function addDefaultText()
{
   name =  $(this).attr('name');
   value = $(this).val();
   
   if (name =="commentarea")
   {
      if ($.trim(value).length == 0 )
      {
         $("textarea[name=commentarea]","#commentbox").val("Type your comment here");
      }
      
      
   }
   else if (name == "username")
   {
      if ($.trim(value).length == 0 )
      {
         $("input[name=username]","#commentbox").val("Name");
         
      }
   }
   else if (name == "webaddress")
   {
      if ($.trim(value).length == 0 )
      {
          $("input[name=webaddress]","#commentbox").val("Website (Optional)");
      }
      
   }
   
   
   
}


function postComment(entryid)
{
   
   var data = {};
   text  = $("textarea[name=commentarea]","#commentbox").val();   
   if (($.trim(text).length  <= 0 ) | ($.trim(text) == "Type your comment here"))
        {
            window.alert("Please enter the Comment.........");
            return ;
        }
      
   
   $("#sendbutton").before("<span id='mesageajaximage'> &nbsp; &nbsp; <img src='/appmedia/images/alumclubajax.gif' alt='ajax image'/>  </span>"); 
   $("#sendbutton").attr("disabled", "true");   
   //Bring answer send an ajax request
   serverurl = "/blog/postcomment/"+entryid+"/";
   data.text = text;
   
   if ($("input[name=username]").length > 0 )
   {
      
      username = $("input[name=username]").val();
      if ( ($.trim(username).length  <= 0) | ($.trim(username) == "Name") )
        {
            window.alert("Please enter the Username.........");
            return ;
        }      
      
      data.username = $("input[name=username]").val();
      data.webaddress = $("input[name=webaddress]").val();
   }
   
   
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
      $("#entrycomments").append("<div class='ecomment'>"+data['text']+"</div>");
      $("#sendbutton").removeAttr("disabled");
      $("#mesageajaximage").remove();
      $("#errormessagespan").html("");
      $("#commentsuccess").html("Sucessfully posted the comment");
      $("textarea[name=commentarea]","#commentbox").val("Type your comment here");
      
      if ($("input[name=username]").length > 0 )
       {
         
         $("input[name=username]","#commentbox").val("Name");         
         $("input[name=webaddress]","#commentbox").val("Website (Optional)");
             
       }   
      
       
      
            
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



function specifyWhichButton()
{
   $("input[name=whichbutton]").val("submit");    
   
   return true;
   
}