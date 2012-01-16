$(document).ready(function() {    
  
 
    
 });


function putVote(model,object_id,direction,from)
{
   upvotediv = ""
   downvotediv = ""
   scorediv = ""
   
  
   if (model.indexOf("Question") >= 0)
   {
      serverurl = "/askalumini/voting/question"+"/"+object_id+"/"+direction+"vote/";
      upvotediv = "#qupvote"+object_id;
      downvotediv = "#qdownvote"+object_id;
      scorediv = "#qscore"+object_id;
      
   }
   else{
      serverurl = "/askalumini/voting/answer"+"/"+object_id+"/"+direction+"vote/";
      upvotediv = "#aupvote"+object_id;
      downvotediv = "#adownvote"+object_id;
      scorediv = "#ascore"+object_id;      
   }
    prevscore = parseInt($(scorediv).text())
   
   weight = 0;
   
   if (direction.indexOf("up") >= 0)
   {
    weight = 1
   }
   else if (direction.indexOf("down") >= 0){
    weight = -1;
   }
   else
   {
    weight = 0;
   }   
    if (weight == 1){
        
            $(upvotediv).html(" <a href=\"javascript:void(0)\"  onclick=\"putVote('"+model+"',"+object_id+",'clear','up')\">  <img src=\"/appmedia/images/vote-arrow-up-on.png\" alt=\"vote up\" />    </a> ");
            $(downvotediv).html("<a href=\"javascript:void(0)\"  onclick=\"putVote('"+model+"',"+object_id+",'down','down')\">   <img src=\"/appmedia/images/vote-arrow-down.png\" alt=\"vote down\"/>  </a> ");
            prevscore = prevscore + 1;
            if (prevscore == 0 )
            {
                 prevscore = 1
            }
            $(scorediv).html(prevscore);     
   }
   else if (weight == -1){                
                $(downvotediv).html("<a href=\"javascript:void(0)\"  onclick=\"putVote('"+model+"',"+object_id+",'clear','down')\">   <img src=\"/appmedia/images/vote-arrow-down-on.png\" alt=\"vote down\"/>  </a> ");
                $(upvotediv).html(" <a href=\"javascript:void(0)\"  onclick=\"putVote('"+model+"',"+object_id+",'up','up')\">  <img src=\"/appmedia/images/vote-arrow-up.png\" alt=\"vote up\" />    </a> ");                            
                
                prevscore = prevscore - 1;
                if (prevscore == 0 )
                {
                     prevscore = -1
                }     
                $(scorediv).html(prevscore);  
     }
     else{
        
        if (from.indexOf("up") >= 0)
        {
         prevscore = prevscore -1;
         $(upvotediv).html(" <a href=\"javascript:void(0)\"  onclick=\"putVote('"+model+"',"+object_id+",'up','up')\">  <img src=\"/appmedia/images/vote-arrow-up.png\" alt=\"vote up\" />    </a> ");
         
        }
        else
        {
         prevscore = prevscore +1;
         $(downvotediv).html("<a href=\"javascript:void(0)\"  onclick=\"putVote('"+model+"',"+object_id+",'down','down')\">   <img src=\"/appmedia/images/vote-arrow-down.png\" alt=\"vote down\"/>  </a> ");
            
        }
        $(scorediv).html(prevscore);  
        
     }
   
   var data = {};   
   //Get the answer
   $.post(serverurl,
            data,
            afterSubmit,
            "json"
           );
}

function afterSubmit(data)
{
    
    
}
   
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
