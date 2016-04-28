$(document).ready( function(){
	$('#btn_save').click( function( event ){
		event.preventDefault();

		// error handling needs to be added here

		save_answer();
	});


});

function save_answer(){
    /* function to make ajax request to save function.*/
	var node = $('#node').val();
    var book = $('#book').val();
    var chapter = $('#chapter').val();
    var module = $('#module').val();
	$.ajax({
        url : "/module/" + module + "/book/" + book + "/chapter/" +  chapter + "/save-jax/" + node + "/", //endpoint
        type : "POST", // http method
        data : { 
        	user :$('#user').val(),
        	jax_answer : $('textarea').val(),
        }, // data sent with the post request
        
        //get the csrf_token
        beforeSend: function(xhr, settings) {
        	//console.log("Before Send");
        	$.ajaxSettings.beforeSend(xhr, settings);
    	},

        // handle a successful response
        success : function(json) {
            // console.log(json); // log the returned json to the console
            // console.log("success");
            update_screen(json);
        },

        // handle a non-successful response
        error : function(xhr,errmsg,err) {
            console.log(xhr.responseText);
        }
    });
}

function update_screen(json){
    /* Function to update UI after Ajax request, MathJax is also
    updated once request is made. */
	$('#answer_box').html('Your Answer: ' + json.jax_answer);
    // update the mathjax after request
    MathJax.Hub.Queue(["Typeset",MathJax.Hub,'answer_box']);
	alert("Answer saved.");
}