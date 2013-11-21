// Declare use of strict javascript
'use strict';

// Application -----------------------------------------------------------------

// nombre de la app, cambiar para nuevas aplicaciones, cambiando el nombre de la variable y el modulo

var tribus = angular.module('tribus',
    [ 'Tribs' , 'Timeline', 'Comments', 'Search', 'UserProfile', 'User', 'infinite-scroll', 'UserFollows', 'UserFollowers']);



// Controllers -----------------------------------------------------------------

tribus.controller('TribController', ['$scope', '$timeout', 'Tribs', 'Timeline',
    TribController]);
tribus.controller('CommentController', ['$scope', '$timeout', 'Comments',
    CommentController]);
tribus.controller('UserController',['$scope','UserProfile', 'User' ,
    UserController]);
tribus.controller('FollowsController',['$scope','$filter','UserFollows','UserProfile','$timeout',
    FollowsController]);

tribus.controller('FollowersController',['$scope','$filter','UserFollowers','UserProfile', '$timeout',
    FollowersController]);

tribus.filter('startFrom', function() {
    return function(input, start) {
        start = +start; //parse to int
        return input.slice(start);
    }
});

