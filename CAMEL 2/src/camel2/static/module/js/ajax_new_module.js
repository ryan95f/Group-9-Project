$(document).ready( function(){
	$("#form_submit").click( function(){
        var send = true;
        var error = "";
        $('#id_title').css('background-color', "#FFF");
        $('#id_code').css('background-color', "#FFF");
		
        event.preventDefault(); // prevent redirect

        // error handling
        if((!($('#id_title').val().length > 0)) || (!(new RegExp(/\w/).test($('#id_title').val())))){
            $('#id_title').css('background-color', "#ff4d4d");
            send = false;
            error += "<p>Please ensure a valid string in entered</p>";
        }

        if((!($('#id_code').val().length > 0)) || (!(new RegExp(/^\M{1}\A{1}\d{4}$/).test($('#id_code').val())))){
            $('#id_code').css('background-color', "#ff4d4d");
            send = false;
            error += "<p>Please enter valid module code. E.g. MA0000</p>";
        }

        if(send){ // if flag to send is true
            new_module_request();
        }else{
            $('#dash_error').html(error);
        }
        return;

	});
});

function new_module_request(){
	$.ajax({
        url : "/module/NewModule/", //endpoint
        type : "POST", // http method
        data : { 
        	code : $('#id_code').val(),
        	year : $('#id_year option:selected').text(),
        	title : $('#id_title').val(),
        }, // data sent with the post request
        
        //get the csrf_token
        beforeSend: function(xhr, settings) {
        	//console.log("Before Send");
        	$.ajaxSettings.beforeSend(xhr, settings);
    	},

        // handle a successful response
        success : function(json) {
        	$('#id_title').val("");
            $('#id_code').val("");
            console.log(json); // log the returned json to the console
            // console.log("success");

        },

        // handle a non-successful response
        error : function(xhr,errmsg,err) {
            console.log(xhr);
            alert("Module code already exists");
        }
    });
}

function show_new_module(json){
	// adding module to table
	$('#module_table').append(
		"<tr>" + 
			"<th>" + json.module_code + "</th>" + 
			"<th>" + json.module_year + "</th>" + 
			"<th>" + json.module_title + "</th>" + 
            "<th><button>Edit " + json.module_code + "</button></th>" + 
		"</tr>"
		);
}