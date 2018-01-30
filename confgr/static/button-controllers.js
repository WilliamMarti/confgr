
var selected = [];


$(document).on('click','#netboxlinkbutton',function(){

	var netboxurl = $('#netboxurl').val();
	var netboxapikey = $('#netboxapikey').val();

	$('#netboxlinkbutton').text("Connecting...");

	$.ajax({

		type: "POST",
		url: '/admin',
		data: {"netboxurl":netboxurl, "netboxapikey":netboxapikey},
		timeout: 0,

		success: function(data) {

			if (status != "Failed"){

				$("#netboxconnectionstatus").html("Connected");
				$("#netboxconnectionstatus").css('color', 'green');
				
			}
			else {

				$("#netboxconnectionstatus").html("Connection Failed");
				$("#netboxconnectionstatus").css('color', 'red');

			}

			$('#netboxlinkbutton').text("Connect");


		}

	});


});



$(document).on('click','#loginbutton',function(){

	var username = $('#username').val();
	var password = $('#password').val();


	$.ajax({

		type: "POST",
		url: '/login',
		data: {"username":username, "password":password},
		timeout: 0,

		success: function(data) {

			if(data == "True"){

				window.location.replace("/");

			}
			else{

				$('#login-result').text("Incorrect Login Information");

			}

		}

	});


});



$(document).on('click','#profilesubmit',function(){

	var first = $('#firstname').val();
	var last = $('#lastname').val();
	var email = $('#email').val();
	var username = $('#username').text().trim();

	$.ajax({

		type: "POST",
		url: '/profileedit',
		data: {"first":first, "last":last, "email":email, "username": username},
		timeout: 0,

		success: function(data) {



		},
		complete: function(data) {

			window.location.replace("/profile/" + username);

		} 

	});



});


$(document).on('click','.devicecheckbox',function(){

	var clicked = $(this).attr('id');


	if ($(this).is(':checked') == true){

		var newrow = "<div id='selected" + clicked + "' class='row'>\
						<div class='col-md-12'>\
							" + clicked + "\
						</div>\
					</div>";

		$("#selecteddevices").append(newrow);

		selected.push(clicked);

	}
	else {

		$("#selected" + clicked).remove();
		selected.pop(clicked);

	}



});


$(document).on('click','#createuser',function(){

	var username = $('#username').val();
	var first = $('#firstname').val();
	var last = $('#lastname').val();
	var email = $('#email').val();

	$.ajax({

		type: "POST",
		url: '/createuser',
		data: {"username": username, "password":$('#password').val(), "first":first, "last":last, "email":email},
		timeout: 0,

		complete: function(data) {

			window.location.replace("/admin");

		} 

	});



});

$(document).on('click','#deleteuserconfirm',function(){

	var username = $('#user').text().trim();

	$.ajax({

		type: "POST",
		url: '/deleteuser',
		data: {"username": username},
		timeout: 0,

		complete: function(data) {

			window.location.replace("/admin");

		} 

	});

});


$(document).on('click','#deleteuser',function(){

	$('#deleteusermodal').modal("toggle");

});


$(document).on('click','#deleteusercancel',function(){

	$('#deleteusermodal').modal("toggle");


});


$(document).on('click','#runbutton',function(){


	var device = "10.0.0.2"
	var deviceusername = $('#deviceusername').val().trim();
	var devicepassword = $('#devicepassword').val().trim();
	var commandstorun = $('#commandstorun').val().trim();

	$.ajax({

		type: "POST",
		url: '/runcommands',
		data: {"device": device,"deviceusername": deviceusername, "devicepassword": devicepassword, "commandstorun": commandstorun},
		timeout: 0,

		complete: function(data) {

			console.log(data['responseText']);


		}

	});

});