angular.module('index.services', ['ngResource']).
    factory('Tribs', function($resource, $http){
        return $resource('/api/0.1/trib/', {}, {
            query: {
                method: 'GET',
                isArray: true,
                transformResponse: function(data){ return angular.fromJson(data).objects;}
            },
            create: { method: 'POST' }
        });
    });