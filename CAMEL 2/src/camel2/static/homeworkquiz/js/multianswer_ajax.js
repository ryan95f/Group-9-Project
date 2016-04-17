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

    // get answers and add them to an array
    // array then is passed to python view
    var user_answers = [];
    $('input[type=checkbox]:checked').each(function () {
        user_answers.push($(this).val());
    });

	$.ajax({
        url : "/module/" + module + "/book/" + book + "/chapter/" +  chapter +"/save-multi/" + node + "/", //endpoint
        type : "POST", // http method
        data : { 
        	user :$('#user').val(),
        	multiplechoice : user_answers,
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
            update_screen();
        },

        // handle a non-successful response
        error : function(xhr,errmsg,err) {
            console.log(xhr.responseText);
        }
    });
}

function update_screen(){
    // alert user to indicate it has been saved
	alert("Answer Saved");
}