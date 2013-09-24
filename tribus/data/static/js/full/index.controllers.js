function TribListCtrl($scope, TribsFactory) {
	$scope.tribs = TribsFactory.query();

	$scope.createNewTrib = function(){
		TribsFactory.create($scope.newtrib);
		console.log($scope.newtrib);
	};
}
