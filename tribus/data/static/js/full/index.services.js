angular.module('index.services', ['ngResource'])
    .factory('Tribs', function($resource){        
        return $resource('/api/0.1/tribs/', {},{
            save: { method: 'POST' },
            query: {
                method: 'GET',
                isArray: true,
                headers: {'X-CSRFToken': $('input[name=csrfmiddlewaretoken]').val()},
                transformResponse: function(data){return angular.fromJson(data).objects;}
            }
        });
    });