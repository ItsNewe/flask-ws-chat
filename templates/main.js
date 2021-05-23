$(document).ready(function () {
	// start up the SocketIO connection to the server - the namespace 'test' is also included here if necessary
	var socket = io.connect('http://' + document.domain + ':' + location.port);
	// this is a callback that triggers when the "my response" event is emitted by the server.
	socket.on('reponse', function (msg) {
		var a = document.createElement('p');
		a.innerHTML = msg;
		document.getElementById('messages').append(a);
		console.log('rcv');
	});
	//example of triggering an event on click of a form submit button
	$('form#emit').submit(function (event) {
		socket.emit('chat message', {
			data: $('#message').val()
		});
		return false;
	});
});