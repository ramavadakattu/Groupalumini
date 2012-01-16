$(document).ready(function() {    
  $('#wmd-input').htmlarea();
  
    if ($("#questionform").length > 0)
    {
      $("#questionform").submit(fetchText);          
    }
    
    if ($("#jobform").length > 0)
    {
      $("#jobform").submit(fetchDescription);                    
    }
    
   
   
    if ($("#answerform").length > 0)
    {
      $("#answerform").submit(answerText);          
    }   
    
 });


function fetchDescription()
{
  
    var html = $("#wmd-input").htmlarea("toHtmlString");
    $("textarea[name=description]").val(html); 
   
    return true;
  
  
}

function fetchText()
{
   
    var html = $("#wmd-input").htmlarea("toHtmlString");
    $("textarea[name=description]").val(html); 
   
    return true;

}

function answerText()
{
    var html = $("#wmd-input").htmlarea("toHtmlString");
    $("textarea[name=text]").val(html);    
    return true;
  
}