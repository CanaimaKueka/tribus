$(document).ready(function(){

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