angular.module('index.services', ['ngResource']).
    factory('Tribs', function($resource){
        return $resource('/api/0.1/trib/', {}, {
            query: { method: 'GET', params: {
                author_id: user_id,
                order_by: '-trib_pub_date',
            }},
            create: { method: 'POST' }
        });
    });