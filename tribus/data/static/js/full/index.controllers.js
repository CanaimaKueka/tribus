function TribList($scope, $timeout, Tribs, Timeline) {

    $scope.controller_busy = controller_busy;
    $scope.trib_limit_to = trib_limit_to;
    $scope.trib_limit = trib_limit;
    $scope.trib_offset = trib_offset;
    $scope.trib_orderby = trib_orderby;
    $scope.tribs = [];
    $scope.temp_new_tribs = [];

    $scope.createNewTrib = function(){

        var newtrib = {
            author_id: user_id,
            author_username: user_username,
            author_first_name: user_first_name,
            author_last_name: user_last_name,
            trib_content: $('textarea.action_box').val(),
            trib_pub_date: new Date(),
            retribs: []
        };

        Tribs.save(newtrib, function(){
            $scope.temp_new_tribs.unshift(newtrib);
            $('textarea.action_box').val('')
        });
    };

    $scope.addOldTribs = function(){

        if ($scope.tribs_end) return;
        
        if ($scope.controller_busy) return;

        $scope.controller_busy = true;

        var old_tribs = Timeline.query({
            order_by: $scope.trib_orderby,
            limit: $scope.trib_limit,
            offset: $scope.trib_offset
        }, function(){

            for(var i = 0; i < old_tribs.length; i++){
                var old_id_appears = false;

                for(var j = 0; j < $scope.tribs.length; j++){
                    if(old_tribs[i].id == $scope.tribs[j].id) old_id_appears = true;
                }

                if(!old_id_appears) $scope.tribs.push(old_tribs[i]);
            }

            if($scope.tribs.length > $scope.trib_offset){
                $scope.trib_offset = $scope.trib_offset + trib_add;
            }

            if($scope.tribs.length > $scope.trib_limit_to){
                $scope.trib_limit_to = $scope.tribs.length;
            }

            if(old_tribs.length === 0){
                $scope.tribs_end = true;
            }

            $scope.controller_busy = false;
            
        });
    };

    function addNewTribs($scope, trib_offset) {

        $scope.new_tribs_offset = trib_offset;
        $scope.temp_new_tribs = [];

        var fresh_tribs = Timeline.query({
            order_by: $scope.trib_orderby,
            limit: $scope.trib_limit,
            offset: $scope.new_tribs_offset
        }, function(){
            for(var i = 0; i < fresh_tribs.length; i++){
                if(fresh_tribs[i].id != $scope.first_trib_id){
                    var fresh_id_appears = false;

                    for(var j = 0; j < $scope.tribs.length; j++){
                        if(fresh_tribs[i].id == $scope.tribs[j].id) fresh_id_appears = true;
                    }

                    if(!fresh_id_appears){
                        $scope.tribs.unshift(fresh_tribs[i]);

                        if($scope.tribs.length > $scope.trib_limit_to){
                            $scope.trib_limit_to = $scope.tribs.length;
                        }
                    }

                    if(i == (fresh_tribs.length-1)) addNewTribs($scope, trib_offset+trib_add);

                } else {
                    break;
                }
            }

            $scope.first_trib_id = $scope.tribs[0].id;
            $timeout(function(){addNewTribs($scope, trib_offset);}, 60000);
        });
    }

    function waitTribs($scope, trib_offset){
        if($scope.tribs.length > 0){
            $scope.first_trib_id = $scope.tribs[0].id;
            addNewTribs($scope, trib_offset);
        } else {
            $timeout(function(){waitTribs($scope, trib_offset);}, 10000);
        }
    }

    waitTribs($scope, trib_offset);
}