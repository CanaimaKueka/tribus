"use strict";

angular.module('ui-gravatar', []).
		directive('gravatarImage', function () {
        return {
        	restrict:"EAC",
            link:function ($scope, elm, attrs) {

                $scope.$watch(attrs.gravatarImage, function (value) {
                    elm.text(value);
                    console.log(elm);
                    console.log(value);
				// let's do nothing if the value comes in empty, null or undefined
                    if ((value !== null) && (value !== undefined) && (value !== '')) {
                        // convert the value to lower case and then to a md5 hash
                        var hash = md5(value.toLowerCase());
                        // construct the tag to insert into the element

                        var tag = '<img alt="" src="http://www.gravatar.com/avatar/' + hash + '?s=40&r=pg&d=404" />'
                        // insert the tag into the element
                        elm.append(tag);
                    }                    
            });      
        }};
    });