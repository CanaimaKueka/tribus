// Declare use of strict javascript
'use strict';

// Elements  -----------------------------------------------------------------

angular.element(document).ready(function(){
	
	var switch_list = document.querySelectorAll('input[type=checkbox].ace.ace-switch');
	
	for(var i = 0; i < switch_list.length; i++){
		console.log(angular.element(switch_list[i]).next());
		angular.element(switch_list[i]).next().on('click', function(){
			console.log(switch_list[i]);
			console.log(angular.element(switch_list[i]).attr('checked'));
			
			if(angular.element(switch_list[i]).attr('checked') == 'checked'){
				angular.element(switch_list[i]).attr('checked', '');
			} else {				
				angular.element(switch_list[i]).attr('checked', 'checked');
			}
		});
	}
	
});
