// Declare use of strict javascript
'use strict';

// Application -----------------------------------------------------------------

var tribus = angular.module('tribus',
    [ 'Tribs' , 'Timeline', 'Comments', 'Search', 'UserProfile', 'User',
    'UserFollows', 'UserFollowers', 'infinite-scroll', 'angularMoment', 'ui.bootstrap']);


// Controllers -----------------------------------------------------------------

tribus.controller('TribController', ['$scope', '$timeout', '$modal', 'Tribs', 'Timeline',
    TribController]);
tribus.controller('CommentController', ['$scope', '$timeout', '$modal', 'Comments',
    CommentController]);
tribus.controller('UserController',['$scope','UserProfile', 'User',
    UserController]);
tribus.controller('FollowsController', ['$scope','$filter','UserFollows','UserProfile','$timeout',
    FollowsController]);
tribus.controller('FollowersController', ['$scope','$filter','UserFollowers','UserProfile', '$timeout',
    FollowersController]);

tribus.filter('startFrom', function() {
    return function(input, start) {
        start = +start; //parse to int
        return input.slice(start);
    }
});

