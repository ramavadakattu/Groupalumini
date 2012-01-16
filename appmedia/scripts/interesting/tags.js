

$(document).ready(function() {
    
    
    $("#submittags").click(submitTags);   
    
 });


function submitTags()
{
    
   
     //Bring answer send an ajax request
    var serverurl = "/interesting/submittags/"   
   var data = {};
   
   $("#errormessage").html("<img src='/appmedia/images/alumclubajax.gif' alt='ajax image'/>  Submitting....... ")   
   data.tags =  $("input[name=tags]").val();
   $("#submittags").attr("disabled", "true");
   
   //Get the answer
   $.post(serverurl,
            data,
            tagSubmissionDone,
            "json"
           ); 
   
}

function tagSubmissionDone(data)
{
    $("#submittags").removeAttr("disabled");
    if (data['error'] == undefined )
    {
        
    $("#errormessage").html("");
        
    }
    else
    {
        $("#errormessage").html(data['error']);
        
    }
    
}





