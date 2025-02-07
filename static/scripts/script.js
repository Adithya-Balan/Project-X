const showPopup = () => {
    // Code to show the popup
    const popup = document.getElementById('popup');
    popup.classList.toggle('fixed')
    popup.classList.toggle('hidden')
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
                    block: 'center'
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
