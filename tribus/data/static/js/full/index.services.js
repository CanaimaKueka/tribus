angular.module('index.services', ['ngResource']).
	factory('TribsFactory', function($resource){
  		return $resource('/api/0.1/trib/', {}, {
    		query: { method: 'GET', params: { author_id: user_id }},
    		create: { method: 'POST' }
  		});
	}); 