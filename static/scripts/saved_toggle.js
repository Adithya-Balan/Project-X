// Function to get CSRF token from cookies (if not using ajaxSetup)
function getCSRFToken() {
    let cookieValue = null;
    if (document.cookie && document.cookie !== "") {
        const cookies = document.cookie.split(";");
        for (let i = 0; i < cookies.length; i++) {
            const cookie = cookies[i].trim();
            // Check if this cookie string begins with "csrftoken="
            if (cookie.substring(0, "csrftoken=".length) === "csrftoken=") {
                cookieValue = cookie.substring("csrftoken=".length);
                break;
            }
        }
    }
    return cookieValue;
}

$(document).ready(function () {
    // Optionally, set up CSRF globally if you prefer:
    $.ajaxSetup({
        beforeSend: function(xhr, settings) {
            xhr.setRequestHeader("X-CSRFToken", getCSRFToken());
        }
    });

    // Attach click handler to all toggle-save buttons
    $(".toggle-save-btn").click(function () {
        var btn = $(this);
        var projectId = btn.data("project-id");
        var actionUrl = `/toggle_project_save/${projectId}/`; // Adjust the URL if needed

        $.ajax({
            url: actionUrl,
            type: "POST",
            success: function(response) {
                // Update the button text based on the saved status
                if (response.saved) {
                    btn.find(".btn-text").text("Unsave");
                } else {
                    btn.find(".btn-text").text("Save");
                }
                // Update the saved count (assumes a corresponding element with class 'saved-count-{projectId}')
                // $(".saved-count-" + projectId).text(response.followers_count + " Saved");
            },
            error: function(xhr) {
                console.error("Error:", xhr.responseText);
            }
        });
    });
});
