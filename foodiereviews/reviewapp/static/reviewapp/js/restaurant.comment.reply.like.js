function addLike(form){
    var endpoint = "/reviewapp/api/like/add/";
    var review_id = form.children[name="review_id"].value;

    $.ajax({
        method: "POST",
        url: endpoint,
        data: {
            review_id: review_id,
            user_id: user_id,
        },
        success: function(data) {
            if (data.success){
                displayNewLike(review_id, data.total_likes);
                console.log(data);
            }
        }
    });
}

function displayNewLike(review_id, total_likes){
    console.log("displaying");
    console.log("review_id, total_likes>>>"+review_id+total_likes);

    var newLike = $("#newLike").clone().removeAttr("id");
    newLike.find("span.likes-count").text(total_likes); // total likes
    newLike.show();

    var likesDiv = "#rl" + review_id;
    $(likesDiv).replaceWith(newLike).hide().fadeIn('slow');//replace
}


function createAddReply(commentId, replyButton){
    var newAddReply = $("#newAddReply").clone().removeAttr("id");
    newAddReply.find("input[name=comment_id]").val(commentId);
    newAddReply.show()

    var repliesDiv = "#cc" + commentId;
    $(repliesDiv).empty(); //Remove replyButton as it is only needed once
    $(repliesDiv).append(newAddReply);
}

function addReply(form){
    var endpoint = "/reviewapp/api/reply/add/";

    var comment_id = form.children[name="comment_id"].value;
    var reply_description_input = form.children[name="reply_description"];
    var reply_description = reply_description_input.value;
    var reply_user_id = user_id;
    isComplete = validateComplete([comment_id, reply_user_id, reply_description]);
    
    if (!isComplete){
        return false;
    }

    $.ajax({
        method: "POST",
        url: endpoint,
        data: {
            comment_id: comment_id,
            reply_user_id: reply_user_id,
            reply_description: reply_description
        },
        success: function(data) {
            if (data.success){
                displayNewReply(comment_id, user_username, reply_description, data.new_reply_pk, reply_description_input);
                console.log(data);
            }
        }
    });
}

function displayNewReply(comment_id, reply_username, reply_description, reply_id, reply_description_input) {

    var newReply = $("#newReply").clone().removeAttr("id");
    newReply.find("span.comment-reply-username").text(reply_username);
    newReply.find("span.comment-reply-description").text(reply_description);
    newReply.show();

    var repliesDiv = "#c" + comment_id;
    $(repliesDiv).prepend(newReply[0]).hide().fadeIn('slow');
    reply_description_input.value = "";
    reply_description_input.blur();
}

function addComment(form){
    var endpoint = "/reviewapp/api/comment/add/";

    var review_id = form.children[name="review_id"].value;
    var comment_description_input = form.children[name="comment_description"];
    var comment_description = comment_description_input.value;
    var comment_user_id = user_id;
    isComplete = validateComplete([review_id, comment_user_id, comment_description]);

    if (!isComplete){
        return false;
    }

    $.ajax({
        method: "POST",
        url: endpoint,
        data: {
            review_id: review_id,
            comment_user_id: comment_user_id,
            comment_description: comment_description
        },
        success: function(data) {
            if (data.success){
                displayNewComment(review_id, user_username, comment_description, data.new_comment_pk, comment_description_input);
                console.log(data);
            }
        }
    });
}

function validateComplete(fields){
    return fields.every(function(field){
        console.log(field);
        return field !== "";
    });
}

function displayNewComment(review_id, comment_username, comment_description, comment_id, comment_description_input){
    var onclick_script = "createAddReply("+ comment_id +", this); return false;"

    var newComment = $("#newComment").clone().removeAttr("id");
    newComment.find("span.comment-reply-username").text(comment_username);
    newComment.find("span.comment-reply-description").text(comment_description);
    newComment.find("a").attr("onclick", onclick_script);
    newComment.find(".replies").attr("id", "c" + comment_id);
    newComment.find(".replies-with-comment-options").attr("id", "cc" + comment_id);
    newComment.show();

    var commentsDiv = "#rc" + review_id;
    $(commentsDiv).prepend(newComment[0]).hide().fadeIn('slow');
    comment_description_input.value = "";
    comment_description_input.blur();
}