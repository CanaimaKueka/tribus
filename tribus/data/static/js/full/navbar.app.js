// Declare use of strict javascript
'use strict';

// Controllers -----------------------------------------------------------------

tribus.controller('SearchListController', ['$scope', 'Search',
    SearchListController]);

function SearchListController($scope, Search){

	$scope.refreshResults = function(){
		if ($scope.top_search.length > 0) {
			$scope.no_results = false
			$scope.package_results = [];
			$scope.user_results = [];
			
			var q = Search.query(
				{
					q: $scope.top_search
				}, function(){
					if (q.objects.length === 0) {
						$scope.no_results = true
					}else{
						for(var i = 0; i < q.objects.length; i++){
							
							if (q.objects[i].type === "user"){
								q.objects[i].url = user_url_placer.replace('%PACKAGE%', q.objects[i].dest);
								$scope.package_results.push(q.objects[i]);
							}
							else if (q.objects[i].type === "package"){
								q.objects[i].url = packages_url_placer.replace('%PACKAGE%', q.objects[i].dest);
								$scope.user_results.push(q.objects[i]);
							}
						}
						
						//$scope.results = q.objects;
					}
				}
			);

		}
	}
}

// Services --------------------------------------------------------------------

angular.module('Search', ['ngResource'])
    .factory('Search',  function($resource){
        return $resource('/api/0.1/search/', {}, {
            query: {
                method: 'GET',
                isArray: false
            },
        });
    });
    
