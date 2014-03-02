var live = new ReconnectingWebSocket("ws://" + location.host + "/live");

live.onmessage = function(message) {
	var data = JSON.parse(message.data);
	console.log(data);
	$('#live').prepend("<div><strong>@" + data.screen_name + ":</strong> " + data.text + "</div>");
};

live.onclose = function() {
	console.log('live stream closed, reopening');
	this.live = new WebSocket(live.url);
};
