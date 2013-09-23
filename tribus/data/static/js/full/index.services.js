angular.module('index.services', ['ngResource']).
	factory('TribsFactory', function($resource){
  		return $resource('/api/0.1/trib/?author_id='+user_id, {}, {
    		query: { method: 'GET' }
  		});
	}); 