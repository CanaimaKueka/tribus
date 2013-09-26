$(document).ready(function(){

    var opts = {
      lines: 7, // The number of lines to draw
      length: 6, // The length of each line
      width: 11, // The line thickness
      radius: 30, // The radius of the inner circle
      corners: 1, // Corner roundness (0..1)
      rotate: 0, // The rotation offset
      direction: 1, // 1: clockwise, -1: counterclockwise
      color: '#000', // #rgb or #rrggbb or array of colors
      speed: 1, // Rounds per second
      trail: 60, // Afterglow percentage
      shadow: true, // Whether to render a shadow
      hwaccel: false, // Whether to use hardware acceleration
      className: 'spinner', // The CSS class to assign to the spinner
      zIndex: 2e9, // The z-index (defaults to 2000000000)
      top: '0', // Top position relative to parent in px
      left: '0', // Left position relative to parent in px
      position: 'relative'
    };

    // var target = document.getElementById('trib_list_spinner');
    // var spinner = new Spinner(opts).spin(target);

    $('#trib_list_spinner').after(new Spinner(opts).spin().el);

	// Autoresize all textareas with "autosize" class when
	// writing on them. Uses "autogrow" jQuery plugin
    $('textarea.autosize').autogrow({ animate: false, fixMinHeight: false, cloneClass: 'autosize' });

    // Expands all textareas with "expand" class when
	// focusing on them. Uses "autosize" jQuery plugin
    $('textarea.action_box').keyup(function () {
    	if($(this).val().length > 0){
    		$('button.action_button').removeAttr('disabled');
    	}

    	if($(this).val().length == 0){
    		$('button.action_button').attr('disabled', 'disabled');
    	}

	});

    $('textarea.action_box').focus(function () {
    	if($(this).val().length == 0){
    		$(this).animate({ height: "3.5em" }, 200);
    	}
	});

    $('textarea.action_box').blur(function(){
    	if($(this).val().length == 0){
    		$(this).animate({ height: "2em" }, 200);
    	}
	});

	$('textarea.action_box').trigger('keyup');
});