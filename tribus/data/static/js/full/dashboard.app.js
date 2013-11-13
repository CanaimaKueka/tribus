// Declare use of strict javascript
'use strict';


// Application -----------------------------------------------------------------

var tribus = angular.module('tribus',
    ['Tribs', 'Timeline', 'Comments', 'Search', 'infinite-scroll']);


// Controllers -----------------------------------------------------------------

tribus.controller('TribController', ['$scope', '$timeout', 'Tribs', 'Timeline',
    TribController]);
tribus.controller('CommentController', ['$scope', '$timeout', 'Comments',
    CommentController]);


function TribController($scope, $timeout, Tribs, Timeline){

    $scope.user_gravatar = user_gravatar;
    $scope.comment_gravatar = comment_gravatar;
    $scope.controller_busy = controller_busy;
    $scope.trib_limit_to = trib_limit_to;
    $scope.trib_limit = trib_limit;
    $scope.trib_offset = trib_offset;
    $scope.new_tribs_offset = trib_offset;
    $scope.trib_orderby = trib_orderby;
    $scope.tribs = [];
    $scope.first_trib_id = '';

    $scope.createNewTrib = function(){
        Tribs.save({
            author_id: user_id,
            author_username: user_username,
            author_first_name: user_first_name,
            author_last_name: user_last_name,
            author_email: user_email,
            trib_content: $scope.trib_content,
            trib_pub_date: new Date().toISOString()
        }, function(e){
            $scope.trib_content = '';
            $timeout(function(){$scope.addNewTribs();});
            $timeout(function(){$('textarea.action_textarea').trigger('keyup');});
            $timeout(function(){$('textarea.action_textarea').trigger('focus');});
            $timeout(function(){
                $.bootstrapGrowl(trib_save_success, {
                    ele: 'body',
                    type: 'success',
                    offset: { from: 'top', amount: 50 },
                    align: 'right',
                    width: 400,
                    delay: 10000,
                    allow_dismiss: true,
                    stackup_spacing: 5
                });
            }, 100);
        }, function(e){
            $timeout(function(){
                $.bootstrapGrowl(trib_save_error, {
                    ele: 'body',
                    type: 'error',
                    offset: { from: 'top', amount: 50 },
                    align: 'right',
                    width: 400,
                    delay: 10000,
                    allow_dismiss: true,
                    stackup_spacing: 5
                });
            }, 100);
        });
    };

    $scope.pollNewTribs = function(){
        $timeout(function(){$scope.initTribs();});
        $timeout(function(){
            $timeout(function(){$scope.addNewTribs();});
            $timeout(function(){$scope.pollNewTribs();});
        }, 60000);
    };

    $scope.toggleTrib = function(){
        if($scope.tribs[this.$index].reply_show === false ||
           $scope.tribs[this.$index].reply_show === undefined){
            $scope.tribs[this.$index].reply_show = true;
        } else {
            $scope.tribs[this.$index].reply_show = false;
        }
    };

    $scope.configDeleteTrib = function(){
        $scope.delete_trib_id = $scope.tribs[this.$index].id;
        $scope.delete_trib_index = this.$index;
    };

    $scope.deleteTrib = function(){
        Tribs.delete({
            id: $scope.delete_trib_id
        }, function(e){
            $scope.tribs.splice($scope.delete_trib_index, 1);
            $timeout(function(){
                $.bootstrapGrowl(trib_delete_success, {
                    ele: 'body',
                    type: 'success',
                    offset: { from: 'top', amount: 50 },
                    align: 'right',
                    width: 400,
                    delay: 10000,
                    allow_dismiss: true,
                    stackup_spacing: 5
                });
            }, 100);
        }, function(e){
            $timeout(function(){
                $.bootstrapGrowl(trib_delete_error, {
                    ele: 'body',
                    type: 'error',
                    offset: { from: 'top', amount: 50 },
                    align: 'right',
                    width: 400,
                    delay: 10000,
                    allow_dismiss: true,
                    stackup_spacing: 5
                });
            }, 100);
        });
    };

    $scope.addOldTribs = function(){

        if ($scope.tribs_end) return;
        if ($scope.controller_busy) return;
        $scope.controller_busy = true;

        var old_tribs = Timeline.query({
            order_by: $scope.trib_orderby,
            limit: $scope.trib_limit,
            offset: $scope.trib_offset
        }, function(){
            if(old_tribs.objects.length === 0){
                $scope.tribs_end = true;
            } else {
                for(var i = 0; i < old_tribs.objects.length; i++){
                    var old_id_appears = false;

                    for(var j = 0; j < $scope.tribs.length; j++){
                        if(old_tribs.objects[i].id == $scope.tribs[j].id) old_id_appears = true;
                    }

                    if(!old_id_appears){
                        var gravatar = 'http://www.gravatar.com/avatar/'+md5(old_tribs.objects[i].author_email)+'?d=mm&s=70&r=x';
                        old_tribs.objects[i].author_gravatar = gravatar;
                        $scope.tribs.push(old_tribs.objects[i]);
                    }
                }

                if($scope.tribs.length > $scope.trib_offset){
                    $scope.trib_offset = $scope.trib_offset + trib_add;
                }

                if($scope.tribs.length > $scope.trib_limit_to){
                    $scope.trib_limit_to = $scope.tribs.length;
                }

                $timeout(function(){$('.trib_list').trigger('reload_dom');});
                $scope.controller_busy = false;
            }
        }, function(e){
            $timeout(function(){
                $.bootstrapGrowl(trib_add_error, {
                    ele: 'body',
                    type: 'error',
                    offset: { from: 'top', amount: 50 },
                    align: 'right',
                    width: 400,
                    delay: 10000,
                    allow_dismiss: true,
                    stackup_spacing: 5
                });
            }, 100);
        });
    };

    $scope.initTribs = function(){

        if ($scope.controller_busy) return;
        $scope.controller_busy = true;

        var init_tribs = Timeline.query({
            order_by: trib_orderby,
            limit: trib_limit,
            offset: trib_offset
        }, function(){
            for(var i = 0; i < init_tribs.objects.length; i++){
                var gravatar = 'http://www.gravatar.com/avatar/'+md5(init_tribs.objects[i].author_email)+'?d=mm&s=70&r=x';
                init_tribs.objects[i].author_gravatar = gravatar;
                $scope.tribs.push(init_tribs.objects[i]);

                if($scope.tribs.length > $scope.trib_limit_to){
                    $scope.trib_limit_to = $scope.tribs.length;
                }
            }

            $timeout(function(){$(".trib_list").trigger('reload_dom');});        
            $scope.controller_busy = false;

        }, function(e){
            $timeout(function(){
                $.bootstrapGrowl(trib_add_error, {
                    ele: 'body',
                    type: 'error',
                    offset: { from: 'top', amount: 50 },
                    align: 'right',
                    width: 400,
                    delay: 10000,
                    allow_dismiss: true,
                    stackup_spacing: 5
                });
            }, 100);
        });
    };

    $scope.addNewTribs = function(){

        if ($scope.controller_busy) return;
        $scope.controller_busy = true;
        $scope.first_trib_id = $scope.tribs[0].id;

        var fresh_tribs = Timeline.query({
            order_by: $scope.trib_orderby,
            limit: $scope.trib_limit,
            offset: $scope.new_tribs_offset
        }, function(){
            console.log($scope.new_tribs_offset)
            for(var i = 0; i < fresh_tribs.objects.length; i++){
                console.log(fresh_tribs.objects[i].id+'    '+$scope.first_trib_id);
                if(fresh_tribs.objects[i].id != $scope.first_trib_id){
                    var fresh_id_appears = false;

                    for(var j = 0; j < $scope.tribs.length; j++){
                        if(fresh_tribs.objects[i].id == $scope.tribs[j].id) fresh_id_appears = true;
                    }

                    if(!fresh_id_appears){
                        var gravatar = 'http://www.gravatar.com/avatar/'+md5(fresh_tribs.objects[i].author_email)+'?d=mm&s=70&r=x';
                        fresh_tribs.objects[i].author_gravatar = gravatar;
                        $scope.tribs.unshift(fresh_tribs.objects[i]);
                    }

                    if($scope.tribs.length > $scope.trib_limit_to){
                        $scope.trib_limit_to = $scope.tribs.length;
                    }

                    if(i == (fresh_tribs.objects.length-1)){
                        $scope.new_tribs_offset = $scope.new_tribs_offset + trib_add;
                        $timeout(function(){$scope.addNewTribs();});
                    }
                } else {
                    $scope.first_trib_id = $scope.tribs[0].id;
                    break;
                }
            }

            $timeout(function(){$(".trib_list").trigger('reload_dom');});        
            $scope.controller_busy = false;
        }, function(e){
            $timeout(function(){
                $.bootstrapGrowl(trib_add_error, {
                    ele: 'body',
                    type: 'error',
                    offset: { from: 'top', amount: 50 },
                    align: 'right',
                    width: 400,
                    delay: 10000,
                    allow_dismiss: true,
                    stackup_spacing: 5
                });
            }, 100);
        });
    };
}


function CommentController($scope, $timeout, Comments){

    $scope.comment_limit_to = comment_limit_to;
    $scope.comment_limit = comment_limit;
    $scope.comment_offset = comment_offset;
    $scope.comment_orderby = comment_orderby;
    $scope.comments = [];

    $scope.createNewComment = function(){
        Comments.save({
            author_id: user_id,
            author_username: user_username,
            author_first_name: user_first_name,
            author_last_name: user_last_name,
            author_email: user_email,
            comment_content: this.comment_content,
            comment_pub_date: new Date().toISOString(),
            trib_id: $scope.trib_id
        }, function(){
            $scope.comment_content = '';
            $timeout(function(){$scope.addNewComments();});
            $timeout(function(){
                $.bootstrapGrowl(comment_save_success, {
                    ele: 'body',
                    type: 'success',
                    offset: { from: 'top', amount: 50 },
                    align: 'right',
                    width: 400,
                    delay: 10000,
                    allow_dismiss: true,
                    stackup_spacing: 5
                });
            }, 100);
        }, function(){
            $timeout(function(){
                $.bootstrapGrowl(comment_save_success, {
                    ele: 'body',
                    type: 'success',
                    offset: { from: 'top', amount: 50 },
                    align: 'right',
                    width: 400,
                    delay: 10000,
                    allow_dismiss: true,
                    stackup_spacing: 5
                });
            }, 100);
        });
    };

    $scope.configDeleteComment = function(){
        $scope.delete_comment_id = $scope.comments[this.$index].id;
        $scope.delete_comment_index = this.$index;
    };

    $scope.deleteComment = function(){
        Comments.delete({
            id: $scope.delete_comment_id
        }, function(e){
            $scope.comments.splice($scope.delete_comment_index, 1);
            $timeout(function(){
                $.bootstrapGrowl(comment_delete_success, {
                    ele: 'body',
                    type: 'success',
                    offset: { from: 'top', amount: 50 },
                    align: 'right',
                    width: 400,
                    delay: 10000,
                    allow_dismiss: true,
                    stackup_spacing: 5
                });
            }, 100);
        }, function(e){
            $timeout(function(){
                $.bootstrapGrowl(comment_delete_error, {
                    ele: 'body',
                    type: 'error',
                    offset: { from: 'top', amount: 50 },
                    align: 'right',
                    width: 400,
                    delay: 10000,
                    allow_dismiss: true,
                    stackup_spacing: 5
                });
            }, 100);
        });
    };

    $scope.addOldComments = function(){

        if ($scope.comments_end) return;
        if ($scope.controller_busy) return;
        $scope.controller_busy = true;

        var old_comments = Comments.query({
            trib_id: $scope.trib_id,
            order_by: $scope.comment_orderby,
            limit: $scope.comment_limit,
            offset: $scope.comment_offset
        }, function(){
            for(var i = 0; i < old_comments.objects.length; i++){
                var old_id_appears = false;

                for(var j = 0; j < $scope.comments.length; j++){
                    if(old_comments.objects[i].id == $scope.comments[j].id) old_id_appears = true;
                }

                if(!old_id_appears){
                    var gravatar = 'http://www.gravatar.com/avatar/'+md5(old_comments.objects[i].author_email)+'?d=mm&s=30&r=x';
                    old_comments.objects[i].author_gravatar = gravatar;
                    $scope.comments.push(old_comments.objects[i]);
                }
            }

            if($scope.comments.length > $scope.comment_offset){
                $scope.comment_offset = $scope.comment_offset + comment_add;
            }

            if($scope.comments.length > $scope.comment_limit_to){
                $scope.comment_limit_to = $scope.comments.length;
            }

            if(old_comments.objects.length === 0){
                $scope.comments_end = true;
            }

            $timeout(function(){$('.comment_list').trigger('reload_dom');});
            $scope.controller_busy = false;
        }, function(e){
            $timeout(function(){
                $.bootstrapGrowl(comment_add_error, {
                    ele: 'body',
                    type: 'error',
                    offset: { from: 'top', amount: 50 },
                    align: 'right',
                    width: 400,
                    delay: 10000,
                    allow_dismiss: true,
                    stackup_spacing: 5
                });
            }, 100);
        });
    };

    $scope.addNewComments = function(){

        if ($scope.controller_busy) return;
        $scope.controller_busy = true;
        $scope.new_comments_offset = comment_offset;
        $scope.temp_new_comments = [];
        $scope.first_comment_id = '';

        if($scope.comments.length > 0){
            $scope.first_comment_id = $scope.comments[0].id;
        }

        var fresh_comments = Comments.query({
            trib_id: $scope.trib_id,
            order_by: $scope.comment_orderby,
            limit: $scope.comment_limit,
            offset: $scope.new_comments_offset
        }, function(){
            for(var i = 0; i < fresh_comments.objects.length; i++){
                if(fresh_comments.objects[i].id != $scope.first_comment_id){
                    var fresh_id_appears = false;

                    for(var j = 0; j < $scope.comments.length; j++){
                        if(fresh_comments.objects[i].id == $scope.comments[j].id) fresh_id_appears = true;
                    }

                    if(!fresh_id_appears){
                        var gravatar = 'http://www.gravatar.com/avatar/'+md5(fresh_comments.objects[i].author_email)+'?d=mm&s=30&r=x';
                        fresh_comments.objects[i].author_gravatar = gravatar;
                        $scope.comments.unshift(fresh_comments.objects[i]);

                        if($scope.comments.length > $scope.comment_limit_to){
                            $scope.comment_limit_to = $scope.comments.length;
                        }
                    }

                    if(i == (fresh_comments.objects.length-1)){
                        $scope.addNewComments($scope, $timeout, Comments, comment_offset+comment_add);
                    }

                } else {
                    break;
                }
            }

            $timeout(function(){$(".comment_list").trigger('reload_dom');});        
            $scope.controller_busy = false;
        }, function(e){
            $timeout(function(){
                $.bootstrapGrowl(comment_add_error, {
                    ele: 'body',
                    type: 'error',
                    offset: { from: 'top', amount: 50 },
                    align: 'right',
                    width: 400,
                    delay: 10000,
                    allow_dismiss: true,
                    stackup_spacing: 5
                });
            }, 100);
        });
    };

};


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