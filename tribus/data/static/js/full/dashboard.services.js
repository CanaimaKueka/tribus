angular.module('Tribs', ['ngResource'])
    .factory('Tribs', function($resource){        
        return $resource('/api/0.1/user/tribs/', {},{
            save: {
                method: 'POST',
                headers: {'X-CSRFToken': $('input[name=csrfmiddlewaretoken]').val()},
            },
            query: {
                method: 'GET',
                isArray: true,
                transformResponse: function(data){return angular.fromJson(data).objects;}
            },
            delete: {
                method: 'DELETE',
                headers: {'X-CSRFToken': $('input[name=csrfmiddlewaretoken]').val()},
            },
        });
    });

angular.module('Timeline', ['ngResource'])
    .factory('Timeline', function($resource){        
        return $resource('/api/0.1/user/timeline/', {},{
            query: {
                method: 'GET',
                isArray: true,
                transformResponse: function(data){return angular.fromJson(data).objects;}
            }
        });
    });