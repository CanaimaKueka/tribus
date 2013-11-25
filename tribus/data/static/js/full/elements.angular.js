angular.element(document).ready(function(){

    var topSearchInput, tribButton, tribCharCounter, commentButton,
        actionTextarea, tribList;

    actionTextarea = angular.element(
        document.querySelector('textarea.action_textarea'));
    tribList = angular.element(
        document.querySelector('div.trib_list'));
    topSearchInput = angular.element(
        document.querySelector('input.top_search_input'));

    topSearchInput.bind('keyup', function(){

        if(this.value.length > 1){
            angular.element(this).next()
                .css('display', 'block');
        }

        if(this.value.length === 0){
            angular.element(this).next()
                .css('display', 'none');
        }
    });

    topSearchInput.bind('blur', function(){
        angular.element(this).next()
            .css('display', 'none');
    });

    actionTextarea.bind('keyup', function(){

        tribCharCounter = angular.element(this.parentNode.children[1]);
        tribButton = angular.element(this.parentNode
                                        .parentNode
                                        .parentNode
                                        .children[2]
                                        .children[0]);
        this.style.height = '30px';
        this.style.height = this.scrollHeight + 12 + 'px';

        if(this.value.length === 0){
            angular.element(this).css('height', '1.5em');
            tribButton.attr('disabled', 'disabled');
        }

        if(this.value.length > 0){
            tribButton.removeAttr('disabled');
        }

        if(this.value.length >= 190){
            tribCharCounter.css('color', 'rgb(237, 110, 40)');
        } else {
            tribCharCounter.css('color', 'rgb(214, 214, 214)');
        }

        tribCharCounter.text(200-this.value.length);
    });

    actionTextarea.bind('keypress', function(e){

        if (e.which < 0x20) {
            return;
        }

        if(this.value.length == 200){
            e.preventDefault();
        } else if (this.value.length > 200) {
            this.value = this.value.substring(0, 200);
        }
    });

    actionTextarea.bind('focus', function(){
        if(this.value.length === 0){
            angular.element(this).css('height', '3em');
        }
    });

    actionTextarea.bind('blur', function(){
        if(this.value.length === 0){
            angular.element(this).css('height', '1.5em');
        }
    });

    tribList.bind('reload_dom', function(event){

        commentTextarea = angular.element(
            document.querySelector('textarea.comment_textarea'));

        commentTextarea.bind('keyup', function(){

            commentButton = angular.element(this.parentNode
                                                .parentNode
                                                .parentNode
                                                .children[2]
                                                .children[0]);
            if(this.value.length > 0){
                commentButton.removeAttr('disabled');
            }

            if(this.value.length === 0){
                commentButton.attr('disabled', 'disabled');
            }
        });

        commentTextarea.bind('focus', function(){
            if(this.value.length === 0){
                angular.element(this).css('height', '2em');
            }
        });

        commentTextarea.bind('blur', function(){
            if(this.value.length === 0){
                angular.element(this).css('height', '1.5em');
            }
        });
    });
});