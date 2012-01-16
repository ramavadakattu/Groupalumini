
$(document).ready(function() {
    
    $("input[name='alumini']").click(displayStudentbox);
    $("input[name='faculty']").click(displayFacultybox);
    displayStudentbox();
    displayFacultybox();
 });


function displayStudentbox()
{
    
    if ( $("input[name='alumini']").is(':checked'))
    {
        //display student box
        $("#studentcbox").css("display","block");
        
    }
    else{
         $("#studentcbox").css("display","none");       
        
        $("select[name='department']").val("");
        $("select[name='program']").val("");
        $("select[name='country']").val("");
        $("select[name='passoutyear']").val("");
        $("select[name='industry']").val("");
        $("select[name='market']").val("");        
    }
}

function displayFacultybox()
{
    if ( $("input[name='faculty']").is(':checked'))
    {
        //display faculty box
        $("#facultycbox").css("display","block");        
    }
    else
    {
        $("#facultycbox").css("display","none");
        $("select[name='fdepartment']").val("");
        $("select[name='fcountry']").val("");
    }
    
}