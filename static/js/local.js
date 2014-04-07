var live = new ReconnectingWebSocket("ws://" + location.host + "/live");
var template = Handlebars.compile($('#tweet-template').html());

live.onmessage = function(message) {
	var data = JSON.parse(message.data);
	console.log(data);
	
	$('#teaser').slideUp().animate({opacity: 0}, {queue: false});
	
	// format the date all nice
	var date = new Date(data.created_at);
	data.nice_date = date.format("mmmm d, yyyy 'at' h:MM TT Z");
	
	// link urls in the text for us
	data.nice_text = Autolinker.link(data.text);
	
	// add it
	var content = $(template(data));
	content.prependTo($('#live'));
	content.hide().css('opacity', 0).slideDown().animate({opacity: 1}, {queue: false});
	
	while ($('#live').children().length > 200) {
		$('#live').children().last().remove();
	}
};

live.onclose = function() {
	console.log('live stream closed, reopening');
	this.live = new WebSocket(live.url);
};
