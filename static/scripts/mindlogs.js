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

document.addEventListener('DOMContentLoaded', function () {
    const execTab = document.getElementById('tab-exec');
    const logTab = document.getElementById('tab-log');
    const execSection = document.getElementById('exec-section');
    const logSection = document.getElementById('log-section');

    if (execTab && logTab && execSection && logSection) {
      execTab.addEventListener('click', () => {
        execSection.classList.remove('hidden');
        logSection.classList.add('hidden');
        execTab.classList.add('bg-green-600');
        logTab.classList.remove('bg-green-600');
        logTab.classList.add('bg-gray-800');
      });

      logTab.addEventListener('click', () => {
        execSection.classList.add('hidden');
        logSection.classList.remove('hidden');
        logTab.classList.add('bg-green-600');
        execTab.classList.remove('bg-green-600');
        execTab.classList.add('bg-gray-800');
      });
  }
});

document.addEventListener('DOMContentLoaded', () => {
    const latencyRange = document.getElementById('latencyRange');
    const latencyValue = document.getElementById('latencyValue');
    const selectedColorInput = document.getElementById('selectedColor');
    const colorPicker = document.getElementById('colorPicker');

    // 💡 Update latency output live
    if (latencyRange && latencyValue) {
        latencyValue.textContent = latencyRange.value + 'ms';

        latencyRange.addEventListener('input', () => {
        latencyValue.textContent = latencyRange.value + 'ms';
        });
    }

    // 🎨 Color picker logic
    if (colorPicker && selectedColorInput) {
        const colorDivs = colorPicker.querySelectorAll('div');

        // Set initial selection if already has value
        const initialColor = selectedColorInput.value;
        if (initialColor) {
        colorDivs.forEach(div => {
            if (div.dataset.color === initialColor) {
            div.classList.add('ring-2');
            }
        });
        }

        colorDivs.forEach(div => {
        div.addEventListener('click', () => {
            const selected = div.dataset.color;
            selectedColorInput.value = selected;

            // Remove highlight from others
            colorDivs.forEach(d => d.classList.remove('ring-2'));
            div.classList.add('ring-2');
        });
        });
    }
});


// For opening and closing navigation menu
document.addEventListener('DOMContentLoaded', function () {
  const navToggle = document.getElementById('navToggle');
  const navMenu = document.getElementById('navMenu');

  if (navToggle && navMenu) {
    navToggle.addEventListener('click', () => {
      navMenu.classList.toggle('hidden');
    });

    // Optional: close menu on outside click
    document.addEventListener('click', function (e) {
      if (!navMenu.contains(e.target) && !navToggle.contains(e.target)) {
        navMenu.classList.add('hidden');
      }
    });
  }
});

//Shortcuts
document.addEventListener('DOMContentLoaded', () => {
    const userData = document.getElementById('user-data');
    const username = userData ? userData.getAttribute('data-username') : null;
    const routes = {
        'ALT+T': '/logs/terminal/',             // Terminal for logging and execution
        'ALT+L': '/logs/',     // Explore logs
        'ALT+B': username ? `/logs/logbook/${username}/` : null,      // Personal logbook
        'ALT+Q': '/'                  // Exit to homepage
    };

    document.addEventListener('keydown', (e) => {
        // Ignore input fields to avoid interrupting typing
        const tag = e.target.tagName.toLowerCase();
        const isTyping = tag === 'input' || tag === 'textarea' || e.target.isContentEditable;
        if (isTyping) return;

        const combo = `ALT+${e.key.toUpperCase()}`;
        if (routes[combo]) {
        e.preventDefault();  // Prevent browser default action
        window.location.href = routes[combo];
        }
    });
});


// For handling commands in terminal
document.addEventListener("DOMContentLoaded", () => {
  const executeBtn = document.getElementById("execute-btn");
  const inputField = document.getElementById("mind-log-query");
  const helpText = document.getElementById("help_error_terminal");

  if (executeBtn && inputField && helpText) {
    executeBtn.addEventListener("click", () => {
      const input = inputField.value.trim();

      if (input.endsWith(".mind.logs")) {
        const username = input.replace(".mind.logs", "");
        if (username) {
          window.location.href = `/logs/logbook/${username}/`;
          return;
        }
      }

      // Invalid command
      helpText.style.display = "block";
    });
  }
});

//For Deleting logs
$(document).ready(function () {
  $(document).on('click', '.delete-log-btn', function () {
    const button = $(this);
    const sig = button.data('sig');
    const logCard = $(`#log-${sig}`);

    if (!confirm("Are you sure you want to delete this log?")) return;

    $.ajax({
      type: "POST",
      url: `/logs/delete-log/${sig}/`,
      headers: {
        "X-CSRFToken": getCSRFToken(),
      },
      success: function (response) {
        if (response.success) {
          logCard.fadeOut(400, function () {
            $(this).remove();
          });
          toast("Log deleted successfully!", "error");
        } else {
          alert("Failed to delete the log.");
        }
      },
      error: function (xhr) {
        if (xhr.status === 403) {
          alert("Unauthorized: You can only delete your own logs.");
        } else if (xhr.status === 404) {
          alert("Log not found.");
        } else {
          alert("An error occurred. Please try again.");
        }
      }
    });
  });
});

// For toggle like.
$(document).ready(function() {
    $(document).on('click', '.log-like-container', function() {
        let container = $(this);
        let logSig = container.data("log-sig");
        let heartIcon = container.find("i");
        let likeCountSpan = container.find("span");
        let actionUrl = `/logs/toggle_log_like/${logSig}/`; 
        
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

// for loading more logs
document.addEventListener("DOMContentLoaded", function () {
    const loadBtn = document.getElementById("logs-load-more-btn");
    const container = document.getElementById("log-container");

    if (!loadBtn || !container) return;

    loadBtn.addEventListener("click", function () {
      const page = parseInt(loadBtn.dataset.page);
      loadBtn.disabled = true;
      loadBtn.innerText = "Loading ...";

      fetch(`/logs/load-more/?page=${page}`)
        .then(response => response.json())
        .then(data => {
          if (data.logs_html) {
            container.insertAdjacentHTML("beforeend", data.logs_html);
          }

          if (data.has_next) {
            loadBtn.dataset.page = page + 1;
            loadBtn.disabled = false;
            loadBtn.innerText = "Load More ⟳";
          } else {
            loadBtn.remove();
          }
        })
        .catch(error => {
          console.error("Load error:", error);
          loadBtn.disabled = false;
          loadBtn.innerText = "Retry ⟳";
        });
    });
});


//for load more personal logs
document.addEventListener("DOMContentLoaded", function () {
    const loadBtn = document.getElementById("personal-logs-load-more-btn");
    const container = document.getElementById("log-container");
    if (!loadBtn || !container) return;

    const username = loadBtn.dataset.username;
    loadBtn.addEventListener("click", function () {
      const page = parseInt(loadBtn.dataset.page);
      loadBtn.disabled = true;
      loadBtn.innerText = "Loading ...";

      fetch(`/logs/personal-load-more/${username}/?page=${page}`)
        .then(response => response.json())
        .then(data => {
          if (data.logs_html) {
            container.insertAdjacentHTML("beforeend", data.logs_html);
          }

          if (data.has_next) {
            loadBtn.dataset.page = page + 1;
            loadBtn.disabled = false;
            loadBtn.innerText = "Load More ⟳";
          } else {
            loadBtn.remove();
          }
        })
        .catch(error => {
          console.error("Load error:", error);
          loadBtn.disabled = false;
          loadBtn.innerText = "Retry ⟳";
        });
    });
});




