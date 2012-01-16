$(document).ready(function() {
  
  
  $('#flayer1').Draggable( 
        { 
            zIndex:  25, 
            ghosting:false, 
            opacity: 0.5, 
            handle:    '#layer1_handle'
        } 
    );
 $("#flayer1").hide();
 
 $('#fclose').click(function() 
{ 
    $("#flayer1").hide();
    $("#blackbox").hide();
});
 
 $("#blackbox").hide();
 
 //function which helps us to put a div in center
 jQuery.fn.center = function () {
    this.css("position","absolute");
    this.css("top", ( $(window).height() - this.height() ) / 2+$(window).scrollTop() + "px");
    this.css("left", ( $(window).width() - this.width() ) / 2+$(window).scrollLeft() + "px");
    return this;
}


$('#flayer1_form').ajaxForm({
    dataType:'json',
    success: feedbackSuccess,
    beforeSubmit: beforeFeedbackSubmit
});


$('#flayer1_form').submit("beforeFeedbackSubmit");

   
});


function beforeFeedbackSubmit()
{
   $("#feedbackSubmitButton").before("<span id='mesageajaximage'> &nbsp; &nbsp; <img src='/appmedia/images/alumclubajax.gif' alt='ajax image'/>  </span>");
   $("#feedbackSubmitButton").attr("disabled", "true"); 
   $(this).ajaxSubmit(); 
   return true;
}



function feedbackSuccess(data)
{
 if (data['error']   === undefined )
    {
      $("#flayer1").hide();
      $("#blackbox").hide();
      $("#feedbackSubmitButton").removeAttr("disabled");
      $("div.errorbox").html("<ul>"+"<li class='messages'>"+"Sucessfully submitted the feedback"+"</li>"+"</ul>");
      window.location = window.location+"#";
       
    }
    else{        
        
        $("#mesageajaximage").remove();
        $("#feedbackSubmitButton").removeAttr("disabled");
         
    } 
  
  
}


function openModelWindow()
{  
   $("#blackbox").show();
   $("#blackbox").addClass("cvrShow");   
    $("#blackbox").css("top",$(window).scrollTop());
     $("#flayer1").show();
   $("#flayer1").center();  
  
}