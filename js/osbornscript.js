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
	var thanks = $('<p style="text-align:center;font-size:1.2em;">Thanks '+  name+' . Check your email for details.</p>');
	$('.modal-wrapper').replaceWith(thanks);
}		
