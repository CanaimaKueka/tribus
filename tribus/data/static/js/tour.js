$(document).ready(function() {

	$('#slide_1').css('height', function() {
		return $(window).height();
	});

	$('#flat_earth').css('top', function() {
		return ($(window).height()-$('#flat_earth').height())/2.5;
	});

	// $('#slide_1a').css('height', function() {
	// 	return $(window).height();
	// });
	// $('#slide_1b').css('height', function() {
	// 	return $(window).height();
	// });
	
	// $('#slide_2').css('height', function() {
	// 	return $(window).height();
	// });
	$('#slide_3').css('height', function() {
		return $(window).height();
	});
	$('.scrollblock').css('width', function() {
		return $(window).width()-100;
	});
	
	// initialize the plugin, pass in the class selector for the sections of content (blocks)
	var scrollorama = $.scrollorama({ blocks:'.scrollblock' });


	// animate the parallaxing
	scrollorama
		.animate('#slide_1',{ delay: 0, duration: 3000, property:'zoom', start:1, end:5, pin: true })
		.animate('#slide_1',{ delay: 0, duration: 3000, property:'left', end:$(window).width()-200, pin: true})
		.animate('#slide_1a',{ delay: 3000, duration: 1000, property:'top', end:$(window).height()*(-1), pin: true})
		.animate('#slide_1b',{ delay: 3000, duration: 1000, property:'top', end:$(window).height()*(-0.9), pin: true})
		.animate('#slide_2',{ delay: 0, duration: 6000, property:'left', start:0, end:-1000})
		.animate('#slide_2',{ delay: 0, duration: 3000, property:'top', start:-500, end:1500})
		.animate('#slide_2',{ delay: 0, duration: 6000, property:'zoom', start:1, end:3})
		.animate('#slide_3',{ delay: 6000, duration: 3000, property:'top', end:$(window).height()*(-1)})

});