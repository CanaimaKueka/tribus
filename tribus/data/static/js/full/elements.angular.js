angular.element(document).ready(function(){

    angular.element(document.querySelector('textarea.action_textarea'))
        .bind('keyup', function(){

        if(this.value.length === 0){
            angular.element(document.querySelector('button.action_button'))
                .attr('disabled', 'disabled');
        }

        if(this.value.length > 0){
            angular.element(document.querySelector('button.action_button'))
                .removeAttr('disabled');
        }

        if(this.value.length >= 190){
            angular.element(this)
                .parent()
                .find('.action_validation')
                .css('color', 'rgb(237, 110, 40)');
        } else {
            angular.element(this)
                .parent()
                .find('.action_validation')
                .css('color', 'rgb(214, 214, 214)');
        }

        angular.element(this)
            .parent()
            .find('.action_validation')
            .text(200-this.value.length);
    });

    angular.element(document.querySelector('textarea.action_textarea'))
        .bind('keypress', function(e){

        if (e.which < 0x20) {
            return;
        }

        if (this.value.length == 200) {
            e.preventDefault();
        } else if (this.value.length > 200) {
            this.value = this.value.substring(0, 200);
        }
    });

    angular.element(document.querySelector('textarea.action_textarea'))
        .bind('focus', function(){
        if(this.value.length === 0){
            angular.element(this).css('height', '3em');
        }
    });

    angular.element(document.querySelector('textarea.action_textarea'))
        .bind('blur', function(){
        if(this.value.length === 0){
            angular.element(this).css('height', '1em');
        }
    });

    angular.element(document.querySelector('.trib_list'))
        .bind('reload_dom', function(event){

        angular.element(document.querySelector('textarea.comment_textarea'))
            .bind('keyup', function(){

            if(this.value.length > 0){
                angular.element(this)
                    .parent().parent().parent()
                    .contents()
                    .find('button.comment_button')
                    .removeAttr('disabled');
            }

            if(this.value.length === 0){
                angular.element(this)
                    .parent().parent().parent()
                    .contents()
                    .find('button.comment_button')
                    .attr('disabled', 'disabled');
            }
        });

        angular.element(document.querySelector('textarea.comment_textarea'))
            .bind('focus', function(){
            if(this.value.length === 0){
                angular.element(this).css('height', '2em');
            }
        });

        angular.element(document.querySelector('textarea.comment_textarea'))
            .bind('blur', function(){
            if(this.value.length === 0){
                angular.element(this).css('height', '1em');
            }
        });
    });
});

$(document).ready(function(){
    $('input.top_search_input').keyup(function(){
        if($(this).val().length > 1){
            $(this).next().css('display', 'block');
        }

        if($(this).val().length === 0){
            $(this).next().css('display', 'none');
        }
    });

    $('input.top_search_input').blur(function(){
        $(this).next().css('display', 'none');
    });
});