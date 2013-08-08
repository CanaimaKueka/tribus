$(document).ready(function() {
	
	// initialize the plugin, pass in the class selector for the sections of content (blocks)
	var scrollorama = $.scrollorama({ blocks:'.scrollblock' });


	// animate the parallaxing
	scrollorama
		.animate('#slide_1',{ delay: 0, duration: 3000, property:'zoom', start:1, end:5, pin: true })
		.animate('#slide_1',{ delay: 0, duration: 3000, property:'left', end:$(window).width()-200})
		.animate('#slide_1',{ delay: 0, duration: 3000, property:'height', start:$(window).height(), end:$(window).height()})
		// .animate('#slide_2',{ delay: 0, duration: 1200, property:'top', start:0, end:100 })
		// .animate('#slide_2',{ delay: 0, duration: 3000, property:'height', start:$(window).height(), end:$(window).height()})
		// .animate('#slide_3',{ delay: 0, duration: 1200, property:'top', start:0, end:100 })
		// .animate('#slide_3',{ delay: 0, duration: 3000, property:'height', start:$(window).height(), end:$(window).height()})
	
});