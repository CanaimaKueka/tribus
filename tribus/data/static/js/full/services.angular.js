// Declare use of strict javascript
'use strict';

// Services --------------------------------------------------------------------

angular.module('User', ['ngResource'])
.factory('User',  function($resource){
    return $resource('/api/0.1/user/details/:user_id',
        { user_id: '@user_id' }, {
            save: {
                method: 'POST',
                headers: {
                    'X-CSRFToken': angular.element(document.querySelector('input[name=csrfmiddlewaretoken]')).val()
                },
            },

            modify: {
                method: 'PATCH',
                headers: {
                    'X-CSRFToken': angular.element(document.querySelector('input[name=csrfmiddlewaretoken]')).val()
                },
            },
            query: {
                method: 'GET',
                isArray: true,
                transformResponse: function(data){
                    return angular.fromJson(data).objects;
                },
            },
        });
});


angular.module('UserFollowers', ['ngResource'])
.factory('UserFollowers',  function($resource){
    return $resource('/api/0.1/user/followers/',{},{
        query: {
            method: 'GET',
            isArray: true,
            transformResponse: function(data){
                return angular.fromJson(data).objects;
            },
        },
    });
});

angular.module('UserFollows', ['ngResource'])
    .factory('UserFollows', function($resource){
    return $resource('/api/0.1/user/follows/', {}, {
        query: {
            method: 'GET',
            isArray: true,
            transformResponse: function(data){
                return angular.fromJson(data).objects;
            },
        },
    });
});

angular.module('UserProfile', ['ngResource'])
.factory('UserProfile',  function($resource){
    return $resource('/api/0.1/user/profile/:user_id',
        { user_id: '@user_id' }, {
            save: {
                method: 'POST',
                headers: {
                    'X-CSRFToken': angular.element(document.querySelector('input[name=csrfmiddlewaretoken]')).val()
                },
            },

            modify: {
                method: 'PATCH',
                headers: {
                    'X-CSRFToken': angular.element(document.querySelector('input[name=csrfmiddlewaretoken]')).val()
                },
            },
            query: {
                method: 'GET',
                isArray: true,
                transformResponse: function(data){
                    return angular.fromJson(data).objects;
                },
            },
        });
});


angular.module('Tribs', ['ngResource'])
    .factory('Tribs',  function($resource){
        return $resource('/api/0.1/user/tribs/:id',
            { id: '@id' }, {
            save: {
                method: 'POST',
                headers: {
                    'X-CSRFToken': angular.element(document.querySelector('input[name=csrfmiddlewaretoken]')).val()
                },
            },
            query: {
                method: 'GET',
                isArray: false
            },
            remove: {
                method: 'DELETE',
                headers: {
                    'X-CSRFToken': angular.element(document.querySelector('input[name=csrfmiddlewaretoken]')).val()
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
                    'X-CSRFToken': angular.element(document.querySelector('input[name=csrfmiddlewaretoken]')).val()
                },
            },
            query: {
                method: 'GET',
                isArray: false
            },
            remove: {
                method: 'DELETE',
                headers: {
                    'X-CSRFToken': angular.element(document.querySelector('input[name=csrfmiddlewaretoken]')).val()
                },
            },
        });
    });

angular.module('Search', ['ngResource'])
    .factory('Search', function($resource){
        return $resource('/api/0.1/search/', {}, {
            query: {
                method: 'GET',
                isArray: false
            },
        });
    });

