// Declare use of strict javascript
'use strict';

// Controllers -----------------------------------------------------------------

tribus.controller('SearchListController', ['$scope', 'Search',
    SearchListController]);

function SearchListController($scope, Search){
	$scope.package_results = [];
	$scope.users_results = [];
	
	$scope.hasPackages = function(){
		return $scope.package_results.length > 0;
	},
	
	$scope.hasUsers = function(){
		return $scope.users_results.length > 0;
	},
	
	$scope.noResults = function(){
		return !$scope.hasUsers() && !$scope.hasPackages() 
	},

	$scope.refreshResults = function(){
		if ($scope.top_search.length > 1) {
			$scope.no_results = false
			$scope.package_results = [];
			$scope.users_results = [];
			
			var q = Search.query(
				{
					q: $scope.top_search
				}, function(){
					$scope.package_results = [];
					$scope.users_results = [];
					
					if (q.objects.length > 0) {
						for(var i = 0; i < q.objects.length; i++){
							if (q.objects[i].type === "user"){
								q.objects[i].url = user_url_placer.replace('%PACKAGE%', q.objects[i].username);
								$scope.users_results.push(q.objects[i]);
							}
							else if (q.objects[i].type === "package"){
								q.objects[i].url = packages_url_placer.replace('%PACKAGE%', q.objects[i].autoname);
								$scope.package_results.push(q.objects[i]);
							}
						}
					}
				}
			);
		}
	}
}

// Services --------------------------------------------------------------------

angular.module('Search', ['ngResource']).factory('Search',  function($resource){
    return $resource('/api/0.1/search/', {}, {
        query: {
            method: 'GET',
            isArray: false
        },
    });
});