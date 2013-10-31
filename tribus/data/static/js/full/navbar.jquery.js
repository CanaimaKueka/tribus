$(document).ready(function(){
    $('input.top_search_input').keyup(function () {
        if($(this).val().length > 1){
        	$(this).next().css('display', 'block');
        }

        if($(this).val().length === 0){
        	$(this).next().css('display', 'none');
        }
    });

});