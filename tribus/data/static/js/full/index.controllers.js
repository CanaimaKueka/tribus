function TribListCtrl($scope, TribsFactory) {
	$scope.tribs = TribsFactory.query();
	console.log($scope.newtrib);

	$scope.createNewTrib = function(){
		TribsFactory.create($scope.newtrib);
		console.log($scope.newtrib);
	};
}
