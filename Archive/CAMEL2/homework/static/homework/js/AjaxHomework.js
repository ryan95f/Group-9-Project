$(document).ready( function(){
	$("input[name='save-answer']").click( function( event ){
		event.preventDefault();
		var inAnswer = $('#answer-text').val();
		var pk = $('#id_question').val();
		var user_id = $('#id_user').val();
        if(answer_validation()){
            save_answer(inAnswer, pk, user_id);
        }
	});
});

function save_answer(answer, pk, user_id){
	$.ajax({
        url : "/homework/answers/edit/" + pk +'/ajax/', // the endpoint
        type : "POST", // http method
        data : {
        	question: parseInt(pk),
        	user: parseInt(user_id),
        	text: answer,
        	save: "save-answer",
        }, // data sent with the post request
        
        //get the csrf_token
        beforeSend: function(xhr, settings) {
        	//console.log("Before Send");
        	$.ajaxSettings.beforeSend(xhr, settings);
    	},

        // handle a successful response
        success : function(json) {
            //console.log(json); // log the returned json to the console
            // console.log("success");
            // console.log(json);
            $('.previewbox > p').text(json.out_text);
            update_jax(json.out_text);
        },

        // handle a non-successful response
        error : function(xhr,errmsg,err) {
            console.log(xhr.responseText);
        }
    });
}

function update_jax(TeX){
    // ajax update for MathJax
    TeX = TeX.replace(/\$/g, '');
    console.log(TeX);
    var QUEUE = MathJax.Hub.queue;
    var math = null;

    QUEUE.Push(function () {
      math = MathJax.Hub.getAllJax("jax_wrapper")[0];
    }); 

    QUEUE.Push(["Text",math,"\\displaystyle{"+TeX+"}"]);
}