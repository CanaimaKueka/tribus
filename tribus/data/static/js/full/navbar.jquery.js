$(document).ready(function(){
    $('input.top_search_input').keyup(function () {
        if($(this).val().length > 2){
        	$(this).next().css('display', 'block');
        	/*$.ajax({
				url: "/api/0.1/packages/search/", 
				dataType: 'json',
				data: {'q': $(this).val()},
				success: function(data) {
				},
			});*/
        }

        if($(this).val().length === 0){
        	$(this).next().css('display', 'none');
        }
    });

});