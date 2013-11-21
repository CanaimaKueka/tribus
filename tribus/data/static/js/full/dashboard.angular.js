// Declare use of strict javascript
'use strict';


// Application -----------------------------------------------------------------

var tribus = angular.module('tribus',
    ['Tribs', 'Timeline', 'Comments', 'Search', 'infinite-scroll']);


// Controllers -----------------------------------------------------------------

tribus.controller('TribController', ['$scope', '$timeout', 'Tribs', 'Timeline',
    TribController]);
tribus.controller('CommentController', ['$scope', '$timeout', 'Comments',
    CommentController]);