function TribListCtrl($scope, TribsFactory) {
	$scope.tribs = TribsFactory.query();
}
