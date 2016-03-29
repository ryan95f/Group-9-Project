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
	$.ajax({
        url : "/homework/save-single/" + node + "/", //endpoint
        type : "POST", // http method
        data : { 
        	user :$('#user').val(),
        	singlechoice : $('input:checked').val(),
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