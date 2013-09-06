$(document).ready(function() {

	$('#slide_1').css('height', function() {
		return $(window).height();
	});

	$('#slide_1').css('margin-left', '200px');

	$('#flat_earth').css('top', function() {
		return ($(window).height()-$('#flat_earth').height())/2.5;
	});

	// $('#slide_1a').css('height', function() {
	// 	return $(window).height();
	// });
	// $('#slide_1b').css('height', function() {
	// 	return $(window).height();
	// });
	
	$('#slide_2').css('height', function() {
		return $(window).height();
	});
	
	$('#slide_2').css('width', function() {
		return $(window).width()*0.5;
	});

	
	$('#slide_3').css('width', function() {
		return $(window).width()*0.5;
	});

	$('#slide_3').css('height', function() {
		return $(window).height();
	});
	$('#slide_4').css('height', function() {
		return $(window).height();
	});
	$('#slide_5').css('height', function() {
		return $(window).height();
	});
	$('#slide_6').css('height', function() {
		return $(window).height();
	});
	$('.scrollblock').css('width', function() {
		return $(window).width()-100;
	});
	
	// initialize the plugin, pass in the class selector for the sections of content (blocks)
	var scrollorama = $.scrollorama({ blocks:'.scrollblock' });


	// animate the parallaxing
	scrollorama
		.animate('#slide_0',{ delay: 0, duration: 1000, property:'opacity', start:1, end:0 })
		.animate('#slide_1',{ delay: 0, duration: 3000, property:'zoom', start:1, end:5, pin: true })
		.animate('#slide_1',{ delay: 0, duration: 3000, property:'left', end:$(window).width()-200, pin: true})
		.animate('#slide_1a',{ delay: 3000, duration: 2000, property:'top', end:$(window).height()*(-1), pin: true})
		.animate('#slide_1b',{ delay: 3000, duration: 3000, property:'top', end:$(window).height()*(-1), pin: true})
		.animate('#slide_2',{ delay: 0, duration: 1000, property:'top', start:-500, end:500})
		.animate('#slide_2',{ delay: 0, duration: 1000, property:'left', start:0, end:$(window).width()*0.5})
		.animate('#slide_3',{ delay: 0, duration: 1000, property:'top', start:200, end:600})
		.animate('#slide_3',{ delay: 0, duration: 1000, property:'left', start:$(window).width(), end:$(window).width()*0.5})		.animate('#slide_3',{ delay: 0, duration: 1000, property:'top', start:200, end:600})
		.animate('#slide_4',{ delay: 300, duration: 2000, property:'top', start:300, end:600})
		.animate('#slide_5',{ delay: 500, duration: 2000, property:'top', start:-200, end:700})
		.animate('#slide_6',{ delay: 700, duration: 2000, property:'top', start:-600, end:800})
		// .animate('#slide_4',{ delay: 0, duration: 1000, property:'left', start:$(window).width(), end:$(window).width()*0.5})
		// .animate('#slide_4',{ delay: 2000, duration: 1000, property:'top', start:0, end:1500})

});