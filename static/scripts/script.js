function getCSRFToken() {
    let cookieValue = null;
    if (document.cookie && document.cookie !== "") {
        const cookies = document.cookie.split(";");
        for (let i = 0; i < cookies.length; i++) {
            const cookie = cookies[i].trim();
            if (cookie.startsWith("csrftoken=")) {
                cookieValue = cookie.substring("csrftoken=".length);
                break;
            }
        }
    }
    return cookieValue;
}


const showPopup = () => {
    // Code to show the popup
    const popup = document.getElementById('popup');
    popup.classList.toggle('fixed')
    popup.classList.toggle('hidden')
}

const showPostOption = () => { //code to post options in Navbar
    const postOption = document.getElementById('postOption')
    postOption.classList.toggle('absolute')
    postOption.classList.toggle('hidden')
}

function getExplore() { //code to select multiple explore pages such as events, projects
    const allExplore = document.getElementById('allExplore')
    allExplore.classList.toggle('flex')
    allExplore.classList.toggle('hidden')
}


const openFilter = () => {
    if (window.screen.width < 1024) {
        const filterElement = document.getElementById('filterElement');
        const openFilterParent = document.getElementById('openFilterParent');
        filterElement.classList.toggle('fixed')
        filterElement.classList.add('flex')
        filterElement.classList.remove('hidden')
        openFilterParent.classList.remove('hidden')
    }
}

const closeFilter = () => {
    const filterElement = document.getElementById('filterElement');
    const openFilterParent = document.getElementById('openFilterParent');
    filterElement.classList.remove('fixed')
    filterElement.classList.add('hidden')
    openFilterParent.classList.add('hidden')
}


// for handling reply btn action

const handleReply = (commentId, name) => {
    const textArea = document.getElementById('commentTextArea');
    const parentCommentId = document.getElementById('parentCommentId');
    textArea.focus();
    textArea.placeholder = `Replying to ${name}`;
    parentCommentId.value = commentId;
}

document.addEventListener('DOMContentLoaded', function () {
    document.querySelectorAll('.replyBtn').forEach(anchor => {
        anchor.addEventListener('click', function (e) {
            e.preventDefault();
            const target = document.querySelector(this.getAttribute('href'));
            if (target) {
                target.scrollIntoView({
                    behavior: 'smooth',
                    block: 
                    'center'
                });
                target.focus();
            }
        });
    });
});


const goTo = (url) => {
    window.open('https://' + url, '_blank');
}


const showMenu = () => {
    // Code to show the popup
    const threeDotMenu = document.getElementById('threeDotMenu');
    threeDotMenu.classList.toggle('flex')
    threeDotMenu.classList.toggle('hidden')
}

const viewProfile = () => {
    const entireSection = document.getElementById('entireSection')
    const zoomProfile = document.getElementById('zoomProfile')
    entireSection.classList.toggle('blur')
    zoomProfile.classList.toggle('flex')
    zoomProfile.classList.toggle('hidden')
}

const closeProfile = () => {
    const entireSection = document.getElementById('entireSection')
    const zoomProfile = document.getElementById('zoomProfile')
    entireSection.classList.remove('blur')
    zoomProfile.classList.add('hidden')
    zoomProfile.classList.remove('flex')
}

// resize post
const postImgContainer = document.getElementById('postImgContainer')
const resizePost = (size) => {
    const postImg = document.getElementById('postImg')
    postImg.classList.add('object-cover')
    postImg.classList.remove('object-contain')
    if (size) {
        postImgContainer.classList.add('aspect-video')
        postImgContainer.classList.remove('aspect-square')
    }
    else {
        postImgContainer.classList.add('aspect-square')
        postImgContainer.classList.remove('aspect-video')
    }
}

// set original post image
const setImgOriginal = () => {
    const postImg = document.getElementById('postImg')
    postImg.classList.add('object-contain')
    postImg.classList.remove('object-cover')
    postImgContainer.classList.remove('aspect-square')
    postImgContainer.classList.add('aspect-video')
}

//Get aspect ratio for userpost
function setAspectRatio(ratio){
    document.getElementById('aspectRatioInput').value = ratio
}

// upload post
const uploadPost = document.getElementById('uploadPost')
const uploadPostContainer = document.getElementById('uploadPostContainer')
const uploadPostLabel = document.getElementById('uploadPostLabel')

uploadPost.addEventListener('change', (event) => {
    postImgContainer.classList.remove('object-contain')
    postImgContainer.classList.remove('aspect-square')
    postImgContainer.classList.add('aspect-video')
    const postImg = document.getElementById('postImg')

    const file = event.target.files[0]
    if (file) {
        const reader = new FileReader()
        reader.onload = () => {


            postImg.classList.remove('hidden')
            postImg.classList.add('block')
            postImg.src = reader.result
            uploadPostContainer.classList.add('hidden')
            uploadPostLabel.classList.remove('hidden')
        }
        reader.readAsDataURL(file)
    }
})

// opening create post div function
const openPost = () => {
    const entireSection = document.getElementById('entireSection')
    const createPost = document.getElementById('createPost')
    entireSection.classList.add('blur-md')
    createPost.classList.remove('hidden')
    createPost.classList.add('flex')
    console.log("openPost called!");
}

// closing create post div function
const closePost = () => {
    const entireSection = document.getElementById('entireSection')
    const createPost = document.getElementById('createPost')
    entireSection.classList.remove('blur-md')
    createPost.classList.add('hidden')
    createPost.classList.remove('flex')
}

// #Toggle like for post
$(document).ready(function() {
    $(".like-container").click(function() {
        let container = $(this);
        let postId = container.data("post-id");
        let heartIcon = container.find("i");
        let likeCountSpan = container.find("span");
        let actionUrl = `/toggle_like/${postId}/`; 
        
        $.ajax({
            url: actionUrl,
            type: "POST",
            headers: { "X-CSRFToken": getCSRFToken() },
            success: function(response) {
                // Update the heart icon's style based on like status
                if (response.liked) {
                    heartIcon.addClass("text-[#6feb85]");
                } else {
                    heartIcon.removeClass("text-[#6feb85]");
                }
                // Update the like count in the span
                likeCountSpan.text(response.total_likes);
            },
            error: function(xhr) {
                console.error("Error toggling like:", xhr.responseText);
            }
        });
    });
});


// for toggling the comments
const commentBtn = document.querySelectorAll('.commentBtn')
const commentsSection = document.querySelectorAll('.commentsSection')
commentBtn.forEach((element, i) => {
    element.addEventListener('click', () => {   //shifted this from profile.js
        if (commentsSection[i].classList.contains("hidden")){
            commentsSection[i].classList.remove('hidden')
        }
        else{
            commentsSection[i].classList.add('hidden')
        }
    })
});

//for saving post comments
$(document).ready(function(){
    $(document).on("submit", ".postCommentForm", function(event){
        event.preventDefault();
        var form = $(this);
        var commentText = form.find("input[name='comment']").val();
        var postId = form.data("post-id");
        var csrftoken = form.find("input[name='csrfmiddlewaretoken']").val();

        $.ajax({
            url: form.attr("action"),
            type: 'POST',
            data: {
                'comment': commentText,
                'post_id': postId,
                'csrfmiddlewaretoken': csrftoken
            },
            success: function(response) {
                var commentHTML = "<div class='flex items-start space-x-2 mt-2'>" +
                                        "<a href='/user-profile/" + response.username + "'/>" +
                                           "<img src='" + response.profile_image_url + "' alt='User' class='w-8 h-8 rounded-sm object-cover'>" +
                                        "</a>" +
                                        "<div class='bg-gray-50 p-2 rounded-lg w-full'>" +
                                            "<a href='/user_profile/" + response.username + "/' class='text-sm font-semibold -mt-2'>" + response.username + "</a>" +
                                            "<p class='text-sm mt-2'>" + response.comment + "</p>" +
                                        "</div>" +
                                    "</div>";

                $("#postCommentContainer" + postId).prepend(commentHTML);
                // Clear the comment text input
                form.find("input[name='comment']").val('');
                // Update the comment count if available
                $("#postCommentCount" + postId).text(response.comments_count);
            },  error: function(xhr, errmsg, err) {
                console.error("Error saving comment: " + errmsg);
            }
        });
    });
});

// Post save Toggle
$(document).ready(function() {
    $(".bookmark-container").click(function() {
        let container = $(this);
        let postId = container.data("post-id");
        let bookmarkIcon = container.find("i");
        let actionUrl = `/toggle_post_save/${postId}/`; 

        $.ajax({
            url: actionUrl,
            type: "POST",
            headers: { "X-CSRFToken": getCSRFToken() },
            success: function(response) {
                if (response.saved) {
                    bookmarkIcon.addClass("text-[#6feb85]");
                } else {
                    bookmarkIcon.removeClass("text-[#6feb85]");
                }
                // Update the like count in the span
                // likeCountSpan.text(response.total_likes);
            },
            error: function(xhr) {
                console.error("Error toggling save:", xhr.responseText);
            }
        });
    });
});

// Project Save Toggle
$(document).ready(function() {
    $(".bookmark-container-project").click(function() {
        let container = $(this);
        let projectId = container.data("project-id");
        let bookmarkIcon = container.find("i");
        let actionUrl = `/toggle_project_save/${projectId}/`; 

        $.ajax({
            url: actionUrl,
            type: "POST",
            headers: { "X-CSRFToken": getCSRFToken() },
            success: function(response) {
                // Update the heart icon's style based on like status
                if (response.saved) {
                    bookmarkIcon.addClass("text-[#6feb85]");
                } else {
                    bookmarkIcon.removeClass("text-[#6feb85]");
                }
            },
            error: function(xhr) {
                console.error("Error toggling save:", xhr.responseText);
            }
        });
    });
});

//event save toggle
$(document).ready(function() {
    $(".bookmark-container-event").click(function() {
        let container = $(this);
        let eventId = container.data("event-id");
        let bookmarkIcon = container.find("i");
        let actionUrl = `/toggle_event_save/${eventId}/`; 

        $.ajax({
            url: actionUrl,
            type: "POST",
            headers: { "X-CSRFToken": getCSRFToken() },
            success: function(response) {
                // Update the heart icon's style based on like status
                if (response.saved) {
                    bookmarkIcon.addClass("text-[#6feb85]");
                } else {
                    bookmarkIcon.removeClass("text-[#6feb85]");
                }
            },
            error: function(xhr) {
                console.error("Error toggling save:", xhr.responseText);
            }
        });
    });
});
//Filters, popup for mobile, comments reply for project, dp view for profile, add posts