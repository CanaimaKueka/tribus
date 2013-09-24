function TribList($scope, Tribs) {
    $scope.tribs = Tribs.query();
    $scope.newtrib = {
        author_id: user_id,
        author_username: user_username,
        author_first_name: user_first_name,
        author_last_name: user_last_name,
        trib_pub_date: new Date(),
        retribs: []
    };

    $scope.createNewTrib = function(){
        Tribs.create($scope.newtrib);
        $scope.tribs = Tribs.query();
    };
}