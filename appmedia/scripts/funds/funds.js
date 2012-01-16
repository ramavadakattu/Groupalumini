$(document).ready(function() {    
   
    if ($("form[name='enteramountform']").length > 0)
    {
         $("form[name='enteramountform']").submit(checkAmount);
    }
    else if ($("form[name='confirmform']").length > 0) {
         $("form[name='confirmform']").submit(onConfirm);       
    }
    
 });


function checkAmount()
{    
    var intRegex = /^\d+$/;
    var floatRegex = /^((\d+(\.\d *)?)|((\d*\.)?\d+))$/;

    amount = $("input[name=amount]").val();    
    if ($.trim(amount).length <= 0 )
    {
        window.alert("you have not entered any amount............");
        return false;     
        
    }
        
    if(  intRegex.test(amount) || floatRegex.test(amount)) {
      
    }
    else
    {        
        window.alert("please enter a valid number");
        return false
    }
    
    
    $("input[type='submit']").before("<span id='mesageajaximage'> &nbsp; &nbsp; <img src='/appmedia/images/alumclubajax.gif' alt=''/>  </span>");
    $("input[type='submit']").attr("disabled", "true");
 
    return true;        
    
}


function onConfirm()
{
    
    $("input[type='submit']").before("<span id='mesageajaximage'> &nbsp; &nbsp; <img src='/appmedia/images/alumclubajax.gif' alt=''/>  </span>");
    $("input[type='submit']").attr("disabled", "true");
    
    return true;                
}
