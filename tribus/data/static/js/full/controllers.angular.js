// Declare use of strict javascript
'use strict';


function TribController($scope, $timeout, Tribs, Timeline){

    $scope.user_gravatar = user_gravatar;
    $scope.comment_gravatar = comment_gravatar;
    $scope.controller_busy = controller_busy;
    $scope.trib_limit_to = trib_limit_to;
    $scope.trib_limit = trib_limit;
    $scope.trib_offset = trib_offset;
    $scope.trib_orderby = trib_orderby;
    $scope.tribs = [];
    $scope.first_trib_id = '';
    $scope.new_tribs_passes = 0;
    $scope.new_tribs_offset = trib_offset;

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
                $scope.controller_busy = false;
            } else {
                $scope.tribs_end = false;
                for(var i = 0; i < old_tribs.objects.length; i++){
                    var old_id_appears = false;

                    for(var j = 0; j < $scope.tribs.length; j++){
                        if(old_tribs.objects[i].id == $scope.tribs[j].id){
                            old_id_appears = true;
                        }
                    }

                    if(!old_id_appears){
                        old_tribs.objects[i].author_gravatar = 'http://www.gravatar.com/avatar/';
                        old_tribs.objects[i].author_gravatar += md5(old_tribs.objects[i].author_email);
                        old_tribs.objects[i].author_gravatar += '?d=mm&s=70&r=x';
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

    $scope.addNewTribs = function(){

        if ($scope.controller_busy) return;
        $scope.controller_busy = true;

        if($scope.new_tribs_passes === 0 && $scope.tribs.length > 0){
            $scope.first_trib_id = $scope.tribs[0].id;
        }
        
        var fresh_tribs = Timeline.query({
            order_by: $scope.trib_orderby,
            limit: $scope.trib_limit,
            offset: $scope.new_tribs_offset
        }, function(){
            for(var i = 0; i < fresh_tribs.objects.length; i++){
                if(fresh_tribs.objects[i].id != $scope.first_trib_id){
                    var fresh_id_appears = false;

                    for(var j = 0; j < $scope.tribs.length; j++){
                        if(fresh_tribs.objects[i].id == $scope.tribs[j].id){
                            fresh_id_appears = true;
                        }
                    }

                    if(!fresh_id_appears){
                        fresh_tribs.objects[i].author_gravatar = 'http://www.gravatar.com/avatar/';
                        fresh_tribs.objects[i].author_gravatar += md5(fresh_tribs.objects[i].author_email);
                        fresh_tribs.objects[i].author_gravatar += '?d=mm&s=70&r=x';
                        $scope.tribs.push(fresh_tribs.objects[i]);
                    }

                    if($scope.tribs.length > $scope.trib_limit_to){
                        $scope.trib_limit_to = $scope.tribs.length;
                    }

                    if(i == (fresh_tribs.objects.length-1)){
                        $scope.new_tribs_offset = $scope.new_tribs_offset + trib_add;
                        $scope.new_tribs_passes = $scope.new_tribs_passes + 1;
                        $timeout(function(){$scope.addNewTribs();});
                    }
                } else {
                    $scope.new_tribs_offset = trib_offset;
                    $scope.new_tribs_passes = 0;
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
    $scope.new_comments_offset = comment_offset;
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
            $timeout(function(){$('textarea.comment_textarea').trigger('keyup');});
            $timeout(function(){$('textarea.comment_textarea').trigger('focus');});
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

    $scope.addNewComments = function(){

        if ($scope.comments_end) return;
        if ($scope.controller_busy) return;
        $scope.comments_end = false;
        $scope.controller_busy = true;

        var new_comments = Comments.query({
            trib_id: $scope.trib_id,
            order_by: '-'+$scope.comment_orderby,
            limit: $scope.comment_limit,
            offset: $scope.new_comments_offset
        }, function(){
            if(new_comments.objects.length === 0){
                $scope.comments_end = true;
                $scope.controller_busy = false;
            } else {

                for(var i = 0; i < new_comments.objects.length; i++){
                    var old_id_appears = false;

                    for(var j = 0; j < $scope.comments.length; j++){
                        if(new_comments.objects[i].id == $scope.comments[j].id){
                            old_id_appears = true;
                        }
                    }

                    if(!old_id_appears){
                        new_comments.objects[i].author_gravatar = 'http://www.gravatar.com/avatar/';
                        new_comments.objects[i].author_gravatar += md5(new_comments.objects[i].author_email);
                        new_comments.objects[i].author_gravatar += '?d=mm&s=70&r=x';
                        $scope.comments.push(new_comments.objects[i]);
                    }
                }

                if($scope.comments.length > $scope.new_comments_offset){
                    $scope.new_comments_offset = $scope.new_comments_offset + comment_add;
                }

                if($scope.comments.length > $scope.comment_limit_to){
                    $scope.comment_limit_to = $scope.comments.length;
                }

                $timeout(function(){$('.trib_list').trigger('reload_dom');});
                $scope.controller_busy = false;

            }

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

    $scope.addOldComments = function(){

        if ($scope.comments_end) return;
        if ($scope.controller_busy) return;
        $scope.comments_end = false;
        $scope.controller_busy = true;

        var old_comments = Comments.query({
            trib_id: $scope.trib_id,
            order_by: $scope.comment_orderby,
            limit: $scope.comment_limit,
            offset: $scope.comment_offset
        }, function(){
            if(old_comments.objects.length === 0){
                $scope.comments_end = true;
                $scope.controller_busy = false;
            } else {

                for(var i = 0; i < old_comments.objects.length; i++){
                    var old_id_appears = false;

                    for(var j = 0; j < $scope.comments.length; j++){
                        if(old_comments.objects[i].id == $scope.comments[j].id){
                            old_id_appears = true;
                        }
                    }

                    if(!old_id_appears){
                        old_comments.objects[i].author_gravatar = 'http://www.gravatar.com/avatar/';
                        old_comments.objects[i].author_gravatar += md5(old_comments.objects[i].author_email);
                        old_comments.objects[i].author_gravatar += '?d=mm&s=70&r=x';
                        $scope.comments.push(old_comments.objects[i]);
                    }
                }

                if($scope.comments.length > $scope.comment_offset){
                    $scope.comment_offset = $scope.comment_offset + comment_add;
                }

                if($scope.comments.length > $scope.comment_limit_to){
                    $scope.comment_limit_to = $scope.comments.length;
                }

                $timeout(function(){$('.trib_list').trigger('reload_dom');});
                $scope.controller_busy = false;

            }

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