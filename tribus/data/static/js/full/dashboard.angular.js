// Declare use of strict javascript
'use strict';

// Application -----------------------------------------------------------------

var tribus = angular.module('tribus', ['Tribs', 'Timeline', 'Comments',
	'Search', 'infinite-scroll', 'angularMoment', 'ui.bootstrap']);

// Controllers -----------------------------------------------------------------

tribus.controller('TribController', ['$scope', '$timeout', '$modal', 'Tribs', 'Timeline',
    TribController]);
tribus.controller('CommentController', ['$scope', '$timeout', '$modal', 'Comments',
    CommentController]);