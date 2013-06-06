$(document).ready(function(){
	$('#textarea').keyup(function(){
		n = (140 - $('#textarea').val().length)
		$('#count').html(n)
		if(n > 9)
		{
			$('#count').attr({'class' : 'label label-info'});
		}else{
			$('#count').attr({'class' : 'label label-important'});
		};
	});
});