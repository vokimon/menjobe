$(document).ready(function()
{
	$('.carousel').carousel({
		interval: 10000
		});
	$("[data-toggle=tooltip]").tooltip();

	//Handles menu drop down`enter code here`
	$('.dropdown-menu').find('form').click(function (e) {
		e.stopPropagation();
	});

});

function notImplemented() {
	$('#notImplemented').modal('show');
}

