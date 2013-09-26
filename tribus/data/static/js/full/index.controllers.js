function TribList($scope, $timeout, Tribs) {

    var trib_offset = 0;
    var trib_add = 5;
    var trib_limit = 5;
    var trib_orderby = '-trib_pub_date';
    var controller_busy = false;

    $scope.controller_busy = controller_busy;
    $scope.trib_limit = trib_limit;
    $scope.trib_offset = trib_offset;
    $scope.trib_orderby = trib_orderby;
    $scope.newtrib = {
        author_id: user_id,
        author_username: user_username,
        author_first_name: user_first_name,
        author_last_name: user_last_name,
        retribs: []
    };

    $scope.tribs = [];

    $scope.addMoreItems = function(){

        if ($scope.controller_busy) return;

        $scope.controller_busy = true;

        var next_tribs = Tribs.query({
            author_id: user_id,
            order_by: $scope.trib_orderby,
            limit: $scope.trib_limit,
            offset: $scope.trib_offset
        }, function(){

            for (var i = 0; i < next_tribs.length; i++) {
                $scope.tribs.push(next_tribs[i]);
            }

            if($scope.tribs.length >= $scope.trib_limit){
                $scope.trib_offset = $scope.trib_offset + trib_add;
            }
            setTimeout(function(){$scope.controller_busy = false;}, 5000);
            
        });
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