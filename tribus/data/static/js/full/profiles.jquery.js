$(document).ready(function(){

    //$("id_email").name.defaultValue = user_email;
    document.Form.email.defaultValue= user_email;
    
    // Autoresize all textareas with "autosize" class when
    // writing on them. Uses "autogrow" jQuery plugin
    $('textarea.autosize').autogrow({ animate: false,
                                      fixMinHeight: false,
                                      cloneClass: 'autosize' });

    $('textarea.action_textarea').keyup(function () {
        if($(this).val().length > 0){
            $('button.action_button').removeAttr('disabled');
        }

        if($(this).val().length === 0){
            $('button.action_button').attr('disabled', 'disabled');
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