/**
 * Created by Yuzhang on 11/19/16.
 */
function populateList() {
    console.log("populatelist");
    var res_name = document.getElementById("restaurant_name").innerHTML;

    $.get("/get-posts", {res_name:res_name})
        .done(function (data) {
            console.log("i want to show data"+data);
            var list = $("#postcontent");
            list.data('max-time', data['max-time']);
            console.log("1 max-time:" + list.data('max-time'));
            list.html('')
            for (var i = 0; i < data.blogs.length; i++) {
                console.log("postblog");
                blog = data.blogs[i];
                var new_blog = $(blog.html);
                new_blog.data("blog-id", blog.id);
                list.append(new_blog);

                console.log("before comment")

                var comment_list = $("#comment_list_" + blog.id);
                console.log(blog.id);
                var comments = blog.comments;
                console.log(comments.length);
                for (var j = 0; j < comments.length; j++) {
                  var comment = comments[j];
                  var new_comment = $(comment.html);
                  console.log("add com");
                  comment_list.append(new_comment);

                }

                // var comment_list = $("#comment_list_" + blog.id);
                // // console.log(blog.id);
                // var comments = blog.comments;
                // console.log(comments.length);
                // for (var j = 0; j < comments.length; j++) {
                //     var comment = comments[j];
                //     var new_comment = $(comment.html);
                //     console.log("add com");
                //     comment_list.append(new_comment);
                // }

            }
        });

}


function add_post() {
    console.log("can add post");
    var postField = $("#content_text");
    var res_name = document.getElementById("restaurant_name").innerHTML;

        $.post("/post-new", {post: postField.val(),res_name:res_name})
        .done(function (data) {
            getUpdates();
            postField.val("").focus();
        });
}


function getUpdates() {
    var list = $("#postcontent");
    var max_time = list.data("max-time");
    var res_name = document.getElementById("restaurant_name").innerHTML;
    $.get("/get-changes/" + max_time, {res_name:res_name})
        .done(function (data) {
            list.data('max-time', data['max-time']);
            for (var i = 0; i < data.blogs.length; i++) {
                var blog = data.blogs[i];
                var new_blog = $(blog.html);
                new_blog.data("blog-id", blog.id);
                list.prepend(new_blog);

            }
        });
}




function add_comment(){
    var blog_id = parseInt($(this).attr('btn-id'));
    var commentField = $("#commentField_" + blog_id);
    $.post("/comment/" + blog_id, {comment: commentField.val()})
        .done(function(data){
            var comment_list = $("#comment_list_" + blog_id);
            comment = $(data.comments[data.comments.length-1].html);
            comment_list.append(comment);
            commentField.val("").focus();
        });
}



function addpost(evt){
    evt.preventDefault();
	var formData = new FormData($(this)[0]);
	console.log("add post")
	$.ajax({
        url: '/post-new',
        type: 'POST',
        data: formData,
        async: false,
        cache: false,
        contentType: false,
        enctype: 'multipart/form-data',
        processData: false,
        success: function (data){
            console.log("successfully add photo")
            var list = $("#postcontent");
            var content =$("#blogContent").val()
            var photo = $("#blogPhoto")
            var username = $("#curUsername").val();
            var result = "<br><br><br><div><div class='box box-widget'>" +
                "<div class='box-header with-border'>" +
                    "<div class='user-block'>" +
                        "<img class='round-border' src='/photo"+data.userid+"' alt='username'>" +
                            "<span class='username_ '><a>"+username+" </a></span>" +
                                "<span class='description'>"+data.time+"</span> " +
                    "</div></div><p class='post_content_blog'>"+content+"</p>" +
                    "<img class='img-responsive show-in-modal' src='/get_comment_photo"+data.id+"' alt='Photo'>" +
                    "<button id='comment-toggle'"+data.id+" class='btn btn-default move_comment_up'>Show comments</button>" +
                    "</div>"
        result += "<div hidden id='comment-area'>" +
            "<div class='form-group comment-btn'><div class='col-sm-8'>" +
            "<input id='commentField_"+data.id+"' class='moveright-comment form-control' placeholder='Input comment...' type='text'> " +
            "</div><div class='col-sm-2'><button id='commentbtn' btn-id="+data.id+" class='btn btn-primary'>" +
            "Comment</button></div></div><ol id='comment_list_"+data.id+"'></ol></div></div>"
        var new_blog = $(result);
        new_blog.data("blog-id", data.id);
        list.prepend(new_blog);

        }
    });
}


$(document).ready(function () {
    // Add event-handlers
    console.log("start");
    $(document).on("click","#postbtn",add_post);
    $(document).on("click","#commentbtn",add_comment);
    $("#postForm").on('submit', addpost);

    // $(document).on("click","#commentbtn",add_comment);
    // $(document).on("click","#commentbtnf",add_commentf);
    // Set up to-do list with initial DB items and DOM data
    populateList();
    $(document).on("click","[id^='comment-toggle']",function(){
      $(this).parent().parent().children("div#comment-area").toggle();
  });
    // $(document).on("click","[id^='comment-toggle']",function(){
    //     $(this).parent().parent().parent().children("div#comment-area").toggle();
    // });
    // $(document).on("click","#qu",function(){
    //     alert("Welcome to Xingchen's Grumblr~~ Have a good day~~ (^-^)");
    // });
    // Periodically refresh to-do list
    // window.setInterval(getUpdates, 5000);

    // CSRF set-up copied from Django docs
      window.setInterval(getUpdates, 4000);



    function getCookie(name) {
        var cookieValue = null;
        if (document.cookie && document.cookie != '') {
            var cookies = document.cookie.split(';');
            for (var i = 0; i < cookies.length; i++) {
                var cookie = jQuery.trim(cookies[i]);
                // Does this cookie string begin with the name we want?
                if (cookie.substring(0, name.length + 1) == (name + '=')) {
                    cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                    break;
                }
            }
        }
        return cookieValue;
    }

    var csrftoken = getCookie('csrftoken');
    $.ajaxSetup({
        beforeSend: function (xhr, settings) {
            xhr.setRequestHeader("X-CSRFToken", csrftoken);
        }
    });
});
