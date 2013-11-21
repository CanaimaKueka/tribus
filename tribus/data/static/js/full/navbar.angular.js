// Declare use of strict javascript
'use strict';

// Controllers -----------------------------------------------------------------

var tribus = angular.module('tribus',
    ['Search']);


tribus.controller('SearchListController', ['$scope', 'Search',
    SearchListController]);


// Services --------------------------------------------------------------------

