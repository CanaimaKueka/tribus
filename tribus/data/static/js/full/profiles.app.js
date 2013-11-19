// Declare use of strict javascript
'use strict';

// Application -----------------------------------------------------------------

// nombre de la app, cambiar para nuevas aplicaciones, cambiando el nombre de la variable y el modulo

var tribus = angular.module('tribus',
    [ 'Tribs' , 'Comments', 'Search', 'UserProfile', 'User', 'infinite-scroll', 'UserFollows', 'UserFollowers']);


// Events ----------------------------------------------------------------------


// Controllers -----------------------------------------------------------------

tribus.controller('TribController', ['$scope', '$timeout', 'Tribs',
    TribController]);
tribus.controller('CommentController', ['$scope', '$timeout', 'Comments',
    CommentController]);
tribus.controller('UserController',['$scope','UserProfile', 'User' ,
    UserController]);
tribus.controller('FollowsController',['$scope','$filter','UserFollows',
    FollowsController]);

tribus.controller('FollowersController',['$scope','$filter','UserFollowers',
    FollowersController]);

tribus.filter('startFrom', function() {
    return function(input, start) {
        start = +start; //parse to int
        return input.slice(start);
    }
});


function UserController($scope, UserProfile){
    $scope.user_gravatar = user_gravatar;
    $scope.userview_gravatar = userview_gravatar;

    
    var user_follow = UserProfile.query({id:user_id},function(){
        $scope.add = false;
        for (var i = 0; i < user_follow[0].follows.length; i++ ){
            if (user_follow[0].follows[i] ==  "/api/0.1/user/details/" + userview_id){
                $scope.add = true;
                break;
                
            }
            
        }     
        console.log("iniciado add ", $scope.add);
    });


    $scope.follow = function(){
        var agregado = false;

        var profile = UserProfile.query({id:user_id},function(){
            var profileview = UserProfile.query({id:userview_id},function(){
                console.log(profile, profileview);

                    
                // console.log("/api/0.1/user/profile/"+userview_id); 
                for (var ind = 0; ind<profile[0].follows.length; ind++){
                    if (profile[0].follows[ind] == "/api/0.1/user/details/" + userview_id){
                        console.log("----->  ELIMINADO.", profile);

                        profileview[0].followers.pop(ind);
                        profileview[0].$modify({author_id: userview_id});

                        profile[0].follows.pop(ind);
                        profile[0].$modify({author_id: user_id});
                        agregado = true;
                        $scope.add = false;
                  
                        break;
                    }
                }
                if (agregado == false){                     

                    $scope.add= true;
                    profileview[0].followers.push("/api/0.1/user/details/"+user_id);
                    profileview[0].$modify({author_id: userview_id});
                    console.log("----->  AGREGADO.", profileview); 
                    profile[0].follows.push("/api/0.1/user/details/"+userview_id);
                    profile[0].$modify({author_id: user_id});

                  
                }
                // if (agregado ==false){

                // }
                // else{
                //     profileview[0].followers.pop(indidce);
                //     profileview[0].$modify({author_id: userview_id});
                // }
                
            });             
        });
        // $scope.$watch($scope.add,function(){
        // console.log($scope.add, "-----");
        // });  

    };


    // $scope.$watch($scope.add,function(){
    // console.log($scope.add, "-----");
    // });    
 }

function FollowsController($scope, $filter, UserFollows ){

    $scope.currentPage = 0;
    $scope.pageSize = 5;
    $scope.follows = UserFollows.query({},function(){
        $scope.$watch('query',function(){
            console.log($scope.add);
            $scope.currentPage = 0;
            $scope.filtername = $filter('filter')($scope.follows, $scope.query);
            $scope.numberOfPages=function(){
                return Math.ceil($scope.filtername.length / $scope.pageSize);
             $scope.follows = $scope.filtername;
            
            }
            console.log($scope.filtername.length);

        });
    });
    $scope.convertmd5 = function(email){
        console.log(email);
        var url = 'http://www.gravatar.com/avatar/'+md5(email)+'?d=mm&s=70&r=x';
        return url
    };

};

function FollowersController($scope, $filter, UserFollowers ){
    $scope.currentPage = 0;
    $scope.pageSize = 5;
    $scope.followers = UserFollowers.query({},function(){
        $scope.$watch('query2',function(){
            console.log($scope.add);
            $scope.currentPage = 0;
            $scope.filtername = $filter('filter')($scope.followers, $scope.query);
            $scope.numberOfPages=function(){
                return Math.ceil($scope.filtername.length / $scope.pageSize);
             $scope.followers = $scope.filtername;
            
            }
            console.log($scope.filtername.length);

        });
    });
    $scope.convertmd5 = function(email){
        console.log(email);
        var url = 'http://www.gravatar.com/avatar/'+md5(email)+'?d=mm&s=70&r=x';
        return url
    };



};



function TribController($scope, $timeout, Tribs, Timeline){

    $scope.user_gravatar = user_gravatar;
    $scope.controller_busy = controller_busy;
    $scope.trib_limit_to = trib_limit_to;
    $scope.trib_limit = trib_limit;
    $scope.trib_offset = trib_offset;
    $scope.trib_orderby = trib_orderby;
    $scope.tribs = [];

    $scope.createNewTrib = function(){
        Tribs.save({
            author_id: user_id,
            author_username: user_username,
            author_first_name: user_first_name,
            author_last_name: user_last_name,
            author_email: user_email,
            trib_content: $scope.trib_content,
            trib_pub_date: new Date().toISOString()
        }, function(e){
            $scope.trib_content = '';
            $timeout(function(){$scope.addNewTribs();});
            $timeout(function(){$('textarea.action_textarea').trigger('keyup');});
            $timeout(function(){
                $.bootstrapGrowl(trib_save_success, {
                    ele: 'body',
                    type: 'success',
                    offset: {from: 'top', amount: 50},
                    align: 'right',
                    width: 400,
                    delay: 10000,
                    allow_dismiss: true,
                    stackup_spacing: 5
                });
            }, 100);
        }, function(e){
            $timeout(function(){
                $.bootstrapGrowl(trib_save_error, {
                    ele: 'body',
                    type: 'error',
                    offset: {from: 'top', amount: 50},
                    align: 'right',
                    width: 400,
                    delay: 10000,
                    allow_dismiss: true,
                    stackup_spacing: 5
                });
            }, 100);
        });
    };

    $scope.pollNewTribs = function(){
        $timeout(function(){
            $timeout(function(){$scope.addNewTribs();});
            $timeout(function(){$scope.pollNewTribs();});
        }, 60000);
    };

    $scope.toggleTrib = function(){
        if($scope.tribs[this.$index].reply_show === false ||
           $scope.tribs[this.$index].reply_show === undefined){
            $scope.tribs[this.$index].reply_show = true;
        } else {
            $scope.tribs[this.$index].reply_show = false;
        }
    };

    $scope.configDeleteTrib = function(){
        $scope.delete_trib_id = $scope.tribs[this.$index].id;
        $scope.delete_trib_index = this.$index;
    };

    $scope.deleteTrib = function(){
        Tribs.delete({
            id: $scope.delete_trib_id
        }, function(e){
            $scope.tribs.splice($scope.delete_trib_index, 1);
            $timeout(function(){
                $.bootstrapGrowl(trib_delete_success, {
                    ele: 'body',
                    type: 'success',
                    offset: {from: 'top', amount: 50},
                    align: 'right',
                    width: 400,
                    delay: 10000,
                    allow_dismiss: true,
                    stackup_spacing: 5
                });
            }, 100);
        }, function(e){
            $timeout(function(){
                $.bootstrapGrowl(trib_delete_error, {
                    ele: 'body',
                    type: 'error',
                    offset: {from: 'top', amount: 50},
                    align: 'right',
                    width: 400,
                    delay: 10000,
                    allow_dismiss: true,
                    stackup_spacing: 5
                });
            }, 100);
        });
    };

    $scope.addOldTribs = function(){

        if ($scope.tribs_end) return;
        if ($scope.controller_busy) return;
        $scope.controller_busy = true;

        var old_tribs = Tribs.query({
            author_id: userview_id,
            order_by: $scope.trib_orderby,
            limit: $scope.trib_limit,
            offset: $scope.trib_offset
        }, function(){
            for(var i = 0; i < old_tribs.length; i++){
                var old_id_appears = false;

                for(var j = 0; j < $scope.tribs.length; j++){
                    if(old_tribs[i].id == $scope.tribs[j].id) old_id_appears = true;
                }

                if(!old_id_appears){
                    var gravatar = 'http://www.gravatar.com/avatar/'+md5(old_tribs[i].author_email)+'?d=mm&s=70&r=x';
                    old_tribs[i].author_gravatar = gravatar;
                    $scope.tribs.push(old_tribs[i]);
                }
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

            $timeout(function(){$('.trib_list').trigger('reload_dom');});
            $scope.controller_busy = false;
        }, function(e){
            $timeout(function(){
                $.bootstrapGrowl(trib_add_error, {
                    ele: 'body',
                    type: 'error',
                    offset: {from: 'top', amount: 50},
                    align: 'right',
                    width: 400,
                    delay: 10000,
                    allow_dismiss: true,
                    stackup_spacing: 5
                });
            }, 100);
        });
    };

    $scope.addNewTribs = function(){

        if ($scope.controller_busy) return;
        $scope.controller_busy = true;
        $scope.new_tribs_offset = trib_offset;
        $scope.temp_new_tribs = [];
        $scope.first_trib_id = '';

        if($scope.tribs.length > 0){
            $scope.first_trib_id = $scope.tribs[0].id;
        }

        var fresh_tribs = Tribs.query({
            author_id: userview_id,
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
                        var gravatar = 'http://www.gravatar.com/avatar/'+md5(fresh_tribs[i].author_email)+'?d=mm&s=70&r=x';
                        fresh_tribs[i].author_gravatar = gravatar;
                        $scope.tribs.unshift(fresh_tribs[i]);

                        if($scope.tribs.length > $scope.trib_limit_to){
                            $scope.trib_limit_to = $scope.tribs.length;
                        }
                    }

                    if(i == (fresh_tribs.length-1)){
                        $scope.addNewTribs($scope, $timeout, Timeline, trib_offset+trib_add);
                    }

                } else {
                    break;
                }
            }

            $timeout(function(){$(".trib_list").trigger('reload_dom');});        
            $scope.controller_busy = false;
        }, function(e){
            $timeout(function(){
                $.bootstrapGrowl(trib_add_error, {
                    ele: 'body',
                    type: 'error',
                    offset: {from: 'top', amount: 50},
                    align: 'right',
                    width: 400,
                    delay: 10000,
                    allow_dismiss: true,
                    stackup_spacing: 5
                });
            }, 100);
        });
    };
}


function CommentController($scope, $timeout, Comments){

    $scope.comment_limit_to = comment_limit_to;
    $scope.comment_limit = comment_limit;
    $scope.comment_offset = comment_offset;
    $scope.comment_orderby = comment_orderby;
    $scope.comments = [];

    $scope.createNewComment = function(){
        Comments.save({
            author_id: user_id,
            author_username: user_username,
            author_first_name: user_first_name,
            author_last_name: user_last_name,
            author_email: user_email,
            comment_content: this.comment_content,
            comment_pub_date: new Date().toISOString(),
            trib_id: $scope.trib_id
        }, function(){
            $scope.comment_content = '';
            $scope.addNewComments();
        }, function(){

        });
    };

    $scope.configDeleteComment = function(){
        $scope.delete_comment_id = $scope.comments[this.$index].id;
        $scope.delete_comment_index = this.$index;
    };

    $scope.deleteComment = function(){
        Comments.delete({
            id: $scope.delete_comment_id
        }, function(e){
            $scope.comments.splice($scope.delete_comment_index, 1);
            $timeout(function(){
                $.bootstrapGrowl(comment_delete_success, {
                    ele: 'body',
                    type: 'success',
                    offset: {from: 'top', amount: 50},
                    align: 'right',
                    width: 400,
                    delay: 10000,
                    allow_dismiss: true,
                    stackup_spacing: 5
                });
            }, 100);
        }, function(e){
            $timeout(function(){
                $.bootstrapGrowl(comment_delete_error, {
                    ele: 'body',
                    type: 'error',
                    offset: {from: 'top', amount: 50},
                    align: 'right',
                    width: 400,
                    delay: 10000,
                    allow_dismiss: true,
                    stackup_spacing: 5
                });
            }, 100);
        });
    };

    $scope.addNewComments = function(){
        var fresh_comments = Comments.query({
            trib_id: $scope.trib_id,
            order_by: $scope.comment_orderby,
            limit: $scope.comment_limit,
            offset: $scope.comment_offset
        }, function(){
            $scope.comments = fresh_comments.objects;
            $scope.comment_limit_to = $scope.comments.length;
            $scope.comment_limit = $scope.comment_limit + comment_add;
            $timeout(function(){$('.trib_list').trigger('reload_dom');});
        }, function(){

        });
    };
}



// Services --------------------------------------------------------------------

angular.module('UserProfile', ['ngResource'])
    .factory('UserProfile',  function($resource){
        return $resource('/api/0.1/user/profile/:author_id',
            { author_id: '@author_id' }, {
            save: {
                method: 'POST',
                headers: {
                    'X-CSRFToken': $('input[name=csrfmiddlewaretoken]').val()
                },
            },

            modify: {
                method: 'PATCH',
                headers: {
                    'X-CSRFToken': $('input[name=csrfmiddlewaretoken]').val()
                },
            },            
            query: {
                method: 'GET',
                isArray: true,
                transformResponse: function(data){
                    return angular.fromJson(data).objects;
                },
            },
        });
    });


angular.module('User', ['ngResource'])
    .factory('User',  function($resource){
        return $resource('/api/0.1/user/details/:author_id',
            { author_id: '@author_id' }, {
            save: {
                method: 'POST',
                headers: {
                    'X-CSRFToken': $('input[name=csrfmiddlewaretoken]').val()
                },
            },

            modify: {
                method: 'PATCH',
                headers: {
                    'X-CSRFToken': $('input[name=csrfmiddlewaretoken]').val()
                },
            },            
            query: {
                method: 'GET',
                isArray: true,
                transformResponse: function(data){
                    return angular.fromJson(data).objects;
                },
            },
        });
    });  


angular.module('UserFollowers', ['ngResource'])
    .factory('UserFollowers',  function($resource){
        return $resource('/api/0.1/user/followers/',{},{       
            query: {
                method: 'GET',
                isArray: true,
                transformResponse: function(data){
                    return angular.fromJson(data).objects;
                },
            },
        });
    });  

angular.module('UserFollows', ['ngResource'])
    .factory('UserFollows',  function($resource){
        return $resource('/api/0.1/user/follows/',{},{       
            query: {
                method: 'GET',
                isArray: true,
                transformResponse: function(data){
                    return angular.fromJson(data).objects;
                },
            },
        });
    });  


angular.module('Tribs', ['ngResource'])
    .factory('Tribs',  function($resource){
        return $resource('/api/0.1/user/tribs/:id',
            { id: '@id' }, {
            save: {
                method: 'POST',
                headers: {
                    'X-CSRFToken': $('input[name=csrfmiddlewaretoken]').val()
                },
            },
            query: {
                method: 'GET',
                isArray: true,
                transformResponse: function(data){
                    return angular.fromJson(data).objects;
                }
            },
            delete: {
                method: 'DELETE',
                headers: {
                    'X-CSRFToken': $('input[name=csrfmiddlewaretoken]').val()
                },
            },
        });
    });

angular.module('Comments', ['ngResource'])
    .factory('Comments',  function($resource){
        return $resource('/api/0.1/tribs/comments/:id',
            { id: '@id' }, {
            save: {
                method: 'POST',
                headers: {
                    'X-CSRFToken': $('input[name=csrfmiddlewaretoken]').val()
                },
            },
            query: {
                method: 'GET',
                isArray: false
            },
            delete: {
                method: 'DELETE',
                headers: {
                    'X-CSRFToken': $('input[name=csrfmiddlewaretoken]').val()
                },
            },
        });
    });