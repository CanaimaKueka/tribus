angular.module('infiniteScroll', [])
    .directive('infiniteScroll', [ "$window", function($window){
        return {
            link: function(scope, element, attrs){
                var offset = parseInt(attrs.infiniteScrollDistance) || 0;
                var e = element[0];

                element.bind('scroll', function(){
                    if (scope.$eval(attrs.infiniteScrollDisabled) && e.scrollTop + e.offsetHeight >= e.scrollHeight - offset) {
                        scope.$apply(attrs.infiniteScroll);
                    }
                });
            }
        };
    }]);