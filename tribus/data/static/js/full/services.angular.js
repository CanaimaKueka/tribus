// Declare use of strict javascript
'use strict';

// Services --------------------------------------------------------------------

angular.module('Tribs', ['ngResource'])
    .factory('Tribs',  function($resource){
        return $resource('/api/0.1/user/tribs/:id',
            { id: '@id' }, {
            save: {
                method: 'POST',
                headers: {
                    'X-CSRFToken': $('input[name=csrfmiddlewaretoken]').val()
                },
            },
            query: {
                method: 'GET',
                isArray: false
            },
            delete: {
                method: 'DELETE',
                headers: {
                    'X-CSRFToken': $('input[name=csrfmiddlewaretoken]').val()
                },
            },
        });
    });

angular.module('Timeline', ['ngResource'])
    .factory('Timeline', function($resource){
        return $resource('/api/0.1/user/timeline', {}, {
            query: {
                method: 'GET',
                isArray: false
            }
        });
    });

angular.module('Comments', ['ngResource'])
    .factory('Comments',  function($resource){
        return $resource('/api/0.1/tribs/comments/:id',
            { id: '@id' }, {
            save: {
                method: 'POST',
                headers: {
                    'X-CSRFToken': $('input[name=csrfmiddlewaretoken]').val()
                },
            },
            query: {
                method: 'GET',
                isArray: false
            },
            delete: {
                method: 'DELETE',
                headers: {
                    'X-CSRFToken': $('input[name=csrfmiddlewaretoken]').val()
                },
            },
        });
    });