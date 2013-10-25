// Declare use of strict javascript
'use strict';


// Application -----------------------------------------------------------------

//var tribus = angular.module('tribus', []);


// Events ----------------------------------------------------------------------

/*navbar.run(function($rootScope){
    $rootScope.$on('addNewTribsRefreshEmit', function(event, args){
        $rootScope.$broadcast('addNewTribsRefreshReceive', args);
    });
});*/


// Controllers -----------------------------------------------------------------
/*
celulares.controller('PhoneListCtrl', function PhoneListCtrl($scope, $http) {
               $http.get('phones/phones.json').success(function(data){
                       $scope.telefonos*/ 

tribus.controller('SearchListController', ['$scope', 'Packages',
    SearchListController]);

function SearchListController($scope){
	
	$scope.results = [];

	
	/*
	 $scope.autocompletar = function ($scope, packages){
		var paquetes = packages.query();
		console.log(paquetes);
		        	$.ajax({
					url: "/api/0.1/packages/search/", 
					dataType: 'json',
					data: {'q': $(this).val()},
					success: function(data) {
						console.log(data);
						
			};
	$scope.prueba = function(){
		alert("funciona =D ");
	};*/

}




// Services --------------------------------------------------------------------

angular.module('Packages', ['ngResource'])
    .factory('Packages',  function($resource){
        return $resource('/api/0.1/packages/search/?=:package_name',
            { package_name: '@package_name' }, {
            query: {
                method: 'GET',
                isArray: false
            },
        });
    });
    
