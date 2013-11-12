$(document).ready(function(){

    // $('.action_avatar').css('background-image', 'url("'+user_gravatar+'")');

    // Autoresize all textareas with "autosize" class when
    // writing on them. Uses "autogrow" jQuery plugin
    $('textarea.autosize').autogrow({ animate: false,
                                      fixMinHeight: false,
                                      cloneClass: 'autosize' });

    $('textarea.action_textarea').keyup(function () {

        if(this.value.length === 0){
            $('button.action_button').attr('disabled', 'disabled');
        }
        
        if(this.value.length > 0){
            $('button.action_button').removeAttr('disabled');
        }
        
        if(this.value.length >= 190){
            $(this).siblings('.action_validation').css('color', '#ED6E28');
        } else {
            $(this).siblings('.action_validation').css('color', 'rgb(133, 133, 133)');
        }
        
        $(this).siblings('.action_validation').text(200-this.value.length);

    });

    $('textarea.action_textarea').keypress(function(e) {
        if (e.which < 0x20) {
            return;
        }

        if (this.value.length == 200) {
            e.preventDefault();
        } else if (this.value.length > 200) {
            this.value = this.value.substring(0, 200);
        }
    });

    $('textarea.action_textarea').focus(function () {
        if($(this).val().length === 0){
            $(this).animate({ height: "3em" }, 200);
        }
    });

    $('textarea.action_textarea').blur(function(){
        if($(this).val().length === 0){
            $(this).animate({ height: "1em" }, 200);
        }
    });

    $(".trib_list").on('reload_dom', function(event){

        $("h4.timeago").timeago();

        $('textarea.comment_textarea').keyup(function () {
            if($(this).val().length > 0){
                $(this).parents('.comment_box')
                    .contents()
                    .find('button.comment_button')
                    .removeAttr('disabled');
            }

            if($(this).val().length === 0){
                $(this).parents('.comment_box')
                    .contents()
                    .find('button.comment_button')
                    .attr('disabled', 'disabled');
            }
        });

        $('textarea.comment_textarea').focus(function () {
            if($(this).val().length === 0){
                $(this).animate({ height: "2em" }, 200);
            }
        });

        $('textarea.comment_textarea').blur(function(){
            if($(this).val().length === 0){
                $(this).animate({ height: "1em" }, 200);
            }
        });

    });

});