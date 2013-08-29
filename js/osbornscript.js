$(function(){
	$('#submit-btn').on('click', validateForm);
});

	
function validateForm(evt) {
	var x=document.forms["myForm"]["inputName"].value;
	if (x==null || x=="") {
		alert("Name must be filled out");
		evt.preventDefault();
		return;
	}
	sayThanks(evt);
}
	
	function sayThanks (evt){
	var name = document.getElementById('inputName').value;
	var thanks = $('<p>Thanks for your response ' +name+'. We\'ll be in touch</p>');
	$('.modal-wrapper').replaceWith(thanks);
}		
