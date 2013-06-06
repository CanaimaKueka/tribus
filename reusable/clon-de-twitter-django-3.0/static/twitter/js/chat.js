$(document).ready(function(){
	actualiza = function(data){
		conectados = data.conectados;
		mensajes = data.mensajes;

		html_len = $('<a class="btn btn-mini btn-info" id="showcon"></a>');
		html_len.text('Conectados(' + conectados.length + ')');
		$('<br>').appendTo($(html_len));

		html_con = $('<p class="conectados">');
		for(i = 0; i < conectados.length; i++)
		{
			u = conectados[i];
			html_u = $('<a class="btn btn-mini btn-success" href="/twitter/profile/' + u + '/">');
			html_u.text('@' + u);
			html_con.append(html_u)
		};

		html_mensajes = $('<div>');
		for(i = 0; i < mensajes.length; i++)
		{
			u = mensajes[i][0];
			c = mensajes[i][1];
			p = $('<span>');
			a = $('<a href="/profile/' + u + '/">');
			a.text('@' + u + ': ');
			a.appendTo(p);
			p.append(c);
			p.append('<br>')
			p.appendTo(html_mensajes);
		};

		e = $('.chat');
		e.html('');
		e.append(html_len);
		e.append(html_con);
		e.append(html_mensajes);

		}
	ejecutando = false;
	setInterval(function(){
		if (!ejecutando)
		{
			ejecutando = true
			$.ajax({
				url: '/twitter/chat/',
				dataType: 'json',
				success: actualiza,
				});
			ejecutando = false;;
		}
	}, 250);
	$(".chatform").submit(function(){
		if ($('#inputderecho').val() != ''){
			input = '#inputderecho';
		}else{
			input = '#inputmodal';
		}
		ejecutando = true;
		$.ajax({
			type: 'POST',
			url: '/twitter/chat/',
			data: {accion: 'send', mensaje: $(input).val(), csrfmiddlewaretoken : csrf},
			dataType: 'json',
			success: actualiza
		});
		ejecutando = false;
		$('.chatform input').val('')
		return false;
		});
	$('.conectados').css('display:none')
	});
