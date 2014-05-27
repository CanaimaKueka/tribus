// Declare use of strict javascript
'use strict';

// Application -----------------------------------------------------------------

var tribus = angular.module('tribus', ['ngSanitize', 'Tribs', 'Timeline', 'Comments',
	'Search', 'infinite-scroll', 'angularMoment', 'ui.bootstrap']);

// Controllers -----------------------------------------------------------------


if (waffle.switch_is_active('profile')){
	tribus.controller('TribController', ['$scope', '$timeout', '$modal', 'Tribs', 'Timeline',
		TribController]);
	tribus.controller('CommentController', ['$scope', '$timeout', '$modal', 'Comments',
		CommentController]);
};