function answer_validation(){
	$('#answer-text').css({'background-color':'#fff'});
	if($('#answer-text').val().length > 0){
		return true;
	}
	$('#answer-text').css({'background-color':'#ffd633'});
	return false;
}