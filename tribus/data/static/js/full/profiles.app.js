// Declare use of strict javascript
'use strict';


// Application -----------------------------------------------------------------

// nombre de la app, cambiar para nuevas aplicaciones, cambiando el nombre de la variable y el modulo

/*
var profiles = angular.module('tribus',
    ['Tribs','packages', 'User', 'infinite-scroll', 'ui.gravatar']);
*/


// Events ----------------------------------------------------------------------



// Controllers -----------------------------------------------------------------

// tribus.controller('CommentController',['$scope','$timeout','Tribs',
//     CommentController]);
// tribus.controller('NewTribController',['$scope','$timeout','Tribs',
//     NewTribController]);
// tribus.controller('TribListController',['$scope','$timeout','Tribs',
//     TribListController]);
tribus.controller('UserController',['$scope','UserProfile', 'User',
    UserController]);


function CommentController($scope, $timeout, Tribs){

}

function UserController($scope, UserProfile, User){
    $scope.follow = function(){

        var profile = UserProfile.query({id:user_id},
            function(){
                var agregado = false;
                // console.log("/api/0.1/user/profile/"+userview_id); 
                for (var ind = 0; ind<profile[0].follows.length; ind++){
                    if (profile[0].follows[ind] == "/api/0.1/user/details/"+userview_id){
                        console.log("----->  ELIMINADO.");
                        console.log(profile[0].follows);
                        profile[0].follows.pop(ind);
                        profile[0].$modify({author_id: user_id});
                        agregado = true;
                        break;
                    }
                }
                if (agregado == false){
                    console.log("----->  AGREGADO.");
                    profile[0].follows.push("/api/0.1/user/details/"+userview_id);
                    profile[0].$modify({author_id: user_id});
                    }

                });
        };


        // var follow = User.modify({follows:[], author_id: 3},
        //     function(){
        //         console.log(follow);

        //         });
        // alert($scope.);
        // $scope.mensaje = "add as follow"

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


angular.module('packages', ['ngResource'])
    .factory('packages',  function($resource){
        return $resource('/api/0.1/packages/search/?=:package_name',
            { package_name: '@package_name' }, {
            query: {
                method: 'GET',
            },
        });
    });
