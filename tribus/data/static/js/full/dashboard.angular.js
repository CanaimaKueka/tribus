// Declare use of strict javascript
'use strict';


// Application -----------------------------------------------------------------

var tribus = angular.module('tribus',
    ['Tribs', 'Timeline', 'Comments', 'Search', 'infiniteScroll',
    'angularMoment', 'angular-growl', 'ui.bootstrap', 'autoGrow']);


// Controllers -----------------------------------------------------------------

tribus.controller('TribController', ['$scope', '$timeout', 'Tribs', 'Timeline', 'growl',
    TribController]);
tribus.controller('CommentController', ['$scope', '$timeout', 'Comments', 'growl',
    CommentController]);