
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
				
				console.log(data);

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

			console.log(data);


			if(data == "True"){

				window.location.replace("/");

			}
			else{

				console.log("Bad Password");

			}



		}

	});


});


$(document).on('click','.devicecheckbox',function(){

	var clicked = $(this).attr('id');

	//console.log(clicked);

	console.log($(this).is(':checked'));

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