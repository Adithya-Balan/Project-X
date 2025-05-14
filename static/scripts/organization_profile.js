const image = document.getElementById('image')
const croppingImg = document.getElementById('croppingImg')
const imgInput = document.getElementById('imgInput')
const cropImgContainer = document.getElementById('cropImgContainer')
const cropBtn = document.getElementById('cropBtn')
const originalProfile = document.getElementById('originalProfile')
const croppedImageInput = document.getElementById('croppedImage');

let cropper
// for cropping the image
imgInput.addEventListener('change', (event) => {
    const file = event.target.files[0];
    if (file) {
        const reader = new FileReader();
        reader.onload = () => {
            croppingImg.src = reader.result;
            cropImgContainer.classList.remove('hidden');
            cropImgContainer.classList.add('flex');

            if (cropper) {
                cropper.destroy();
            }
            cropper = new Cropper(croppingImg, {
                aspectRatio: 1,
                autoCropArea: 1
            });
            cropBtn.classList.remove('hidden');
        };
        reader.readAsDataURL(file);
    }
});

// when crop btn is cliked 
const crop = () => {
    if (!cropper) {
        console.error('Cropper instance is not initialized.');
        return;
    }
    const canvas = cropper.getCroppedCanvas();
    if (!canvas) {
        console.error('Failed to get cropped canvas. Ensure the image is loaded and cropped.');
        return;
    }

    const croppedImageData = canvas.toDataURL('image/jpeg'); // Convert to base64 (JPEG format)
    image.src = croppedImageData; // Update the displayed image
    console.log('Updated Image Source:', image.src);

    // Ensure croppedImageInput exists before setting its value
    if (!croppedImageInput) {
        console.error('Hidden input element with id "croppedImage" not found.');
        return;
    }

    croppedImageInput.value = croppedImageData; // Set the hidden input value
    console.log('Hidden Input Value Set:', croppedImageInput.value);

    cropImgContainer.classList.add('hidden');
    cropBtn.classList.add('hidden');
};

const openEdit = () => {
    const editContainer = document.getElementById('editContainer')
    const entireSection = document.getElementById('entireSection')
    editContainer.classList.remove('hidden')
    editContainer.classList.add('flex')
    entireSection.classList.add('blur-md')
}

// close edit div function
const closeEdit = () => {
    const editContainer = document.getElementById('editContainer')
    const entireSection = document.getElementById('entireSection')
    editContainer.classList.add('hidden')
    editContainer.classList.remove('flex')
    entireSection.classList.remove('blur-md')
}

// for organization ... option
document.addEventListener('DOMContentLoaded', () => {
    const trigger = document.getElementById('threeDotTrigger');
    const menu = document.getElementById('threeDotMenu');
    const overlay = document.getElementById('threeDotOverlay');

    if (trigger && menu && overlay) {
        // Prevent aria-hidden on trigger and parent
        trigger.removeAttribute('aria-hidden');
        trigger.parentElement.removeAttribute('aria-hidden');

        trigger.addEventListener('click', () => {
            const isOpen = menu.classList.contains('hidden');
            menu.classList.toggle('hidden');
            menu.classList.toggle('flex');
            overlay.classList.toggle('hidden');
            trigger.setAttribute('aria-expanded', isOpen);
        });

        overlay.addEventListener('click', () => {
            menu.classList.add('hidden');
            menu.classList.remove('flex');
            overlay.classList.add('hidden');
            trigger.setAttribute('aria-expanded', 'false');
        });

        menu.querySelectorAll('div, a').forEach(item => {
            item.addEventListener('click', () => {
                menu.classList.add('hidden');
                menu.classList.remove('flex');
                overlay.classList.add('hidden');
                trigger.setAttribute('aria-expanded', 'false');
            });
        });
    }
});