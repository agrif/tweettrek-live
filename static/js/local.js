var live = new ReconnectingWebSocket("ws://" + location.host + "/live");

live.onmessage = function(message) {
	var data = JSON.parse(message.data);
	console.log(data);
	
	$('#teaser').hide();
	
	container = $("<div></div>");
	twttr.widgets.createTweet(data.id, container.get()[0], null, {
		conversation: 'none',
		cards: 'none'
	});
	container.prependTo($('#live'));
	
	while ($('#live').children().length > 200) {
		$('#live').children().last().remove();
	}
};

live.onclose = function() {
	console.log('live stream closed, reopening');
	this.live = new WebSocket(live.url);
};
