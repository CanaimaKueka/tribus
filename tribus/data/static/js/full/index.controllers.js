function TribList($scope, $timeout, Tribs) {
    $scope.tribs = Tribs.query();
    $scope.newtrib = {
        author_id: user_id,
        author_username: user_username,
        author_first_name: user_first_name,
        author_last_name: user_last_name,
        retribs: []
    };

    $scope.createNewTrib = function(){
        $scope.newtrib.trib_pub_date = new Date();
        Tribs.create($scope.newtrib);
    };

    // (function tick() {
    //     $scope.tribs = Tribs.query(function(){
    //         $timeout(tick, 10000);
    //     });
    // })();
}