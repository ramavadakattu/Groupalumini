$(document).ready(function() {    
    $(':input:visible:enabled:first').focus();
    //intialize the submit button
  
   
    
    
 });

function approve(flag,id,entity)
/*
  if flag is 0 ===================> REject
  if flag is 1 ====================> Approve  
*/
{
   
   $("#approvebutton").before("<span id='approveajax'> &nbsp; &nbsp; <img src='/appmedia/images/alumclubajax.gif' alt='ajax image'/>  </span>") 
   $('#approvebutton').attr("disabled", "true");
   $('#rejectbutton').attr("disabled", "true");   
   //Bring answer send an ajax request
   serverurl = "/institution/approvemembers/"
   var data = {};
   data.id =  id
   data.flag =  flag
   data.entity = entity
   //Get the answer
   $.post(serverurl,
            data,
            approvalDone,
            "json"
           );
   
   
    
}


function approvalDone(data)
{
       
     // $("#approvebutton").removeAttr('disabled');
     //  $("#rejectbutton").removeAttr('disabled');
    $("#approveajax").remove()       
    $("#approvebutton").before("<span  id='errormessage'>"+data['message']+"</span>");
    
    
}

