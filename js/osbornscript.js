$(function(){
	$('#submit-btn').on('click', validateForm);
});

	
function validateForm(evt) {
	var x=document.forms["myForm"]["inputName"].value;
	if (x==null || x=="") {
		alert("Name and Email must be filled out");
		evt.preventDefault();
		return;
	}
	sayThanks(evt);
}
	
	function sayThanks (evt){
	var name = document.getElementById('inputName').value;
	//alert("Thanks for your response ' +name+'. We'll be in touch")
	var thanks = $('<p style="text-align:center;">Thanks for your response ' +name+'. We\'ll be in touch</p>');
	$('.modal-wrapper').replaceWith(thanks);
}		
