$(document).ready(function(){

    // Autoresize all textareas with "autosize" class when
    // writing on them. Uses "autogrow" jQuery plugin
    $('textarea.autosize').autogrow({ animate: false, fixMinHeight: false, cloneClass: 'autosize' });

    // Expands all textareas with "expand" class when
    // focusing on them. Uses "autosize" jQuery plugin
    // $('textarea.action_box').keyup(function () {
    //     if($(this).val().length > 0){
    //         $('button.action_button').removeAttr('disabled');
    //     }

    //     if($(this).val().length === 0){
    //         $('button.action_button').attr('disabled', 'disabled');
    //     }
    // });

    $('textarea.action_box').focus(function () {
        if($(this).val().length === 0){
            $(this).animate({ height: "3.5em" }, 200);
        }
    });

    $('textarea.action_box').blur(function(){
        if($(this).val().length === 0){
            $(this).animate({ height: "2em" }, 200);
        }
    });

    $('textarea.action_box').trigger('keyup');

    $(".trib_list").on('reload_dom', function(event){

        $("h4.timeago").timeago();

        $('.trib_item').off('mouseenter');
        $('.trib_item').off('mouseleave');
        $('.trib_body').off('click');

        $('.trib_item').on('mouseenter',
            function(event){
                $(this).children('span.arrow_left').css('border-right-color', 'rgb(255, 255, 255)');
                $(this).children('span.trib_body').css('background-color', 'rgb(255, 255, 255)');
            }
        );

        $('.trib_item').on('mouseleave',
            function(event){
                $(this).children('span.arrow_left').css('border-right-color', 'rgb(248, 248, 241)');
                $(this).children('span.trib_body').css('background-color', 'rgb(248, 248, 241)');
            }
        );

        // $('.trib_body').on('click',
        //     function(event){

        //         if($(this).parent().children('.trib_reply').html().length > 0){
        //             $(this).parent().children('.trib_reply').html('');
        //         }else{

        //             var $injector = angular.injector(['ng']);

        //             $injector.invoke(function($rootScope, $compile){
        //                 link = $compile($('#trib_reply_seed').html())($rootScope);
        //                 $rootScope.$digest();
        //             });

        //             $(this).parent().children('.trib_reply').html(link[0].outerHTML);
        //         }
        //     }
        // );

    });

});