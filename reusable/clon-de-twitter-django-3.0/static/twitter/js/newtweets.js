//$('#nuevostweets').show(500);
$(document).ready(function(){
	$('#nuevostweets a').click(function(){
		$('.tweetoculto').show(500);
		$('.tweetoculto').removeClass('tweetoculto');
		$('#nuevostweets').css('display', 'none');
		$('title').text('Twitter');
		return false;
	});
	setInterval(function(){
		$.ajax({
			url: '/twitter/newtweets/',
			data: {'id' : tweet_id, 'busqueda' : busqueda},
			dataType: 'json',
			success: newtweet,
		})
	}, 5000);
});
newtweet = function(data){
	if(data.length)
	{
		tweet_id = data[0].tpk;
	}
	for(i = 0; i < data.length; i++)
	{
		t = data[i];

		article = $('<article>');
		article.addClass('tweetoculto')
		header = $('<header>');
		h3 = $('<h3>');
		a = $('<a>').text('@' + t.user).attr('href', '/twitter/profile/' + t.user + '/');
		h3.text(t.name + ' (' );
		h3.append(a);
		h3.append(')');
		h3.appendTo(header);
		header.appendTo(article);

		article.append(t.contenido)

		footer = $('<footer>');
		p = $('<p>');
		if(t.retweet){
			r = $('<strong>');
			r.append('Retwitteado por ');
			r.append($('<a>').attr('href','/profile/' + t.retweet + '/').text('@' + t.retweet));
			r.append('<br>');
			r.appendTo(p)
		};
		p.append($('<strong>').text('Publicado: ' + t.fecha + ' '));
		if(t.respuesta){
			p.append('<a href="/twitter/conversacion/' + pk + '/">Ver conversacion completa</a><br>');
		};
		p.append('<a href="/twitter/retweet/' + t.pk + '/"><i class="icon-retweet"></i>Retweet</a>');
		p.append('<a href="/twitter/responder/' + t.pk + '/"><i class="icon-share-alt"></i>Responder</a>');
		if(t.user == user)
		{
			p.append('<a href="/twitter/borrar/' + t.pk + '/"><i class="icon-trash"></i>Borrar</a>')
		};
		p.appendTo(footer);
		footer.appendTo(article);

		article.prependTo($('#tweets'));
	}
	if(data.length){
		l = $('.tweetoculto').length;
		$('#nuevostweets a').text(l + ' nuevos tweets');
		$('#nuevostweets').show(500);
		$('title').text('Twitter (' + l + ')');
	};
};