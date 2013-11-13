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
	};
	
	$scope.hasUsers = function(){
		return $scope.users_results.length > 0;
	};
	
	$scope.noResults = function(){
		return !$scope.hasUsers() && !$scope.hasPackages();
	};

	$scope.refreshResults = function(){
		if (($scope.top_search != undefined) && ($scope.top_search.length > 1)) {
			$scope.no_results = false;
			$scope.package_results = [];
			$scope.users_results = [];
			var q = Search.query(
				{
					q: $scope.top_search
				}, function(){
					$scope.package_results = [];
					$scope.users_results = [];
					if (q.objects[0].packages.length > 0) {
						var packages = q.objects[0].packages;
						for(var i = 0; i < packages.length; i++){
							packages[i].url = packages_url_placer.replace('%PACKAGE%', packages[i].name);
							$scope.package_results.push(packages[i]);
						}
					}
					
					if (q.objects[0].users.length > 0) {
						var users = q.objects[0].users;
						for(var i = 0; i < users.length; i++){
							users[i].url = user_url_placer.replace('%PACKAGE%', users[i].username);
							$scope.users_results.push(users[i]);
						}
					}
					//console.log($scope.package_results);
					//console.log($scope.users_results);
				}
			);
		}
	};
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